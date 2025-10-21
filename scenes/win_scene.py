# scenes/win_scene.py

import pygame
from scenes.base_scene import Scene
from state import GameState
from screens import WinScreen

class WinScene(Scene):
    """Victory / win scene."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self.win_screen = WinScreen(self.window)

    def on_enter(self) -> None:
        """Called when entering win scene."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle win screen input - ENTER returns to menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.change_scene(GameState.MAIN_MENU)

    def update(self, dt: float) -> None:
        """Update win screen (nothing to do)."""
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Render the win screen."""
        self.win_screen.draw()
