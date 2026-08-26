"""STT model utilities."""

from telecomcall.stt.base import STTModel
from telecomcall.stt.local.moonshine import MoonshineSTT


def get_stt_model(model: str) -> STTModel:
    """Get the STT model based on the model name."""
    if model == "moonshine":
        return MoonshineSTT()
    else:
        raise ValueError(f"Invalid STT model: {model}. Available: moonshine")
