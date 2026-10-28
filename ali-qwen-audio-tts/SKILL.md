---
name: ali-qwen-audio-tts
description: 通过阿里云百炼 Qwen-Audio-TTS 或 Sambert 合成语音，选择模型音色，生成配音、旁白和带字级时间戳的音频。Qwen 支持指令控制；Sambert 支持音素时间戳。
---

# 阿里云语音合成：Qwen-Audio-TTS 与 Sambert

先按用户指定的模型系列选择入口。Qwen-Audio-TTS 使用下文的 HTTP 脚本与音色表；Sambert 使用 [Sambert 说明](reference/Sambert/使用指南.md)和 [scripts/sambert_tts.py](scripts/sambert_tts.py)。未指定系列时，按用户对音色、时延、指令控制或时间戳的要求选型；不要把 Qwen 的 `voice`、`instruction` 参数套到 Sambert。批量合成前仍须确认计费和额度。

## Sambert 快速入口

Sambert 是北京地域的实时语音合成模型。`sambert-...-v1` 是 Sambert 的音色 ID，例如 `sambert-beth-v1`、`sambert-betty-v1`、`sambert-zhiyue-v1`；通过 `--voice` 选择。调用脚本要求 Python 3.9 或更高版本。可保存完整音频、字级时间戳及音素时间戳。

选择 Sambert 音色时，只读 [sambert.csv](reference/voices/sambert.csv)，按语言、适用场景、声线特质、默认采样率和时间戳支持筛选。该文件中的 `免费额度` 是参考文档当前列出的音色，不表示账户还有可用额度；实际额度以控制台和接口结果为准。

```bash
python3 -m pip install -U dashscope
export DASHSCOPE_API_KEY='你的北京地域 API Key'
export ALI_WORKSPACE_ID='你的北京地域业务空间 ID'
python3 scripts/sambert_tts.py \
  --voice sambert-zhichu-v1 --text '西湖十景，为什么能流传千年？' \
  --format wav --output ./sambert.wav --timestamps ./sambert.timestamps.json
```

常规 Sambert 配音只需要本文件、`reference/voices/sambert.csv` 和 [scripts/sambert_tts.py](scripts/sambert_tts.py)。仅在修改 SDK 请求/响应逻辑时读 [SDK 文档](reference/Sambert/sdk接入.md)，仅在实现或排查原始 WebSocket 协议时读 [WebSocket 协议](reference/Sambert/接入api.md)。Sambert 文本须一次提交，音频可流式返回；当前脚本使用 SDK 的同步调用，完整写入音频后返回。Sambert 不使用下文 Qwen 专属的音色表、流式开关或指令控制。

默认端点策略是先连北京业务空间专属域名；只有该域名发生 DNS 连接失败时，脚本才回退到旧域名。`AllocationQuota.FreeTierOnly` 说明免费额度已用完，不能靠重试解决；具体处理方式见 Sambert 使用指南。

## Qwen-Audio-TTS

本技能面向 `SpeechSynthesizer` HTTP 接口，详细字段以 [reference/qwen-audio-tts-http-api.md](reference/qwen-audio-tts-http-api.md) 为准。

支持的模型：

- `qwen-audio-3.1-tts-plus`：侧重音质与高分辨率，适合影视配音、有声内容、品牌音色等专业场景
- `qwen-audio-3.1-tts-flash`（**脚本默认模型**）：侧重实时合成与低延迟
- `qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`

## 选音色

选音色只读当前模型那一份音色表：`reference/voices/<model>.csv`（UTF-8，可用 Excel 打开）。不同模型的音色不能混用；3.1 plus 与 3.1 flash 有同名 voice（如 `longanhuan_v3.1`），也要按模型查各自的表。

