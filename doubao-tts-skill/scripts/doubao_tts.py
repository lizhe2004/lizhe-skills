#!/usr/bin/env python3
"""豆包单向流式 HTTP TTS 的最小可复用客户端。

响应可能是单个 JSON，也可能是换行分隔的 JSON；脚本会合并其中的 base64 data，
并在开启字级时间戳时（--enable-subtitle 或 --timestamps）聚合响应中的
sentence.words，输出结构化时间轴 JSON，供视频合成等音画同步场景使用。

发请求前按 reference/voices/ 的音色表检查音色与资源是否匹配；网络中断、限流、
超并发和服务端错误会自动重试；其余错误输出一行中文说明并附 request_id / logid。
"""
from __future__ import annotations

import sys

if sys.version_info < (3, 9):
    sys.exit(f"需要 Python 3.9 及以上，当前是 {sys.version.split()[0]}（{sys.executable}）。")

import argparse
import base64
import csv
import http.client
import json
import os
import socket
import ssl
import time
import uuid
import wave
from io import BytesIO
from pathlib import Path
from urllib import error, request

ENDPOINT = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
DONE_CODE = 20000000
VOICES = Path(__file__).resolve().parent.parent / "reference" / "voices"
RESOURCES = ("seed-tts-2.0", "seed-icl-2.0")
ICL_MODELS = ("seed-tts-2.0-standard", "seed-tts-2.0-expressive")   # model 参数只对复刻音色生效

# 推流中途断开、连接被重置、超时：服务端偶发，重试即可
NETWORK_ERRORS = (http.client.IncompleteRead, http.client.RemoteDisconnected, ConnectionError,
                  TimeoutError, socket.timeout, ssl.SSLError, error.URLError)


