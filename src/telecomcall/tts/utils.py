"""TTS model utilities."""

from telecomcall.tts.base import TTSModel
from telecomcall.tts.local.edge_tts_impl import EdgeTTSModel


def get_tts_model(model_name: str) -> TTSModel:
    """Get a TTS model by name.

    Available options:
        - "edge-tts": Microsoft Edge TTS (cloud, free, no API key)
    """
    if model_name == "edge-tts":
        return EdgeTTSModel()
    else:
        raise ValueError(
            f"Invalid TTS model name: {model_name}. Available: edge-tts"
        )
