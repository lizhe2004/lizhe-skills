#!/usr/bin/env python3
"""从官方音色文档生成每个模型一份的音色表 CSV。

输入（均在 maintenance/source/ 下）：
  - qwen-audio-音色列表.md                 系统音色（3.1 plus、3.1 flash、3.0 plus、3.0 flash）
  - qwen-audio-3.0-tts-{plus,flash}基础音色.xlsx   3.0 两个模型的基础音色

输出：maintenance/data/<model>.official.csv，列结构统一，UTF-8 带 BOM（Excel 直接打开不乱码）。
官方文档更新后重新运行本脚本即可。只用标准库。
"""
from __future__ import annotations

import csv
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from paths import DATA, VOICE_LIST_MD as MD, basic_xlsx, official

COLUMNS = ["voice", "名称", "性别", "年龄", "类别", "声线特质", "适用场景", "语言",
           "地域", "SSML", "指令控制", "时间戳", "试听文件"]

# 3.1 多语种与方言音色的语言范围写在说明段落里，不在表格中
MULTILINGUAL_31 = ("普通话、英语；方言：上海话、广东话、东北话、重庆话、陕西话、云南话、宁波话、甘肃话；"
                   "外语：日语、韩语、法语、德语、葡萄牙语、意大利语、越南语、印尼语")


def clean(cell: str) -> str:
    return " ".join(re.sub(r"<[^>]+>|\*\*|\\", "", cell).split())


def rows_of(block: str) -> list[list[str]]:
    rows = []
    for tr in re.findall(r"<tr>(.*?)</tr>", block, re.S):
        cells = [clean(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if cells:
            rows.append(cells)
    return rows


def features(cell: str) -> dict:
    out = {}
    for key in ("SSML", "指令控制", "时间戳"):
        m = re.search(key + r"\s*[:：]\s*(\S+)", cell)
        out[key] = m.group(1) if m else ""
    return out


def field(text: str, key: str) -> str:
    """从「名称：X voice参数：Y 特质：Z …」这类单元格里取一个字段。"""
    text = text.replace("voice 参数", "voice参数")  # 3.1 表格写作「voice 参数」，统一成一个词再切分
    key = key.replace("voice 参数", "voice参数")
    m = re.search(key + r"\s*[:：]\s*(.*?)(?=\s+\S+\s*[:：]|$)", text)
    return m.group(1).strip() if m else ""


def section(md: str, model: str) -> str:
    start = md.index(f"### {model}")
    nxt = re.search(r"^#{2,3} ", md[start + 4:], re.M)
    return md[start: start + 4 + nxt.start()] if nxt else md[start:]


def parse_31(md: str, model: str) -> list[dict]:
    """3.1 系列：按 <Tab> 分类别，每类一张表，首列是音色信息（列名为「音色信息」或「名称」）。"""
    sec = section(md, model)
    tabs = [(m.start(), m.group(1)) for m in re.finditer(r'<Tab title="([^"]+)"', sec)] + [(len(sec), "")]
    out = []
    for (a, tab), (b, _) in zip(tabs, tabs[1:]):
        block = sec[a:b]
        heads = [clean(h) for h in re.findall(r"<th[^>]*>(.*?)</th>", block, re.S)]
        for cells in rows_of(block):
            col = dict(zip(heads, cells))
            info = cells[0]
            row = {
                "voice": field(info, "voice 参数"),
                "名称": field(info, "名称"),
                "性别": col.get("性别", ""),
                "类别": tab,
                "声线特质": col.get("声线特质") or col.get("口音", ""),
                "适用场景": col.get("适用场景", ""),
                "语言": {"多语种与方言音色": MULTILINGUAL_31, "精品中文音色": "中文",
                        "精品英文音色": "英文"}.get(tab, ""),
                # 3.1 flash 的文档说明：多语种与方言、精品英文支持北京和新加坡，其他仅北京；3.1 plus 未说明
                "地域": "" if model != "qwen-audio-3.1-tts-flash" else
                        "北京、新加坡" if tab in ("多语种与方言音色", "精品英文音色") else "北京",
                **features(col.get("特性支持", "")),
            }
            out.append(row)
    return out


def parse_30_system(md: str, model: str) -> list[dict]:
    out, scene = [], ""
    for cells in rows_of(section(md, model)):
        if len(cells) == 4:      # 首行带「适用场景」，后续行沿用（rowspan）
            scene, info, feat = cells[0], cells[1], cells[2]
        else:
            info, feat = cells[0], cells[1]
        out.append({
            "voice": field(info, "voice参数"),
            "名称": field(info, "名称"),
            "性别": field(info, "性别"),
            "年龄": field(info, "年龄").removesuffix("岁"),
            "类别": "系统音色",
            "声线特质": field(info, "特质"),
            "适用场景": scene,
            "语言": field(info, "语言"),
            **features(feat),
        })
    return out


def read_xlsx(path: Path) -> list[list[str]]:
    """最小 xlsx 读取：第一个工作表，共享字符串 + 内联值。"""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{ns['m']}}}t")))
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    rows = []
    for r in sheet.iter(f"{{{ns['m']}}}row"):
        vals = {}
        for c in r.findall("m:c", ns):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            v = c.find("m:v", ns)
            text = "" if v is None else v.text or ""
            if c.get("t") == "s":
                text = shared[int(text)]
            elif c.get("t") == "inlineStr":
                text = "".join(t.text or "" for t in c.iter(f"{{{ns['m']}}}t"))
            vals[col] = text
        width = max((ord(k[-1]) - 64 for k in vals), default=0)
        rows.append([vals.get(chr(65 + i), "") for i in range(width)])
    return rows


def parse_30_basic(model: str) -> list[dict]:
    path = basic_xlsx(model)
    rows = read_xlsx(path)
    head = rows[0]
    out = []
    for r in rows[1:]:
        col = dict(zip(head, r))
        if not col.get("voice参数"):
            continue
        out.append({
            "voice": col["voice参数"], "名称": col.get("名称", ""), "性别": col.get("性别", ""),
            "年龄": col.get("年龄", "").removesuffix(".0"), "类别": "基础音色（声音复刻）",
            "声线特质": col.get("特质", ""), "适用场景": col.get("适用场景", ""),
            "语言": col.get("语种", ""), "试听文件": col.get("预览音频文件名", ""),
        })
    return out


def write(model: str, rows: list[dict]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    path = official(model)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in COLUMNS})
    voices = [r["voice"] for r in rows]
    dup = {v for v in voices if voices.count(v) > 1}
    empty = sum(1 for v in voices if not v)
    odd = sorted({r.get("性别", "") for r in rows} - {"男", "女", ""})
    print(f"{path.name}: {len(rows)} voices"
          + (f"  [warn] duplicate: {sorted(dup)}" if dup else "")
          + (f"  [warn] {empty} rows without voice" if empty else "")
          + (f"  [warn] unexpected 性别 values: {odd}" if odd else ""))


def main() -> int:
    md = MD.read_text(encoding="utf-8")
    for model in ("qwen-audio-3.1-tts-plus", "qwen-audio-3.1-tts-flash"):
        write(model, parse_31(md, model))
    for model in ("qwen-audio-3.0-tts-plus", "qwen-audio-3.0-tts-flash"):
        write(model, parse_30_system(md, model) + parse_30_basic(model))
    return 0


if __name__ == "__main__":
    sys.exit(main())
