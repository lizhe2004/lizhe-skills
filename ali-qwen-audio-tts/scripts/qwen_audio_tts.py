#!/usr/bin/env python3
"""Synthesize audio with Alibaba Cloud Qwen-Audio-TTS HTTP API."""
from __future__ import annotations

import sys

# 旧版 Python 自带的 OpenSSL 与百炼接口 TLS 握手不兼容（实测 Anaconda 3.8 报 SSL: EOF occurred in violation of protocol）
if sys.version_info < (3, 10):
    sys.exit(f"需要 Python 3.10 及以上，当前是 {sys.version.split()[0]}（{sys.executable}）。"
             "请换用较新的 Python，例如 Homebrew 的 python3。")

import argparse
import base64
import http.client
import json
import os
import socket
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

# 推流中断、连接被重置、超时：服务端偶发，重试即可（实测 12 段里出现过 6 次 IncompleteRead）
NETWORK_ERRORS = (http.client.IncompleteRead, http.client.RemoteDisconnected, ConnectionError,
                  TimeoutError, socket.timeout, ssl.SSLError, urllib.error.URLError)


# 百炼错误码文档：这些虽然可能是 429 或带 Throttling 前缀，但属于计费/配额/订购问题，重试无效
NOT_RETRYABLE = ("AllocationQuota", "insufficient_quota", "CommodityNotPurchased", "BillOverdue",
                 "BudgetLimitExceeded", "Arrearage")


class ApiError(RuntimeError):
    """接口返回的业务错误。retryable 表示限流或服务端临时故障，可以重试。"""

    def __init__(self, status: int | None, code: str, message: str, request_id: str | None):
        self.status, self.code, self.message, self.request_id = status, code or "", message or "", request_id
        billing = any(x in self.code for x in NOT_RETRYABLE)
        self.retryable = not billing and (status in (429, 500, 502, 503, 504) or self.code.startswith("Throttling"))
        super().__init__(f"{self.code}: {self.message}")


def parse_error(status: int | None, body: str) -> ApiError:
    """兼容两种错误体：{"code","message","request_id"} 和 OpenAI 兼容的 {"error":{"code","message","id"}}。"""
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return ApiError(status, f"HTTP {status}", body[:300], None)
    err = data.get("error") if isinstance(data.get("error"), dict) else data
    return ApiError(status, err.get("code") or err.get("type") or "", err.get("message", ""),
                    data.get("request_id") or err.get("id"))


