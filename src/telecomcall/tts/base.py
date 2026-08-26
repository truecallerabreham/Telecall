"""Abstract base class for TTS models."""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Tuple

import numpy as np


AudioChunk = Tuple[int, np.ndarray]


class TTSModel(ABC):
    """Base class for Text-to-Speech models."""

    @abstractmethod
    async def stream_tts(self, text: str) -> AsyncIterator[AudioChunk]:
        """Convert text to speech audio chunks.

        Args:
            text: Text to synthesize.

        Yields:
            Audio chunks as (sample_rate, numpy_array) tuples.
        """
        pass
