# sound_manager.py

import pygame
import random
import logging
from config import Config
from resource_path import get_resource_path

logger = logging.getLogger(__name__)

class SoundManager:
    """
    Manages sound effects and background music using pygame.mixer.
    """

    def __init__(self) -> None:
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
                logger.info("Pygame mixer initialized successfully.")
            except pygame.error as e:
                logger.error(f"Failed to initialize Pygame mixer: {e}")

        self.sounds = {}
        self.background_music_tracks = []
        self.music_on = True
        self.current_music = None
        self._load_sounds()

    def _load_sounds(self) -> None:
        for category, sounds_dict in Config.SOUNDS.items():
            self.sounds[category] = {}
            for name, path in sounds_dict.items():
                if category == "environment" and name == "background_music":
                    # Background music is a list of paths
                    self.background_music_tracks = [get_resource_path(p) for p in path]
                    continue
                try:
                    # Use resource_path helper for PyInstaller compatibility
                    resource_file = get_resource_path(path)
                    snd = pygame.mixer.Sound(resource_file)
                    volume = Config.SOUND_VOLUMES.get(name, Config.DEFAULT_SOUND_VOLUME)
                    snd.set_volume(volume)
                    self.sounds[category][name] = snd
                except pygame.error as e:
                    logger.warning(f"Could not load sound '{name}' from '{path}': {e}")
                    self.sounds[category][name] = None

        if not self.background_music_tracks:
            logger.info("No background music tracks found.")

    def play(self, category: str, name: str, loops: int = 0) -> None:
        sfx = self.sounds.get(category, {}).get(name, None)
        if sfx:
            sfx.play(loops=loops)
        else:
            logger.warning(f"Sound '{name}' in category '{category}' not found or invalid.")

    def play_music(self) -> None:
        if not self.music_on or not self.background_music_tracks:
            return
        selected_music = random.choice(self.background_music_tracks)
        try:
            pygame.mixer.music.load(selected_music)
            pygame.mixer.music.set_volume(Config.DEFAULT_SOUND_VOLUME)
            pygame.mixer.music.play(-1)
            self.current_music = selected_music
            logger.info(f"Playing background music: {selected_music}")
        except pygame.error as e:
            logger.warning(f"Could not load background music '{selected_music}': {e}")

    def toggle_music(self) -> None:
        if self.music_on:
            pygame.mixer.music.pause()
            self.music_on = False
            logger.info("Background music paused.")
        else:
            pygame.mixer.music.unpause()
            self.music_on = True
            logger.info("Background music resumed.")

    def stop_music(self) -> None:
        pygame.mixer.music.stop()
        self.music_on = False
        logger.info("Background music stopped.")

    def is_music_on(self) -> bool:
        return self.music_on

    def set_sound_volume(self, category: str, name: str, volume: float) -> None:
        volume = max(0.0, min(1.0, volume))
        sfx = self.sounds.get(category, {}).get(name, None)
        if sfx:
            sfx.set_volume(volume)
            Config.SOUND_VOLUMES[name] = volume
        else:
            logger.warning(f"Sound '{name}' in category '{category}' not found.")

    def set_music_volume(self, volume: float) -> None:
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)
        Config.DEFAULT_SOUND_VOLUME = volume
        logger.info(f"Background music volume set to {volume}.")

sound_manager = SoundManager()
