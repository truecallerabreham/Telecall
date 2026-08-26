"""Abstract base class for STT models."""

from abc import ABC, abstractmethod
from typing import Tuple

import numpy as np


AudioChunk = Tuple[int, np.ndarray]


class STTModel(ABC):
    """Base class for Speech-to-Text models."""

    @abstractmethod
    def stt(self, audio: AudioChunk) -> str:
        """Transcribe audio to text.

        Args:
            audio: Tuple of (sample_rate, numpy_array) audio data.

        Returns:
            Transcribed text.
        """
        pass
