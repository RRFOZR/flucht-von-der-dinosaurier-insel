# scenes/base_scene.py

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

class Scene:
    """
    Base class for all game scenes.
    Provides lifecycle methods for scene management.
    """

    def __init__(self, game: 'Game') -> None:
        """
        Initialize the scene.

        Args:
            game: Reference to the main Game instance
        """
        self.game = game
        self.window = game.window

    def on_enter(self) -> None:
        """Called when the scene becomes active."""
        pass

    def on_exit(self) -> None:
        """Called when the scene is about to be deactivated."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle a single pygame event.

        Args:
            event: The pygame event to handle
        """
        pass

    def update(self, dt: float) -> None:
        """
        Update scene logic.

        Args:
            dt: Delta time in seconds since last update
        """
        pass

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the scene.

        Args:
            surface: The surface to render to
        """
        pass
