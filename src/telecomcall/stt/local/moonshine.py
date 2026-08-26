"""Moonshine STT implementation."""

from fastrtc import get_stt_model

from telecomcall.stt.base import STTModel, AudioChunk


class MoonshineSTT(STTModel):
    """Moonshine STT model for local speech-to-text."""

    def __init__(self):
        self._model = get_stt_model("moonshine")

    def stt(self, audio: AudioChunk) -> str:
        """Transcribe audio using Moonshine."""
        return self._model.stt(audio)
