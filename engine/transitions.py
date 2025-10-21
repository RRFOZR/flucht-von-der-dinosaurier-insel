# engine/transitions.py

import pygame
from typing import Callable, Optional

class Transition:
    """
    Scene transition effects (fade in/out, wipe, etc.)
    """

    def __init__(self, surface: pygame.Surface) -> None:
        """
        Initialize transition system.

        Args:
            surface: The surface to apply transitions to
        """
        self.surface = surface
        self.active = False
        self.alpha = 0
        self.duration = 0.5
        self.timer = 0.0
        self.fade_in = True
        self.callback: Optional[Callable] = None
        self.color = (0, 0, 0)  # Black by default

    def fade_to_black(self, duration: float = 0.5, callback: Optional[Callable] = None) -> None:
        """
        Fade to black.

        Args:
            duration: Fade duration in seconds
            callback: Function to call when fade completes
        """
        self.active = True
        self.fade_in = False
        self.duration = duration
        self.timer = 0.0
        self.callback = callback
        self.alpha = 0

    def fade_from_black(self, duration: float = 0.5, callback: Optional[Callable] = None) -> None:
        """
        Fade from black.

        Args:
            duration: Fade duration in seconds
            callback: Function to call when fade completes
        """
        self.active = True
        self.fade_in = True
        self.duration = duration
        self.timer = 0.0
        self.callback = callback
        self.alpha = 255

    def crossfade(self, duration: float = 0.5, callback: Optional[Callable] = None) -> None:
        """
        Quick crossfade (fade out then fade in).

        Args:
            duration: Total duration in seconds
            callback: Function to call at midpoint (when fully black)
        """
        # Fade out, then fade in
        self.fade_to_black(duration / 2, lambda: self.fade_from_black(duration / 2))
        self.callback = callback

    def update(self, dt: float) -> None:
        """
        Update transition state.

        Args:
            dt: Delta time in seconds
        """
        if not self.active:
            return

        self.timer += dt

        # Calculate alpha based on fade direction
        progress = min(1.0, self.timer / self.duration)

        if self.fade_in:
            # Fading from black (alpha 255 -> 0)
            self.alpha = int(255 * (1.0 - progress))
        else:
            # Fading to black (alpha 0 -> 255)
            self.alpha = int(255 * progress)

        # Check if complete
        if progress >= 1.0:
            self.active = False
            if self.callback:
                self.callback()
                self.callback = None

    def render(self) -> None:
        """Render the transition overlay."""
        if not self.active and self.alpha == 0:
            return

        overlay = pygame.Surface((self.surface.get_width(), self.surface.get_height()))
        overlay.fill(self.color)
        overlay.set_alpha(self.alpha)
        self.surface.blit(overlay, (0, 0))

    def is_active(self) -> bool:
        """Check if transition is currently active."""
        return self.active

    def set_color(self, color: tuple[int, int, int]) -> None:
        """
        Set transition color.

        Args:
            color: RGB color tuple
        """
        self.color = color
