# scenes/intro_scene.py

import pygame
from scenes.base_scene import Scene
from state import GameState
from screens import IntroScreen

class IntroScene(Scene):
    """Intro story scene."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self.intro_screen = IntroScreen(self.window)

    def on_enter(self) -> None:
        """Called when entering the intro."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle intro input - any key starts the game."""
        if event.type == pygame.KEYDOWN:
            self.game.reset_game()
            self.game.change_scene(GameState.PLAYING)

    def update(self, dt: float) -> None:
        """Update intro (nothing to do)."""
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Render the intro."""
        self.intro_screen.draw()
