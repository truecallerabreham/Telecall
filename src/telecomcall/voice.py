"""Background sound effects for the voice agent."""


class KeyboardEffect:
    """Keyboard typing sound effect."""

    def __init__(self, duration: float = 3.0):
        self._duration = duration

    async def stream(self):
        """Stream keyboard sound effect audio chunks."""
        # Placeholder - will be replaced with actual sound effect
        # For now, yield silence
        import numpy as np
        sample_rate = 24000
        samples = int(sample_rate * self._duration)
        silence = np.zeros(samples, dtype=np.int16)
        yield (sample_rate, silence)


def get_sound_effect(effect_type=None):
    """Create and return a sound effect instance."""
    effect_type = effect_type or KeyboardEffect
    return effect_type()
