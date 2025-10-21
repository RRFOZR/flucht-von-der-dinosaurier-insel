# game.py

import pygame
import sys
import time
import logging

from config import Config
from state import GameState
from map_gen import generate_island_map
from entities import Player
from hud import HUD
from sound_manager import sound_manager
import boat_manager

# Import all scenes
from scenes import (
    MenuScene, IntroScene, HelpScene, PauseScene,
    GameOverScene, WinScene, PlayingScene
)

# Import delta smoother for better frame pacing
from engine import DeltaSmoother

logger = logging.getLogger(__name__)

class Game:
    """
    Main game class using the modernized engine architecture.
    Now uses scene management, improved delta time, and modular systems.
    """

    def __init__(self) -> None:
        """Initialize the game with all systems."""
        pygame.init()
        self.window = pygame.display.set_mode((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
        pygame.display.set_caption("Flucht von der Dinosaurier Insel")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)

        self.running = True

        # Delta time management with smoothing
        self.dt = 0
        self.accumulator = 0
        self.fixed_dt = 1 / 60.0  # Fixed physics timestep (60 FPS)
        self.delta_smoother = DeltaSmoother(sample_size=10)  # Smooth frame times

        # Game state and data (will be set by reset_game)
        self.game_map = None
        self.player = None
        self.hud = None
        self.items = []
        self.dinosaurs = []
        self.lava_fields = []
        self.last_lava_time = 0

        # Boat
        self.boat_active = False
        self.boat_x = None
        self.boat_y = None
        self.boat_frames = []
        self.boat_current_frame = 0
        self.boat_animation_timer = 0.0
        self.boat_animation_interval = 0.3

        # Initialize all scenes
        self.scenes = {
            GameState.MAIN_MENU: MenuScene(self),
            GameState.INTRO: IntroScene(self),
            GameState.HELP: HelpScene(self),
            GameState.PAUSE: PauseScene(self),
            GameState.GAME_OVER: GameOverScene(self),
            GameState.WON: WinScene(self),
            GameState.PLAYING: PlayingScene(self)
        }

        self.current_scene = self.scenes[GameState.MAIN_MENU]
        self.current_scene.on_enter()

        # Play startup sound
        sound_manager.play("actions", "game_start")

        logger.info("Game initialized with modernized engine")

    def change_scene(self, new_state: GameState) -> None:
        """
        Change to a different game scene.

        Args:
            new_state: The GameState to transition to
        """
        logger.info(f"Changing scene from {type(self.current_scene).__name__} to {new_state.name}")

        # Exit current scene
        if self.current_scene:
            self.current_scene.on_exit()

        # Enter new scene
        self.current_scene = self.scenes[new_state]
        self.current_scene.on_enter()

    def reset_game(self) -> None:
        """
        Reset game state: generate map, create Player, spawn items/dinosaurs.
        Called when starting a new game.
        """
        logger.info("Resetting game state...")

        # Generate map
        self.game_map = generate_island_map()

        # Create player at center
        cx = Config.MAP_WIDTH // 2
        cy = Config.MAP_HEIGHT // 2
        self.player = Player(cx, cy)

        # Create HUD
        self.hud = HUD(self.player, self)

        # Clear entities
        self.items = []
        self.dinosaurs = []

        # Spawn items and dinosaurs
        import spawn_manager
        spawn_manager.spawn_items(self, count=6)
        spawn_manager.spawn_dinosaurs(
            self,
            n_normal=Config.DINOSAUR_COUNT_NORMAL,
            n_aggressive=Config.DINOSAUR_COUNT_AGGRESSIVE
        )

        # Reset boat
        self.boat_active = False
        self.boat_x = None
        self.boat_y = None
        self.boat_frames = boat_manager.create_boat_frames()
        self.boat_current_frame = 0
        self.boat_animation_timer = 0.0

        # Reset lava
        self.lava_fields = []
        self.last_lava_time = time.time()

        # Start background music
        sound_manager.play_music()

        logger.info("Game reset complete")

    def run(self) -> None:
        """
        Main game loop with improved delta time handling.
        Uses a fixed timestep for physics and variable timestep for rendering.
        """
        try:
            while self.running:
                # Get frame time and smooth it
                raw_frame_time = self.clock.tick(Config.FPS) / 1000.0
                frame_time = self.delta_smoother.smooth(raw_frame_time)
                self.accumulator += frame_time

                # Process events
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False
                    else:
                        # Delegate to current scene
                        self.current_scene.handle_event(event)

                # Fixed timestep updates for consistent physics
                while self.accumulator >= self.fixed_dt:
                    self.current_scene.update(self.fixed_dt)
                    self.accumulator -= self.fixed_dt

                # Render
                self.window.fill((30, 30, 30))
                self.current_scene.render(self.window)
                pygame.display.flip()

        except Exception as e:
            logger.error(f"Caught exception in main loop: {e}", exc_info=True)
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources before exiting."""
        logger.info("Cleaning up resources...")

        # Stop all sounds
        pygame.mixer.stop()
        pygame.mixer.music.stop()

        # Quit joystick if it exists
        playing_scene = self.scenes.get(GameState.PLAYING)
        if playing_scene and hasattr(playing_scene, 'joystick_handler') and playing_scene.joystick_handler:
            playing_scene.joystick_handler.quit()

        pygame.quit()
        sys.exit()

    def world_to_screen(self, wx: float, wy: float) -> tuple[int, int]:
        """
        Convert world coords to screen coords.
        Delegates to the playing scene's camera if available.

        Args:
            wx: World x position in tiles
            wy: World y position in tiles

        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        # If we're in the playing scene, use its camera
        if isinstance(self.current_scene, PlayingScene):
            return self.current_scene.camera.world_to_screen(wx, wy)

        # Fallback: simple conversion without camera
        sx = wx * Config.TILE_SIZE
        sy = wy * Config.TILE_SIZE
        return int(sx), int(sy)