| 模型 | 音色表 | 音色数 | voice 写法 |
| --- | --- | --- | --- |
| `qwen-audio-3.1-tts-plus` | [qwen-audio-3.1-tts-plus.csv](reference/voices/qwen-audio-3.1-tts-plus.csv) | 4 | `xxx_v3.1`，如 `xunanchuan_v3.1` |
| `qwen-audio-3.1-tts-flash` | [qwen-audio-3.1-tts-flash.csv](reference/voices/qwen-audio-3.1-tts-flash.csv) | 68 | `xxx_v3.1`，如 `longanzhi_v3.1` |
| `qwen-audio-3.0-tts-plus` | [qwen-audio-3.0-tts-plus.csv](reference/voices/qwen-audio-3.0-tts-plus.csv) | 2 系统 + 597 基础 | 系统如 `longanlingxin`；基础 `qwen-audio-3.0-tts-plus-xxx` |
| `qwen-audio-3.0-tts-flash` | [qwen-audio-3.0-tts-flash.csv](reference/voices/qwen-audio-3.0-tts-flash.csv) | 12 系统 + 597 基础 | 系统如 `longanfengyue`；基础 `qwen-audio-3.0-tts-flash-xxx` |

每张表只保留对选音色有用的列，某个模型里全空或全相同的列已省略：

| 列 | 含义 |
| --- | --- |
| `建议性别` | 综合官方文档、实测基频、听感判断后的结论：男 / 女 / 童声/少年（文档：男\|女）/ 待确认 |
| `性别备注` | 仅在存疑时填写原因；为空表示没有疑问 |
| `年龄段`、`音色关键词`、`情绪风格`、`播讲风格`、`适用场景`、`不适合`、`一句话描述` | Qwen3.8-Omni-Flash 试听官方样例后的听感描述 |
| `基频中位Hz`、`语速字每秒` | 对官方试听音频的声学测量，便于横向比较音高和语速 |
| `类别`、`声线特质(文档)`、`适用场景(文档)`、`语言`、`地域`、`年龄(文档)`、`SSML`/`指令控制`/`时间戳`、`试听文件` | 官方文档原文（各模型列不完全相同） |

选择步骤与注意事项：

- 先按 `适用场景`、`播讲风格`、`音色关键词` 筛候选，再比较 `基频中位Hz`、`语速字每秒`，最后用一句短文本实际合成试听，定稿前务必人耳确认。
- 按性别筛选只用 `建议性别`。`待确认` 的音色（如 `andi_v3.1`）文档、基频与听感互相矛盾，使用前先试听；听感描述是 Omni 的原话，个别描述里的性别可能与 `建议性别` 不一致，以 `建议性别` 为准。
- 3.1 plus、3.1 flash 的全部音色都支持 SSML、指令控制和字级时间戳（表中已省略这三列）。3.0 只有系统音色标注了这三项；3.0 基础音色未标注，需要字级时间戳时优先选系统音色，或先试一句确认 `word_count` 不为 0。
- `地域`：3.1 flash 的多语种与方言、精品英文音色支持北京和新加坡，其他仅北京；3.1 plus 和 3.0 文档未按音色标注地域。
- `语速字每秒` 是官方试听样例的语速，实际合成会受 `instruction` 影响（例如"带一点悬念感"会明显拉长停顿），只作横向比较。
- 对支持方言指令的音色，可在 `instruction` 中指定方言，例如 `请讲上海话。`。
- 官方试听包里还有约 428 个 3.0 基础音色未列入官方 Excel，表中暂未收录。

音色表的生成与更新流程见 [maintenance/README.md](maintenance/README.md)，使用 skill 时不需要读 `maintenance/` 下的任何文件。

## 必需配置

- 设置 `DASHSCOPE_API_KEY`，或者通过 `--api-key` 传入。
- 设置 `ALI_WORKSPACE_ID`，或者通过 `--workspace-id` 传入。
- 业务空间和 API Key 必须属于同一地域。
- 北京地域使用 `--region beijing`；新加坡地域使用 `--region singapore`。
- `voice` 区分大小写，必须与所选 `model` 的音色表匹配。
- 需要 Python 3.10 及以上（只用标准库）。旧版 Python 自带的 OpenSSL 与接口握手不兼容，会报 `SSL: EOF occurred in violation of protocol`；脚本启动时会检查版本并提示，macOS 上可用 Homebrew 的 `python3`。

## 计费与报错