class DoubaoError(RuntimeError):
    """接口返回的错误。retryable：限流、超并发、服务端错误或合成超时，可以重试。"""

    def __init__(self, status: int | None, code, message: str, request_id: str, logid: str | None):
        self.status, self.code, self.message = status, code, message or ""
        self.request_id, self.logid = request_id, logid
        code_s = str(code or "")
        # 依据 reference/错误码.md：5 开头和超并发一般可重试，但「资源与音色不匹配」「请求体过大」是配置问题，重试无效
        not_retryable = "mismatched" in self.message or "size too large" in self.message
        self.retryable = not not_retryable and (
            status in (429, 500, 502, 503, 504) or code_s.startswith("5")
            or "concurrency" in self.message or "timeout" in self.message.lower())
        super().__init__(f"{code}: {self.message}")


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="调用豆包单向流式 HTTP TTS")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text")
    src.add_argument("--text-file", type=Path)
    p.add_argument("--speaker", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--api-key", default=os.getenv("DOUBAO_API_KEY"))
    p.add_argument("--resource-id", default=os.getenv("DOUBAO_RESOURCE_ID", "seed-tts-2.0"), choices=RESOURCES,
                   help="seed-tts-2.0：预置 2.0 音色；seed-icl-2.0：声音复刻音色")
    p.add_argument("--model", choices=ICL_MODELS,
                   help="仅复刻音色（seed-icl-2.0）使用，默认 seed-tts-2.0-standard；指定后不能再用 --context-text")
    p.add_argument("--format", choices=["mp3", "pcm", "ogg_opus", "wav"], default="mp3")
    p.add_argument("--sample-rate", type=int, default=24000)
    p.add_argument("--speech-rate", type=int, default=0)
    p.add_argument("--loudness-rate", type=int, default=0)
    p.add_argument("--explicit-language")
    p.add_argument("--context-text", action="append", default=[])
    p.add_argument("--silence-duration", type=int, default=0)
    p.add_argument("--enable-subtitle", action="store_true")
    p.add_argument("--usage-tokens", action="store_true", help="要求接口返回计费字符数")
    p.add_argument("--disable-markdown-filter", action="store_true")
    p.add_argument("--disable-emoji-filter", action="store_true")
    p.add_argument("--additions", help="JSON 对象；脚本会序列化为接口要求的 additions 字符串")
    p.add_argument("--timestamps", type=Path, help="字级时间轴 JSON 输出路径；开启 --enable-subtitle 但不指定时默认写到音频旁的 <文件名>.timestamps.json")
    p.add_argument("--endpoint", default=ENDPOINT)
    p.add_argument("--timeout", type=int, default=300, help="单次请求超时秒数（默认 300，长文本可调大）")
    p.add_argument("--retries", type=int, default=3,
                   help="网络中断、限流、超并发、服务端错误时的重试次数（默认 3，0 表示不重试）")
    p.add_argument("--skip-voice-check", action="store_true", help="跳过发请求前的音色/资源匹配检查")
    return p.parse_args()


def load_voices(name: str) -> dict[str, dict]:
    path = VOICES / name
    if not path.exists():
        return {}
    return {r["voice_type"]: r for r in csv.DictReader(path.open(encoding="utf-8-sig"))}


def check_voice(a: argparse.Namespace) -> None:
    """发请求前拦下必然失败或会被静默忽略的组合，避免浪费调用、拿到难懂的错误码。"""
    if a.model and a.resource_id != "seed-icl-2.0":
        raise SystemExit("--model 只用于声音复刻音色，需同时指定 --resource-id seed-icl-2.0。")
    if a.model and a.context_text:
        raise SystemExit("复刻音色指定 --model 后不支持语音指令 --context-text，请二选一。")
    if a.skip_voice_check:
        return
    v2, v1, rt = load_voices("doubao-tts-2.0.csv"), load_voices("doubao-tts-1.0.csv"), load_voices("doubao-realtime-s2s.csv")
    if a.speaker in v2:
        if a.resource_id != "seed-tts-2.0":
            raise SystemExit(f"{a.speaker} 是 2.0 预置音色，需使用 --resource-id seed-tts-2.0（当前 {a.resource_id}）。")
        if a.context_text and v2[a.speaker].get("指令遵循") != "是":
            print(f"提示：音色表未标注 {a.speaker} 支持指令遵循，--context-text 可能不生效。", file=sys.stderr)
        return
    if a.speaker in v1:
        alt_name = v1[a.speaker].get("对应2.0音色", "")
        alt = next((k for k, r in v2.items() if alt_name and r.get("音色名称") == alt_name), "")
        hint = f"可改用对应的 2.0 音色「{alt_name}」：{alt}" if alt else "请在 reference/voices/doubao-tts-2.0.csv 中另选音色"
        raise SystemExit(f"{a.speaker} 是 1.0 音色，本接口只支持 seed-tts-2.0 / seed-icl-2.0。{hint}。")
    if a.speaker in rt:
        raise SystemExit(f"{a.speaker} 是实时语音（S2S/SC）专用音色，不能用于单向 TTS 接口。")
    if a.resource_id != "seed-icl-2.0":
        raise SystemExit(f"音色表里找不到 {a.speaker}。若是声音复刻音色，需使用 --resource-id seed-icl-2.0；"
                         "若是预置音色，请检查拼写（区分大小写）。确认无误可加 --skip-voice-check 跳过检查。")


def explain(e: DoubaoError) -> str:
    """常见错误翻译成可操作的中文提示。错误码页面混合了多个接口，这里按 message 关键字和码段识别。"""
    msg, code = e.message, str(e.code or "")
    if "mismatched" in msg:
        return ("该资源下没有这个音色：依次检查服务是否已开通、音色 ID 拼写、复刻音色是否过期、账号是否有该音色权限；"
                "预置 2.0 音色用 seed-tts-2.0，复刻音色用 seed-icl-2.0。")
    if "size too large" in msg:
        return "请求体过大：缩短单次文本，按自然句拆成多次请求。"
    if "InvalidDialect" in msg:
        return "explicit_dialect 参数非法：按 reference/tts-http-api.md 修正，并确认所选音色支持该方言。"
    if "unmarshal" in msg:
        return "请求体不是合法 JSON：检查 --additions 等参数。"
    if "connect downstream service timeout" in msg:
        return "网关连接下游服务超时，已重试仍失败：稍后再试；持续出现请带 logid 联系技术支持。"
    if "speaker" in msg.lower() and ("not found" in msg.lower() or "invalid" in msg.lower()):
        return "音色不存在或为空：检查 --speaker 拼写，并确认它与 --resource-id 匹配（预置 2.0 用 seed-tts-2.0，复刻用 seed-icl-2.0）。"
    if "concurrency" in msg:
        return "超出并发上限，已重试仍失败：降低并发或错峰调用；如需更高并发可在控制台增购。"
    if "InvalidModel" in msg:
        return "model 参数非法：只有复刻音色可用，取值 seed-tts-2.0-standard 或 seed-tts-2.0-expressive。"
    if "No readable text" in msg:
        return "文本里没有可朗读的内容：检查 --text 是否只剩标点、Markdown 或 Emoji（可调整过滤开关）。"
    if "synthesis processing timeout" in msg or "timeout" in msg.lower():
        return "服务端合成超时，通常是单次文本过长：按自然句拆成多次请求，或错峰调用。"
    if "EmptyRequest" in msg or "req_params" in msg:
        return "请求体缺少 req_params：脚本或参数构造有误。"
    if "审核" in msg or "audit" in msg.lower():
        return "文本或合成结果未通过内容审核：调整文本后重试。"
    if e.status == 401:
        return "鉴权失败：检查 DOUBAO_API_KEY 是否正确。"
    if e.status == 403:
        return "无权调用：确认该资源（--resource-id）已在控制台开通，且账户有可用额度。"
    if code.startswith("4"):
        return "请求参数有误：按 reference/tts-http-api.md 检查参数取值与约束。"
    if e.retryable:
        return "服务端错误或限流，已按设定次数重试仍失败，请稍后再试。"
    return "接口返回错误。"


def find_code_message(obj) -> tuple:
    """错误体结构不固定（可能嵌在 header 等字段里），递归找第一组 code / message。"""
    if isinstance(obj, dict):
        if "code" in obj or "message" in obj:
            return obj.get("code"), obj.get("message", "")
        for v in obj.values():
            c, m = find_code_message(v)
            if c is not None or m:
                return c, m
    return None, ""


def parse_json_stream(raw: bytes) -> list[dict]:
    text = raw.decode("utf-8", errors="replace").strip()
    if not text:
        return []
    try:
        value = json.loads(text)
        return value if isinstance(value, list) else [value]
    except json.JSONDecodeError:
        out = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"响应不是有效 JSON：{line[:200]}") from exc
        return out


