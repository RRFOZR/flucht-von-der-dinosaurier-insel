# engine/camera.py

import pygame
from config import Config

class Camera:
    """
    Camera system with smooth following and world-to-screen conversion.
    Provides smooth camera movement and handles coordinate transformations.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the camera.

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
        self.smoothness = 0.15  # Higher = faster following (0-1)

    def set_target(self, x: float, y: float) -> None:
        """
        Set the camera's target position in world coordinates.

        Args:
            x: Target x position in world tiles
            y: Target y position in world tiles
        """
        self.target_x = x
        self.target_y = y

    def update(self, dt: float) -> None:
        """
        Update camera position with smooth interpolation.

        Args:
            dt: Delta time in seconds
        """
        # Smooth lerp towards target
        target_cam_x = self.target_x * Config.TILE_SIZE - self.width // 2
        target_cam_y = self.target_y * Config.TILE_SIZE - self.height // 2

        # Interpolate camera position
        self.x += (target_cam_x - self.x) * self.smoothness
        self.y += (target_cam_y - self.y) * self.smoothness

    def apply(self, x: float, y: float) -> tuple[int, int]:
        """
        Convert world coordinates to screen coordinates.

        Args:
            x: World x position in tiles
            y: World y position in tiles

        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        screen_x = x * Config.TILE_SIZE - self.x
        screen_y = y * Config.TILE_SIZE - self.y
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

    def get_visible_bounds(self) -> tuple[int, int, int, int]:
        """
        Get the bounds of the visible area in world coordinates.

        Returns:
            Tuple of (start_x, start_y, end_x, end_y) in tiles
        """
        tile_cols = self.width // Config.TILE_SIZE
        tile_rows = self.height // Config.TILE_SIZE

        cam_tile_x = self.x / Config.TILE_SIZE
        cam_tile_y = self.y / Config.TILE_SIZE

        start_x = max(0, int(cam_tile_x) - 1)
        end_x = min(Config.MAP_WIDTH, int(cam_tile_x) + tile_cols + 2)
        start_y = max(0, int(cam_tile_y) - 1)
        end_y = min(Config.MAP_HEIGHT, int(cam_tile_y) + tile_rows + 2)

        return start_x, start_y, end_x, end_y
