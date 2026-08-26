"""Edge TTS implementation - Microsoft's free TTS, no API key needed."""

import io
import struct
import numpy as np
import edge_tts

from telecomcall.tts.base import TTSModel, AudioChunk
from telecomcall.config import settings


class EdgeTTSModel(TTSModel):
    """Edge TTS - free cloud text-to-speech from Microsoft."""

    def __init__(self, voice: str = "en-US-JennyNeural"):
        self._voice = voice

    async def stream_tts(self, text: str) -> AudioChunk:
        """Convert text to speech using Edge TTS."""
        communicate = edge_tts.Communicate(text, self._voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]

        # Convert mp3 bytes to raw PCM using wave module
        # Edge TTS returns mp3, we need to convert
        sample_rate = 24000
        audio_array = self._mp3_to_pcm(audio_data, sample_rate)
        yield (sample_rate, audio_array)

    def _mp3_to_pcm(self, mp3_data: bytes, sample_rate: int = 24000) -> np.ndarray:
        """Convert mp3 bytes to numpy array. Falls back to raw bytes if no decoder."""
        try:
            import subprocess
            import tempfile
            import os

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                f.write(mp3_data)
                mp3_path = f.name

            wav_path = mp3_path.replace(".mp3", ".wav")
            subprocess.run(
                ["ffmpeg", "-i", mp3_path, "-ar", str(sample_rate), "-ac", "1", "-f", "wav", wav_path, "-y"],
                capture_output=True,
                check=True,
            )

            import wave
            with wave.open(wav_path, "rb") as wf:
                frames = wf.readframes(wf.getnframes())
                audio = np.frombuffer(frames, dtype=np.int16)

            os.unlink(mp3_path)
            os.unlink(wav_path)
            return audio

        except Exception:
            # Fallback: return silence if ffmpeg not available
            return np.zeros(sample_rate, dtype=np.int16)
