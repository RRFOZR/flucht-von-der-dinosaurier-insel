# engine/debug_overlay.py

import pygame
import time
from typing import Dict, Any
from config import Config

class DebugOverlay:
    """
    Debug overlay showing FPS, entity count, and other performance metrics.
    Toggle with F3 key.
    """

    def __init__(self) -> None:
        """Initialize the debug overlay."""
        self.enabled = False
        self.font = pygame.font.SysFont("Consolas", 14)
        self.font_large = pygame.font.SysFont("Consolas", 18, bold=True)

        # Performance tracking
        self.fps = 0.0
        self.frame_times = []
        self.max_frame_samples = 60
        self.last_update_time = time.time()

        # Custom metrics
        self.metrics: Dict[str, Any] = {}

    def toggle(self) -> None:
        """Toggle debug overlay on/off."""
        self.enabled = not self.enabled

    def update(self, dt: float) -> None:
        """
        Update performance metrics.

        Args:
            dt: Delta time in seconds
        """
        # Calculate FPS
        self.frame_times.append(dt)
        if len(self.frame_times) > self.max_frame_samples:
            self.frame_times.pop(0)

        if len(self.frame_times) > 0:
            avg_dt = sum(self.frame_times) / len(self.frame_times)
            self.fps = 1.0 / avg_dt if avg_dt > 0 else 0.0

    def set_metric(self, name: str, value: Any) -> None:
        """
        Set a custom metric to display.

        Args:
            name: Metric name
            value: Metric value
        """
        self.metrics[name] = value

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the debug overlay.

        Args:
            surface: Surface to render to
        """
        if not self.enabled:
            return

        # Background panel
        panel_width = 280
        panel_height = 200
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        surface.blit(panel, (10, 10))

        y_offset = 20

        # Title
        title = self.font_large.render("DEBUG INFO (F3 to toggle)", True, (0, 255, 0))
        surface.blit(title, (20, y_offset))
        y_offset += 30

        # FPS
        fps_color = (0, 255, 0) if self.fps >= 55 else (255, 255, 0) if self.fps >= 30 else (255, 0, 0)
        fps_text = self.font.render(f"FPS: {self.fps:.1f}", True, fps_color)
        surface.blit(fps_text, (20, y_offset))
        y_offset += 20

        # Frame time
        if len(self.frame_times) > 0:
            avg_ft = sum(self.frame_times) / len(self.frame_times) * 1000
            ft_text = self.font.render(f"Frame Time: {avg_ft:.2f}ms", True, (200, 200, 200))
            surface.blit(ft_text, (20, y_offset))
            y_offset += 25

        # Custom metrics
        for name, value in self.metrics.items():
            metric_text = self.font.render(f"{name}: {value}", True, (200, 200, 200))
            surface.blit(metric_text, (20, y_offset))
            y_offset += 20

    def is_enabled(self) -> bool:
        """Check if debug overlay is enabled."""
        return self.enabled
