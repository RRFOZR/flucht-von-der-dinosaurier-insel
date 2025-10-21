# engine/easing.py

import math
from typing import Callable, Any

class Easing:
    """
    Easing functions for smooth animations.
    All functions take a value from 0 to 1 and return an eased value.
    """

    @staticmethod
    def linear(t: float) -> float:
        """Linear interpolation (no easing)."""
        return t

    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Quadratic ease in."""
        return t * t

    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Quadratic ease out."""
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Quadratic ease in-out."""
        if t < 0.5:
            return 2 * t * t
        return -1 + (4 - 2 * t) * t

    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Cubic ease in."""
        return t * t * t

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Cubic ease out."""
        return (t - 1) ** 3 + 1

    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Cubic ease in-out."""
        if t < 0.5:
            return 4 * t * t * t
        return (t - 1) * (2 * t - 2) * (2 * t - 2) + 1

    @staticmethod
    def ease_in_expo(t: float) -> float:
        """Exponential ease in."""
        return 0 if t == 0 else 2 ** (10 * (t - 1))

    @staticmethod
    def ease_out_expo(t: float) -> float:
        """Exponential ease out."""
        return 1 if t == 1 else 1 - 2 ** (-10 * t)

    @staticmethod
    def bounce_out(t: float) -> float:
        """Bounce ease out."""
        if t < (1 / 2.75):
            return 7.5625 * t * t
        elif t < (2 / 2.75):
            t -= (1.5 / 2.75)
            return 7.5625 * t * t + 0.75
        elif t < (2.5 / 2.75):
            t -= (2.25 / 2.75)
            return 7.5625 * t * t + 0.9375
        else:
            t -= (2.625 / 2.75)
            return 7.5625 * t * t + 0.984375

    @staticmethod
    def elastic_out(t: float) -> float:
        """Elastic ease out."""
        if t == 0 or t == 1:
            return t
        return 2 ** (-10 * t) * math.sin((t - 0.075) * (2 * math.pi) / 0.3) + 1


class Tween:
    """
    Tweening system for smooth value interpolation.
    """

    def __init__(self, start_value: float, end_value: float, duration: float,
                 ease_function: Callable[[float], float] = Easing.linear) -> None:
        """
        Initialize a tween.

        Args:
            start_value: Starting value
            end_value: Target value
            duration: Duration in seconds
            ease_function: Easing function to use
        """
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.ease_function = ease_function
        self.timer = 0.0
        self.current_value = start_value
        self.complete = False
        self.callback = None

    def update(self, dt: float) -> float:
        """
        Update tween and return current value.

        Args:
            dt: Delta time in seconds

        Returns:
            Current tweened value
        """
        if self.complete:
            return self.current_value

        self.timer += dt
        progress = min(1.0, self.timer / self.duration)

        # Apply easing
        eased_progress = self.ease_function(progress)

        # Interpolate
        self.current_value = self.start_value + (self.end_value - self.start_value) * eased_progress

        if progress >= 1.0:
            self.complete = True
            self.current_value = self.end_value
            if self.callback:
                self.callback()

        return self.current_value

    def on_complete(self, callback: Callable) -> 'Tween':
        """
        Set callback for when tween completes.

        Args:
            callback: Function to call when complete

        Returns:
            Self for chaining
        """
        self.callback = callback
        return self

    def is_complete(self) -> bool:
        """Check if tween is complete."""
        return self.complete
