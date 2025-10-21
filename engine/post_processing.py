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

        # Pre-create vignette surface
        self.vignette_surface = self._create_vignette()

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
        Apply CRT-style scanlines.

        Args:
            surface: Surface to apply effect to
        """
        if not self.scanlines_enabled:
            return

        for y in range(0, self.height, 2):
            pygame.draw.line(surface, (0, 0, 0),
                           (0, y), (self.width, y), 1)
            # Make it subtle
            line_surf = pygame.Surface((self.width, 1), pygame.SRCALPHA)
            line_surf.fill((0, 0, 0, self.scanline_intensity))
            surface.blit(line_surf, (0, y))

    def apply_screen_noise(self, surface: pygame.Surface) -> None:
        """
        Apply random pixel noise (old TV static effect).

        Args:
            surface: Surface to apply effect to
        """
        if not self.screen_noise_enabled:
            return

        noise_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Add random pixels
        num_pixels = (self.width * self.height) // 200  # Sparse noise
        for _ in range(num_pixels):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            intensity = random.randint(0, self.noise_intensity)
            color = (intensity, intensity, intensity, 100)
            noise_surface.set_at((x, y), color)

        surface.blit(noise_surface, (0, 0))

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
