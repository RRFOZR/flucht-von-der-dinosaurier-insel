# scenes/help_scene.py

import pygame
from scenes.base_scene import Scene
from state import GameState
from screens import HelpScreen

class HelpScene(Scene):
    """Help/instructions scene."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self.help_screen = HelpScreen(self.window)

    def on_enter(self) -> None:
        """Called when entering help."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle help input - any key returns to menu."""
        if event.type == pygame.KEYDOWN:
            self.game.change_scene(GameState.MAIN_MENU)

    def update(self, dt: float) -> None:
        """Update help (nothing to do)."""
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Render the help screen."""
        self.help_screen.draw()
