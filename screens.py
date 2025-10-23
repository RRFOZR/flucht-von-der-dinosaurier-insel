# screens.py

from __future__ import annotations
import pygame
import logging
from config import Config
from state import GameState
from sound_manager import sound_manager
from resource_path import get_resource_path

logger = logging.getLogger(__name__)

class BaseScreen:
    """
    Generic base class for menu/pause/help/intro/win/lose screens.
    """
    def __init__(self, screen_key: str, text_key: str, window: pygame.Surface) -> None:
        self.window = window
        self.text_lines = Config.TEXTS.get(text_key, [])
        self.font_title = pygame.font.SysFont("Arial", 40)
        self.font_text = pygame.font.SysFont("Arial", 24)

        image_path = Config.get_screen_image(screen_key)
        self.image = None
        if image_path:
            try:
                # Use resource_path helper for PyInstaller compatibility
                resource_file = get_resource_path(image_path)
                loaded = pygame.image.load(resource_file).convert_alpha()
                self.image = self.scale_image(loaded, Config.WINDOW_WIDTH * 0.9, Config.WINDOW_HEIGHT * 0.4)
            except pygame.error as e:
                logger.warning(f"Could not load background image '{screen_key}': {e}")

    def scale_image(self, image: pygame.Surface, max_width: float, max_height: float) -> pygame.Surface:
        w, h = image.get_size()
        ratio = min(max_width / w, max_height / h)
        new_size = (int(w * ratio), int(h * ratio))
        return pygame.transform.scale(image, new_size)

    def draw(self) -> None:
        self.window.fill((30, 30, 30))
        if self.image:
            rect = self.image.get_rect()
            rect.centerx = Config.WINDOW_WIDTH // 2
            rect.top = 80
            self.window.blit(self.image, rect)

        y_start = 80 + (self.image.get_height() if self.image else 0) + 40
        for idx, line in enumerate(self.text_lines):
            if idx == 0 and len(self.text_lines) > 1:
                txt_surf = self.font_title.render(line, True, (255, 215, 0))
            else:
                txt_surf = self.font_text.render(line, True, (255, 255, 255))
            x_pos = Config.WINDOW_WIDTH // 2 - txt_surf.get_width() // 2
            self.window.blit(txt_surf, (x_pos, y_start))
            y_start += txt_surf.get_height() + 15

    def handle_event(self, event: pygame.event.Event, game: 'Game') -> None:
        pass


class TitleScreen(BaseScreen):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__("title", "MAIN_MENU", window)


class IntroScreen(BaseScreen):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__("begin", "INTRO_SCREEN", window)


class HelpScreen(BaseScreen):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__("help", "HELP_SCREEN", window)


class PauseScreen(BaseScreen):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__("pause", "PAUSE_SCREEN", window)

    def handle_event(self, event: pygame.event.Event, game: 'Game') -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.state = GameState.PLAYING
            elif event.key == pygame.K_h:
                game.state = GameState.HELP
            elif event.key == pygame.K_q:
                game.running = False
            elif event.key == pygame.K_m:
                sound_manager.toggle_music()


class LoseScreen(BaseScreen):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__("lose", "LOSE_SCREEN", window)


class WinScreen(BaseScreen):
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__("win", "WIN_SCREEN", window)
