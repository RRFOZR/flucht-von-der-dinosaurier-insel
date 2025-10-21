# engine/resource_preloader.py

import pygame
from typing import Dict, List, Callable, Optional, Any
from pathlib import Path
import logging
from threading import Thread
from queue import Queue

logger = logging.getLogger(__name__)


class ResourcePreloader:
    """
    Asynchronous resource preloader with loading screen.
    Loads images, sounds, fonts, and other resources.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize resource preloader.

        Args:
            screen: Pygame screen surface for loading screen
        """
        self.screen = screen
        self.resources: Dict[str, Any] = {}
        self.load_queue: List[tuple] = []
        self.total_resources = 0
        self.loaded_resources = 0
        self.current_resource = ""
        self.loading_complete = False
        self.loading_error: Optional[str] = None

        # Loading screen customization
        self.bg_color = (20, 20, 30)
        self.bar_color = (50, 150, 250)
        self.text_color = (255, 255, 255)
        self.bar_bg_color = (50, 50, 60)

    def queue_image(self, name: str, filepath: str, convert_alpha: bool = True) -> None:
        """
        Queue an image for loading.

        Args:
            name: Resource identifier
            filepath: Path to image file
            convert_alpha: Whether to convert with alpha channel
        """
        self.load_queue.append(("image", name, filepath, {"convert_alpha": convert_alpha}))

    def queue_sound(self, name: str, filepath: str) -> None:
        """
        Queue a sound for loading.

        Args:
            name: Resource identifier
            filepath: Path to sound file
        """
        self.load_queue.append(("sound", name, filepath, {}))

    def queue_font(self, name: str, filepath: str, size: int = 24) -> None:
        """
        Queue a font for loading.

        Args:
            name: Resource identifier
            filepath: Path to font file
            size: Font size
        """
        self.load_queue.append(("font", name, filepath, {"size": size}))

    def queue_spritesheet(
        self,
        name: str,
        filepath: str,
        frame_width: int,
        frame_height: int,
        num_frames: int
    ) -> None:
        """
        Queue a spritesheet for loading.

        Args:
            name: Resource identifier
            filepath: Path to spritesheet file
            frame_width: Width of each frame
            frame_height: Height of each frame
            num_frames: Number of frames in the sheet
        """
        self.load_queue.append((
            "spritesheet",
            name,
            filepath,
            {
                "frame_width": frame_width,
                "frame_height": frame_height,
                "num_frames": num_frames
            }
        ))

    def load_all(self, threaded: bool = False) -> None:
        """
        Load all queued resources.

        Args:
            threaded: Whether to load in a background thread (experimental)
        """
        self.total_resources = len(self.load_queue)
        self.loaded_resources = 0
        self.loading_complete = False
        self.loading_error = None

        if threaded:
            self._load_threaded()
        else:
            self._load_sync()

    def _load_sync(self) -> None:
        """Load resources synchronously with loading screen updates."""
        clock = pygame.time.Clock()

        for resource_type, name, filepath, params in self.load_queue:
            self.current_resource = f"Loading {name}..."

            # Render loading screen
            self._render_loading_screen()
            pygame.display.flip()

            # Load the resource
            try:
                if resource_type == "image":
                    self._load_image(name, filepath, params)
                elif resource_type == "sound":
                    self._load_sound(name, filepath, params)
                elif resource_type == "font":
                    self._load_font(name, filepath, params)
                elif resource_type == "spritesheet":
                    self._load_spritesheet(name, filepath, params)

                self.loaded_resources += 1

            except Exception as e:
                logger.error(f"Failed to load {name}: {e}")
                self.loading_error = f"Failed to load {name}"

            # Handle events to keep window responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            clock.tick(60)

        self.loading_complete = True
        self.current_resource = "Complete!"
        self._render_loading_screen()
        pygame.display.flip()
        pygame.time.wait(500)  # Brief pause to show completion

    def _load_threaded(self) -> None:
        """Load resources in a background thread (experimental)."""
        def load_worker():
            for resource_type, name, filepath, params in self.load_queue:
                self.current_resource = f"Loading {name}..."
                try:
                    if resource_type == "image":
                        self._load_image(name, filepath, params)
                    elif resource_type == "sound":
                        self._load_sound(name, filepath, params)
                    elif resource_type == "font":
                        self._load_font(name, filepath, params)
                    elif resource_type == "spritesheet":
                        self._load_spritesheet(name, filepath, params)

                    self.loaded_resources += 1
                except Exception as e:
                    logger.error(f"Failed to load {name}: {e}")
                    self.loading_error = f"Failed to load {name}"

            self.loading_complete = True

        thread = Thread(target=load_worker, daemon=True)
        thread.start()

        # Render loading screen until complete
        clock = pygame.time.Clock()
        while not self.loading_complete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self._render_loading_screen()
            pygame.display.flip()
            clock.tick(60)

    def _load_image(self, name: str, filepath: str, params: dict) -> None:
        """Load an image file."""
        image = pygame.image.load(filepath)
        if params.get("convert_alpha", True):
            image = image.convert_alpha()
        else:
            image = image.convert()
        self.resources[name] = image

    def _load_sound(self, name: str, filepath: str, params: dict) -> None:
        """Load a sound file."""
        sound = pygame.mixer.Sound(filepath)
        self.resources[name] = sound

    def _load_font(self, name: str, filepath: str, params: dict) -> None:
        """Load a font file."""
        size = params.get("size", 24)
        font = pygame.font.Font(filepath, size)
        self.resources[name] = font

    def _load_spritesheet(self, name: str, filepath: str, params: dict) -> None:
        """Load a spritesheet and split into frames."""
        sheet = pygame.image.load(filepath).convert_alpha()
        frame_width = params["frame_width"]
        frame_height = params["frame_height"]
        num_frames = params["num_frames"]

        frames = []
        for i in range(num_frames):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            x = (i * frame_width) % sheet.get_width()
            y = (i * frame_width) // sheet.get_width() * frame_height
            frame.blit(sheet, (0, 0), (x, y, frame_width, frame_height))
            frames.append(frame)

        self.resources[name] = frames

    def _render_loading_screen(self) -> None:
        """Render the loading screen."""
        self.screen.fill(self.bg_color)

        # Calculate progress
        progress = self.loaded_resources / max(1, self.total_resources)

        # Title
        font_large = pygame.font.Font(None, 72)
        title = font_large.render("Loading", True, self.text_color)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(title, title_rect)

        # Progress bar
        bar_width = 600
        bar_height = 40
        bar_x = (self.screen.get_width() - bar_width) // 2
        bar_y = 300

        # Background bar
        pygame.draw.rect(self.screen, self.bar_bg_color, (bar_x, bar_y, bar_width, bar_height), border_radius=10)

        # Progress bar
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            pygame.draw.rect(
                self.screen,
                self.bar_color,
                (bar_x, bar_y, progress_width, bar_height),
                border_radius=10
            )

        # Border
        pygame.draw.rect(self.screen, self.text_color, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=10)

        # Progress text
        font_small = pygame.font.Font(None, 36)
        progress_text = font_small.render(
            f"{self.loaded_resources} / {self.total_resources}",
            True,
            self.text_color
        )
        progress_rect = progress_text.get_rect(center=(self.screen.get_width() // 2, bar_y + bar_height + 40))
        self.screen.blit(progress_text, progress_rect)

        # Current resource text
        resource_text = font_small.render(self.current_resource, True, self.text_color)
        resource_rect = resource_text.get_rect(center=(self.screen.get_width() // 2, bar_y + bar_height + 90))
        self.screen.blit(resource_text, resource_rect)

        # Error message (if any)
        if self.loading_error:
            error_font = pygame.font.Font(None, 28)
            error_text = error_font.render(self.loading_error, True, (255, 100, 100))
            error_rect = error_text.get_rect(center=(self.screen.get_width() // 2, bar_y + bar_height + 140))
            self.screen.blit(error_text, error_rect)

    def get_resource(self, name: str) -> Optional[Any]:
        """
        Get a loaded resource.

        Args:
            name: Resource identifier

        Returns:
            The resource or None if not found
        """
        return self.resources.get(name)

    def is_complete(self) -> bool:
        """Check if loading is complete."""
        return self.loading_complete

    def clear(self) -> None:
        """Clear all loaded resources."""
        self.resources.clear()
        self.load_queue.clear()
        self.total_resources = 0
        self.loaded_resources = 0
        self.loading_complete = False
