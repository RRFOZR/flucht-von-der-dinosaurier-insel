# scenes/playing_scene.py

import pygame
import time
import logging
from scenes.base_scene import Scene
from state import GameState
from config import Config
from utils import is_night
from sound_manager import sound_manager
from engine import (Camera, SpatialGrid, ParticleSystem, DebugOverlay,
                   Audio3D, PostProcessing, InputBuffer)
import spawn_manager
import collision_manager
import boat_manager

logger = logging.getLogger(__name__)

class PlayingScene(Scene):
    """Main gameplay scene with all game logic and advanced engine features."""

    def __init__(self, game) -> None:
        super().__init__(game)

        # Initialize core engine systems
        self.camera = Camera(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.spatial_grid = SpatialGrid(cell_size=10)
        self.particle_system = ParticleSystem()

        # Advanced engine systems
        self.debug_overlay = DebugOverlay()
        self.audio_3d = Audio3D()
        self.post_processing = PostProcessing(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.input_buffer = InputBuffer(buffer_time=0.15)

        # Configure camera with map bounds
        map_bounds = pygame.Rect(0, 0,
                                 Config.MAP_WIDTH * Config.TILE_SIZE,
                                 Config.MAP_HEIGHT * Config.TILE_SIZE)
        self.camera.set_bounds(map_bounds)

        # Timing
        self.start_time = 0
        self.old_night_state = None

        # Lava warning system
        self.lava_warning_time = 2.0  # Show warnings 2 seconds before lava
        self.showing_lava_warning = False

        # Joystick handler
        self.joystick_handler = None
        if Config.ENABLE_JOYSTICK:
            try:
                from joystick_handler import JoystickHandler
                self.joystick_handler = JoystickHandler()
            except Exception as e:
                logger.warning(f"Failed to initialize joystick handler: {e}")

        # Pre-render tile surfaces for performance
        self.tile_cache = {}
        for tile_id, biome_data in Config.BIOMES.items():
            tile_surf = pygame.Surface((Config.TILE_SIZE, Config.TILE_SIZE))
            tile_surf.fill(biome_data["color"])
            self.tile_cache[tile_id] = tile_surf
        # Add lava tile
        lava_surf = pygame.Surface((Config.TILE_SIZE, Config.TILE_SIZE))
        lava_surf.fill((255, 0, 0))
        self.tile_cache['lava'] = lava_surf
        logger.info(f"Pre-rendered {len(self.tile_cache)} tile surfaces")

    def on_enter(self) -> None:
        """Called when entering playing state."""
        self.start_time = time.time()
        self.old_night_state = None
        self.camera.set_target(self.game.player.x, self.game.player.y)

    def on_exit(self) -> None:
        """Called when exiting playing state."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle gameplay input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene(GameState.PAUSE)
            elif event.key == pygame.K_F3:
                # Toggle debug overlay
                self.debug_overlay.toggle()
            elif event.key == pygame.K_F4:
                # Toggle post-processing effects
                self.post_processing.toggle_vignette()
            elif event.key == pygame.K_SPACE:
                # Use repellent with input buffering
                self.input_buffer.buffer_input("use_repellent")
            elif event.key in (pygame.K_e, pygame.K_RSHIFT):
                # Use potion
                self.input_buffer.buffer_input("use_potion")

    def update(self, dt: float) -> None:
        """Update all gameplay logic."""
        # Update debug metrics
        self.debug_overlay.update(dt)
        self.debug_overlay.set_metric("Entities", len(self.game.dinosaurs) + len(self.game.items) + 1)
        self.debug_overlay.set_metric("Particles", self.particle_system.get_particle_count())
        self.debug_overlay.set_metric("Position", f"({int(self.game.player.x)}, {int(self.game.player.y)})")
        self.debug_overlay.set_metric("Camera Shake", "Yes" if self.camera.is_shaking() else "No")

        # Update audio listener position
        self.audio_3d.set_listener_position(self.game.player.x, self.game.player.y)

        # Update post-processing effects
        self.post_processing.update(dt)

        # Get player input
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])

        # Joystick input
        if Config.ENABLE_JOYSTICK and self.joystick_handler:
            jdx, jdy = self.joystick_handler.get_movement()
            dx += jdx
            dy += jdy

        # Normalize diagonal movement to prevent faster speed
        if dx != 0 and dy != 0:
            # Diagonal movement - normalize to keep same speed
            length = (dx * dx + dy * dy) ** 0.5
            dx /= length
            dy /= length

        # Move player (frame-independent with delta time)
        dx *= Config.PLAYER_SPEED * dt
        dy *= Config.PLAYER_SPEED * dt
        self.game.player.move(dx, dy, self.game.game_map)
        self.game.player.update(dt)

        # Process buffered inputs
        self._process_buffered_inputs()

        # Update HUD
        self.game.hud.update(dt)

        # Day/Night cycle
        now = time.time()
        current_time = now - self.start_time
        night = is_night(current_time)
        if self.old_night_state is None:
            self.old_night_state = night
        elif night != self.old_night_state:
            self.old_night_state = night

        # Lava spawning with warnings
        time_until_lava = Config.LAVA_INTERVAL - (now - self.game.last_lava_time)

        # Show warning particles before lava spawns
        if 0 < time_until_lava <= self.lava_warning_time and not self.showing_lava_warning:
            self.showing_lava_warning = True
            self.game.hud.trigger_flash((255, 100, 0), 80, 0.3)
            logger.info("Lava warning! Eruption imminent!")

        # Spawn lava
        if time_until_lava <= 0:
            lava_list = spawn_manager.spawn_lava(self.game)
            self.game.lava_fields = set(lava_list)  # Convert to set for fast lookups
            self.game.last_lava_time = now
            self.showing_lava_warning = False

            # Camera shake for lava!
            self.camera.shake(intensity=6, duration=0.5, falloff="exponential")

            # Screen flash for dramatic effect
            self.game.hud.trigger_flash((255, 0, 0), 120, 0.4)

            # Emit lava particles at each lava field for visual feedback
            for i, (lx, ly) in enumerate(self.game.lava_fields):
                if i >= 10:  # Limit particles for performance
                    break
                px, py = self.camera.world_to_screen(lx, ly)
                self.particle_system.emit(
                    px + Config.TILE_SIZE // 2,
                    py + Config.TILE_SIZE // 2,
                    count=8,
                    color=(255, 100, 0),
                    speed_range=(20, 50),
                    lifetime_range=(1.0, 2.0),
                    spread_angle=90,
                    direction=-90,
                    gravity=80
                )

        # Build spatial grid for efficient collision detection
        self.spatial_grid.clear()
        for dino in self.game.dinosaurs:
            self.spatial_grid.insert(dino)

        # Update dinosaurs with spatial optimization
        for dino in self.game.dinosaurs:
            dino.update(self.game.player, self.game.game_map, night, dt)

        # Collision detection
        collision_manager.check_collisions(self.game)

        # Update camera to follow player smoothly
        self.camera.set_target(self.game.player.x, self.game.player.y)
        self.camera.update(dt)

        # Update particle system
        self.particle_system.update(dt)

        # Update input buffer
        self.input_buffer.update()

        # Boat arrival
        cycles_passed = int(current_time // Config.CYCLE_LENGTH)
        if (cycles_passed >= Config.BOAT_ARRIVAL_CYCLES) and not self.game.boat_active:
            self.game.boat_active = True
            boat_manager.place_boat(self.game)
            # Big camera shake for boat arrival!
            self.camera.shake(intensity=15, duration=1.2, falloff="exponential")

        # Win condition
        if self.game.boat_active and self.game.boat_x is not None:
            if int(self.game.player.x) == self.game.boat_x and int(self.game.player.y) == self.game.boat_y:
                sound_manager.play("actions", "win_game")
                self.game.change_scene(GameState.WON)

        # Lose condition
        if self.game.player.hp <= 0:
            sound_manager.play("actions", "game_over")
            self.game.change_scene(GameState.GAME_OVER)

        # Boat animation
        if self.game.boat_active:
            self.game.boat_animation_timer += dt
            if self.game.boat_animation_timer >= self.game.boat_animation_interval:
                self.game.boat_animation_timer = 0.0
                self.game.boat_current_frame = (self.game.boat_current_frame + 1) % len(self.game.boat_frames)

    def _process_buffered_inputs(self) -> None:
        """Process buffered inputs for better control feel."""
        # Check for buffered repellent use
        if self.input_buffer.consume_input("use_repellent"):
            if self.game.player.inventory.get("repellent", 0) > 0:
                self.game.player.trigger_repellent()
                self.game.hud.trigger_flash((0, 0, 255), 100, 0.2)
                # Screen shake!
                self.camera.shake(intensity=3, duration=0.2)
                # Emit particle effect
                px, py = self.camera.world_to_screen(self.game.player.x, self.game.player.y)
                self.particle_system.emit(
                    px + Config.TILE_SIZE // 2,
                    py + Config.TILE_SIZE // 2,
                    count=25,
                    color=(0, 0, 255),
                    speed_range=(50, 120),
                    lifetime_range=(0.3, 0.9),
                    spread_angle=360
                )

        # Check for buffered potion use
        if self.input_buffer.consume_input("use_potion"):
            self.game.player.use_potion()
            if self.game.player.inventory.get("potion", 0) >= 0:
                px, py = self.camera.world_to_screen(self.game.player.x, self.game.player.y)
                self.particle_system.emit(
                    px + Config.TILE_SIZE // 2,
                    py + Config.TILE_SIZE // 2,
                    count=20,
                    color=(0, 255, 0),
                    speed_range=(30, 80),
                    lifetime_range=(0.5, 1.2),
                    spread_angle=360,
                    gravity=-30
                )

    def render(self, surface: pygame.Surface) -> None:
        """Render the game world with all effects."""
        # Draw map
        self._draw_map(surface)

        # Draw entities
        self._draw_entities(surface)

        # Draw particles
        self.particle_system.render(surface, self.camera.x, self.camera.y)

        # Draw HUD
        self.game.hud.draw(surface)

        # Night overlay
        now = time.time()
        if is_night(now - self.start_time):
            overlay = pygame.Surface((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill(Config.NIGHT_OVERLAY)
            surface.blit(overlay, (0, 0))

        # Apply post-processing effects
        self.post_processing.apply_all(surface)

        # Draw debug overlay (if enabled)
        self.debug_overlay.render(surface)

    def _draw_map(self, surface: pygame.Surface) -> None:
        """Draw the game map tiles using cached surfaces."""
        start_x, start_y, end_x, end_y = self.camera.get_visible_bounds()

        for ty in range(start_y, end_y):
            for tx in range(start_x, end_x):
                tile_id = self.game.game_map[ty][tx]

                # Use lava tile if this position has lava, otherwise use terrain tile
                if (tx, ty) in self.game.lava_fields:
                    tile_surf = self.tile_cache['lava']
                else:
                    tile_surf = self.tile_cache[tile_id]

                sx, sy = self.camera.world_to_screen(tx, ty)
                surface.blit(tile_surf, (sx, sy))

        # Draw boat
        if self.game.boat_active and self.game.boat_x is not None:
            bx, by = self.game.boat_x, self.game.boat_y
            if start_x <= bx < end_x and start_y <= by < end_y:
                sx, sy = self.camera.world_to_screen(bx, by)
                surface.blit(self.game.boat_frames[self.game.boat_current_frame], (sx, sy))

    def _draw_entities(self, surface: pygame.Surface) -> None:
        """Draw all game entities with optimized culling."""
        # Draw player
        sx, sy = self.camera.world_to_screen(self.game.player.x, self.game.player.y)
        surface.blit(self.game.player.get_current_frame(), (sx, sy))

        # Draw dinosaurs (only those visible on screen)
        start_x, start_y, end_x, end_y = self.camera.get_visible_bounds()
        visible_dinos = self.spatial_grid.query_range(start_x, start_y, end_x, end_y)

        for dino in visible_dinos:
            dsx, dsy = self.camera.world_to_screen(dino.x, dino.y)
            surface.blit(dino.get_current_frame(), (dsx, dsy))

        # Draw items
        for item in self.game.items:
            if start_x <= item.x < end_x and start_y <= item.y < end_y:
                isx, isy = self.camera.world_to_screen(item.x, item.y)
                surface.blit(item.get_current_frame(), (isx, isy))
