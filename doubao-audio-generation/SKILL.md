---
name: doubao-audio-generation
description: 使用火山引擎 Seed Audio 1.0 非流式音频生成 API，根据自然语言提示词、参考音频或参考图片生成最长 120 秒的音效、配音和定制音频；当用户要求豆包音频创作、音效生成或参考素材驱动的音频生成时使用。
---

# 豆包音频生成

这个技能调用 `POST /api/v3/tts/create` 生成完整音频文件，不负责实时流式 TTS、声音复刻注册或语音识别。它不是逐句 TTS 拼接器，而是用单条自然语言 Prompt 编排连续的人声、对白、背景音乐、环境音效、转场音效和时间关系。支持纯文本提示词、文本+参考音频、文本+参考图片三种主要模式。

## 运行条件

从环境变量读取凭证，不要把 API Key 写入脚本、命令行示例、日志或生成文件：

- `DOUBAO_API_KEY`：请求头 `X-Api-Key`。
- 请求头 `X-Api-Request-Id` 使用新的 UUID。
- 默认模型为 `seed-audio-1.0`，默认端点为 `https://openspeech.bytedance.com/api/v3/tts/create`。

## 工作流

1. 判断生成模式：无参考资源时，`text_prompt` 直接描述要生成的完整音频；参考音频通过 `@音频1`、`@音频2`、`@音频3` 引用；参考图片模式将图片作为参考并在 `text_prompt` 中写待生成内容。
2. 读取 [references/音频生成api.md](references/音频生成api.md)，确认模型、输入资源限制和输出参数。单次最多 120 秒；提示词最多 3000 字符。
3. 校验参考资源：最多 3 条音频，每条不超过 30 秒、10 MB，格式为 WAV/MP3/PCM/OGG Opus；最多 1 张图片，不超过 10 MB，格式为 JPEG/PNG/WebP。参考图片不能与参考音频或 `speaker` 混用。
4. `speaker`、`audio_data`、`audio_url` 三者互斥；参考音频的上传顺序必须与 `text_prompt` 中 `@音频N` 的编号一致。
5. 对长内容优先按“章节/场景”拆成少量连续长段，而不是按句切片；用 `00:00–00:08` 这样的时间块直接编排每幕的人声、背景音乐、环境音和音效，使生成结果能与视频时间轴对齐。每段 Prompt 都要明确声明角色与音频引用槽位的绑定，例如 `旁白（饰演者为@音频1）`，不要写成 `旁白（speaker=...）`。`@音频N` 是 Prompt 中的音频引用标记：它可以指向 `references` 中的预置音色项，也可以指向上传的参考音频；使用预置音色时，将其作为 `references: [{"speaker": "zh_male_m191_uranus_bigtts"}]` 的对应引用。还要写清情绪、音乐风格、音效进入/退出和层级关系。若 API 的 120 秒上限迫使分段，所有段落沿用同一音频引用映射，并复制统一的声音设定。
6. 默认不调整语速、音量和音调（`speech_rate=0`、`loudness_rate=0`、`pitch_rate=0`）。优先用 Prompt 的时间轴描述控制节奏；只有用户明确要求时才修改参数，并遵守 API 范围。
7. 需要字幕对齐时设置 `enable_subtitle=true`，保存响应中的 `subtitle.sentences` 和 `words`；不要凭空伪造时间戳。
8. 用 `scripts/doubao_audio_generate.py` 发起请求，保存 Base64 音频或下载临时 URL，并可用 `--metadata` 保存完整响应（脱敏后再分享）。
9. 合成后检查文件可播放、格式、采样率、时长和响应码；接口失败时报告 `code`/`message`，不得输出 API Key。

## 常用提示词写法

把声音内容、角色设定、环境、动作、情绪、背景音乐/音效层次和时间轴要求写进 `text_prompt`。不要把大量禁止项堆在开头；优先用一份“音频导演脚本”按时间块描述成品听感。除非用户明确要求纯干声，否则不要默认禁止背景音乐。

```text
一段 8 秒的西湖夜晚影视级环境音：00:00–00:02 微风与远处水波；00:02–00:03 一声很轻的木桨划水；00:03–00:08 加入极简、空灵的箫与弦乐铺底，保持水面与柳叶声，结尾自然淡出。
```

需要参考音频时，在提示词中明确引用；参考音频只作为音色、节奏和表达方式的基准，不要把“@音频1”等说明读出来：

```text
导游（中年男性，声音沉稳清晰，饰演者为@音频1）用普通话说一段 10 秒的杭州导游开场，语气亲切、清晰；前 2 秒有很轻的湖面环境音，随后人声进入，环境音始终低于人声，不要旋律性背景音乐。
```

## 参考资料路由

- 请求字段、资源互斥关系、格式限制、响应字幕结构：阅读 [references/音频生成api.md](references/音频生成api.md)。

## 命令示例

纯文本音效：

```bash
python scripts/doubao_audio_generate.py \
  --text-prompt "一段 8 秒的西湖夜晚环境音：微风、轻微水波声，不要人声" \
  --output xihu-night.wav \
  --format wav \
  --enable-subtitle
```

使用预置音色生成定制音频：

```bash
python scripts/doubao_audio_generate.py \
  --text-prompt "生成一段 10 秒的普通话景点开场，语气亲切清晰" \
  --speaker zh_female_xiaohe_uranus_bigtts \
  --output intro.mp3 \
  --format mp3
```
