# engine/save_load.py

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class SaveLoadSystem:
    """
    System for saving and loading game state.
    Supports multiple save slots and auto-save.
    """

    def __init__(self, save_dir: str = "saves") -> None:
        """
        Initialize save/load system.

        Args:
            save_dir: Directory to store save files
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.current_slot = 0
        self.auto_save_enabled = True
        self.auto_save_interval = 60.0  # Auto-save every 60 seconds
        self.auto_save_timer = 0.0

    def save_game(self, game_data: Dict[str, Any], slot: int = 0, auto_save: bool = False) -> bool:
        """
        Save game state to a file.

        Args:
            game_data: Dictionary containing all game state
            slot: Save slot number (0-9)
            auto_save: Whether this is an auto-save

        Returns:
            True if save was successful
        """
        try:
            filename = self._get_save_filename(slot, auto_save)
            filepath = self.save_dir / filename

            # Add metadata
            save_data = {
                "version": "1.0",
                "slot": slot,
                "auto_save": auto_save,
                "data": game_data
            }

            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)

            logger.info(f"Game saved to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to save game: {e}")
            return False

    def load_game(self, slot: int = 0, auto_save: bool = False) -> Optional[Dict[str, Any]]:
        """
        Load game state from a file.

        Args:
            slot: Save slot number (0-9)
            auto_save: Whether to load auto-save

        Returns:
            Dictionary containing game state, or None if load failed
        """
        try:
            filename = self._get_save_filename(slot, auto_save)
            filepath = self.save_dir / filename

            if not filepath.exists():
                logger.warning(f"Save file not found: {filepath}")
                return None

            with open(filepath, 'r') as f:
                save_data = json.load(f)

            logger.info(f"Game loaded from {filepath}")
            return save_data.get("data")

        except Exception as e:
            logger.error(f"Failed to load game: {e}")
            return None

    def save_exists(self, slot: int = 0, auto_save: bool = False) -> bool:
        """
        Check if a save file exists.

        Args:
            slot: Save slot number
            auto_save: Whether to check auto-save

        Returns:
            True if save file exists
        """
        filename = self._get_save_filename(slot, auto_save)
        filepath = self.save_dir / filename
        return filepath.exists()

    def delete_save(self, slot: int = 0, auto_save: bool = False) -> bool:
        """
        Delete a save file.

        Args:
            slot: Save slot number
            auto_save: Whether to delete auto-save

        Returns:
            True if deletion was successful
        """
        try:
            filename = self._get_save_filename(slot, auto_save)
            filepath = self.save_dir / filename

            if filepath.exists():
                filepath.unlink()
                logger.info(f"Deleted save file: {filepath}")
                return True

            return False

        except Exception as e:
            logger.error(f"Failed to delete save: {e}")
            return False

    def get_save_info(self, slot: int = 0, auto_save: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get metadata about a save file without loading it.

        Args:
            slot: Save slot number
            auto_save: Whether to check auto-save

        Returns:
            Dictionary with save metadata, or None if not found
        """
        try:
            filename = self._get_save_filename(slot, auto_save)
            filepath = self.save_dir / filename

            if not filepath.exists():
                return None

            stat = filepath.stat()

            # Load just the metadata (not the full game data)
            with open(filepath, 'r') as f:
                save_data = json.load(f)

            return {
                "slot": save_data.get("slot"),
                "version": save_data.get("version"),
                "modified_time": stat.st_mtime,
                "size_bytes": stat.st_size,
                "auto_save": save_data.get("auto_save", False)
            }

        except Exception as e:
            logger.error(f"Failed to get save info: {e}")
            return None

    def list_saves(self) -> list[Dict[str, Any]]:
        """
        List all available save files.

        Returns:
            List of save file metadata
        """
        saves = []

        # Check all possible slots
        for slot in range(10):
            # Regular save
            info = self.get_save_info(slot, auto_save=False)
            if info:
                saves.append(info)

            # Auto-save
            info = self.get_save_info(slot, auto_save=True)
            if info:
                saves.append(info)

        return saves

    def update_auto_save(self, dt: float, game_data: Dict[str, Any]) -> None:
        """
        Update auto-save timer and save if needed.

        Args:
            dt: Delta time in seconds
            game_data: Current game state to save
        """
        if not self.auto_save_enabled:
            return

        self.auto_save_timer += dt
        if self.auto_save_timer >= self.auto_save_interval:
            self.auto_save_timer = 0.0
            self.save_game(game_data, self.current_slot, auto_save=True)

    def _get_save_filename(self, slot: int, auto_save: bool) -> str:
        """
        Generate save filename.

        Args:
            slot: Save slot number
            auto_save: Whether this is an auto-save

        Returns:
            Filename string
        """
        prefix = "auto_" if auto_save else "save_"
        return f"{prefix}slot_{slot}.json"


# Helper functions for serializing game state

def serialize_player(player) -> Dict[str, Any]:
    """
    Serialize player state to dictionary.

    Args:
        player: Player entity

    Returns:
        Serialized player data
    """
    return {
        "x": player.x,
        "y": player.y,
        "hp": player.hp,
        "score": player.score,
        "inventory": player.inventory.copy(),
        "repellent_active": player.repellent_active,
        "repellent_timer": player.repellent_timer
    }


def serialize_dinosaur(dino) -> Dict[str, Any]:
    """
    Serialize dinosaur state to dictionary.

    Args:
        dino: Dinosaur entity

    Returns:
        Serialized dinosaur data
    """
    return {
        "x": dino.x,
        "y": dino.y,
        "aggressive": dino.aggressive,
        "state": dino.state,
        "just_attacked": dino.just_attacked
    }


def serialize_game_state(game) -> Dict[str, Any]:
    """
    Serialize entire game state to dictionary.

    Args:
        game: Game instance

    Returns:
        Serialized game data
    """
    return {
        "player": serialize_player(game.player),
        "dinosaurs": [serialize_dinosaur(d) for d in game.dinosaurs],
        "items": [(item.x, item.y, item.item_type) for item in game.items],
        "game_time": game.game_time if hasattr(game, 'game_time') else 0,
        "boat_active": game.boat_active,
        "boat_position": (game.boat_x, game.boat_y) if game.boat_x else None,
        "map_seed": game.map_generator.seed if hasattr(game, 'map_generator') else 0
    }
