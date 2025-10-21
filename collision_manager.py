# collision_manager.py

from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from config import Config
from sound_manager import sound_manager

# Import event bus for decoupled event handling
try:
    from engine.event_bus import event_bus
    USE_EVENT_BUS = True
except ImportError:
    USE_EVENT_BUS = False

if TYPE_CHECKING:
    from entities import Player, Dinosaur, Item
    from game import Game

logger = logging.getLogger(__name__)

def check_collisions(game: Game) -> None:
    """
    Check collisions for lava, spikes, dinosaurs, and items,
    updating player's health, inventory, or state as needed.
    """
    player = game.player

    # Lava
    if (int(player.x), int(player.y)) in game.lava_fields:
        player.hp -= Config.LAVA_DAMAGE
        sound_manager.play("entities", "player_damage")
        game.hud.trigger_flash((255, 0, 0), 100, 0.2)
        logger.info("Player hit by lava!")

        # Emit event
        if USE_EVENT_BUS:
            event_bus.emit('player_damaged', damage=Config.LAVA_DAMAGE, source='lava')

    # Spikes
    if Config.SPIKES_ENABLED:
        tile_id = game.game_map[int(player.y)][int(player.x)]
        if tile_id == 5:
            player.hp -= Config.SPIKE_DAMAGE
            sound_manager.play("entities", "player_damage")
            game.hud.trigger_flash((255, 0, 0), 100, 0.2)
            logger.info("Player hit by spikes!")

            # Emit event
            if USE_EVENT_BUS:
                event_bus.emit('player_damaged', damage=Config.SPIKE_DAMAGE, source='spikes')

    # Dinosaur collisions
    for dino in game.dinosaurs:
        if int(dino.x) == int(player.x) and int(dino.y) == int(player.y):
            if dino.aggressive and not player.repellent_active:
                player.hp -= Config.DINOSAUR_ATTACK_DAMAGE
                dino.just_attacked = True
                sound_manager.play("entities", "player_damage")
                game.hud.trigger_flash((255, 0, 0), 100, 0.2)
                logger.info("Player attacked by dinosaur!")

                # Emit event
                if USE_EVENT_BUS:
                    event_bus.emit('player_damaged', damage=Config.DINOSAUR_ATTACK_DAMAGE, source='dinosaur')

    # Item pickups
    for it in game.items[:]:
        if int(it.x) == int(player.x) and int(it.y) == int(player.y):
            player.inventory[it.type] += 1
            player.last_item_picked = it.type
            game.items.remove(it)
            player.score += 10
            it.on_pickup()
            sound_manager.play("actions", "potion_pickup")
            game.hud.trigger_flash((0, 255, 0), 100, 0.2)
            logger.info(f"Player picked up a {it.type} at ({it.x}, {it.y}).")

            # Emit event
            if USE_EVENT_BUS:
                event_bus.emit('item_picked_up', item_type=it.type, x=it.x, y=it.y)