- 合成按字符计费，各模型的免费额度相互独立。百炼控制台可对单个模型开启「仅使用免费额度」：开启后额度用完会直接拒绝请求、不扣费；**未开启则自动转为按量计费**。不确定额度时，先问用户再批量合成，不要随手发测试请求。
- 脚本对网络中断（流式推送中途断开、连接重置、超时）、限流（429 中的 Throttling 类）和服务端临时故障（5xx）自动重试，默认 3 次、间隔 2/4/8 秒，可用 `--retries` 调整。流式结果全部收完才写文件，重试不会留下半截音频；但中途断开的请求可能已计费，批量合成时留意。
- 参数错误、鉴权失败、计费/配额类错误（免费额度用尽、欠费、未订购、账单到期、预算用尽，其中不少也是 429）不会重试，脚本会输出一行中文说明加 `code` 和 `request_id`。完整对照见 [reference/错误码.md](reference/错误码.md)，常见几种：

| 报错提示 | 原因与处理 |
| --- | --- |
| 免费额度已用完 | 403 `AllocationQuota.FreeTierOnly`，没有扣费；开启了「免费额度用完即停」或新账号未认证，需用户关闭开关或认证充值 |
| 复刻音色数量已达上限 / 已超出配额上限 | 同为 `Throttling.AllocationQuota`：400 时删复刻音色，429 时调配额 |
| 音色…与模型…不匹配或不存在 / 版本不匹配 | `Engine error [411]`、`error code: 418`；到 `reference/voices/<model>.csv` 核对 voice 写法 |
| instruction 参数有误 | `error code: 428`：指令超长或格式不被支持 |
| API Key 无效，或 Key 与业务空间不属于同一地域 | 401；检查环境变量和 `--region` |
| 没有调用…的权限 | 403；模型未在当前业务空间开通，或地域不支持该模型/音色 |
| 网络连接中断，已重试仍失败 | 稍后再试，或加大 `--retries` |

## 调用脚本

使用 [scripts/qwen_audio_tts.py](scripts/qwen_audio_tts.py) 进行调用。它负责组装请求、隐藏密钥、下载非流式接口返回的临时音频 URL，并可保存元数据和时间戳。

脚本不会自动验证某个音色是否属于某个模型，因此调用前要核对该模型的音色表（见上文「选音色」）。

## 工作流程

1. 修改请求字段或响应处理逻辑前，先阅读 API 参考文档。
2. 需要选择音色时，只查当前模型对应的 `reference/voices/<model>.csv`，按 `建议性别`、`适用场景`、`播讲风格`、`地域` 筛选（见上文「选音色」）。
3. 生成完整音频时使用非流式模式；需要低延迟、句子事件或字级时间戳时使用流式模式。
4. 请求体的 `input` 至少包含 `text`、`voice`，通常还应指定 `format` 和 `sample_rate`。
5. 使用 `instruction` 控制普通话、方言、情感、角色、播音方式或场景语气；只有文本包含受支持的 SSML 时才启用 `enable_ssml`。
6. 用于视频旁白时保留自然生成时长，不要为了凑固定时长而加速或拉伸音频；应依据音频实际时长重新安排字幕和画面节奏。
7. 检查输出文件和音频时长；需要后期对齐时同时保存响应元数据或时间戳。

示例：

```bash
export DASHSCOPE_API_KEY='你的API Key'
export ALI_WORKSPACE_ID='你的业务空间ID'

python3 scripts/qwen_audio_tts.py \
  --voice longsanshu_v3.1 \
  --text '西湖十景，为什么能流传千年？' \
  --instruction '普通话，纪录片旁白，沉稳有力，语速适中，句间不拖长停顿。' \
  --format mp3 --sample-rate 24000 \
  --output ./xihu-intro.mp3 \
  --metadata ./xihu-intro.json
```

`longsanshu_v3.1`（龙三叔）是 3.1 flash 的浑厚中年男声，适合纪录片和有声书旁白。模型可省略，默认即 `qwen-audio-3.1-tts-flash`。

更看重音质时用 3.1 plus，并配它自己音色表里的音色：

```bash
python3 scripts/qwen_audio_tts.py \
  --model qwen-audio-3.1-tts-plus \
  --voice xunanchuan_v3.1 \
  --text '这是一段需要逐字对齐的旁白。' \
  --timestamps ./narration.timestamps.json \
  --output ./narration.mp3
```

