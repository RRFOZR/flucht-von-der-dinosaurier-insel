# hud.py

from __future__ import annotations
import pygame
import logging
from config import Config
from entities import Player
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

logger = logging.getLogger(__name__)

class HUD:
    """
    Renders in-game HUD elements: health bar, score, inventory, etc.
    """
    def __init__(self, player: Player, game: Game) -> None:
        self.player = player
        self.game = game
        self.font = pygame.font.SysFont("Arial", 20)
        self.health_bar_position = (20, 40)
        self.health_bar_size = (200, 25)
        self.score_position = (20, Config.WINDOW_HEIGHT - 60)
        self.inventory_position = (Config.WINDOW_WIDTH - 150, Config.WINDOW_HEIGHT - 100)
        self.screen_flash = None
        self.flash_timer = 0.0

        # Load small item icons
        self.item_sprites = {}
        for item_type in ["potion", "repellent"]:
            path = Config.get_sprite_path("items", item_type)
            if path:
                try:
                    sprite = pygame.image.load(path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, (32, 32))
                    self.item_sprites[item_type] = sprite
                except pygame.error as e:
                    logger.warning(f"Could not load HUD sprite '{item_type}' from '{path}': {e}")
                    self.item_sprites[item_type] = None
            else:
                self.item_sprites[item_type] = None

        # Minimap caching for performance
        self.minimap_size = (200, 150)
        self.minimap_pos = (Config.WINDOW_WIDTH - self.minimap_size[0] - 10, 10)
        self.minimap_terrain_cache = None
        self.minimap_needs_refresh = True

    def update(self, dt: float) -> None:
        if self.screen_flash:
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                self.screen_flash = None

    def draw(self, surface: pygame.Surface) -> None:
        self.draw_health_bar(surface)
        self.draw_score(surface)
        self.draw_inventory(surface)
        self.draw_status_effects(surface)
        self.draw_flash(surface)
        self.draw_minimap()

    def draw_health_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255, 0, 0), (*self.health_bar_position, *self.health_bar_size))
        ratio = max(0, min(1, self.player.hp / Config.PLAYER_MAX_HP))
        green_width = self.health_bar_size[0] * ratio
        pygame.draw.rect(surface, (0, 255, 0),
                         (self.health_bar_position[0], self.health_bar_position[1],
                          green_width, self.health_bar_size[1]))
        text = self.font.render(f"HP: {self.player.hp}/{Config.PLAYER_MAX_HP}", True, (255, 255, 255))
        surface.blit(text, (self.health_bar_position[0], self.health_bar_position[1] - 25))

    def draw_score(self, surface: pygame.Surface) -> None:
        score_txt = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        surface.blit(score_txt, self.score_position)

    def draw_inventory(self, surface: pygame.Surface) -> None:
        x, y = self.inventory_position
        for item_type, sprite in self.item_sprites.items():
            if sprite:
                surface.blit(sprite, (x, y))
            count = self.player.inventory.get(item_type, 0)
            count_txt = self.font.render(f"x{count}", True, (255, 255, 255))
            surface.blit(count_txt, (x + 40, y + 5))
            y += 50

    def draw_status_effects(self, surface: pygame.Surface) -> None:
        if self.player.repellent_active:
            player_screen_pos = self.game.world_to_screen(self.player.x, self.player.y)
            pygame.draw.circle(surface, (0, 0, 255), player_screen_pos, 50, 5)

    def draw_flash(self, surface: pygame.Surface) -> None:
        if self.screen_flash:
            color, alpha, _ = self.screen_flash
            overlay = pygame.Surface((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((*color, alpha))
            surface.blit(overlay, (0, 0))

    def trigger_flash(self, color: tuple[int, int, int], alpha: int, duration: float) -> None:
        self.screen_flash = (color, alpha, duration)
        self.flash_timer = duration

    def _refresh_minimap_terrain(self) -> None:
        """Render the minimap terrain (static tiles) to cache."""
        mw, mh = self.minimap_size
        mapw, maph = Config.MAP_WIDTH, Config.MAP_HEIGHT

        # Create cached surface if needed
        if self.minimap_terrain_cache is None:
            self.minimap_terrain_cache = pygame.Surface(self.minimap_size)

        # Background
        self.minimap_terrain_cache.fill((50, 50, 50))

        # Draw all terrain tiles (only needs to be done once!)
        for my in range(mh):
            row = int(my / mh * maph)
            for mx in range(mw):
                col = int(mx / mw * mapw)
                tile = self.game.game_map[row][col]
                c = Config.BIOMES[tile]["color"]
                self.minimap_terrain_cache.set_at((mx, my), c)

        self.minimap_needs_refresh = False

    def draw_minimap(self) -> None:
        """Draw the minimap with cached terrain and dynamic entities."""
        mw, mh = self.minimap_size
        mmx, mmy = self.minimap_pos
        mapw, maph = Config.MAP_WIDTH, Config.MAP_HEIGHT

        # Refresh terrain cache if needed (only on first call or map change)
        if self.minimap_needs_refresh or self.minimap_terrain_cache is None:
            self._refresh_minimap_terrain()

        # Blit cached terrain
        self.game.window.blit(self.minimap_terrain_cache, (mmx, mmy))

        # Draw lava fields (dynamic)
        for lx, ly in self.game.lava_fields:
            mx = int(lx / mapw * mw)
            my = int(ly / maph * mh)
            if 0 <= mx < mw and 0 <= my < mh:
                self.game.window.set_at((mmx + mx, mmy + my), (255, 0, 0))

        # Draw player (dynamic)
        px = int(self.player.x / mapw * mw)
        py = int(self.player.y / maph * mh)
        pygame.draw.rect(self.game.window, (0, 0, 255),
                        (mmx + px - 1, mmy + py - 1, 3, 3))

        # Draw dinosaurs (dynamic)
        for dino in self.game.dinosaurs:
            dx = int(dino.x / mapw * mw)
            dy = int(dino.y / maph * mh)
            color = (255, 0, 0) if dino.aggressive else (0, 255, 0)
            pygame.draw.rect(self.game.window, color,
                           (mmx + dx - 1, mmy + dy - 1, 2, 2))
