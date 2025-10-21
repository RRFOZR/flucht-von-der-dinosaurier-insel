# engine/delta_smoother.py

from collections import deque

class DeltaSmoother:
    """
    Smooths delta time to prevent stuttering from frame time spikes.
    """

    def __init__(self, sample_size: int = 10) -> None:
        """
        Initialize delta time smoother.

        Args:
            sample_size: Number of frames to average
        """
        self.sample_size = sample_size
        self.samples = deque(maxlen=sample_size)
        self.smoothed_dt = 1 / 60.0  # Start with 60 FPS assumption

    def smooth(self, dt: float) -> float:
        """
        Add a delta time sample and return smoothed value.

        Args:
            dt: Raw delta time in seconds

        Returns:
            Smoothed delta time
        """
        # Clamp extreme values
        dt = max(0.001, min(0.1, dt))  # Between 1ms and 100ms

        self.samples.append(dt)

        # Calculate average
        if len(self.samples) > 0:
            self.smoothed_dt = sum(self.samples) / len(self.samples)

        return self.smoothed_dt

    def get_smoothed_dt(self) -> float:
        """Get the current smoothed delta time."""
        return self.smoothed_dt

    def reset(self) -> None:
        """Reset the smoother."""
        self.samples.clear()
        self.smoothed_dt = 1 / 60.0
