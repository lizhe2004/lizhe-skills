# 音色表维护

使用 skill 时不需要读这个目录。这里放生成 `reference/voices/*.csv` 的源文件和脚本。

| 路径 | 内容 |
| --- | --- |
| `source/音色列表.md` | 官方「在线音色列表」原文 |
| `source/out-of-scope/音频生成api.md` | Seed-Audio 音频生成接口文档，与本 skill 的单向 TTS 接口无关，仅留档 |
| `scripts/build_voice_tables.py` | 把音色列表拆成三份 CSV（只用标准库，需 Python 3.9+） |

更新流程：用官方最新内容替换 `source/音色列表.md`，在 skill 根目录运行

```bash
python3 maintenance/scripts/build_voice_tables.py
```

输出：

| 文件 | 内容 | 本 skill 能否使用 |
| --- | --- | --- |
| `reference/voices/doubao-tts-2.0.csv` | 2.0 中文/通用 + 2.0 外语音色，含指令遵循、引用上文能力 | 能（`seed-tts-2.0`） |
| `reference/voices/doubao-tts-1.0.csv` | 1.0 音色，含情感参数、对应 2.0 音色 | 不能，用于找替代 |
| `reference/voices/doubao-realtime-s2s.csv` | 实时语音 S2S/SC 音色 | 不能 |

解析说明：官方表格用行首 `||`（首列留空）表示合并单元格，脚本沿用上一行的「场景」；同一音色在原文多个场景下重复列出时合并成一行。`scripts/doubao_tts.py` 发请求前按这三张表检查音色与资源是否匹配，所以音色列表更新后要重新生成。
