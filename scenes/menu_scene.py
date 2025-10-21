# scenes/menu_scene.py

import pygame
from scenes.base_scene import Scene
from state import GameState
from screens import TitleScreen

class MenuScene(Scene):
    """Main menu scene."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self.title_screen = TitleScreen(self.window)

    def on_enter(self) -> None:
        """Called when entering the menu."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle menu input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.change_scene(GameState.INTRO)
            elif event.key == pygame.K_h:
                self.game.change_scene(GameState.HELP)
            elif event.key == pygame.K_q:
                self.game.running = False

    def update(self, dt: float) -> None:
        """Update menu (nothing to do)."""
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Render the menu."""
        self.title_screen.draw()
