"""Groq Whisper STT implementation."""

import groq

from telecomcall.stt.base import STTModel
from telecomcall.config import settings


class GroqWhisperSTT(STTModel):
    """Groq Whisper STT - cloud speech-to-text via free tier."""

    def __init__(self):
        self._client = groq.Groq(api_key=settings.groq.api_key)

    def stt(self, audio: bytes, sample_rate: int = 16000) -> str:
        """Transcribe audio using Groq Whisper."""
        transcription = self._client.audio.transcriptions.create(
            file=("audio.wav", audio, "audio/wav"),
            model="whisper-large-v3-turbo",
            language="en",
        )
        return transcription.text
