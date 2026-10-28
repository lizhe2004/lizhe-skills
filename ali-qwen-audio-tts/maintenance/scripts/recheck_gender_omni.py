#!/usr/bin/env python3
"""对「文档性别」与「Omni 听感性别」不一致的音色，用 Qwen3.8-Omni-Flash 做一次专门的性别复核。

与 describe_voices_omni.py 的区别：只问性别与年龄、要求给出声学依据和置信度；不告诉模型文档标注；
开启思考模式；每条样例独立问多次取多数。结果缓存到 maintenance/samples/omni-gender/，
汇总到 maintenance/data/<model>.gender-recheck.csv，build_voice_profiles.py 会读取它。

用法：
  python3 scripts/recheck_gender_omni.py --model qwen-audio-3.1-tts-flash          # 自动选不一致的音色
  python3 scripts/recheck_gender_omni.py --model qwen-audio-3.1-tts-flash --voices andi_v3.1 --runs 3
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from describe_voices_omni import MODEL, audio_ref, endpoint, system_urls  # noqa: E402

from paths import DATA, SAMPLES  # noqa: E402

CACHE = SAMPLES / "omni-gender"

PROMPT = """请只根据这段音频中说话人的嗓音判断说话人的生理特征，不要根据说话内容推断。
重点听：基频高低、胸腔/头腔共鸣、喉部厚度、声带振动质感、气息，以及是否有刻意压低或抬高嗓音的痕迹。
严格输出一个 JSON 对象，不要输出其他文字：
{
  "成人或儿童": "成人|儿童|难以判断",
  "性别": "男|女|难以判断",
  "性别置信度": 0到1之间的小数,
  "估计年龄": "如 6-9岁、20-30岁",
  "依据": "不超过60字，说明主要听到了什么声学特征",
  "是否可能为中性或刻意塑造的音色": "是|否"
}"""


def ask(url: str, key: str, audio: str) -> tuple[dict, dict]:
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": [
            {"type": "input_audio", "input_audio": {"data": audio, "format": "wav"}},
            {"type": "text", "text": PROMPT}]}],
        "stream": True,
        "stream_options": {"include_usage": True},
        "enable_thinking": True,
    }
    req = urllib.request.Request(url, json.dumps(body).encode(), {
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"}, method="POST")
    text, usage = "", {}
    with urllib.request.urlopen(req, timeout=300) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:") or line[5:].strip() == "[DONE]":
                continue
            ev = json.loads(line[5:].strip())
            if ev.get("usage"):
                usage = ev["usage"]
            for ch in ev.get("choices") or []:
                text += (ch.get("delta") or {}).get("content") or ""
    return json.loads(text[text.find("{"): text.rfind("}") + 1]), usage


def one(row: dict, run: int, url: str, key: str, urls: dict) -> dict:
    cache = CACHE / f"{hashlib.md5(row['file'].encode()).hexdigest()[:12]}-{run}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    last = None
    for _ in range(3):
        try:
            result, usage = ask(url, key, audio_ref(row, urls))
            out = {"voice": row["voice"], "file": row["file"], "run": run, "result": result, "usage": usage}
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
            return out
        except Exception as e:  # 网络中断或未按 JSON 输出，重试
            last = f"{type(e).__name__}: {e}"
    return {"voice": row["voice"], "file": row["file"], "run": run, "error": last}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--voices", nargs="*")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--yes", action="store_true", help="确认调用付费接口")
    a = ap.parse_args()
    key = os.environ.get("DASHSCOPE_API_KEY") or sys.exit("Missing DASHSCOPE_API_KEY")
    off = {r["voice"]: r for r in csv.DictReader((DATA / f"{a.model}.official.csv").open(encoding="utf-8-sig"))}
    omni = {r["voice"]: r for r in csv.DictReader((DATA / f"{a.model}.omni.csv").open(encoding="utf-8-sig"))}
    meas = {r["voice"]: r for r in csv.DictReader((DATA / f"{a.model}.measured.csv").open(encoding="utf-8-sig"))}
    profile = {v: {"性别(文档)": off[v].get("性别", ""), "性别(听感)": omni.get(v, {}).get("性别(听感)", ""),
                   "基频中位Hz": meas.get(v, {}).get("基频中位Hz", "")} for v in off}
    voices = a.voices or [v for v, r in profile.items() if r["性别(文档)"] != r["性别(听感)"]]
    rows = [r for r in csv.DictReader((SAMPLES / "index.csv").open(encoding="utf-8-sig"))
            if r["model"] == a.model and r["voice"] in voices]
    url, urls = endpoint(), system_urls()
    jobs = [(r, k) for r in rows for k in range(1, a.runs + 1)]
    uncached = [j for j in jobs if not (CACHE / f"{hashlib.md5(j[0]['file'].encode()).hexdigest()[:12]}-{j[1]}.json").exists()]
    print(f"{len(voices)} voices, {len(rows)} samples, {len(jobs)} runs, {len(uncached)} need paid calls", file=sys.stderr)
    if uncached and not a.yes:
        sys.exit("未调用接口。确认费用后加 --yes 重新运行。")
    with ThreadPoolExecutor(4) as pool:
        outs = list(pool.map(lambda j: one(j[0], j[1], url, key, urls), jobs))
    errors = [o for o in outs if "error" in o]
    for e in errors:
        print("error:", e["voice"], e["error"], file=sys.stderr)
    tokens = Counter()
    for o in outs:
        for k, v in (o.get("usage") or {}).items():
            if isinstance(v, int):
                tokens[k] += v
    print("tokens:", dict(tokens), file=sys.stderr)

    cols = ["voice", "性别(文档)", "性别(首次听感)", "基频中位Hz", "复核性别", "复核一致度", "成人或儿童",
            "平均置信度", "估计年龄", "依据", "可能为中性或塑造音色", "复核结论"]
    table = []
    for v in voices:
        rs = [o["result"] for o in outs if o["voice"] == v and "result" in o]
        if not rs:
            continue
        genders = Counter(r.get("性别", "") for r in rs)
        g, n = genders.most_common(1)[0]
        adult = Counter(r.get("成人或儿童", "") for r in rs).most_common(1)[0][0]
        conf = sum(float(r.get("性别置信度") or 0) for r in rs) / len(rs)
        p = profile[v]
        doc = p["性别(文档)"]
        if adult == "儿童":
            verdict = "儿童音色，性别以文档为准"
        elif g == doc and n == len(rs):
            verdict = "复核与文档一致，首次听感有误"
        elif g == doc:
            verdict = "复核多数与文档一致"
        elif g in ("男", "女") and n == len(rs):
            verdict = "复核一致认为与文档相反，建议人工试听"
        else:
            verdict = "复核结果不稳定，建议人工试听"
        table.append({"voice": v, "性别(文档)": doc, "性别(首次听感)": p["性别(听感)"], "基频中位Hz": p["基频中位Hz"],
                      "复核性别": g, "复核一致度": f"{n}/{len(rs)}", "成人或儿童": adult, "平均置信度": round(conf, 2),
                      "估计年龄": Counter(r.get("估计年龄", "") for r in rs).most_common(1)[0][0],
                      "依据": rs[0].get("依据", ""),
                      "可能为中性或塑造音色": Counter(r.get("是否可能为中性或刻意塑造的音色", "") for r in rs).most_common(1)[0][0],
                      "复核结论": verdict})
    out = DATA / f"{a.model}.gender-recheck.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(table)
    for t in table:
        print(json.dumps(t, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
