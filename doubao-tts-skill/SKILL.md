---
name: doubao-tts
description: 使用火山引擎豆包语音合成 HTTP API 生成普通话或多语种音频、字级时间戳和字幕对齐数据；当用户要求豆包 TTS、语音指令、声音复刻音色或旁白合成时使用。
---

# 豆包语音合成

这个技能把文本、字幕或旁白稿合成为音频，并可同时保存字级时间戳。它面向火山引擎豆包语音合成 HTTP 单向流式接口，不负责声音复刻注册、实时语音对话或语音识别。

## 先确认运行条件

从环境变量读取凭证，不要把 API Key 写入脚本、命令行示例、日志或生成文件：

- `DOUBAO_API_KEY`：请求头 `X-Api-Key`
- `DOUBAO_RESOURCE_ID`：请求头 `X-Api-Resource-Id`，本接口只接受两个值：预置 2.0 音色用 `seed-tts-2.0`（默认），声音复刻音色用 `seed-icl-2.0`
- 需要 Python 3.9 及以上（只用标准库），命令里用 `python3`；脚本启动时会检查版本。

请求还必须带一个新的 UUID 作为 `X-Api-Request-Id`。默认端点是 `https://openspeech.bytedance.com/api/v3/tts/unidirectional`。

## 工作流

1. 判断输入是纯文本、SRT/VTT，还是需要语音指令的旁白稿。保留用户原文；括号、Markdown、Emoji 是否朗读要明确设置。
2. 选择实际可用的 `speaker`：只查 [reference/voices/doubao-tts-2.0.csv](reference/voices/doubao-tts-2.0.csv)（466 个预置 2.0 音色），按 `场景`、`语种/方言`、`指令遵循`、`引用上文` 筛选，不要臆造 ID。1.0 音色和实时语音（S2S/SC）音色不能用于本接口，分别列在 `doubao-tts-1.0.csv`（含「对应 2.0 音色」，用来找替代）和 `doubao-realtime-s2s.csv`。脚本发请求前会按这三张表检查音色与 `--resource-id` 是否匹配，选错会直接给出中文提示和替代建议。
3. 选择资源与模型：预置 2.0 音色用 `--resource-id seed-tts-2.0`，不要传 `--model`；声音复刻音色用 `--resource-id seed-icl-2.0`，可选 `--model seed-tts-2.0-standard`（默认）或 `seed-tts-2.0-expressive`，但指定 `--model` 后不能再用 `--context-text`。复刻音色不在音色表里，需确认已完成复刻。
4. 对中文解说优先使用 `format=mp3` 或流式推荐的 `pcm`，`sample_rate=24000`；需要播放器直接打开时使用 MP3，需要后续音频处理时使用 PCM/WAV。
5. 需要情绪、语气、方言、语速、音调或引用上文时，只对音色表中 `指令遵循` / `引用上文` 为「是」的音色使用 `context_texts`（未标注的音色脚本会提示可能不生效）。每条指令写成自然语言，例如 `#用平实、准确、稍带悬念的百科解说语气说`；指令文本不计费。语音指令放进 `context_texts`，待合成内容仍放进 `text`。
6. 要求字级时间戳时设置 `enable_subtitle=true`（脚本中传 `--enable-subtitle` 或 `--timestamps` 即自动开启），脚本会聚合响应里各分片的 `sentence.words` 输出结构化时间轴 JSON；服务只对中英文提供字级时间戳。
7. 使用 `scripts/doubao_tts.py` 发送请求并保存音频。网络中断、限流、超并发、服务端错误会自动重试（见下文「报错与重试」）；其余错误脚本输出一行中文说明并附 `code`、`request_id`、`logid`，不会打印 API Key，也不会把错误响应当作音频写入。
8. 合成后检查音频可播放、时长、采样率，并用接口返回的时间戳生成或校准 SRT。长旁白优先按自然句拆分请求，避免单次文本过长造成异常加速。

## 参数边界

- `speech_rate` 范围为 `-50..100`，其中 `100` 约为 2 倍速，`-50` 约为 0.5 倍速；`loudness_rate` 同样使用 `-50..100`。
- `explicit_language=zh-cn` 适合中文为主、允许中英混读；显式语种优先级高于自动识别。
- `ssml` 目前只对支持的中英文音色适用；启用 SSML 时按接口要求处理 Markdown 过滤设置。
- 发音词典放在 `additions` 的 JSON 字符串中，例如 `{"pronunciation_dict":{"tone":["杭州/(hang2)(zhou1)"]}}`；同一文本片段不要同时依赖发音词典和 SSML。
- `silence_duration` 是文本末尾静音，单位毫秒，范围 `0..30000`。
- `enable_subtitle` 只适用于中文和英文；没有返回时间戳时不要伪造字级时间。

## 报错与重试

- 自动重试（默认 3 次，间隔 2/4/8 秒，`--retries` 调整，`0` 为不重试）：网络中断、HTTP 429/5xx、`5` 开头的错误码（「资源与音色不匹配」「请求体过大」除外）、超并发（`quota exceeded for types: concurrency`）、合成超时。每次重试都用新的 `X-Api-Request-Id`；响应完整读完才写文件，不会留下半截音频，但中途失败的请求可能已计费。
- 单次请求超时默认 300 秒，长文本可用 `--timeout` 调大；更推荐按自然句拆分。
- 不重试、直接给出中文说明的常见错误：