def audio_duration(audio: bytes, fmt: str, sample_rate: int) -> float | None:
    """按容器/编码估算音频时长（秒）；mp3/ogg 无法直接计算时返回 None。"""
    if fmt == "wav":
        try:
            with wave.open(BytesIO(audio), "rb") as wf:
                return wf.getnframes() / wf.getframerate()
        except wave.Error:
            return None
    if fmt == "pcm":
        # 接口 PCM 为单声道 16bit 小端有符号整型。
        return len(audio) / 2 / sample_rate
    return None


def normalize_sentence(sent: dict) -> dict:
    """把一条 sentence 归一成 {text, start, end, words[, phonemes]}，时间单位秒。"""
    words = [
        {
            "word": w.get("word"),
            "start": w.get("startTime"),
            "end": w.get("endTime"),
            "confidence": w.get("confidence"),
        }
        for w in sent.get("words") or []
    ]
    starts = [w["start"] for w in words if w["start"] is not None]
    ends = [w["end"] for w in words if w["end"] is not None]
    out = {
        "text": sent.get("text"),
        "start": min(starts) if starts else None,
        "end": max(ends) if ends else None,
        "words": words,
    }
    if sent.get("phonemes"):
        out["phonemes"] = sent["phonemes"]
    return out


def build_timeline(sentences: list[dict]) -> list[dict]:
    """汇总各响应分片里的 sentence，返回按序排列的句子列表。

    接口各分片的 startTime/endTime 均以整段音频起点为零基准（秒，float），
    按到达顺序排列即可，不需要额外偏移；字级时间戳嵌在每句的 words 中，
    需要扁平字轨时由使用方自行摊平（信息无损）。
    """
    # 接口会额外下发一条 words 为空的 sentence，回显整段输入原文，不是时间轴片段，丢弃。
    return [normalize_sentence(s) for s in sentences if s.get("words")]


