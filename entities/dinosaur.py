# entities/dinosaur.py

from __future__ import annotations  # Enables postponed evaluation of annotations (Python 3.7+)
import math
import random
import pygame
import logging
from config import Config
from entities.base_entity import Entity
from utils import is_passable, direction_towards, load_frames
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player  # Imported only for type checking to avoid circular imports

logger = logging.getLogger(__name__)

class Dinosaur(Entity):
    """
    Dinosaur entity that can chase, idle, or flee.
    """
    IDLE = 0
    CHASE = 1
    FLEE = 2

    def __init__(self, x: float, y: float, aggressive: bool = False) -> None:
        super().__init__(x, y)
        self.aggressive = aggressive
        self.state = Dinosaur.IDLE
        self.just_attacked = False

        sprite_subtype = "aggressive" if self.aggressive else "normal"
        self.frames_right, self.frames_left = load_frames(
            ["idle_0", "idle_1"],
            "entities",
            "dinosaur",
            sprite_subtype
        )

        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_interval = 0.15  # Faster animation for smooth 60 FPS
        self.facing_left = False

    def update(self, player: Player, game_map: list[list[int]], night: bool, dt: float = 1/60.0) -> None:
        """
        Update the dinosaur's state based on the player's position and time of day.

        Args:
            player (Player): The player instance.
            game_map (list[list[int]]): The game map grid.
            night (bool): Whether it's currently night time.
            dt (float): Delta time in seconds since last update.
        """
        dist = math.dist((self.x, self.y), (player.x, player.y))

        if self.just_attacked:
            self.state = Dinosaur.FLEE
        else:
            if self.aggressive:
                sight = Config.DINOSAUR_SIGHT_NIGHT if night else Config.DINOSAUR_SIGHT_DAY
                if dist <= sight and not player.repellent_active:
                    self.state = Dinosaur.CHASE
                else:
                    self.state = Dinosaur.IDLE
            else:
                self.state = Dinosaur.IDLE

        if self.state == Dinosaur.CHASE:
            self._chase(player, game_map)
        elif self.state == Dinosaur.FLEE:
            self._flee(player, game_map)
        else:
            self._idle_move(game_map)

        # Use dt for frame-independent animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_interval:
            self.animation_timer = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.frames_right)

    def get_current_frame(self) -> pygame.Surface:
        """
        Get the current animation frame based on direction.

        Returns:
            pygame.Surface: The current frame image.
        """
        if self.facing_left:
            return self.frames_left[self.current_frame]
        return self.frames_right[self.current_frame]

    def _chase(self, player: Player, game_map: list[list[int]]) -> None:
        """
        Chase the player.

        Args:
            player (Player): The player instance.
            game_map (list[list[int]]): The game map grid.
        """
        dx, dy = direction_towards(self.x, self.y, player.x, player.y)
        nx = self.x + dx * Config.DINOSAUR_SPEED_AGGRESSIVE
        ny = self.y + dy * Config.DINOSAUR_SPEED_AGGRESSIVE
        if is_passable(int(nx), int(ny), game_map, for_dino=True):
            self.x = nx
            self.y = ny
        self.facing_left = (dx < 0)

    def _flee(self, player: Player, game_map: list[list[int]]) -> None:
        """
        Flee from the player.

        Args:
            player (Player): The player instance.
            game_map (list[list[int]]): The game map grid.
        """
        dx, dy = direction_towards(player.x, player.y, self.x, self.y)
        nx = self.x + dx * Config.DINOSAUR_SPEED_AGGRESSIVE
        ny = self.y + dy * Config.DINOSAUR_SPEED_AGGRESSIVE
        if is_passable(int(nx), int(ny), game_map, for_dino=True):
            self.x = nx
            self.y = ny
        self.facing_left = (dx < 0)

        dist2 = math.dist((self.x, self.y), (player.x, player.y))
        if dist2 > Config.DINOSAUR_RUNAWAY_DISTANCE:
            self.just_attacked = False
            self.state = Dinosaur.IDLE

    def _idle_move(self, game_map: list[list[int]]) -> None:
        """
        Perform random movement when idle.

        Args:
            game_map (list[list[int]]): The game map grid.
        """
        if random.random() < Config.DINOSAUR_RANDOM_MOVE_CHANCE:
            direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            nx = self.x + direction[0] * Config.DINOSAUR_SPEED_NORMAL
            ny = self.y + direction[1] * Config.DINOSAUR_SPEED_NORMAL
            if is_passable(int(nx), int(ny), game_map, for_dino=True):
                self.x = nx
                self.y = ny
            self.facing_left = (direction[0] < 0)