def explain(e: ApiError, model: str, voice: str) -> str:
    """把常见错误翻译成可操作的中文提示；认不出的原样给出。"""
    msg, code, low = e.message, e.code, e.message.lower()
    # 依据百炼错误码文档（摘要见 reference/错误码.md），先判计费/配额，再判限流：二者都可能是 429
    if "FreeTierOnly" in code or "free quota exhausted" in low or "free tier" in low:
        return (f"{model} 的免费额度已用完，请求被拒绝，没有扣费。可能是控制台开启了「免费额度用完即停」，"
                "也可能是新账号未实名认证。如需继续：关闭该开关（之后按量计费）或完成认证并充值；"
                "关闭后仍报错可尝试重置 API Key。")
    # 同一个 Throttling.AllocationQuota：400 是复刻音色数达上限，429 是调用配额超限
    if ("voice storage limit" in low or "voice-clone voice limit" in low
            or (code == "Throttling.AllocationQuota" and e.status == 400)):
        return "复刻音色数量已达账号上限：删除不用的复刻音色后再试。"
    if "Arrearage" in code or "good standing" in low:
        return "账户欠费：到阿里云控制台充值后重试。"
    if "CommodityNotPurchased" in code:
        return "业务空间尚未订购该服务：先在百炼控制台订购。"
    if "BillOverdue" in code:
        return "业务空间账单已到期或推理商品已失效：到控制台续费后重试。"
    if "BudgetLimitExceeded" in code:
        return "预算管理中设置的预算已用尽且开启了「达预算即停」：提高预算或关闭该开关。"
    if "AllocationQuota" in code or "insufficient_quota" in code:
        return "已超出配额上限：在控制台调高配额或检查套餐与账单。"
    if e.status == 429 or code.startswith("Throttling"):
        return "请求被限流（频率、突发或并发超限），已按设定次数重试仍失败：稍后再试或降低并发。"
    if "DataInspection" in code or "inappropriate content" in low:
        return "文本未通过内容安全审核：修改文本后重试。"
    if "error code: 418" in msg:
        return (f"音色 {voice} 不正确，或与模型 {model} 版本不匹配（不同版本模型的音色不能混用）。"
                f"请在 reference/voices/{model}.csv 中核对。")
    if "error code: 428" in msg:
        return "instruction 参数有误：可能超长，或格式、语言不被当前模型和音色支持。缩短或改写后重试。"
    if "request voice is invalid" in low:
        return "没有设置音色：检查 --voice 是否为空。"
    if "411" in msg or ("voice" in low and code == "InvalidParameter"):
        return (f"音色 {voice} 与模型 {model} 不匹配或不存在（voice 区分大小写）。"
                f"请在 reference/voices/{model}.csv 中核对。")
    if e.status == 401 or "ApiKey" in code or "api key" in low or "api-key provided" in low:
        return "API Key 无效，或 Key 与业务空间不属于同一地域（检查 DASHSCOPE_API_KEY、ALI_WORKSPACE_ID、--region）。"
    if "API-Key restrictions" in msg:
        return f"该 API Key 被设置了可调用模型范围，不包含 {model}：在控制台调整 Key 的权限或换一个 Key。"
    if "Workspace" in code or "workspace" in low:
        return "业务空间不存在或无权访问：检查 ALI_WORKSPACE_ID，以及 API Key 是否属于该业务空间。"
    if e.status == 403 or "AccessDenied" in code:
        return f"没有调用 {model} 的权限：确认该模型已在当前业务空间开通，且所选地域支持该模型和音色。"
    if e.retryable:
        return "服务端临时故障，已按设定次数重试仍失败，请稍后再试。"
    return "接口返回错误。"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--text", required=True)
    p.add_argument("--model", default="qwen-audio-3.1-tts-flash")
    p.add_argument("--voice", required=True)
    p.add_argument("--instruction")
    p.add_argument("--workspace-id", default=os.getenv("ALI_WORKSPACE_ID"))
    p.add_argument("--api-key", default=os.getenv("DASHSCOPE_API_KEY"))
    p.add_argument("--region", choices=("beijing", "singapore"), default="beijing")
    p.add_argument("--format", choices=("mp3", "pcm", "wav", "opus"), default="mp3")
    p.add_argument("--sample-rate", type=int, default=24000)
    p.add_argument("--volume", type=int, default=None)
    p.add_argument("--rate", type=float, default=None)
    p.add_argument("--pitch", type=float, default=None)
    p.add_argument("--bit-rate", type=int, default=None)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--language-hint", action="append", dest="language_hints")
    p.add_argument("--enable-ssml", action="store_true")
    p.add_argument("--enable-aigc-tag", action="store_true")
    p.add_argument("--stream", action="store_true")
    p.add_argument("--word-timestamps", action="store_true")
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--metadata", type=Path)
    p.add_argument("--timestamps", type=Path,
                   help="保存字级时间戳的 JSON 路径；给定后自动开启流式模式和 word_timestamp_enabled")
    p.add_argument("--retries", type=int, default=3,
                   help="网络中断、限流或服务端临时故障时的重试次数（默认 3，0 表示不重试）")
    return p.parse_args()


def endpoint(workspace: str, region: str) -> str:
    host = f"{workspace}.cn-beijing.maas.aliyuncs.com" if region == "beijing" else f"{workspace}.ap-southeast-1.maas.aliyuncs.com"
    return f"https://{host}/api/v1/services/audio/tts/SpeechSynthesizer"


def make_payload(a: argparse.Namespace) -> dict:
    inp = {"text": a.text, "voice": a.voice, "format": a.format, "sample_rate": a.sample_rate}
    for key in ("volume", "rate", "pitch", "bit_rate", "seed", "instruction"):
        value = getattr(a, key)
        if value is not None:
            inp[key] = value
    if a.language_hints:
        inp["language_hints"] = a.language_hints
    if a.enable_ssml:
        inp["enable_ssml"] = True
    if a.enable_aigc_tag:
        inp["enable_aigc_tag"] = True
    if a.word_timestamps:
        inp["word_timestamp_enabled"] = True
    return {"model": a.model, "input": inp}


def request(url: str, key: str, payload: dict, stream: bool):
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if stream:
        headers["X-DashScope-SSE"] = "enable"
    req = urllib.request.Request(url, json.dumps(payload).encode(), headers, method="POST")
    try:
        return urllib.request.urlopen(req, timeout=300)
    except urllib.error.HTTPError as e:
        raise parse_error(e.code, e.read().decode("utf-8", "replace")) from e


def save_json(path: Path | None, data: dict) -> None:
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def non_stream(a: argparse.Namespace, response) -> dict:
    result = json.load(response)
    audio = result.get("output", {}).get("audio", {})
    url = audio.get("url")
    if not url:
        raise RuntimeError(f"API returned no audio URL: {json.dumps(result, ensure_ascii=False)}")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(url, a.output)
    except urllib.error.URLError as e:
        raise RuntimeError(f"Could not download returned audio URL: {e}") from e
    return result


