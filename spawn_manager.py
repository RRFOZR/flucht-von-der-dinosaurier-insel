# spawn_manager.py

from __future__ import annotations
import random
import logging
from typing import TYPE_CHECKING

from config import Config
from entities import Dinosaur, Item
from utils import is_passable, get_random_passable_tile

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    # Only imported at type-check time, avoids runtime circular import
    from game import Game

def spawn_items(game: Game, count: int = 6) -> None:
    """
    Spawn items distributed across the map (not just center).
    Items spawn in a wider area to encourage exploration.
    """
    spawned = 0
    attempts = 0
    max_attempts = count * 10  # Prevent infinite loops

    while spawned < count and attempts < max_attempts:
        attempts += 1
        t = random.choice(["potion", "repellent"])

        # Spawn in wider areas - full map coverage
        rx = random.randint(Config.MAP_WIDTH // 4, 3 * Config.MAP_WIDTH // 4)
        ry = random.randint(Config.MAP_HEIGHT // 4, 3 * Config.MAP_HEIGHT // 4)

        if 0 <= rx < Config.MAP_WIDTH and 0 <= ry < Config.MAP_HEIGHT:
            if is_passable(rx, ry, game.game_map):
                # Check that no item is already too close (min 5 tiles apart)
                too_close = any(
                    abs(item.x - rx) < 5 and abs(item.y - ry) < 5
                    for item in game.items
                )
                if not too_close:
                    game.items.append(Item(rx, ry, t))
                    spawned += 1

    logger.info(f"Spawned {spawned} items across the map (requested {count})")

def spawn_dinosaurs(game: Game, n_normal: int, n_aggressive: int) -> None:
    """
    Spawn normal and aggressive dinosaurs.
    """
    for _ in range(n_normal):
        x, y = get_random_passable_tile(game.game_map, for_dino=True)
        game.dinosaurs.append(Dinosaur(x, y, aggressive=False))

    for _ in range(n_aggressive):
        x, y = get_random_passable_tile(game.game_map, for_dino=True)
        game.dinosaurs.append(Dinosaur(x, y, aggressive=True))

    logger.info(f"Spawned {n_normal} normal and {n_aggressive} aggressive dinosaurs.")

def spawn_lava(game: Game, count: int = 8, radius: int = 30) -> list[tuple[int, int]]:
    """
    Spawn lava near the center of the map, damaging the player on contact.
    """
    cx = Config.MAP_WIDTH // 2
    cy = Config.MAP_HEIGHT // 2
    lava_positions = []
    for _ in range(count):
        rx = cx + random.randint(-radius, radius)
        ry = cy + random.randint(-radius, radius)
        if 0 <= rx < Config.MAP_WIDTH and 0 <= ry < Config.MAP_HEIGHT:
            # Only spawn on passable tiles
            if Config.BIOMES[game.game_map[ry][rx]]["passable"]:
                lava_positions.append((rx, ry))
    logger.info(f"Lava spawned at positions: {lava_positions}")
    return lava_positions
