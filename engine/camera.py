# engine/camera.py

import pygame
import random
import math
from config import Config

class Camera:
    """
    Advanced camera system with:
    - Smooth following
    - Screen shake
    - Zoom support
    - Map bounds
    - Dead zone
    - Look-ahead
    - World-to-screen conversion
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the advanced camera.

        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        self.width = width
        self.height = height
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0
        self.smoothness = 0.22  # Optimized for buttery-smooth 60 FPS (0-1)

        # Screen shake
        self.shake_intensity = 0.0
        self.shake_duration = 0.0
        self.shake_timer = 0.0
        self.shake_offset_x = 0.0
        self.shake_offset_y = 0.0
        self.shake_falloff = "linear"  # linear, exponential, or none

        # Zoom
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.zoom_speed = 0.1

        # Bounds (optional - set to None for no bounds)
        self.bounds_rect = None  # pygame.Rect or None

        # Dead zone (area where camera doesn't move)
        self.dead_zone_width = 0  # pixels
        self.dead_zone_height = 0  # pixels

        # Look-ahead (camera shows where you're moving)
        self.look_ahead_distance = 0.0  # tiles
        self.look_ahead_smoothness = 0.1

    def shake(self, intensity: float = 5.0, duration: float = 0.3,
              falloff: str = "exponential") -> None:
        """
        Trigger a screen shake effect.

        Args:
            intensity: Maximum shake offset in pixels
            duration: How long the shake lasts in seconds
            falloff: 'linear', 'exponential', or 'none'
        """
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_timer = duration
        self.shake_falloff = falloff

    def set_zoom(self, zoom: float) -> None:
        """
        Set target zoom level.

        Args:
            zoom: Zoom level (1.0 = normal, 2.0 = 2x zoom in, 0.5 = zoom out)
        """
        self.target_zoom = max(0.1, min(5.0, zoom))  # Clamp between 0.1 and 5.0

    def set_bounds(self, rect: pygame.Rect) -> None:
        """
        Set camera bounds (won't show outside this area).

        Args:
            rect: Rectangle defining the bounds in world pixels
        """
        self.bounds_rect = rect

    def set_dead_zone(self, width: int, height: int) -> None:
        """
        Set dead zone size (area in screen center where camera doesn't move).

        Args:
            width: Dead zone width in pixels
            height: Dead zone height in pixels
        """
        self.dead_zone_width = width
        self.dead_zone_height = height

    def set_look_ahead(self, distance: float) -> None:
        """
        Set look-ahead distance (camera shows ahead of movement).

        Args:
            distance: How many tiles ahead to look
        """
        self.look_ahead_distance = distance

    def set_target(self, x: float, y: float, velocity_x: float = 0, velocity_y: float = 0) -> None:
        """
        Set the camera's target position in world coordinates.

        Args:
            x: Target x position in world tiles
            y: Target y position in world tiles
            velocity_x: Optional velocity for look-ahead
            velocity_y: Optional velocity for look-ahead
        """
        self.target_x = x
        self.target_y = y

        # Apply look-ahead
        if self.look_ahead_distance > 0:
            self.target_x += velocity_x * self.look_ahead_distance
            self.target_y += velocity_y * self.look_ahead_distance

    def update(self, dt: float) -> None:
        """
        Update camera position with smooth interpolation, shake, and zoom.

        Args:
            dt: Delta time in seconds
        """
        # Update zoom
        if abs(self.zoom - self.target_zoom) > 0.01:
            self.zoom += (self.target_zoom - self.zoom) * self.zoom_speed

        # Calculate target camera position
        target_cam_x = self.target_x * Config.TILE_SIZE - self.width // 2
        target_cam_y = self.target_y * Config.TILE_SIZE - self.height // 2

        # Apply dead zone
        if self.dead_zone_width > 0 or self.dead_zone_height > 0:
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            target_center_x = target_cam_x + self.width // 2
            target_center_y = target_cam_y + self.height // 2

            # Only move if outside dead zone
            dx = target_center_x - center_x
            dy = target_center_y - center_y

            if abs(dx) < self.dead_zone_width // 2:
                target_cam_x = self.x
            if abs(dy) < self.dead_zone_height // 2:
                target_cam_y = self.y

        # Smooth interpolation towards target
        self.x += (target_cam_x - self.x) * self.smoothness
        self.y += (target_cam_y - self.y) * self.smoothness

        # Apply bounds
        if self.bounds_rect:
            view_width = self.width / self.zoom
            view_height = self.height / self.zoom

            self.x = max(self.bounds_rect.x, min(self.x,
                        self.bounds_rect.right - view_width))
            self.y = max(self.bounds_rect.y, min(self.y,
                        self.bounds_rect.bottom - view_height))

        # Update screen shake
        if self.shake_timer > 0:
            self.shake_timer -= dt

            # Calculate shake amount based on falloff
            if self.shake_falloff == "exponential":
                shake_amount = self.shake_intensity * (self.shake_timer / self.shake_duration) ** 2
            elif self.shake_falloff == "linear":
                shake_amount = self.shake_intensity * (self.shake_timer / self.shake_duration)
            else:  # none
                shake_amount = self.shake_intensity

            # Random shake offset
            angle = random.uniform(0, math.pi * 2)
            self.shake_offset_x = math.cos(angle) * shake_amount
            self.shake_offset_y = math.sin(angle) * shake_amount
        else:
            self.shake_offset_x = 0.0
            self.shake_offset_y = 0.0

    def apply(self, x: float, y: float) -> tuple[int, int]:
        """
        Convert world coordinates to screen coordinates with shake and zoom.

        Args:
            x: World x position in tiles
            y: World y position in tiles

        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        screen_x = (x * Config.TILE_SIZE - self.x) * self.zoom + self.shake_offset_x
        screen_y = (y * Config.TILE_SIZE - self.y) * self.zoom + self.shake_offset_y
        return int(screen_x), int(screen_y)

    def world_to_screen(self, wx: float, wy: float) -> tuple[int, int]:
        """
        Alias for apply() - converts world coordinates to screen coordinates.

        Args:
            wx: World x position in tiles
            wy: World y position in tiles

        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        return self.apply(wx, wy)

    def screen_to_world(self, sx: int, sy: int) -> tuple[float, float]:
        """
        Convert screen coordinates to world coordinates.

        Args:
            sx: Screen x position in pixels
            sy: Screen y position in pixels

        Returns:
            Tuple of (world_x, world_y) in tiles
        """
        world_x = ((sx - self.shake_offset_x) / self.zoom + self.x) / Config.TILE_SIZE
        world_y = ((sy - self.shake_offset_y) / self.zoom + self.y) / Config.TILE_SIZE
        return world_x, world_y

    def get_visible_bounds(self) -> tuple[int, int, int, int]:
        """
        Get the bounds of the visible area in world coordinates.

        Returns:
            Tuple of (start_x, start_y, end_x, end_y) in tiles
        """
        tile_cols = int(self.width / (Config.TILE_SIZE * self.zoom))
        tile_rows = int(self.height / (Config.TILE_SIZE * self.zoom))

        cam_tile_x = self.x / Config.TILE_SIZE
        cam_tile_y = self.y / Config.TILE_SIZE

        start_x = max(0, int(cam_tile_x) - 1)
        end_x = min(Config.MAP_WIDTH, int(cam_tile_x) + tile_cols + 2)
        start_y = max(0, int(cam_tile_y) - 1)
        end_y = min(Config.MAP_HEIGHT, int(cam_tile_y) + tile_rows + 2)

        return start_x, start_y, end_x, end_y

    def is_shaking(self) -> bool:
        """Check if camera is currently shaking."""
        return self.shake_timer > 0
