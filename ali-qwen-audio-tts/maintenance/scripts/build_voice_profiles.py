#!/usr/bin/env python3
"""把官方信息、声学测量、Omni 听感合并成最终音色表：reference/voices/<model>.csv（使用 skill 时唯一要读的）。

  maintenance/data/<model>.official.csv        官方文档（build_voice_tables.py）
  maintenance/data/<model>.measured.csv        试听音频的声学测量（analyze_voice_samples.py）
  maintenance/data/<model>.omni.csv            Qwen3.8-Omni-Flash 听感描述（describe_voices_omni.py）
  maintenance/data/<model>.gender-recheck.csv  可选，Omni 思考模式性别复核（recheck_gender_omni.py）

最终表只留选音色用得上的列：
  - 性别的核对过程收敛成「建议性别」+「性别备注」（只在存疑时填写）；
  - 听感的音高/语速与测量值重复，只留数值列；
  - 某个模型里全空或全相同的列自动去掉（例如 3.1 的 SSML/指令控制/时间戳全部「支持」），
    运行时打印这些常量，写进 SKILL.md。
核对过程的完整记录仍在 maintenance/data/ 下。只用标准库。
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import DATA, MODELS, VOICES, official  # noqa: E402

COLS = ["voice", "名称", "建议性别", "性别备注", "年龄段", "年龄(文档)", "类别", "音色关键词", "情绪风格",
        "播讲风格", "适用场景", "不适合", "一句话描述", "基频中位Hz", "语速字每秒", "声线特质(文档)",
        "适用场景(文档)", "语言", "地域", "SSML", "指令控制", "时间戳", "试听文件"]


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return {r["voice"]: r for r in csv.DictReader(path.open(encoding="utf-8-sig"))}


def is_child(trait: str, age: str) -> bool:
    return "童" in trait or "少年" in trait or (age.isdigit() and int(age) <= 14)


def gender(doc: str, heard: str, f0: str, trait: str, age: str, rc: dict | None) -> tuple[str, str]:
    """返回（建议性别, 性别备注）。三方一致时备注为空；拿不准的写「待确认」并说明原因。"""
    hz = float(f0) if f0 else None
    male_ish = hz is not None and hz < 165
    female_ish = hz is not None and hz >= 200          # 165–200 Hz 男女重叠，基频不下结论
    f0_txt = f"基频 {round(hz)} Hz" if hz is not None else "无基频测量"
    rc_txt = ""
    if rc:
        rc_txt = f"；Omni 思考模式复核：{rc['复核性别']}（{rc['复核一致度']}，{rc['成人或儿童']}）"
        if heard and heard != rc["复核性别"] and rc["成人或儿童"] != "儿童":
            rc_txt += f"，与重新描述时的判断（{heard}）相反"

    if is_child(trait, age) or heard == "童声" or (rc and rc["成人或儿童"] == "儿童"):
        label = f"童声/少年（文档：{doc}）" if doc in ("男", "女") else "童声/少年"
        return label, ""                               # 儿童嗓音难以从声音区分男女，以文档为准即可
    if doc not in ("男", "女"):
        guess = heard if heard in ("男", "女") else ("男" if male_ish else "女" if female_ish else "")
        return (f"{guess}（推断）" if guess else "待确认"), f"官方文档性别为「{doc}」；听感 {heard}，{f0_txt}"
    if rc:
        if rc["复核结论"] in ("复核与文档一致，首次听感有误", "复核多数与文档一致"):
            return doc, ""
        return "待确认", f"文档 {doc}，{f0_txt}{rc_txt}，需人工试听"
    if heard == doc:
        if (doc == "男" and female_ish) or (doc == "女" and male_ish):
            return "待确认", f"文档与听感均为{doc}，但{f0_txt}偏{'女' if female_ish else '男'}声，建议试听"
        return doc, ""
    if (doc == "男" and male_ish) or (doc == "女" and female_ish):
        return doc, ""                                  # 听感误判（常见于轻柔的男声），基频支持文档
    if (doc == "男" and female_ish) or (doc == "女" and male_ish):
        return "待确认", f"文档 {doc}，但听感为{heard}且{f0_txt}，疑似文档有误，建议试听"
    return "待确认", f"文档 {doc}，听感 {heard}，{f0_txt}（男女重叠区间），建议试听"


def main() -> int:
    VOICES.mkdir(parents=True, exist_ok=True)
    for model in MODELS:
        base = load(official(model))
        meas = load(DATA / f"{model}.measured.csv")
        omni = load(DATA / f"{model}.omni.csv")
        recheck = load(DATA / f"{model}.gender-recheck.csv")
        rows = []
        for voice, b in base.items():
            m, o = meas.get(voice, {}), omni.get(voice, {})
            g, note = gender(b.get("性别", ""), o.get("性别(听感)", ""), m.get("基频中位Hz", ""),
                             b.get("声线特质", ""), b.get("年龄", ""), recheck.get(voice))
            rows.append({
                "voice": voice, "名称": b.get("名称", ""), "建议性别": g, "性别备注": note,
                "年龄段": o.get("年龄段", ""), "年龄(文档)": b.get("年龄", ""), "类别": b.get("类别", ""),
                "音色关键词": o.get("音色关键词", ""), "情绪风格": o.get("情绪风格", ""),
                "播讲风格": o.get("播讲风格", ""), "适用场景": o.get("适用场景", ""), "不适合": o.get("不适合", ""),
                "一句话描述": o.get("一句话描述", ""), "基频中位Hz": m.get("基频中位Hz", ""),
                "语速字每秒": m.get("语速字每秒", ""), "声线特质(文档)": b.get("声线特质", ""),
                "适用场景(文档)": b.get("适用场景", ""), "语言": b.get("语言", ""), "地域": b.get("地域", ""),
                "SSML": b.get("SSML", ""), "指令控制": b.get("指令控制", ""), "时间戳": b.get("时间戳", ""),
                "试听文件": b.get("试听文件", ""),
            })
        # 全空或全相同的列去掉（「性别备注」即使全空也保留，说明没有存疑）
        keep, constants = [], {}
        for c in COLS:
            vals = {r[c] for r in rows}
            if c in ("voice", "名称", "建议性别", "性别备注") or len(vals - {""}) > 1 or ("" in vals and len(vals) > 1):
                keep.append(c)
            elif vals - {""}:
                constants[c] = next(iter(vals - {""}))
        out = VOICES / f"{model}.csv"
        with out.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=keep, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        pending = sum(1 for r in rows if r["建议性别"] == "待确认")
        print(f"{out.relative_to(VOICES.parent.parent)}: {len(rows)} voices, {len(keep)} columns, "
              f"待确认 {pending}" + (f"; 全部相同（已省略）: {constants}" if constants else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
