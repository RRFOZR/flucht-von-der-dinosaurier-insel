# engine/post_processing.py

import pygame
import random

class PostProcessing:
    """
    Post-processing effects like vignette, chromatic aberration, scan lines.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize post-processing.

        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height

        # Effect toggles
        self.vignette_enabled = False
        self.scanlines_enabled = False
        self.chromatic_aberration_enabled = False
        self.screen_noise_enabled = False

        # Effect parameters
        self.vignette_strength = 0.5
        self.scanline_intensity = 50
        self.aberration_strength = 2
        self.noise_intensity = 10

        # Pre-create cached surfaces for performance
        self.vignette_surface = self._create_vignette()
        self.scanline_surface = self._create_scanlines()

        # Noise throttling
        self.noise_surface = None
        self.noise_update_timer = 0.0
        self.noise_update_interval = 0.1  # Update noise every 0.1 seconds

    def _create_vignette(self) -> pygame.Surface:
        """Create vignette overlay surface."""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        center_x = self.width // 2
        center_y = self.height // 2
        max_dist = ((center_x ** 2) + (center_y ** 2)) ** 0.5

        for y in range(self.height):
            for x in range(self.width):
                dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                ratio = dist / max_dist
                alpha = int(255 * ratio * self.vignette_strength)
                surface.set_at((x, y), (0, 0, 0, alpha))

        return surface

    def _create_scanlines(self) -> pygame.Surface:
        """Create cached scanline overlay surface."""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw scanlines every other row
        for y in range(0, self.height, 2):
            pygame.draw.line(surface, (0, 0, 0, self.scanline_intensity),
                           (0, y), (self.width, y), 1)

        return surface

    def apply_vignette(self, surface: pygame.Surface) -> None:
        """
        Apply vignette effect.

        Args:
            surface: Surface to apply effect to
        """
        if self.vignette_enabled:
            surface.blit(self.vignette_surface, (0, 0))

    def apply_scanlines(self, surface: pygame.Surface) -> None:
        """
        Apply CRT-style scanlines using cached surface.

        Args:
            surface: Surface to apply effect to
        """
        if self.scanlines_enabled:
            surface.blit(self.scanline_surface, (0, 0))

    def update(self, dt: float) -> None:
        """
        Update time-based effects like noise.

        Args:
            dt: Delta time in seconds
        """
        if self.screen_noise_enabled:
            self.noise_update_timer += dt
            if self.noise_update_timer >= self.noise_update_interval:
                self.noise_update_timer = 0.0
                self._regenerate_noise()

    def _regenerate_noise(self) -> None:
        """Regenerate the noise surface."""
        self.noise_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Add random pixels
        num_pixels = (self.width * self.height) // 200  # Sparse noise
        for _ in range(num_pixels):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            intensity = random.randint(0, self.noise_intensity)
            color = (intensity, intensity, intensity, 100)
            self.noise_surface.set_at((x, y), color)

    def apply_screen_noise(self, surface: pygame.Surface) -> None:
        """
        Apply random pixel noise (old TV static effect) using cached/throttled surface.

        Args:
            surface: Surface to apply effect to
        """
        if self.screen_noise_enabled and self.noise_surface:
            surface.blit(self.noise_surface, (0, 0))

    def apply_all(self, surface: pygame.Surface) -> None:
        """
        Apply all enabled effects.

        Args:
            surface: Surface to apply effects to
        """
        self.apply_vignette(surface)
        self.apply_scanlines(surface)
        self.apply_screen_noise(surface)

    def toggle_vignette(self) -> None:
        """Toggle vignette effect."""
        self.vignette_enabled = not self.vignette_enabled

    def toggle_scanlines(self) -> None:
        """Toggle scanlines effect."""
        self.scanlines_enabled = not self.scanlines_enabled

    def toggle_screen_noise(self) -> None:
        """Toggle screen noise effect."""
        self.screen_noise_enabled = not self.screen_noise_enabled
