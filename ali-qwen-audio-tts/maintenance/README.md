# 音色表维护

使用 skill 时不需要读这个目录。这里是生成 `reference/voices/<model>.csv` 的流水线和中间数据，只在官方音色有更新、或要修正音色信息时使用。

## 目录

| 路径 | 内容 |
| --- | --- |
| `source/` | 官方原始资料：`qwen-audio-音色列表.md`（系统音色与试听链接）、两个 3.0 基础音色 Excel |
| `data/<model>.official.csv` | 官方文档整理成的统一列结构表 |
| `data/<model>.measured.csv` | 试听音频的声学测量：基频、音域、语调起伏、语速、停顿、频谱质心等 |
| `data/<model>.omni.csv` | Qwen3.8-Omni-Flash 的听感描述，含「描述方式」（首轮批量 / 思考模式重做） |
| `data/<model>.gender-recheck.csv` | 对性别存疑音色的 Omni 思考模式复核（目前只有 3.1 flash） |
| `data/<model>.gender-hints.json` | 重新描述时给 Omni 的参考信息，只能放官方文档事实和客观测量值，不能放模型自己的推断 |
| `samples/` | 试听音频（`system/`、`basic/`）、`index.csv`（样例与音色对应，路径相对 `samples/`）、Omni 缓存（`omni/`、`omni-gender/`） |
| `scripts/` | 流水线脚本，共用路径定义在 `paths.py` |

## 流水线

在 skill 根目录按顺序运行：

```bash
python3 maintenance/scripts/build_voice_tables.py      # source/ -> data/<model>.official.csv
python3 maintenance/scripts/fetch_voice_samples.py     # 下载试听音频 -> samples/（已有文件跳过；基础音色齐全时不下载压缩包）
python3 maintenance/scripts/analyze_voice_samples.py   # 声学测量 -> data/<model>.measured.csv（需 numpy、scipy）
python3 maintenance/scripts/describe_voices_omni.py    # Omni 听感 -> data/<model>.omni.csv
python3 maintenance/scripts/build_voice_profiles.py    # 合并 -> reference/voices/<model>.csv
```

- 需要 Python 3.9+；`build_voice_tables.py`、`fetch_voice_samples.py`、`build_voice_profiles.py` 只用标准库。
- 官方文档更新时，先替换 `source/` 下的文件再从第一步重跑。

## 费用与缓存

`describe_voices_omni.py` 和 `recheck_gender_omni.py` 会调用付费接口 `qwen3.8-omni-flash`（与 TTS 共用 `DASHSCOPE_API_KEY`、`ALI_WORKSPACE_ID`）。

- 结果按样例缓存在 `samples/omni/`、`samples/omni-gender/`，缓存键是相对 `samples/` 的样例路径，移动整个目录不会失效。
- 只要有未缓存的样例，脚本会先打印需要调用的条数并退出，不调用接口；确认费用后加 `--yes` 才会真正调用。没有新样例时，直接运行只会重新汇总缓存。
- 首次全量描述约 700 条样例（3.0 plus/flash 的基础音色共用试听文件，只调用一次），实际消耗约 38.5 万 token。可用 `--limit 6 --yes` 先试点。
- `--voices a b --hints data/<model>.gender-hints.json --thinking --yes`：对指定音色用思考模式重新描述（会覆盖缓存，旧结果备份在 `samples/omni/_previous/`）。

## 已知问题

- 官方 Excel 中 3.0 基础音色「龙川蓉朔」的性别写作「不能」，原样保留，最终表按听感与基频推断。
- 官方试听包有 1025 个基础音色 wav，Excel 只列出 597 个；其余约 428 个未收录。抽测的 2 个可用 3.0 flash 调用，但没有任何官方元数据。
- 没开思考模式时，Omni 会把轻柔的男声（如 `longanzhi_v3.1`）和童声听成女声，所以最终表的 `建议性别` 由官方文档、基频、听感三方综合判断，不直接采用听感。
