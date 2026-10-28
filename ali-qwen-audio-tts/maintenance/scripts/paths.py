"""维护脚本共用的路径。使用 skill 时只需要 reference/voices/<model>.csv，其余都在 maintenance/ 下。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # skill 根目录
MAINT = ROOT / "maintenance"
SOURCE = MAINT / "source"                             # 官方原始资料：音色列表 md、基础音色 Excel
DATA = MAINT / "data"                                 # 中间结果：official / measured / omni / gender-recheck
SAMPLES = MAINT / "samples"                           # 试听音频与 Omni 缓存；index.csv 里的路径相对此目录
VOICES = ROOT / "reference" / "voices"                # 最终音色表（使用时唯一要读的）
VOICE_LIST_MD = SOURCE / "qwen-audio-音色列表.md"
MODELS = ["qwen-audio-3.1-tts-plus", "qwen-audio-3.1-tts-flash",
          "qwen-audio-3.0-tts-plus", "qwen-audio-3.0-tts-flash"]


def basic_xlsx(model: str) -> Path:
    return SOURCE / f"{model}基础音色.xlsx"


def official(model: str) -> Path:
    return DATA / f"{model}.official.csv"
