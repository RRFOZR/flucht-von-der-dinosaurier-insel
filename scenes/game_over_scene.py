# scenes/game_over_scene.py

import pygame
from scenes.base_scene import Scene
from state import GameState
from screens import LoseScreen

class GameOverScene(Scene):
    """Game over / lose scene."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self.lose_screen = LoseScreen(self.window)

    def on_enter(self) -> None:
        """Called when entering game over."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle game over input - ENTER returns to menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.change_scene(GameState.MAIN_MENU)

    def update(self, dt: float) -> None:
        """Update game over (nothing to do)."""
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Render the game over screen."""
        self.lose_screen.draw()
