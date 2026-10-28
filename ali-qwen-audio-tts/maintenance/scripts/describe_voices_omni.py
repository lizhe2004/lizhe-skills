#!/usr/bin/env python3
"""用 Qwen3.8-Omni-Flash「听」官方试听音频，为每个音色生成听感描述。

输入：maintenance/samples/index.csv（fetch_voice_samples.py 生成）、maintenance/data/<model>.official.csv
输出：
  maintenance/samples/omni/<样例哈希>.json   每条样例的模型原始结论（缓存，重跑跳过；哈希基于相对 samples/ 的路径）
  maintenance/data/<model>.omni.csv          每个音色汇总后的听感画像

调用：OpenAI 兼容 Chat Completions，与 TTS 共用 DASHSCOPE_API_KEY / ALI_WORKSPACE_ID。
公网试听链接直接传 URL，本地文件传 Base64。关闭思考模式以节省 token。只用标准库。

用法：
  python3 scripts/describe_voices_omni.py --limit 6          # 试点
  python3 scripts/describe_voices_omni.py --workers 6         # 全量
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import DATA, MODELS, SAMPLES, VOICE_LIST_MD, official  # noqa: E402

CACHE = SAMPLES / "omni"
MODEL = "qwen3.8-omni-flash"

PROMPT = """你是专业的配音导演。请只根据这段音频里说话人的声音本身来评价音色，不要根据朗读内容的主题去推断。
严格输出一个 JSON 对象，不要输出任何其他文字，字段如下：
{
  "性别": "男|女|童声|不确定",
  "年龄段": "儿童|少年|青年|中年|老年",
  "音高": "低|中低|中|中高|高",
  "语速": "慢|适中|快",
  "语言": "说话所用的语言或方言，如 普通话、粤语、上海话、英语",
  "口音": "无明显口音，或具体口音",
  "音色关键词": ["3到6个描述音色质感的词，如 温暖、磁性、清亮、沙哑、气声、浑厚、甜美、干净"],
  "情绪风格": "如 亲切、沉稳、热情、慵懒、严肃",
  "播讲风格": "如 自然对话、新闻播报、广告促销、故事讲述、助眠低语",
  "适用场景": ["2到4个最合适的配音场景"],
  "不适合": ["1到2个不合适的场景"],
  "一句话描述": "不超过30字",
  "置信度": "高|中|低"
}"""


def endpoint() -> str:
    ws = os.environ.get("ALI_WORKSPACE_ID")
    region = os.environ.get("ALI_REGION", "beijing")
    if not ws:
        raise SystemExit("Missing ALI_WORKSPACE_ID")
    host = f"{ws}.cn-beijing.maas.aliyuncs.com" if region == "beijing" else f"{ws}.ap-southeast-1.maas.aliyuncs.com"
    return f"https://{host}/compatible-mode/v1/chat/completions"


def audio_ref(row: dict, urls: dict) -> str:
    if row["file"] in urls:
        return urls[row["file"]]
    data = (SAMPLES / row["file"]).read_bytes()
    return "data:;base64," + base64.b64encode(data).decode()


def ask(url: str, key: str, audio: str, hint: str = "", thinking: bool = False) -> tuple[dict, dict]:
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": [
            {"type": "input_audio", "input_audio": {"data": audio, "format": "wav"}},
            {"type": "text", "text": (f"参考信息（来自官方文档和声学测量）：{hint}。请仍以你实际听到的为准。\n" if hint else "") + PROMPT}]}],
        "stream": True,
        "stream_options": {"include_usage": True},
        "enable_thinking": thinking,
    }
    req = urllib.request.Request(url, json.dumps(body).encode(), {
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"}, method="POST")
    text, usage = "", {}
    with urllib.request.urlopen(req, timeout=180) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload == "[DONE]":
                break
            ev = json.loads(payload)
            if ev.get("usage"):
                usage = ev["usage"]
            for ch in ev.get("choices") or []:
                text += (ch.get("delta") or {}).get("content") or ""
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < 0:
        raise ValueError(f"no JSON in reply: {text[:200]}")
    return json.loads(text[start:end + 1]), usage


def run_one(row: dict, url: str, key: str, urls: dict, hint: str = "", thinking: bool = False,
            force: bool = False) -> dict:
    cache = CACHE / (hashlib.md5(row["file"].encode()).hexdigest()[:12] + ".json")
    if cache.exists() and force:  # 重新描述前留一份旧结果
        backup = CACHE / "_previous" / cache.name
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(cache.read_bytes())
    if cache.exists() and not force:
        return json.loads(cache.read_text(encoding="utf-8"))
    last = None
    for attempt in range(4):
        try:
            result, usage = ask(url, key, audio_ref(row, urls), hint, thinking)
            out = {"file": row["file"], "model": row["model"], "voice": row["voice"], "label": row["label"],
                   "result": result, "usage": usage, "hint": hint, "thinking": thinking}
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
            return out
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}"
            # 参数/鉴权/计费类错误重试无效；计费类（欠费、配额、未订购、预算）即使是 429 也直接停
            if e.code in (400, 401, 403) or any(x in last for x in (
                    "AllocationQuota", "insufficient_quota", "CommodityNotPurchased", "BillOverdue", "BudgetLimitExceeded")):
                break
        except Exception as e:  # 网络中断、流读取不完整、模型未按 JSON 输出
            last = f"{type(e).__name__}: {e}"
        time.sleep(2 * (attempt + 1))
    return {"file": row["file"], "model": row["model"], "voice": row["voice"], "error": last}


def system_urls() -> dict:
    """本地系统音色文件 -> 官方公网 URL（文件名里保留了原始文件名）。"""
    import re
    md = VOICE_LIST_MD.read_text(encoding="utf-8")
    by_name = {u.rsplit("/", 1)[-1]: u for u in re.findall(r'src="(https://[^"]+\.wav)"', md)}
    out = {}
    for p in (SAMPLES / "system").glob("*.wav"):
        name = p.name.split("-", 1)[1]
        if name in by_name:
            out[str(p.relative_to(SAMPLES))] = by_name[name]
    return out


def vote(values):
    values = [v for v in values if v]
    return Counter(values).most_common(1)[0][0] if values else ""


def merge(items: list[dict]) -> dict:
    rs = [i["result"] for i in items]
    words = Counter(w for r in rs for w in (r.get("音色关键词") or []))
    scenes = Counter(w for r in rs for w in (r.get("适用场景") or []))
    bad = Counter(w for r in rs for w in (r.get("不适合") or []))
    langs = []
    for i in items:
        lang = i["result"].get("语言", "")
        if lang and lang not in langs:
            langs.append(lang)
    return {
        "性别(听感)": vote(r.get("性别") for r in rs), "年龄段": vote(r.get("年龄段") for r in rs),
        "音高(听感)": vote(r.get("音高") for r in rs), "语速(听感)": vote(r.get("语速") for r in rs),
        "样例语言": "、".join(langs), "口音": vote(r.get("口音") for r in rs),
        "音色关键词": "、".join(w for w, _ in words.most_common(6)),
        "情绪风格": vote(r.get("情绪风格") for r in rs), "播讲风格": vote(r.get("播讲风格") for r in rs),
        "适用场景": "、".join(w for w, _ in scenes.most_common(4)),
        "不适合": "、".join(w for w, _ in bad.most_common(2)),
        "一句话描述": rs[0].get("一句话描述", ""), "置信度": vote(r.get("置信度") for r in rs),
        "描述方式": ("思考模式" + ("，参考了官方文档与实测基频" if any(i.get("hint") for i in items) else "，无提示")
                    if any(i.get("thinking") for i in items) else "首轮批量（未开思考）"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 条样例（试点）")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--models", nargs="*", default=None, help="只处理这些模型")
    ap.add_argument("--voices", nargs="*", default=None, help="只处理这些音色（会覆盖已有缓存）")
    ap.add_argument("--hints", default=None,
                    help="JSON 文件：{voice: 提示}。只放官方文档事实和客观测量值，不要放模型自己的推断")
    ap.add_argument("--thinking", action="store_true", help="开启思考模式（更审慎，token 更多）")
    ap.add_argument("--yes", action="store_true", help="确认调用付费接口；不加时只汇总已缓存的结果")
    a = ap.parse_args()
    key = os.environ.get("DASHSCOPE_API_KEY") or sys.exit("Missing DASHSCOPE_API_KEY")
    url = endpoint()
    index = list(csv.DictReader((SAMPLES / "index.csv").open(encoding="utf-8-sig")))
    if a.models:
        index = [r for r in index if r["model"] in a.models]
    if a.voices:
        index = [r for r in index if r["voice"] in a.voices]
    hints = json.loads(Path(a.hints).read_text(encoding="utf-8")) if a.hints else {}
    # 两个 3.0 模型的基础音色共用同一个试听文件，只问一次
    todo, seen = [], set()
    for r in index:
        if r["file"] not in seen:
            seen.add(r["file"])
            todo.append(r)
    if a.limit:
        todo = todo[: a.limit]
    urls = system_urls()
    pending = [r for r in todo if a.voices or not (CACHE / (hashlib.md5(r["file"].encode()).hexdigest()[:12] + ".json")).exists()]
    if pending and not a.yes:
        print(f"{len(pending)} 条样例需要调用 {MODEL}（付费）。确认后加 --yes 重新运行；本次只汇总已缓存结果。",
              file=sys.stderr)
        todo = [r for r in todo if r not in pending]

    done, errors, tokens = 0, [], Counter()
    results = {}
    with ThreadPoolExecutor(a.workers) as pool:
        futs = [pool.submit(run_one, r, url, key, urls, hints.get(r["voice"], ""), a.thinking, bool(a.voices))
                for r in todo]
        for f in as_completed(futs):
            out = f.result()
            done += 1
            if "error" in out:
                errors.append(out)
            else:
                results[out["file"]] = out
                for k, v in (out.get("usage") or {}).items():
                    if isinstance(v, int):
                        tokens[k] += v
            print(f"\rdescribed {done}/{len(todo)}  errors {len(errors)}", end="", file=sys.stderr)
    print(file=sys.stderr)
    for e in errors[:5]:
        print("error:", e["voice"], e["error"], file=sys.stderr)
    if tokens:
        print("tokens (all samples in this run, cached ones included):", dict(tokens), file=sys.stderr)
    if a.limit:
        for out in results.values():
            print(out["voice"], json.dumps(out["result"], ensure_ascii=False))
        return 0

    # 汇总到每个音色（缓存里所有样例都参与，包括以前跑过的）
    by_file = {}
    for p in CACHE.glob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        by_file[d["file"]] = d
    cols = ["voice", "名称", "性别(文档)", "性别(听感)", "年龄段", "音高(听感)", "语速(听感)", "样例语言", "口音",
            "音色关键词", "情绪风格", "播讲风格", "适用场景", "不适合", "一句话描述", "置信度", "描述方式", "样例数"]
    for model in MODELS:
        table = official(model)
        meta = {r["voice"]: r for r in csv.DictReader(table.open(encoding="utf-8-sig"))}
        rows = []
        for voice, m in meta.items():
            files = [r["file"] for r in csv.DictReader((SAMPLES / "index.csv").open(encoding="utf-8-sig"))
                     if r["model"] == model and r["voice"] == voice]
            items = [by_file[f] | {"result": by_file[f]["result"]} for f in files if f in by_file]
            if not items:
                continue
            rows.append({"voice": voice, "名称": m.get("名称", ""), "性别(文档)": m.get("性别", ""),
                         **merge(items), "样例数": len(items)})
        if not rows:
            continue
        out = DATA / f"{model}.omni.csv"
        with out.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print(f"{out.name}: {len(rows)}/{len(meta)} voices")
    return 0


if __name__ == "__main__":
    sys.exit(main())
