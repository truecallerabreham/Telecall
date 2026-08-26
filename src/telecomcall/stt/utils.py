"""STT model utilities."""

from telecomcall.stt.base import STTModel
from telecomcall.stt.local.groq_whisper import GroqWhisperSTT


def get_stt_model(model: str) -> STTModel:
    """Get the STT model based on the model name.

    Available options:
        - "groq-whisper": Groq Whisper API (cloud, free tier)
    """
    if model == "groq-whisper":
        return GroqWhisperSTT()
    else:
        raise ValueError(f"Invalid STT model: {model}. Available: groq-whisper")