def synthesize(a: argparse.Namespace, payload: bytes) -> tuple[str, str | None, list[dict]]:
    """发一次请求并完整读取、解析响应。每次调用用新的 request_id；业务错误抛 DoubaoError。"""
    request_id = str(uuid.uuid4())
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": a.api_key,
        "X-Api-Resource-Id": a.resource_id,
        "X-Api-Request-Id": request_id,
    }
    if a.usage_tokens:
        headers["X-Control-Require-Usage-Tokens-Return"] = "*"
    req = request.Request(a.endpoint, data=payload, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=a.timeout) as response:
            logid = response.headers.get("X-Tt-Logid")
            raw = response.read()
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            code, message = find_code_message(json.loads(body))
        except json.JSONDecodeError:
            code, message = None, body[:300]
        raise DoubaoError(exc.code, code or f"HTTP {exc.code}", message, request_id,
                          exc.headers.get("X-Tt-Logid")) from exc
    messages = parse_json_stream(raw)
    for message in messages:
        # 单向流以 20000000 表示正常结束；它不是错误码。
        if message.get("code", 0) not in (0, None, DONE_CODE):
            raise DoubaoError(None, message.get("code"), message.get("message", ""), request_id, logid)
    return request_id, logid, messages


def main() -> int:
    a = args()
    if not a.api_key:
        raise SystemExit("缺少 API Key：请设置 DOUBAO_API_KEY 或传入 --api-key")
    check_voice(a)
    text = a.text if a.text is not None else a.text_file.read_text(encoding="utf-8")
    # 指定 --timestamps 隐含需要字幕；只开 --enable-subtitle 时默认在音频旁落一份时间轴。
    ts_path = a.timestamps
    subtitle_enabled = a.enable_subtitle or ts_path is not None
    if a.enable_subtitle and ts_path is None:
        ts_path = a.output.with_suffix(a.output.suffix + ".timestamps.json")
    req_params = {
        "text": text,
        "speaker": a.speaker,
        "audio_params": {
            "format": a.format,
            "sample_rate": a.sample_rate,
            "speech_rate": a.speech_rate,
            "loudness_rate": a.loudness_rate,
            "enable_subtitle": subtitle_enabled,
            "silence_duration": a.silence_duration,
            "disable_markdown_filter": a.disable_markdown_filter,
            "disable_emoji_filter": a.disable_emoji_filter,
        },
    }
    if a.model:
        req_params["model"] = a.model
    if a.context_text:
        req_params["context_texts"] = a.context_text
    if a.explicit_language:
        req_params["explicit_language"] = a.explicit_language
    if a.additions:
        try:
            req_params["additions"] = json.dumps(json.loads(a.additions), ensure_ascii=False, separators=(",", ":"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"--additions 不是有效 JSON：{exc}") from exc
    payload = json.dumps({"req_params": req_params}, ensure_ascii=False).encode("utf-8")

    # 整个响应读完、解析完才写文件，中途失败重试不会留下半截音频
    for attempt in range(a.retries + 1):
        try:
            request_id, logid, messages = synthesize(a, payload)
            break
        except DoubaoError as e:
            if not e.retryable or attempt == a.retries:
                raise
            reason = f"code={e.code}"
        except NETWORK_ERRORS as e:
            if attempt == a.retries:
                raise
            reason = type(e).__name__
        wait = 2 ** (attempt + 1)
        print(f"第 {attempt + 1} 次请求失败（{reason}），{wait} 秒后重试…", file=sys.stderr)
        time.sleep(wait)

    audio = bytearray()
    raw_sentences = []
    usage = None
    for message in messages:
        encoded = message.get("data")
        if encoded:
            try:
                audio.extend(base64.b64decode(encoded))
            except (ValueError, TypeError) as exc:
                raise SystemExit("响应中的 data 不是有效 base64") from exc
        sentence = message.get("sentence")
        if isinstance(sentence, dict) and (sentence.get("words") or sentence.get("text")):
            raw_sentences.append(sentence)
        if isinstance(message.get("usage"), dict):
            usage = message["usage"]
    if not audio:
        raise SystemExit(f"接口未返回音频 data；请检查 speaker、resource-id 和请求参数（request_id={request_id} logid={logid}）")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_bytes(audio)

    sentences = build_timeline(raw_sentences)
    total_words = sum(len(s["words"]) for s in sentences)
    if subtitle_enabled and not total_words:
        print("提示：已请求字幕但响应中没有字级时间戳（该能力仅支持中文/英文），时间轴将为空", file=sys.stderr)
    last_word_end = sentences[-1]["words"][-1]["end"] if sentences else None
    container_duration = audio_duration(bytes(audio), a.format, a.sample_rate)
    duration = container_duration
    if duration is None and last_word_end is not None:
        duration = last_word_end
    # 时间轴体检：PCM/WAV 能算出精确容器时长，若与末字 end 差距明显，
    # 可能是各分片时间戳按分段归零（需要累加偏移），不能直接用于音画同步。
    if last_word_end is not None and container_duration is not None:
        drift = container_duration - last_word_end
        tolerance = 0.3 + a.silence_duration / 1000
        if abs(drift) > tolerance:
            print(
                f"警告：时间轴末字 end={last_word_end:.3f}s 与音频容器时长 "
                f"{container_duration:.3f}s 偏差 {drift:+.3f}s（已计入尾部静音 "
                f"{a.silence_duration}ms 容差）。"
                "请检查各分片时间戳是否以整段音频为零基准；若为分段归零，"
                "拼接 words 时需要累加各分片音频时长作为偏移。",
                file=sys.stderr,
            )
    if ts_path:
        timeline = {
            "schema": "doubao-tts-timeline/v1",
            "request_id": request_id,
            "logid": logid,
            "audio": {
                "file": a.output.name,
                "format": a.format,
                "sample_rate": a.sample_rate,
                "bytes": len(audio),
                "duration": duration,
            },
            "duration": duration,
            "sentences": sentences,
            "usage": usage,
        }
        ts_path.parent.mkdir(parents=True, exist_ok=True)
        ts_path.write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"音频已写入：{a.output}（{len(audio)} bytes）")
    if ts_path:
        print(f"字级时间轴已写入：{ts_path}（{len(sentences)} 句 / {total_words} 字，时长 {duration}s）")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit("已取消")
    except DoubaoError as exc:
        print(f"错误：{explain(exc)}\n"
              f"  code={exc.code}  HTTP={exc.status}  request_id={exc.request_id}  logid={exc.logid}\n"
              f"  原始信息：{exc.message[:300]}", file=sys.stderr)
        raise SystemExit(1)
    except NETWORK_ERRORS as exc:
        print(f"错误：网络连接中断，已重试仍失败（{type(exc).__name__}: {exc}）。"
              "可稍后重试，或用 --retries / --timeout 调大。", file=sys.stderr)
        raise SystemExit(1)
    except RuntimeError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        raise SystemExit(1)
