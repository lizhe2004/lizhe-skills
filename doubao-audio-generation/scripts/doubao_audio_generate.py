#!/usr/bin/env python3
"""Call Volcengine Seed Audio 1.0 non-streaming generation API."""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import uuid
from pathlib import Path
from urllib import error, request

ENDPOINT = "https://openspeech.bytedance.com/api/v3/tts/create"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="豆包 Seed Audio 1.0 音频生成")
    p.add_argument("--text-prompt", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--api-key", default=os.getenv("DOUBAO_API_KEY"))
    p.add_argument("--endpoint", default=ENDPOINT)
    p.add_argument("--model", default="seed-audio-1.0")
    p.add_argument("--speaker")
    p.add_argument("--audio-file", action="append", type=Path, default=[])
    p.add_argument("--audio-url", action="append", default=[])
    p.add_argument("--image-file", type=Path)
    p.add_argument("--image-url")
    p.add_argument("--format", choices=["wav", "mp3", "pcm", "ogg_opus"], default="wav")
    p.add_argument("--sample-rate", type=int)
    p.add_argument("--speech-rate", type=int, default=0)
    p.add_argument("--loudness-rate", type=int, default=0)
    p.add_argument("--pitch-rate", type=int, default=0)
    p.add_argument("--enable-subtitle", action="store_true")
    p.add_argument("--aigc-watermark", action="store_true")
    p.add_argument("--aigc-metadata", action="store_true")
    p.add_argument("--content-producer")
    p.add_argument("--produce-id")
    p.add_argument("--content-propagator")
    p.add_argument("--propagate-id")
    p.add_argument("--metadata", type=Path, help="保存响应 JSON（含字幕和时长）")
    return p


def b64_file(path: Path) -> str:
    try:
        return base64.b64encode(path.read_bytes()).decode("ascii")
    except OSError as exc:
        raise SystemExit(f"无法读取参考文件 {path}: {exc}") from exc


def validate(a: argparse.Namespace) -> None:
    if not a.api_key:
        raise SystemExit("缺少 API Key：请设置 DOUBAO_API_KEY 或传入 --api-key")
    if len(a.audio_file) + len(a.audio_url) > 3:
        raise SystemExit("参考音频最多 3 条")
    if a.audio_file and a.audio_url:
        raise SystemExit("--audio-file 与 --audio-url 不要混用；请按上传顺序统一提供")
    if a.image_file and a.image_url:
        raise SystemExit("--image-file 与 --image-url 互斥")
    if (a.image_file or a.image_url) and (a.speaker or a.audio_file or a.audio_url):
        raise SystemExit("参考图片不能与 speaker 或参考音频混用")
    if not -50 <= a.speech_rate <= 100:
        raise SystemExit("speech_rate 必须在 -50..100")
    if not -50 <= a.loudness_rate <= 100:
        raise SystemExit("loudness_rate 必须在 -50..100")
    if not -12 <= a.pitch_rate <= 12:
        raise SystemExit("pitch_rate 必须在 -12..12")


def make_references(a: argparse.Namespace) -> list[dict[str, str]] | None:
    refs: list[dict[str, str]] = []
    # A preset voice is also exposed to the Prompt through an audio-reference
    # slot.  This lets the model resolve ``@音频1`` consistently for roles,
    # rather than relying on a global top-level speaker field.
    if a.speaker:
        refs.append({"speaker": a.speaker})
    for path in a.audio_file:
        refs.append({"audio_data": b64_file(path)})
    for url in a.audio_url:
        refs.append({"audio_url": url})
    if a.image_file:
        refs.append({"image_data": b64_file(a.image_file)})
    elif a.image_url:
        refs.append({"image_url": a.image_url})
    return refs or None


def main() -> int:
    a = build_parser().parse_args()
    validate(a)
    audio_config: dict[str, object] = {
        "format": a.format,
        "speech_rate": a.speech_rate,
        "loudness_rate": a.loudness_rate,
        "pitch_rate": a.pitch_rate,
        "enable_subtitle": a.enable_subtitle,
    }
    if a.sample_rate is not None:
        audio_config["sample_rate"] = a.sample_rate
    prompt = a.text_prompt
    if a.speaker and "@音频" not in prompt:
        prompt = (
            f"主旁白（饰演者为@音频1，预置音色ID为 {a.speaker}）。"
            f"{prompt}"
        )
    body: dict[str, object] = {
        "model": a.model,
        "text_prompt": prompt,
        "audio_config": audio_config,
    }
    refs = make_references(a)
    if refs:
        body["references"] = refs
    watermark: dict[str, object] = {}
    if a.aigc_watermark:
        watermark["aigc_watermark"] = True
    if a.aigc_metadata:
        watermark["aigc_metadata"] = {"enable": True}
    if watermark:
        body["watermark"] = watermark
    for key in ("content_producer", "produce_id", "content_propagator", "propagate_id"):
        value = getattr(a, key)
        if value:
            body[key] = value

    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": a.api_key,
        "X-Api-Request-Id": str(uuid.uuid4()),
    }
    req = request.Request(a.endpoint, data=payload, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=180) as response:
            raw = response.read()
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1200]
        raise SystemExit(f"HTTP {exc.code}：{detail}") from exc
    except error.URLError as exc:
        raise SystemExit(f"网络请求失败：{exc.reason}") from exc

    try:
        result = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit("接口响应不是有效 JSON") from exc
    code = result.get("code", 0)
    if code not in (0, None):
        raise SystemExit(f"豆包接口错误 code={code} message={result.get('message', '')}")

    audio_b64 = result.get("audio")
    if audio_b64:
        try:
            audio = base64.b64decode(audio_b64)
        except (ValueError, TypeError) as exc:
            raise SystemExit("响应中的 audio 不是有效 Base64") from exc
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_bytes(audio)
    elif result.get("url"):
        try:
            with request.urlopen(result["url"], timeout=180) as audio_response:
                audio = audio_response.read()
        except (error.HTTPError, error.URLError) as exc:
            raise SystemExit(f"下载音频 URL 失败：{exc}") from exc
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_bytes(audio)
    else:
        raise SystemExit("接口未返回 audio 或 url")

    if a.metadata:
        a.metadata.parent.mkdir(parents=True, exist_ok=True)
        a.metadata.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"音频已写入：{a.output}（{len(audio)} bytes，{result.get('duration', '?')} 秒）")
    if a.metadata:
        print(f"元数据已写入：{a.metadata}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit("已取消")