视频配音需要和画面对齐时，用上面这种 `--timestamps` 方式保存字级时间戳。

给定 `--timestamps` 后脚本会自动开启流式模式和 `word_timestamp_enabled`，无需再手动加 `--stream --word-timestamps`（显式加上也可以）。

流式模式返回的音频块必须按事件顺序追加到同一个文件，不能把每个音频块当成独立音频。

### 时间戳文件结构

`--timestamps` 保存的 JSON 包含：

- `time_unit` / `time_origin`：时间单位固定毫秒，时间原点为整条音频起点。
- `duration_ms`：由最后一个字的 `end_time` 推出的语音时长（句尾停顿不计入）。
- `word_count`：字块总数。
- `sentences`：按句分组，每句含 `index`、`text`、`begin_time`/`end_time`、`offset_ms` 和 `words`；`words` 中每个字块带 `text`、句内 `begin_index`/`end_index` 和全局 `begin_time`/`end_time`。

字级数据只保存在 `sentences` 里（单一来源，不重复存储）。需要一条连续的扁平时间轴时自行打平，例如 Python：

```python
words = [w for s in result["sentences"] for w in s["words"]]
```

注意：实测 `qwen-audio-3.1-tts-flash`（3.0 flash 行为相同）对短文本返回单个句子；较长文本会被服务端切分为多个 sentence（观察到约每 100 个字块、在就近的句号边界切分，例如 150 块被切成 99+51 两句，切分不以每个标点为界）。各句的 `begin_time/end_time` 均为相对整条音频起点的全局毫秒时间（首字一般从约 80–240ms 开始），句间停顿自然包含在时间轴中（实测约 320ms），因此正常情况下所有句的 `offset_ms` 均为 0。`words` 按合成进度在多个事件中增量增长，脚本会自动合并去重。部分 `words` 元素可能包含标点或与相邻字合并（如 `。第`、`图。`），把所有句的 `text` 按序拼接可还原原文。`begin_index/end_index` 是**字块在整篇文本中的连续序号**（跨句不重置，第二句会接着上一句的编号，如 99→100），不是原文字符偏移，不能用于对原文做字符切片；需要字块内容时直接使用其 `text` 字段。相邻字块间的时间差即为标点/句读停顿（实测逗号约 240–400ms、句号约 240–640ms，因模型和音色而异）。脚本仍保留句首归零的自动校正，以兼容时间基准不同的其他模型；若发生校正会在 `time_origin` 中标注（句间停顿无法从时间戳获知，不计入偏移）。字块总数通过顶层 `word_count` 字段读取；脚本在该值为 0 且显式请求了时间戳时会在 stderr 警告，为 0 说明所选模型/音色不支持字级时间戳，需查阅音色表更换。`duration_ms` 是末字结束时间，不含音频尾部静音（实测比文件总时长略短）。

完整的真实返回样例见仓库根目录：

- [example-timestamps.json](example-timestamps.json)：单句样例（「西湖，位于杭州。自古以来就是著名的游览胜地。」，19 个字块，配套音频 `example-timestamps.mp3`）。
- [example-timestamps-multi.json](example-timestamps-multi.json)：多句样例（约 34 秒、150 字块被服务端切成 2 个 sentence，配套音频 `example-timestamps-multi.mp3`），可参考多句时的全局时间轴、连续的 `begin_index` 和句间停顿。

## 重要约束

- 非流式返回的音频 URL 有效期为 24 小时，应立即下载。
- `rate` 和 `pitch` 的范围是 `0.5–2.0`，除非用户明确要求，否则保持默认值 `1.0`。
- `volume` 范围是 `0–100`。
- `word_timestamp_enabled` 只在流式模式下可用，并且受模型和音色支持情况限制。
- `language_hints` 是数组，当前版本主要使用第一个元素，例如 `['zh']`。
- 不得把 API Key 写进提示词、元数据或用户可见输出。
- 如果返回音色或模型不匹配错误，应重新核对对应音色表，不要静默更换音色。