def _merge_word(existing: dict | None, candidate: dict) -> dict:
    """同一个字可能在多个事件中重复出现，保留带时间戳（且结束时间更新）的那份。"""
    if existing is None:
        return candidate
    existing_has_time = existing.get("end_time") is not None
    candidate_has_time = candidate.get("end_time") is not None
    if candidate_has_time and (not existing_has_time or candidate.get("end_time", 0) >= existing.get("end_time", 0)):
        return candidate
    return existing


def build_timestamps(a: argparse.Namespace, sentences: dict, request_id: str | None) -> dict:
    """把各句事件中收集到的字整理成全局时间轴。

    API 文档未明确多句文本的 begin_time/end_time 是相对句首还是整条音频，
    因此这里按数据自动判断：若后一句的起始时间早于前一句的结束时间（时间归零），
    则按各句时长累加偏移量，把字级时间校正到整条音频的起点。
    """
    ordered: list[dict] = []
    for idx in sorted(sentences):
        bucket = sentences[idx]
        words = sorted(bucket["words"].values(),
                       key=lambda w: (w.get("begin_index") is None, w.get("begin_index", 0)))
        ordered.append({"index": idx, "text": bucket["text"], "words": words})

    ranges: list[tuple[int, int] | None] = []
    for s in ordered:
        times = [w.get("begin_time") for w in s["words"] if w.get("begin_time") is not None]
        ends = [w.get("end_time") for w in s["words"] if w.get("end_time") is not None]
        ranges.append((min(times), max(ends)) if times and ends else None)

    # 第一趟：判定时间戳是全局还是按句相对（后一句起始早于前一句结束即视为归零）
    sentence_relative = False
    prev_end = None
    for rng in ranges:
        if rng is None:
            continue
        if prev_end is not None and rng[0] < prev_end:
            sentence_relative = True
        prev_end = rng[1]

    # 第二趟：按模式计算各句相对整条音频起点的偏移
    offsets: dict[int, int] = {}
    cumulative = 0
    for s, rng in zip(ordered, ranges):
        offsets[s["index"]] = cumulative if sentence_relative else 0
        if sentence_relative and rng is not None:
            cumulative += rng[1]

    out_sentences = []
    duration_ms = 0
    word_count = 0
    for s in ordered:
        offset = offsets.get(s["index"], 0)
        words_out = []
        begin_time = end_time = None
        for w in s["words"]:
            wb, we = w.get("begin_time"), w.get("end_time")
            gb = wb + offset if wb is not None else None
            ge = we + offset if we is not None else None
            words_out.append({
                "text": w.get("text"),
                "begin_index": w.get("begin_index"),
                "end_index": w.get("end_index"),
                "begin_time": gb,
                "end_time": ge,
            })
            if gb is not None and (begin_time is None or gb < begin_time):
                begin_time = gb
            if ge is not None and (end_time is None or ge > end_time):
                end_time = ge
                duration_ms = max(duration_ms, ge)
        word_count += len(words_out)
        out_sentences.append({
            "index": s["index"],
            "text": s["text"],
            "offset_ms": offset,
            "begin_time": begin_time,
            "end_time": end_time,
            "words": words_out,
        })

    if sentence_relative:
        origin = ("audio-start; 原始时间戳按句相对，已按各句时长累加偏移校正"
                  "（句间停顿无法从时间戳获知，未计入偏移）")
    else:
        origin = "audio-start"
    return {
        "request_id": request_id,
        "model": a.model,
        "voice": a.voice,
        "text": a.text,
        "time_unit": "ms",
        "time_origin": origin,
        "duration_ms": duration_ms,
        "word_count": word_count,
        "sentences": out_sentences,
    }


def iter_sse_events(response):
    """按 SSE 规范解析：事件由空行分隔，事件内每个 data: 行是负载的一行。

    该接口把 pretty-printed 的 JSON 拆到多个 data: 行（data:{ / data:  "output"...），
    必须把同一事件的所有 data: 行重新拼回完整 JSON，不能逐行 json.loads。
    id:/event:/冒号开头的注释行一律忽略。
    """
    data_lines: list[str] = []

    def flush(payload: str):
        payload = payload.strip()
        if not payload or payload == "[DONE]":
            return None
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return None

    for raw in response:
        line = raw.decode("utf-8", "replace").rstrip("\r\n")
        if line.startswith("data:"):
            part = line[5:]
            if part.startswith(" "):
                part = part[1:]
            data_lines.append(part)
        elif line == "" and data_lines:
            event = flush("\n".join(data_lines))
            data_lines = []
            if event is not None:
                yield event
    if data_lines:
        event = flush("\n".join(data_lines))
        if event is not None:
            yield event


