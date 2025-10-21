# scenes/pause_scene.py

import pygame
from scenes.base_scene import Scene
from state import GameState
from screens import PauseScreen
from sound_manager import sound_manager

class PauseScene(Scene):
    """Pause menu scene."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self.pause_screen = PauseScreen(self.window)

    def on_enter(self) -> None:
        """Called when entering pause."""
        # Pause the background music
        pygame.mixer.music.pause()

    def on_exit(self) -> None:
        """Called when exiting pause."""
        # Resume the background music
        pygame.mixer.music.unpause()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pause menu input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene(GameState.PLAYING)
            elif event.key == pygame.K_h:
                self.game.change_scene(GameState.HELP)
            elif event.key == pygame.K_m:
                # Toggle music
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                else:
                    sound_manager.play_music()
            elif event.key == pygame.K_q:
                self.game.running = False

    def update(self, dt: float) -> None:
        """Update pause (nothing to do)."""
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Render the pause screen."""
        self.pause_screen.draw()
