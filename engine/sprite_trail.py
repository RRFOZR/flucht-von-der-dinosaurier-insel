# engine/sprite_trail.py

import pygame
from typing import List, Tuple

class TrailSegment:
    """Single segment of a sprite trail."""

    def __init__(self, surface: pygame.Surface, x: float, y: float, alpha: int) -> None:
        self.surface = surface.copy()
        self.x = x
        self.y = y
        self.alpha = alpha
        self.surface.set_alpha(alpha)


class SpriteTrail:
    """
    Creates motion blur / trail effect behind moving sprites.
    """

    def __init__(self, max_segments: int = 5, alpha_decay: float = 50) -> None:
        """
        Initialize sprite trail.

        Args:
            max_segments: Maximum number of trail segments
            alpha_decay: How much alpha decreases per segment
        """
        self.max_segments = max_segments
        self.alpha_decay = alpha_decay
        self.segments: List[TrailSegment] = []

    def add_segment(self, surface: pygame.Surface, x: float, y: float, alpha: int = 200) -> None:
        """
        Add a new trail segment.

        Args:
            surface: Sprite surface to add
            x: X position
            y: Y position
            alpha: Starting alpha value
        """
        segment = TrailSegment(surface, x, y, alpha)
        self.segments.insert(0, segment)

        # Update alpha of existing segments
        for i, seg in enumerate(self.segments):
            seg.alpha = max(0, int(alpha - (i * self.alpha_decay)))
            seg.surface.set_alpha(seg.alpha)

        # Remove old segments
        if len(self.segments) > self.max_segments:
            self.segments = self.segments[:self.max_segments]

    def update(self, dt: float) -> None:
        """
        Update trail (fade out segments).

        Args:
            dt: Delta time in seconds
        """
        # Fade all segments
        fade_amount = int(self.alpha_decay * dt * 10)
        for segment in self.segments:
            segment.alpha = max(0, segment.alpha - fade_amount)
            segment.surface.set_alpha(segment.alpha)

        # Remove fully faded segments
        self.segments = [seg for seg in self.segments if seg.alpha > 0]

    def render(self, surface: pygame.Surface) -> None:
        """
        Render all trail segments.

        Args:
            surface: Surface to render to
        """
        # Render in reverse order (oldest first)
        for segment in reversed(self.segments):
            surface.blit(segment.surface, (int(segment.x), int(segment.y)))

    def clear(self) -> None:
        """Clear all trail segments."""
        self.segments.clear()