| 报错提示 | 处理 |
| --- | --- |
| 音色不存在或为空 | 检查 `--speaker` 拼写和 `--resource-id` 是否匹配 |
| 该资源下没有这个音色（`resource ID is mismatched…`） | 服务未开通、音色拼错、复刻音色过期或无权限；虽是 `55000000` 也不重试 |
| 请求体过大 | 缩短文本或按自然句拆分 |
| model 参数非法 | `--model` 只用于复刻音色，取值 `seed-tts-2.0-standard` / `seed-tts-2.0-expressive` |
| 文本里没有可朗读的内容 | 文本只剩标点、Markdown 或 Emoji；检查过滤开关 |
| 内容审核未通过 | 调整文本后重试 |
| 鉴权失败 / 无权调用 | 检查 `DOUBAO_API_KEY`，确认资源已在控制台开通且有可用额度 |

错误码规则：`4` 开头为请求方问题，`5` 开头为服务端问题。完整对照（含每条是否重试）见 [reference/错误码.md](reference/错误码.md)。同一个错误码下有多种 `message`（如 `55000000` 既有可重试的服务端错误，也有不可重试的资源与音色不匹配），脚本按 `message` 识别。

## 字级时间轴 JSON

`--timestamps out.json`（或仅传 `--enable-subtitle`，默认写到音频旁的 `<音频名>.timestamps.json`）输出按整段音频起点对齐的时间轴，供视频合成做音画同步：

- `sentences`：按接口分片聚合的句子列表，每句含 `text`、句子级 `start`/`end`（秒、float）和嵌套的 `words`；部分音色会额外返回 `phonemes` 音素时间戳；接口另有一条回显整段输入原文、`words` 为空的 sentence，脚本会丢弃；
- `sentences[].words`：该句的字级时间戳，每项为 `{word, start, end, confidence}`，`start`/`end` 同样是相对整段音频开头的秒数；标点会并入相邻字组成一个单元（如 `景，`、`荷、`），不保证一字一项；
- `audio`：音频文件名、格式、采样率、字节数与时长（WAV/PCM 按容器精确计算，MP3/Ogg 回退为最后一个字的 `end`）；
- 另有 `duration`、`request_id`、`logid` 和 `usage`（需 `--usage-tokens`，含计费字数 `text_words`）。

字级时间戳只嵌在句内、不另设顶层摊平数组：逐字高亮等需要线性字轨的场景，用一句 `[w for s in timeline["sentences"] for w in s["words"]]` 摊平即可（信息无损）；反过来无法从字数组重建句子边界，因此以嵌套句结构为唯一事实来源。

实测各分片的 `startTime/endTime` 均以整段音频起点为零基准、全局单调递增，直接按句顺序使用即可，不要为分片累加偏移。PCM/WAV 格式下脚本还会对比时间轴末字 `end` 与容器精确时长（已计入 `silence_duration` 尾部静音容差），偏差超过 0.3s 时打印警告——若未来接口行为变为分段归零，需改为按各分片音频时长累加偏移。JSON 中不含音频数据本身；需要原始响应字段时另行抓包，不要把 base64 音频写进时间轴文件。

## 语音指令写法

把“怎么说”放入 `context_texts`，把“说什么”放入 `text`。推荐使用具体、可执行的描述：

```json
{
  "context_texts": ["#用平实、准确、清晰的普通话百科解说语气说，句末略有停顿"]
}
```

如果需要承接上一句，把上一句放入 `context_texts`，并注明它只是上文、不参与合成。引用上文和语音指令需要根据模型能力选择，不要与复刻模型假设兼容。

## 参考资料路由

- HTTP 请求、请求体字段、响应和发音词典：阅读 [reference/tts-http-api.md](reference/tts-http-api.md)。
- 预置模型、复刻模型和语种能力：阅读 [reference/模型列表.md](reference/模型列表.md)。
- 语音指令和引用上文范式：阅读 [reference/语音指令与标签.md](reference/语音指令与标签.md)。
- 报错排查：阅读 [reference/错误码.md](reference/错误码.md)。
- 选音色：[reference/voices/doubao-tts-2.0.csv](reference/voices/doubao-tts-2.0.csv)；1.0 情感参数与对应 2.0 音色：[reference/voices/doubao-tts-1.0.csv](reference/voices/doubao-tts-1.0.csv)。
- 音色表由 `maintenance/` 下的脚本从官方音色列表生成，使用时不需要读 `maintenance/`；其中 `maintenance/source/out-of-scope/` 是与本 skill 无关的 Seed-Audio 音频生成接口文档。

## 命令示例

```bash
python3 scripts/doubao_tts.py \
  --text "杭州西湖有十景。" \
  --speaker zh_female_vv_uranus_bigtts \
  --output narration.mp3 \
  --enable-subtitle \
  --timestamps narration.timestamps.json
```

脚本默认从 `DOUBAO_API_KEY` 和 `DOUBAO_RESOURCE_ID` 读取凭证；可用 `--context-text` 重复传入语音指令，用 `--usage-tokens` 请求计费字符数。时间轴支持三种用法：显式 `--timestamps 路径`、`--enable-subtitle` 时自动写到 `narration.mp3.timestamps.json`、以及传 `--timestamps` 隐式开启字幕（不必再加 `--enable-subtitle`）。
