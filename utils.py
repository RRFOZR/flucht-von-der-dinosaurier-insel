# utils.py

import random
import math
import pygame
import logging
from config import Config

# Import asset manager for sprite caching
try:
    from engine.asset_manager import asset_manager
    USE_ASSET_MANAGER = True
except ImportError:
    USE_ASSET_MANAGER = False

logger = logging.getLogger(__name__)

def is_night(time_since_start: float) -> bool:
    cycle_pos = time_since_start % Config.CYCLE_LENGTH
    return cycle_pos > Config.DAY_LENGTH

def is_passable(x: int, y: int, game_map: list[list[int]], for_dino: bool = False) -> bool:
    if x < 0 or x >= Config.MAP_WIDTH or y < 0 or y >= Config.MAP_HEIGHT:
        return False
    tile = game_map[y][x]
    if for_dino and tile == 3:
        return False
    return Config.BIOMES[tile]["passable"]

def get_random_passable_tile(game_map: list[list[int]], for_dino: bool=False) -> tuple[int, int]:
    attempts = 0
    while attempts < 1000:
        x = random.randint(0, Config.MAP_WIDTH - 1)
        y = random.randint(0, Config.MAP_HEIGHT - 1)
        if is_passable(x, y, game_map, for_dino=for_dino):
            return x, y
        attempts += 1
    logger.error("Could not find a passable tile after 1000 attempts.")
    raise ValueError("Could not find a passable tile after 1000 attempts.")

def direction_towards(x_from: float, y_from: float, x_to: float, y_to: float) -> tuple[float, float]:
    dx = x_to - x_from
    dy = y_to - y_from
    dist = math.sqrt(dx*dx + dy*dy)
    if dist == 0:
        return 0, 0
    return dx/dist, dy/dist

def load_frames(frame_keys: list[str], *sprite_config_keys: str) -> tuple[list[pygame.Surface], list[pygame.Surface]]:
    """
    Load animation frames using the asset manager for caching.

    Args:
        frame_keys: List of frame identifiers
        *sprite_config_keys: Path through Config.SPRITES hierarchy

    Returns:
        Tuple of (frames_right, frames_left) sprite lists
    """
    frames_right = []
    frames_left = []

    for key in frame_keys:
        path = Config.get_sprite_path(*sprite_config_keys, key)
        if path:
            # Use asset manager if available for caching
            if USE_ASSET_MANAGER:
                sprite = asset_manager.load_sprite(path, size=(Config.TILE_SIZE, Config.TILE_SIZE))
                sprite_left = asset_manager.load_sprite(path, size=(Config.TILE_SIZE, Config.TILE_SIZE), flip_x=True)

                if sprite:
                    frames_right.append(sprite)
                if sprite_left:
                    frames_left.append(sprite_left)
            else:
                # Fallback to direct loading
                try:
                    sprite = pygame.image.load(path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, (Config.TILE_SIZE, Config.TILE_SIZE))
                    frames_right.append(sprite)
                    frames_left.append(pygame.transform.flip(sprite, True, False))
                except pygame.error as e:
                    logger.warning(f"Could not load sprite '{key}' at '{path}': {e}")
        else:
            logger.warning(f"Sprite path not found for '{key}' in {sprite_config_keys}.")

    if not frames_right:
        fallback = pygame.Surface((Config.TILE_SIZE, Config.TILE_SIZE), pygame.SRCALPHA)
        frames_right = [fallback]
        frames_left = [fallback]

    return frames_right, frames_left
