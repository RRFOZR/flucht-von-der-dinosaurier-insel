# engine/asset_manager.py

import pygame
import logging
from typing import Optional
from config import Config
from resource_path import get_resource_path

logger = logging.getLogger(__name__)

class AssetManager:
    """
    Centralized asset manager with caching.
    Loads and caches sprites, sounds, and music to avoid duplicate loading.
    """

    def __init__(self) -> None:
        """Initialize the asset manager with empty caches."""
        self.sprites: dict[str, pygame.Surface] = {}
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.music_tracks: dict[str, str] = {}
        self._sprite_cache_info: dict[str, tuple] = {}  # path -> (size, flip_x, flip_y)

    def load_sprite(self, path: str, size: Optional[tuple[int, int]] = None,
                    flip_x: bool = False, flip_y: bool = False) -> Optional[pygame.Surface]:
        """
        Load a sprite with optional scaling and flipping, with caching.

        Args:
            path: Path to the image file
            size: Optional (width, height) to scale to
            flip_x: Whether to flip horizontally
            flip_y: Whether to flip vertically

        Returns:
            The loaded pygame.Surface, or None if loading failed
        """
        # Create cache key based on transformations
        cache_key = f"{path}:{size}:{flip_x}:{flip_y}"

        if cache_key in self.sprites:
            return self.sprites[cache_key]

        try:
            # Use resource_path helper for PyInstaller compatibility
            resource_file = get_resource_path(path)
            sprite = pygame.image.load(resource_file).convert_alpha()

            if size:
                sprite = pygame.transform.scale(sprite, size)

            if flip_x or flip_y:
                sprite = pygame.transform.flip(sprite, flip_x, flip_y)

            self.sprites[cache_key] = sprite
            logger.debug(f"Loaded sprite: {path} (cached as {cache_key})")
            return sprite

        except (pygame.error, FileNotFoundError) as e:
            logger.warning(f"Could not load sprite '{path}': {e}")
            return None

    def get_sprite(self, path: str, size: Optional[tuple[int, int]] = None,
                   flip_x: bool = False, flip_y: bool = False) -> Optional[pygame.Surface]:
        """
        Alias for load_sprite - get a sprite from cache or load it.

        Args:
            path: Path to the image file
            size: Optional (width, height) to scale to
            flip_x: Whether to flip horizontally
            flip_y: Whether to flip vertically

        Returns:
            The pygame.Surface, or None if not available
        """
        return self.load_sprite(path, size, flip_x, flip_y)

    def load_sound(self, path: str, volume: float = 1.0) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound effect with caching.

        Args:
            path: Path to the sound file
            volume: Volume level (0.0 to 1.0)

        Returns:
            The loaded pygame.mixer.Sound, or None if loading failed
        """
        if path in self.sounds:
            return self.sounds[path]

        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            self.sounds[path] = sound
            logger.debug(f"Loaded sound: {path}")
            return sound

        except (pygame.error, FileNotFoundError) as e:
            logger.warning(f"Could not load sound '{path}': {e}")
            return None

    def preload_all_sprites(self) -> None:
        """Preload all sprites defined in Config.SPRITES."""
        logger.info("Preloading all sprites...")
        self._preload_sprites_recursive(Config.SPRITES)
        logger.info(f"Preloaded {len(self.sprites)} sprites.")

    def _preload_sprites_recursive(self, node, path_parts=None):
        """Recursively preload sprites from nested config structure."""
        if path_parts is None:
            path_parts = []

        if isinstance(node, dict):
            for key, value in node.items():
                self._preload_sprites_recursive(value, path_parts + [key])
        elif isinstance(node, str):
            # It's a path - load it
            self.load_sprite(node, size=(Config.TILE_SIZE, Config.TILE_SIZE))

    def preload_all_sounds(self) -> None:
        """Preload all sounds defined in Config.SOUNDS."""
        logger.info("Preloading all sounds...")
        self._preload_sounds_recursive(Config.SOUNDS)
        logger.info(f"Preloaded {len(self.sounds)} sounds.")

    def _preload_sounds_recursive(self, node, path_parts=None):
        """Recursively preload sounds from nested config structure."""
        if path_parts is None:
            path_parts = []

        if isinstance(node, dict):
            for key, value in node.items():
                self._preload_sounds_recursive(value, path_parts + [key])
        elif isinstance(node, str):
            # Get volume from config if available
            sound_name = path_parts[-1] if path_parts else "unknown"
            volume = Config.SOUND_VOLUMES.get(sound_name, Config.DEFAULT_SOUND_VOLUME)
            self.load_sound(node, volume)
        elif isinstance(node, list):
            # Handle lists (like background music)
            for item in node:
                if isinstance(item, str):
                    self.load_sound(item, Config.DEFAULT_SOUND_VOLUME)

    def clear_cache(self) -> None:
        """Clear all cached assets."""
        self.sprites.clear()
        self.sounds.clear()
        self.music_tracks.clear()
        logger.info("Asset cache cleared.")

    def get_cache_stats(self) -> dict:
        """
        Get statistics about cached assets.

        Returns:
            Dictionary with cache statistics
        """
        return {
            'sprites': len(self.sprites),
            'sounds': len(self.sounds),
            'music': len(self.music_tracks)
        }


# Global singleton instance
asset_manager = AssetManager()
