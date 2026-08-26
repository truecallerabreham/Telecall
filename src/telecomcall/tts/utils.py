"""TTS model utilities."""

from telecomcall.tts.base import TTSModel
from telecomcall.tts.local.kokoro import KokoroTTSModel


def get_tts_model(model_name: str) -> TTSModel:
    """Get a TTS model by name.

    Available options:
        - "kokoro": Local Kokoro TTS via FastRTC
    """
    if model_name == "kokoro":
        return KokoroTTSModel()
    else:
        raise ValueError(
            f"Invalid TTS model name: {model_name}. Available: kokoro"
        )
