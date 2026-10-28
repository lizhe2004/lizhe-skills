#!/usr/bin/env python3
"""对官方试听音频做声学测量，为每个模型生成一份「实测音色画像」。

输入：maintenance/samples/index.csv（由 fetch_voice_samples.py 生成）和 maintenance/data/<model>.official.csv
输出：maintenance/data/<model>.measured.csv

测量全部来自信号本身，不是人耳主观评价：
  基频（YIN）中位数与音域、语调起伏、语速、停顿占比、频谱质心（明亮度）、高频能量占比。
语速：样例带朗读原文时用「有效字数 / 发声时长」；否则用包络峰值计数估算音节率，
并用带原文的样例做线性校准。依赖 numpy、scipy。
"""
import csv
import re
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, find_peaks, resample_poly, sosfiltfilt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import DATA, MODELS, SAMPLES, official  # noqa: E402
SR = 16000
HOP = 160          # 10 ms
WIN = 640          # 40 ms, enough for 60 Hz
FMIN, FMAX = 60.0, 500.0


def load(path):
    sr, x = wavfile.read(path)
    x = x.astype(np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    peak = np.max(np.abs(x)) or 1.0
    x = x / peak
    if sr != SR:
        g = np.gcd(int(sr), SR)
        x = resample_poly(x, SR // g, int(sr) // g)
    return x


def frames(x):
    n = 1 + max(0, (len(x) - WIN) // HOP)
    idx = np.arange(WIN)[None, :] + HOP * np.arange(n)[:, None]
    return x[idx]


def yin(fr, thresh=0.10):
    """逐帧 YIN 基频；无声帧返回 nan。"""
    tmin, tmax = int(SR / FMAX), int(SR / FMIN)
    w = WIN - tmax
    out = np.full(len(fr), np.nan)
    for i, f in enumerate(fr):
        x = f - f.mean()
        e = np.cumsum(np.concatenate([[0.0], x * x]))
        n = 1 << int(np.ceil(np.log2(2 * WIN)))
        spec = np.fft.rfft(x, n)
        acf = np.fft.irfft(spec * np.conj(np.fft.rfft(x[:w], n)), n)[: tmax + 1]
        tau = np.arange(tmax + 1)
        d = e[w] + (e[tau + w] - e[tau]) - 2 * acf
        d[0] = 0
        cmnd = d[1:] * np.arange(1, tmax + 1) / np.maximum(np.cumsum(d[1:]), 1e-12)
        cmnd = np.concatenate([[1.0], cmnd])
        cand = np.where(cmnd[tmin:] < thresh)[0]
        if len(cand) == 0:
            continue
        t = cand[0] + tmin
        while t + 1 <= tmax and cmnd[t + 1] < cmnd[t]:
            t += 1
        # 八度纠错：两倍周期处的周期性明显更强，说明选中的是半周期（二次谐波主导的低沉男声常见）
        if 2 * t + 2 <= tmax:
            t2 = 2 * t - 2 + int(np.argmin(cmnd[2 * t - 2: 2 * t + 3]))
            if cmnd[t2] < 0.5 * cmnd[t]:
                t = t2
        if 1 <= t < tmax:  # 抛物线插值
            a, b, c = cmnd[t - 1], cmnd[t], cmnd[t + 1]
            den = a - 2 * b + c
            t = t + (0.5 * (a - c) / den if den else 0)
        out[i] = SR / t
    return out


def measure(path, text=""):
    x = load(path)
    fr = frames(x)
    rms = np.sqrt((fr ** 2).mean(axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    speech = db > db.max() - 35
    on = np.where(speech)[0]
    if len(on) < 10:
        return None
    a, b = on[0], on[-1] + 1
    span = (b - a) * HOP / SR
    # 停顿：发声区间内连续 ≥150 ms 的静音
    sil, run = 0, 0
    for s in speech[a:b]:
        if not s:
            run += 1
        else:
            if run >= 15:
                sil += run
            run = 0
    pause_ratio = sil / max(1, b - a)

    f0 = yin(fr[a:b][speech[a:b]])
    f0 = f0[np.isfinite(f0)]
    if len(f0) < 20:
        return None
    # 去掉倍频/半频跳点：保留中位数 0.6–1.7 倍以内
    med = np.median(f0)
    f0 = f0[(f0 > med * 0.6) & (f0 < med * 1.7)]
    p10, p50, p90 = np.percentile(f0, [10, 50, 90])
    semis = 12 * np.log2(f0 / p50)

    spec = np.abs(np.fft.rfft(fr[a:b][speech[a:b]] * np.hanning(WIN), axis=1)) ** 2
    freqs = np.fft.rfftfreq(WIN, 1 / SR)
    centroid = float(np.median((spec * freqs).sum(axis=1) / np.maximum(spec.sum(axis=1), 1e-12)))
    hf = float(spec[:, freqs >= 4000].sum() / max(spec.sum(), 1e-12))

    # 音节率估计：300–3000 Hz 包络的峰值数
    sos = butter(4, [300, 3000], "band", fs=SR, output="sos")
    env = np.abs(sosfiltfilt(sos, x))
    env = np.convolve(env, np.ones(400) / 400, mode="same")[::HOP]  # 25 ms 平滑，10 ms 一点
    seg = env[a:b]
    peaks, _ = find_peaks(seg, distance=11, prominence=0.12 * np.percentile(seg, 95))
    # 语速口径：字数 / 首字到末字的总时长（含句间停顿），与常说的「字/秒」一致
    syl_rate = len(peaks) / max(span, 0.1)

    chars = len(re.findall(r"[一-鿿]", text)) + len(re.findall(r"[A-Za-z]+", text))
    rate = chars / span if chars >= 10 else None
    return {"f0": p50, "lo": p10, "hi": p90, "range": 12 * np.log2(p90 / p10),
            "sd": float(np.std(semis)), "pause": pause_ratio, "centroid": centroid, "hf": hf,
            "syl": syl_rate, "rate": rate, "dur": span}


def band(v, cuts, names):
    for c, n in zip(cuts, names):
        if v < c:
            return n
    return names[-1]


def pitch_tag(f0, gender, age, trait=""):
    if (age and age.isdigit() and int(age) <= 12) or "童" in trait:
        return "童声"
    if gender == "男":
        return band(f0, [100, 125, 155, 185], ["低沉", "偏低", "中等", "偏高", "高亢"])
    if gender == "女":
        return band(f0, [175, 205, 240, 275], ["低沉", "偏低", "中等", "偏高", "高亢"])
    return ""


def main():
    index = list(csv.DictReader((SAMPLES / "index.csv").open(encoding="utf-8-sig")))
    tables = {}
    for m in MODELS:
        tables[m] = {r["voice"]: r for r in csv.DictReader(official(m).open(encoding="utf-8-sig"))}

    cache = {}
    results = {}
    for i, r in enumerate(index, 1):
        key = r["file"]
        if key not in cache:
            cache[key] = measure(SAMPLES / key, r["text"])
        m = cache[key]
        if m:
            results.setdefault((r["model"], r["voice"]), []).append((r, m))
        print(f"\ranalyzed {i}/{len(index)}", end="", file=sys.stderr)
    print(file=sys.stderr)

    # 用带原文的样例校准音节率 -> 字/秒
    pairs = np.array([(m["syl"], m["rate"]) for v in results.values() for _, m in v if m["rate"]])
    k, c0 = np.polyfit(pairs[:, 0], pairs[:, 1], 1) if len(pairs) >= 5 else (1.0, 0.0)
    if len(pairs) >= 5:
        pred = k * pairs[:, 0] + c0
        mae = float(np.mean(np.abs(pred - pairs[:, 1])))
        print(f"rate calibration on {len(pairs)} texted samples: chars/s = {k:.2f} * peaks/s + {c0:.2f}, "
              f"MAE {mae:.2f}", file=sys.stderr)

    # 按性别算明亮度、语调起伏的分位数阈值（全体音色）
    agg = {}
    for (model, voice), items in results.items():
        meta = tables.get(model, {}).get(voice, {})
        ms = [m for _, m in items]
        rates = [m["rate"] for m in ms if m["rate"]]
        rate = float(np.median(rates)) if rates else float(k * np.median([m["syl"] for m in ms]) + c0)
        agg[(model, voice)] = {
            "meta": meta, "n": len(ms), "rate": rate, "rate_src": "原文" if rates else "估算",
            **{f: float(np.median([m[f] for m in ms])) for f in ("f0", "lo", "hi", "range", "sd", "pause", "centroid", "hf")},
        }
    pct = {}
    for g in ("男", "女"):
        vals = [a for a in agg.values() if a["meta"].get("性别") == g]
        if vals:
            pct[g] = {f: np.percentile([a[f] for a in vals], [25, 75]) for f in ("centroid", "sd")}

    cols = ["voice", "名称", "性别(文档)", "样例数", "基频中位Hz", "音域Hz(p10-p90)", "音域半音",
            "语调起伏(半音标准差)", "语速字每秒", "语速来源", "停顿占比", "频谱质心Hz", "高频占比",
            "音高", "语调", "语速", "音色", "实测描述", "性别核对", "推荐用途(规则)"]
    for model in tables:
        rows = []
        for (m, voice), a in agg.items():
            if m != model:
                continue
            meta, g = a["meta"], a["meta"].get("性别", "")
            p = pct.get(g)
            pitch = pitch_tag(a["f0"], g, meta.get("年龄", ""), meta.get("声线特质", ""))
            tone = (band(a["sd"], list(p["sd"]), ["平稳", "适中", "起伏大"]) if p else "")
            speed = band(a["rate"], [3.8, 4.6, 5.4], ["慢", "适中", "偏快", "快"])
            timbre = (band(a["centroid"], list(p["centroid"]), ["厚暖", "均衡", "明亮"]) if p else "")
            # 性别核对：文档性别与基频明显矛盾时提示
            check = ""
            if g == "男" and a["f0"] > 200 and pitch != "童声":
                check = "基频偏女声，建议试听"
            elif g == "女" and a["f0"] < 150:
                check = "基频偏男声，建议试听"
            elif g not in ("男", "女"):
                check = f"文档性别为「{g}」，实测更像{'女' if a['f0'] >= 165 else '男'}声"
            uses = []
            if pitch in ("低沉", "偏低", "中等") and tone in ("平稳", "适中") and speed in ("慢", "适中"):
                uses.append("旁白/纪录片")
            if tone == "平稳" and speed in ("适中", "偏快") and pitch in ("中等", "偏低"):
                uses.append("新闻/播报")
            if tone == "起伏大" and speed in ("偏快", "快"):
                uses.append("广告/带货")
            if tone in ("适中", "起伏大") and timbre in ("均衡", "明亮") and pitch not in ("低沉",):
                uses.append("口播/知识分享")
            if speed == "慢" and timbre == "厚暖":
                uses.append("有声书/助眠")
            desc = "，".join(x for x in [f"{g}声" if g in ("男", "女") else "", f"音高{pitch}" if pitch and pitch != "童声" else pitch,
                                         f"语调{tone}" if tone else "", f"语速{speed}", f"音色{timbre}" if timbre else ""] if x)
            rows.append({
                "voice": voice, "名称": meta.get("名称", ""), "性别(文档)": g, "样例数": a["n"],
                "基频中位Hz": round(a["f0"]), "音域Hz(p10-p90)": f"{round(a['lo'])}-{round(a['hi'])}",
                "音域半音": round(a["range"], 1), "语调起伏(半音标准差)": round(a["sd"], 2),
                "语速字每秒": round(a["rate"], 1), "语速来源": a["rate_src"], "停顿占比": round(a["pause"], 2),
                "频谱质心Hz": round(a["centroid"]), "高频占比": round(a["hf"], 3),
                "音高": pitch, "语调": tone, "语速": speed, "音色": timbre, "实测描述": desc,
                "性别核对": check, "推荐用途(规则)": "、".join(uses),
            })
        order = list(tables[model])
        rows.sort(key=lambda r: order.index(r["voice"]) if r["voice"] in order else 1e9)
        out = DATA / f"{model}.measured.csv"
        with out.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        flagged = sum(1 for r in rows if r["性别核对"])
        print(f"{out.name}: {len(rows)} voices, {flagged} gender flags")


if __name__ == "__main__":
    main()
