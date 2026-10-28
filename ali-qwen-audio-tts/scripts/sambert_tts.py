#!/usr/bin/env python3
"""Use the DashScope Python SDK to synthesize Sambert speech in Beijing."""

import argparse
import json
import os
import sys
from pathlib import Path

VOICES_48K = {
    "sambert-zhinan-v1", "sambert-zhiqi-v1", "sambert-zhichu-v1",
    "sambert-zhide-v1", "sambert-zhijia-v1", "sambert-zhiru-v1",
    "sambert-zhiqian-v1", "sambert-zhixiang-v1", "sambert-zhiwei-v1",
}


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--text", required=True)
    p.add_argument("--voice", required=True, help="Sambert voice, e.g. sambert-zhichu-v1")
    p.add_argument("--workspace-id", default=os.getenv("ALI_WORKSPACE_ID"))
    p.add_argument("--api-key", default=os.getenv("DASHSCOPE_API_KEY"))
    p.add_argument("--endpoint", choices=("auto", "workspace", "legacy"), default="auto",
                   help="auto tries the workspace endpoint then falls back on DNS failure")
    p.add_argument("--format", choices=("wav", "mp3", "pcm"), default="wav")
    p.add_argument("--sample-rate", type=int, default=None,
                   help="Defaults to 48 kHz for listed 48k models, otherwise 16 kHz")
    p.add_argument("--volume", type=int, default=None)
    p.add_argument("--rate", type=float, default=None)
    p.add_argument("--pitch", type=float, default=None)
    p.add_argument("--timestamps", type=Path,
                   help="Save sentence and word timestamps; enables word timestamps")
    p.add_argument("--phoneme-timestamps", action="store_true",
                   help="Include phonemes in --timestamps")
    p.add_argument("--metadata", type=Path)
    p.add_argument("--output", required=True, type=Path)
    return p.parse_args(argv)


def validate(a):
    if not a.api_key:
        raise ValueError("缺少 DASHSCOPE_API_KEY；也可传 --api-key")
    if not a.workspace_id:
        raise ValueError("缺少 ALI_WORKSPACE_ID；也可传 --workspace-id")
    if not a.text.strip() or len(a.text) > 10000:
        raise ValueError("--text 必须为 1–10000 个字符")
    if not a.voice.startswith("sambert-"):
        raise ValueError("--voice 必须是 Sambert 音色 ID，见 reference/Sambert/sdk接入.md 的音色列表")
    if a.sample_rate is not None and a.sample_rate not in (8000, 16000, 22050, 24000, 48000):
        raise ValueError("--sample-rate 必须是 8000、16000、22050、24000 或 48000")
    if a.volume is not None and not 0 <= a.volume <= 100:
        raise ValueError("--volume 范围是 0–100")
    for name in ("rate", "pitch"):
        value = getattr(a, name)
        if value is not None and not 0.5 <= value <= 2.0:
            raise ValueError(f"--{name} 范围是 0.5–2.0")
    if a.phoneme_timestamps and not a.timestamps:
        raise ValueError("--phoneme-timestamps 需要同时提供 --timestamps")
    if a.output.suffix.lower() != f".{a.format}":
        raise ValueError(f"--output 扩展名应为 .{a.format}")


def save_json(path, value):
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def endpoint_url(workspace_id, endpoint):
    if endpoint == "legacy":
        return "wss://dashscope.aliyuncs.com/api-ws/v1/inference"
    return f"wss://{workspace_id}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"


def error_message(response):
    """Turn common Sambert SDK failures into an actionable, secret-free message."""
    data = response or {}
    if not isinstance(data, dict):
        return str(data)
    code = data.get("code", "")
    message = data.get("message", "")
    request_id = data.get("request_id", "")
    if code == "AllocationQuota.FreeTierOnly":
        detail = ("免费额度已用完，请求未合成。到百炼控制台完成付费设置，或关闭「仅使用免费额度」后重试"
                  "（关闭后将按量计费）。")
    elif code == "ClientConnectorError":
        detail = "无法连接 WebSocket 域名；检查 DNS 或使用 --endpoint legacy。"
    else:
        detail = message or "Sambert 请求失败。"
    return f"{detail} code={code or 'unknown'} request_id={request_id or 'unknown'}"


def synthesize_once(a, dashscope, synthesizer, endpoint):
    dashscope.base_websocket_api_url = endpoint_url(a.workspace_id, endpoint)
    sample_rate = a.sample_rate or (48000 if a.voice in VOICES_48K else 16000)
    # The SDK names this field model. In this skill, Sambert is the model and
    # its value selects a voice, so the public CLI consistently calls it voice.
    kwargs = {"model": a.voice, "text": a.text, "workspace": a.workspace_id,
              "format": a.format, "sample_rate": sample_rate}
    for name in ("volume", "rate", "pitch"):
        value = getattr(a, name)
        if value is not None:
            kwargs[name] = value
    if a.timestamps:
        kwargs["word_timestamp_enabled"] = True
    if a.phoneme_timestamps:
        kwargs["phoneme_timestamp_enabled"] = True
    return synthesizer.call(**kwargs), sample_rate


def synthesize(a):
    try:
        import dashscope
        from dashscope.audio.tts import SpeechSynthesizer
    except ImportError as exc:
        raise RuntimeError("缺少 DashScope Python SDK：python3 -m pip install -U dashscope") from exc

    dashscope.api_key = a.api_key
    attempts = ("workspace", "legacy") if a.endpoint == "auto" else (a.endpoint,)
    response = None
    for endpoint in attempts:
        result, sample_rate = synthesize_once(a, dashscope, SpeechSynthesizer, endpoint)
        audio = result.get_audio_data()
        response = result.get_response()
        # DNS failures never reach the service, so a legacy retry cannot duplicate a billed request.
        if audio or endpoint != "workspace" or not isinstance(response, dict) or response.get("code") != "ClientConnectorError":
            break
        print("业务空间专属域名无法连接，尝试旧 WebSocket 域名…", file=sys.stderr)
    if not audio:
        raise RuntimeError(f"Sambert 未返回音频：{error_message(response)}")
    timestamps = result.get_timestamps() if a.timestamps else None
    if a.timestamps and not timestamps:
        print("警告：模型未返回时间戳，请核对模型列表的时间戳支持情况。", file=sys.stderr)

    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_bytes(audio)
    save_json(a.timestamps, {
        "model": "sambert", "voice": a.voice, "text": a.text, "time_unit": "ms",
        "time_origin": "audio-start", "sentences": timestamps or [],
    })
    save_json(a.metadata, {"model": "sambert", "voice": a.voice, "text": a.text, "endpoint": endpoint,
                           "format": a.format, "sample_rate": sample_rate,
                           "audio_bytes": len(audio), "sentence_count": len(timestamps or [])})
    return {"output": str(a.output), "endpoint": endpoint, "audio_bytes": len(audio),
            "timestamps": str(a.timestamps) if a.timestamps else None,
            "metadata": str(a.metadata) if a.metadata else None}


def main(argv=None):
    if sys.version_info < (3, 9):
        raise SystemExit("Sambert 接入要求 Python 3.9 或更高版本。")
    a = parse_args(argv)
    validate(a)
    print(json.dumps(synthesize(a), ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        raise SystemExit(1)