def stream(a: argparse.Namespace, response) -> dict:
    # 出错时接口不按 SSE 返回，而是直接给一个 application/json 错误对象
    if response.headers.get_content_type() == "application/json":
        raise parse_error(response.status, response.read().decode("utf-8", "replace"))

    events, audio_bytes = [], bytearray()
    request_id = None
    # sentence index -> {"text": str|None, "words": {(begin_index,end_index,text): word}}
    sentences: dict[int, dict] = {}
    current_index = 0
    for event in iter_sse_events(response):
        if event.get("request_id"):
            request_id = event["request_id"]
        out = event.get("output", {})
        data = out.get("audio", {}).get("data")
        if data:
            audio_bytes.extend(base64.b64decode(data))
            # 音频块已写入 output 文件，不必再以 base64 形式保留在 JSON 元数据里
            out["audio"]["data"] = ""
        events.append(event)

        sentence = out.get("sentence") or {}
        idx = sentence.get("index")
        if idx is None and sentence:
            idx = current_index
        if idx is not None:
            current_index = idx
            bucket = sentences.setdefault(idx, {"text": None, "words": {}})
            if out.get("original_text"):
                bucket["text"] = out["original_text"]
            for word in sentence.get("words") or []:
                key = (word.get("begin_index"), word.get("end_index"), word.get("text"))
                bucket["words"][key] = _merge_word(bucket["words"].get(key), word)

    if not audio_bytes:
        raise RuntimeError("Streaming response contained no audio data")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_bytes(audio_bytes)

    timestamps = build_timestamps(a, sentences, request_id)
    word_count = timestamps["word_count"]
    if a.word_timestamps and word_count == 0:
        print("Warning: word_timestamp_enabled was set but no word timestamps were returned; "
              "check that the model/voice supports word-level timestamps.", file=sys.stderr)
    save_json(a.timestamps, timestamps)
    return {
        "stream": True,
        "request_id": request_id,
        "duration_ms": timestamps["duration_ms"],
        "sentence_count": len(timestamps["sentences"]),
        "word_count": word_count,
        "events": events,
    }


def main() -> int:
    a = parse_args()
    if not a.api_key:
        raise SystemExit("Missing API key: set DASHSCOPE_API_KEY or pass --api-key")
    if not a.workspace_id:
        raise SystemExit("Missing workspace ID: set ALI_WORKSPACE_ID or pass --workspace-id")
    # 字级时间戳仅流式模式返回：指定时间戳文件时自动开启，省去容易遗漏的两个开关
    if a.timestamps and not a.word_timestamps:
        a.word_timestamps = True
    if a.word_timestamps and not a.stream:
        print("Note: word timestamps require streaming mode; enabling --stream automatically.",
              file=sys.stderr)
        a.stream = True
    payload = make_payload(a)
    # 流式结果在全部收完后才写文件，所以中途断开重试不会留下半截音频
    for attempt in range(a.retries + 1):
        try:
            with request(endpoint(a.workspace_id, a.region), a.api_key, payload, a.stream) as response:
                result = stream(a, response) if a.stream else non_stream(a, response)
            break
        except ApiError as e:
            if not e.retryable or attempt == a.retries:
                raise
            reason = f"{e.code or e.status}"
        except NETWORK_ERRORS as e:
            if attempt == a.retries:
                raise
            reason = type(e).__name__
        wait = 2 ** (attempt + 1)
        print(f"第 {attempt + 1} 次请求失败（{reason}），{wait} 秒后重试…", file=sys.stderr)
        time.sleep(wait)
    save_json(a.metadata, {"request": payload, "response": result})
    print(json.dumps({
        "output": str(a.output),
        "stream": a.stream,
        "metadata": str(a.metadata) if a.metadata else None,
        "timestamps": str(a.timestamps) if a.timestamps else None,
        "word_count": result.get("word_count") if a.stream else None,
        "duration_ms": result.get("duration_ms") if a.stream else None,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    args_for_errors = sys.argv[1:]

    def _arg(name: str, default: str) -> str:
        return args_for_errors[args_for_errors.index(name) + 1] if name in args_for_errors[:-1] else default

    try:
        raise SystemExit(main())
    except ApiError as exc:
        print(f"错误：{explain(exc, _arg('--model', 'qwen-audio-3.1-tts-flash'), _arg('--voice', ''))}\n"
              f"  code={exc.code or exc.status}  request_id={exc.request_id}\n"
              f"  原始信息：{exc.message[:300]}", file=sys.stderr)
        raise SystemExit(1)
    except NETWORK_ERRORS as exc:
        print(f"错误：网络连接中断，已重试仍失败（{type(exc).__name__}: {exc}）。"
              "可稍后重试，或用 --retries 增加重试次数。", file=sys.stderr)
        raise SystemExit(1)
    except RuntimeError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        raise SystemExit(1)
