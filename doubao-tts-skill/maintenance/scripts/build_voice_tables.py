#!/usr/bin/env python3
"""把官方「在线音色列表」拆成按用途分开的音色表 CSV。

输入：maintenance/source/音色列表.md（官方文档原文）
输出：reference/voices/ 下三份 CSV（UTF-8 带 BOM，Excel 可直接打开）
  doubao-tts-2.0.csv        本 skill 可用：2.0 中文/通用音色 + 2.0 外语音色（资源 seed-tts-2.0）
  doubao-tts-1.0.csv        1.0 音色：本 skill 的 HTTP 接口不支持，保留情感参数和「对应 2.0 音色」用于找替代
  doubao-realtime-s2s.csv   实时语音 S2S/SC 音色：只能走实时语音链路，本 skill 不可用
官方文档更新后替换 source 文件再运行即可。只用标准库，需 Python 3.9+。
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "maintenance" / "source" / "音色列表.md"
OUT = ROOT / "reference" / "voices"


def clean(cell: str) -> str:
    cell = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cell)          # [文字](链接) -> 文字
    cell = re.sub(r"(<br\s*/?>)+", "；", cell)
    cell = re.sub(r"<[^>]+>|\*\*|\\", "", cell)
    return " ".join(cell.split()).strip("； ")


def sections(md: str) -> dict[str, str]:
    heads = [(m.start(), clean(m.group(1))) for m in re.finditer(r"^##\s+(.*)$", md, re.M)]
    heads.append((len(md), ""))
    return {h: md[a:b] for (a, h), (b, _) in zip(heads, heads[1:])}


def tables(block: str) -> list[dict]:
    """解析一个章节里的所有 Markdown 表格；首列为空的续行沿用上一行的值（官方用空单元格表示合并）。"""
    rows, head, prev = [], None, {}
    for line in block.splitlines():
        if not line.startswith("|"):
            head = None if not line.strip() else head
            continue
        body = line.strip()
        body = body[1:-1] if body.endswith("|") else body[1:]   # 只去最外层竖线；行首「||」表示首列合并留空
        cells = [clean(c) for c in body.split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if head is None or line.startswith("|**"):
            head, prev = cells, {}
            continue
        row = dict(zip(head, cells))
        for k in head[:1]:                       # 只有「场景」一列会被合并单元格省略
            if not row.get(k):
                row[k] = prev.get(k, "")
        prev = row
        rows.append(row)
    return rows


def ability(text: str) -> tuple[str, str]:
    """从「支持能力」里拆出两个布尔：指令遵循、引用上文。"""
    return ("是" if "指令" in text else "", "是" if "上文" in text or "上下文" in text else "")


def dedupe(rows: list[dict]) -> list[dict]:
    """同一 voice_type 在原文多个场景下重复列出时合并成一行，不同的字段值用「；」拼接。"""
    merged: dict[str, dict] = {}
    for r in rows:
        m = merged.setdefault(r["voice_type"], dict(r))
        for k, v in r.items():
            if v and v not in m.get(k, "").split("；"):
                m[k] = "；".join(x for x in (m.get(k, ""), v) if x)
    return list(merged.values())


def write(name: str, cols: list[str], rows: list[dict]) -> None:
    rows = dedupe(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    dup = [v for v, n in Counter(r["voice_type"] for r in rows).items() if n > 1]
    print(f"{path.relative_to(ROOT)}: {len(rows)} voices" + (f"  [warn] duplicate voice_type: {dup}" if dup else ""))


def main() -> int:
    md = SOURCE.read_text(encoding="utf-8")
    secs = sections(md)
    pick = lambda key: next(v for k, v in secs.items() if key in k)  # noqa: E731

    v2 = []
    for label, key in (("中文/通用", "2.0、"), ("外语", "外语音色列表")):
        for r in tables(pick(key)):
            if not r.get("voice_type"):
                continue
            instr, ctx = ability(r.get("支持能力", ""))
            v2.append({
                "voice_type": r["voice_type"], "音色名称": r.get("音色名称", ""), "分组": label,
                "场景": r.get("场景", ""), "语种/方言": r.get("语种/方言", ""),
                "指令遵循": instr, "引用上文": ctx, "支持能力(原文)": r.get("支持能力", ""),
                "推荐推理模式": r.get("推荐推理模式", ""),
                "备注": "；".join(x for x in (r.get("特殊标签", ""), r.get("备注", "")) if x),
            })
    write("doubao-tts-2.0.csv", ["voice_type", "音色名称", "分组", "场景", "语种/方言", "指令遵循", "引用上文",
                                 "支持能力(原文)", "推荐推理模式", "备注"], v2)

    v1 = [{"voice_type": r["voice_type"], "音色名称": r.get("音色名称", ""), "场景": r.get("场景", ""),
           "语种": r.get("语种", ""), "支持的情感": r.get("支持的情感", ""), "对应2.0音色": r.get("对应2.0音色", ""),
           "是否支持MIX": r.get("是否支持MIX", ""), "特殊标签": r.get("特殊标签", ""),
           "本skill可用": "否（HTTP 接口只接受 seed-tts-2.0 / seed-icl-2.0）"}
          for r in tables(pick("1.0")) if r.get("voice_type")]
    write("doubao-tts-1.0.csv", ["voice_type", "音色名称", "场景", "语种", "支持的情感", "对应2.0音色",
                                 "是否支持MIX", "特殊标签", "本skill可用"], v1)

    rt = [{"voice_type": r["voice_type"], "音色名称": r.get("音色名称", ""), "场景": r.get("场景", ""),
           "语种": r.get("语种", ""), "本skill可用": "否（实时语音链路专用）"}
          for r in tables(pick("端到端实时语音")) if r.get("voice_type")]
    write("doubao-realtime-s2s.csv", ["voice_type", "音色名称", "场景", "语种", "本skill可用"], rt)

    # 同一 voice_type 若同时出现在可用表与不可用表，校验时以可用表为准，这里提示出来
    both = {r["voice_type"] for r in v2} & ({r["voice_type"] for r in v1} | {r["voice_type"] for r in rt})
    if both:
        print(f"[note] 同时出现在 2.0 表和 1.0/实时表的 voice_type：{sorted(both)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
