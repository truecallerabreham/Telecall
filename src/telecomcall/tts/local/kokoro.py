"""Kokoro TTS implementation."""

from fastrtc import get_tts_model

from telecomcall.tts.base import TTSModel, AudioChunk
from typing import AsyncIterator


class KokoroTTSModel(TTSModel):
    """Kokoro TTS model for local text-to-speech."""

    def __init__(self):
        self._model = get_tts_model("kokoro")

    async def stream_tts(self, text: str) -> AsyncIterator[AudioChunk]:
        """Convert text to speech using Kokoro."""
        async for audio_chunk in self._model.stream_tts(text):
            yield audio_chunk
