#!/usr/bin/env python3
"""下载官方试听音频，并生成 样例 -> 音色 的索引。

- 系统音色：从 maintenance/source/qwen-audio-音色列表.md 中每个音色的「试听」单元格提取
  （样例标签、朗读原文、wav 链接），下载到 maintenance/samples/system/。
- 基础音色：下载官方试听音频包（3.0 plus/flash 共用），解压到 maintenance/samples/basic/；
  需要的文件都已解压时不再下载压缩包。

输出 maintenance/samples/index.csv：model, voice, sample, label, text, file（file 相对 samples/）。
已下载的文件会跳过，可重复运行。只用标准库。
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_voice_tables import clean, field, read_xlsx  # noqa: E402
from paths import MODELS, SAMPLES, VOICE_LIST_MD as MD, basic_xlsx  # noqa: E402


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=120) as r, tmp.open("wb") as f:
                while chunk := r.read(1 << 16):
                    f.write(chunk)
            tmp.rename(dest)
            return
        except OSError as e:
            if attempt == 2:
                raise RuntimeError(f"download failed: {url}: {e}") from e


def section(md: str, model: str) -> str:
    start = md.index(f"### {model}")
    nxt = re.search(r"^#{2,3} ", md[start + 4:], re.M)
    return md[start: start + 4 + nxt.start()] if nxt else md[start:]


def system_samples(md: str) -> list[dict]:
    out = []
    for model in MODELS:
        sec = section(md, model)
        for tr in re.findall(r"<tr>(.*?)</tr>", sec, re.S):
            cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
            if not cells:
                continue
            info = next((clean(c) for c in cells if "voice" in clean(c) and "参数" in clean(c)), "")
            voice = field(info, "voice参数") or field(info, "voice 参数")
            if not voice:
                continue
            for cell in cells:
                if "<source" not in cell and "<audio" not in cell:
                    continue
                # 每个样例：标签（加粗或纯文字行）+ 可选的 ```text``` 原文 + 一个音频地址。
                # 两种写法：<audio><source src=…/></audio>（3.1 plus、3.0）和 <audio src=…/>（3.1 flash）
                cell = re.sub(r"<audio[^>]*?>\s*(<source[^>]*>)\s*</audio>", r"\1", cell)
                pieces = re.split(r"(<source[^>]*>|<audio[^>]*src=[^>]*>)", cell)
                label, text, n = "", "", 0
                for piece in pieces:
                    m = re.search(r'src="([^"]+)"', piece)
                    if m and (piece.startswith("<source") or piece.startswith("<audio")):
                        n += 1
                        out.append({"model": model, "voice": voice, "sample": n, "label": label or f"试听 {n}",
                                    "text": text, "url": m.group(1)})
                        label, text = "", ""
                        continue
                    code = re.search(r"```text\s*(.*?)```", piece, re.S)
                    if code:
                        text = " ".join(code.group(1).split())
                        piece = piece[:code.start()] + piece[code.end():]
                    lines = [clean(x) for x in piece.splitlines() if clean(x)]
                    if lines:
                        label = lines[-1]
    return out


def main() -> int:
    md = MD.read_text(encoding="utf-8")
    rows = []
    sysrows = system_samples(md)
    for i, r in enumerate(sysrows, 1):
        name = Path(r["url"]).name
        dest = SAMPLES / "system" / f"{hashlib.md5(r['url'].encode()).hexdigest()[:8]}-{name}"
        download(r["url"], dest)
        rows.append({**{k: r[k] for k in ("model", "voice", "sample", "label", "text")},
                     "file": str(dest.relative_to(SAMPLES))})
        print(f"\rsystem samples {i}/{len(sysrows)}", end="", file=sys.stderr)
    print(file=sys.stderr)

    basic_dir = SAMPLES / "basic"
    tables = {m: read_xlsx(basic_xlsx(m)) for m in ("qwen-audio-3.0-tts-plus", "qwen-audio-3.0-tts-flash")}
    needed = {dict(zip(t[0], r)).get("预览音频文件名", "") for t in tables.values() for r in t[1:]} - {""}
    zpath = SAMPLES / "basic.zip"
    if not all((basic_dir / f).exists() for f in needed):  # 缺文件才下载约 210MB 的压缩包
        zurl = re.search(r'https?://[^ "<>)]+\.zip', md).group(0)
        download(zurl, zpath)
        with zipfile.ZipFile(zpath) as z:
            wavs = {Path(n).name: n for n in z.namelist() if n.lower().endswith(".wav")}
            for fname in needed:
                dest = basic_dir / fname
                if fname in wavs and not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(z.read(wavs[fname]))
        zpath.unlink()  # 用完即删，解压后的 wav 已足够
    for model, table in tables.items():
        head = table[0]
        for r in table[1:]:
            col = dict(zip(head, r))
            dest = basic_dir / col.get("预览音频文件名", "")
            if not col.get("voice参数") or not dest.is_file():
                continue
            rows.append({"model": model, "voice": col["voice参数"], "sample": 1, "label": "试听",
                         "text": "", "file": str(dest.relative_to(SAMPLES))})
    with (SAMPLES / "index.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["model", "voice", "sample", "label", "text", "file"])
        w.writeheader()
        w.writerows(rows)
    by_model = {}
    for r in rows:
        by_model.setdefault(r["model"], set()).add(r["voice"])
    for m in MODELS:
        print(f"{m}: {len(by_model.get(m, ()))} voices, {sum(1 for r in rows if r['model'] == m)} samples")
    return 0


if __name__ == "__main__":
    sys.exit(main())
