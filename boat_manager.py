# boat_manager.py

from __future__ import annotations
import pygame
import random
import logging
from typing import TYPE_CHECKING

from config import Config
from sound_manager import sound_manager
from resource_path import get_resource_path

if TYPE_CHECKING:
    from game import Game

logger = logging.getLogger(__name__)

def create_boat_frames() -> list[pygame.Surface]:
    """
    Loads and returns a list of boat frames from the config.
    Returns a list of loaded/missing frames (with fallback if none found).
    """
    frames = []
    for frame_key in ["frame_0", "frame_1"]:
        path = Config.get_sprite_path("boats", frame_key)
        if path:
            try:
                # Use resource_path helper for PyInstaller compatibility
                resource_file = get_resource_path(path)
                boat_img = pygame.image.load(resource_file).convert_alpha()
                boat_img = pygame.transform.scale(
                    boat_img,
                    (Config.TILE_SIZE * Config.BOAT_SIZE_FACTOR,
                     Config.TILE_SIZE * Config.BOAT_SIZE_FACTOR)
                )
                frames.append(boat_img)
            except pygame.error as e:
                logger.warning(f"Could not load boat sprite '{frame_key}' at '{path}': {e}")
        else:
            logger.warning(f"Boat sprite key '{frame_key}' not found in config.")

    # Provide a fallback frame if none were loaded
    if not frames:
        fallback = pygame.Surface((64, 64), pygame.SRCALPHA)
        frames = [fallback]
        logger.info("No boat frames loaded; using fallback surface.")

    return frames

def place_boat(game: Game) -> None:
    """
    Find a coastal tile and place the boat there. If no coast is found,
    place the boat on a random non-water tile.
    """
    logger.info("Placing boat on the map...")
    coast_tiles = []
    for y in range(Config.MAP_HEIGHT):
        for x in range(Config.MAP_WIDTH):
            if game.game_map[y][x] != 3:  # not water
                adjacent_water = False
                for ny in [y-1, y, y+1]:
                    for nx in [x-1, x, x+1]:
                        if 0 <= nx < Config.MAP_WIDTH and 0 <= ny < Config.MAP_HEIGHT:
                            if game.game_map[ny][nx] == 3:
                                adjacent_water = True
                                break
                    if adjacent_water:
                        break
                if adjacent_water:
                    coast_tiles.append((x, y))

    if coast_tiles:
        x, y = random.choice(coast_tiles)
        game.boat_x, game.boat_y = x, y
    else:
        logger.warning("No coastal tile found; placing boat randomly on land.")
        while True:
            x = random.randint(0, Config.MAP_WIDTH - 1)
            y = random.randint(0, Config.MAP_HEIGHT - 1)
            if game.game_map[y][x] != 3:
                game.boat_x, game.boat_y = x, y
                break

    sound_manager.play("environment", "boat_arrives")
    logger.info(f"Boat placed at ({game.boat_x}, {game.boat_y}).")
