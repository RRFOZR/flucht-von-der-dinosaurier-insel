# engine/audio_3d.py

import pygame
import math
from typing import Optional

class Audio3D:
    """
    3D positional audio system with distance attenuation.
    """

    def __init__(self, listener_x: float = 0, listener_y: float = 0) -> None:
        """
        Initialize 3D audio system.

        Args:
            listener_x: Initial listener X position
            listener_y: Initial listener Y position
        """
        self.listener_x = listener_x
        self.listener_y = listener_y
        self.max_distance = 20.0  # tiles
        self.rolloff_factor = 1.0

    def set_listener_position(self, x: float, y: float) -> None:
        """
        Set the listener (player/camera) position.

        Args:
            x: Listener X position in tiles
            y: Listener Y position in tiles
        """
        self.listener_x = x
        self.listener_y = y

    def calculate_volume(self, source_x: float, source_y: float,
                        base_volume: float = 1.0) -> float:
        """
        Calculate volume based on distance from listener.

        Args:
            source_x: Sound source X position in tiles
            source_y: Sound source Y position in tiles
            base_volume: Base volume (0.0 to 1.0)

        Returns:
            Attenuated volume (0.0 to 1.0)
        """
        # Calculate distance
        dx = source_x - self.listener_x
        dy = source_y - self.listener_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Calculate attenuation
        if distance >= self.max_distance:
            return 0.0

        # Linear rolloff
        attenuation = 1.0 - (distance / self.max_distance) ** self.rolloff_factor
        return max(0.0, min(1.0, base_volume * attenuation))

    def calculate_panning(self, source_x: float, source_y: float) -> tuple[float, float]:
        """
        Calculate stereo panning based on position.

        Args:
            source_x: Sound source X position
            source_y: Sound source Y position

        Returns:
            Tuple of (left_volume, right_volume) from 0.0 to 1.0
        """
        dx = source_x - self.listener_x

        # Simple left-right panning
        if abs(dx) < 0.1:
            return (1.0, 1.0)  # Centered

        # Calculate pan (-1 to 1, -1 = left, 1 = right)
        pan = max(-1.0, min(1.0, dx / 10.0))

        left = 1.0 - max(0.0, pan)
        right = 1.0 + min(0.0, pan)

        return (left, right)

    def play_at_position(self, sound: pygame.mixer.Sound,
                        source_x: float, source_y: float,
                        base_volume: float = 1.0) -> Optional[pygame.mixer.Channel]:
        """
        Play a sound at a world position with distance attenuation.

        Args:
            sound: Sound to play
            source_x: Sound source X position
            source_y: Sound source Y position
            base_volume: Base volume before attenuation

        Returns:
            Channel playing the sound, or None if out of range
        """
        volume = self.calculate_volume(source_x, source_y, base_volume)

        if volume <= 0.01:
            return None  # Too far away

        channel = sound.play()
        if channel:
            channel.set_volume(volume)

        return channel
