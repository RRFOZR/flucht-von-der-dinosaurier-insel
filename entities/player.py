# entities/player.py

import pygame
import logging
from config import Config
from entities.base_entity import Entity
from utils import is_passable, load_frames
from sound_manager import sound_manager

logger = logging.getLogger(__name__)

class Player(Entity):
    """
    Player entity with health, inventory, repellent logic, and audio handling.
    """
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.hp = Config.PLAYER_MAX_HP
        self.score = 0
        self.inventory = {"potion": 0, "repellent": 0}
        self.repellent_active = False
        self.repellent_timer = 0.0
        self.last_item_picked = None

        # Load frames
        self.frames_right, self.frames_left = load_frames(["idle_0", "idle_1"], "entities", "player")

        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_interval = 0.15  # Faster animation for smooth 60 FPS
        self.facing_left = False

        # Footstep audio
        self.footstep_sound = sound_manager.sounds["entities"].get("player_move_soft", None)
        self.footstep_channel = pygame.mixer.Channel(1)
        self.is_moving = False

    def move(self, dx: float, dy: float, game_map: list[list[int]]) -> None:
        nx = self.x + dx
        ny = self.y + dy
        if is_passable(int(nx), int(ny), game_map):
            tile_id = game_map[int(ny)][int(nx)]
            factor = 1.0
            if tile_id == 4:  # Mud
                factor = 0.5
            self.x += dx * factor
            self.y += dy * factor

        if dx < 0:
            self.facing_left = True
        elif dx > 0:
            self.facing_left = False

        if dx != 0 or dy != 0:
            if not self.is_moving and self.footstep_sound:
                self.is_moving = True
                if not self.footstep_channel.get_busy():
                    self.footstep_channel.play(self.footstep_sound, loops=-1)
        else:
            if self.is_moving:
                self.is_moving = False
                if self.footstep_channel.get_busy():
                    self.footstep_channel.stop()

    def update(self, dt: float) -> None:
        if self.repellent_active:
            self.repellent_timer -= dt
            if self.repellent_timer <= 0:
                self.repellent_active = False
                sound_manager.play("actions", "repellent_trigger")

        self.animation_timer += dt
        if self.animation_timer >= self.animation_interval:
            self.animation_timer = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.frames_right)

    def get_current_frame(self) -> pygame.Surface:
        if self.facing_left:
            return self.frames_left[self.current_frame]
        return self.frames_right[self.current_frame]

    def trigger_repellent(self) -> None:
        if self.inventory["repellent"] > 0:
            self.inventory["repellent"] -= 1
            self.repellent_active = True
            self.repellent_timer = Config.REPELLENT_DURATION
            logger.info("Repellent activated.")
            sound_manager.play("entities", "repellent_trigger")

    def use_potion(self) -> None:
        if self.inventory["potion"] > 0 and self.hp < Config.PLAYER_MAX_HP:
            self.inventory["potion"] -= 1
            self.hp = min(Config.PLAYER_MAX_HP, self.hp + Config.POTION_HEAL)
            logger.info("Potion used.")
            sound_manager.play("entities", "potion_use")
