"""Abstract base class for STT models."""

from abc import ABC, abstractmethod
from typing import Tuple

import numpy as np


AudioChunk = Tuple[int, np.ndarray]


class STTModel(ABC):
    """Base class for Speech-to-Text models."""

    @abstractmethod
    def stt(self, audio: bytes, sample_rate: int = 16000) -> str:
        """Transcribe audio bytes to text.

        Args:
            audio: Raw audio bytes.
            sample_rate: Audio sample rate.

        Returns:
            Transcribed text.
        """
        pass
