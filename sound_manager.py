# sound_manager.py

import pygame
import random
import logging
from config import Config

logger = logging.getLogger(__name__)

class SoundManager:
    """
    Manages sound effects and background music using pygame.mixer.
    Gracefully handles systems without audio devices.
    """

    def __init__(self) -> None:
        self.audio_available = False
        self.sounds = {}
        self.background_music_tracks = []
        self.music_on = True
        self.current_music = None

        # Try to initialize mixer
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
                self.audio_available = True
                logger.info("Pygame mixer initialized successfully.")
            except pygame.error as e:
                logger.warning(f"Audio not available - running in silent mode: {e}")
                self.audio_available = False
        else:
            self.audio_available = True

        # Only load sounds if audio is available
        if self.audio_available:
            self._load_sounds()
        else:
            logger.info("Skipping sound loading - audio system unavailable")

    def _load_sounds(self) -> None:
        for category, sounds_dict in Config.SOUNDS.items():
            self.sounds[category] = {}
            for name, path in sounds_dict.items():
                if category == "environment" and name == "background_music":
                    self.background_music_tracks = path
                    continue
                try:
                    snd = pygame.mixer.Sound(path)
                    volume = Config.SOUND_VOLUMES.get(name, Config.DEFAULT_SOUND_VOLUME)
                    snd.set_volume(volume)
                    self.sounds[category][name] = snd
                except pygame.error as e:
                    logger.warning(f"Could not load sound '{name}' from '{path}': {e}")
                    self.sounds[category][name] = None

        if not self.background_music_tracks:
            logger.info("No background music tracks found.")

    def play(self, category: str, name: str, loops: int = 0) -> None:
        if not self.audio_available:
            return
        sfx = self.sounds.get(category, {}).get(name, None)
        if sfx:
            try:
                sfx.play(loops=loops)
            except pygame.error as e:
                logger.warning(f"Failed to play sound '{name}': {e}")
        else:
            logger.warning(f"Sound '{name}' in category '{category}' not found or invalid.")

    def play_music(self) -> None:
        if not self.audio_available or not self.music_on or not self.background_music_tracks:
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
        if not self.audio_available:
            return
        try:
            if self.music_on:
                pygame.mixer.music.pause()
                self.music_on = False
                logger.info("Background music paused.")
            else:
                pygame.mixer.music.unpause()
                self.music_on = True
                logger.info("Background music resumed.")
        except pygame.error as e:
            logger.warning(f"Failed to toggle music: {e}")

    def stop_music(self) -> None:
        if not self.audio_available:
            return
        try:
            pygame.mixer.music.stop()
            self.music_on = False
            logger.info("Background music stopped.")
        except pygame.error as e:
            logger.warning(f"Failed to stop music: {e}")

    def is_music_on(self) -> bool:
        return self.music_on

    def set_sound_volume(self, category: str, name: str, volume: float) -> None:
        if not self.audio_available:
            return
        volume = max(0.0, min(1.0, volume))
        sfx = self.sounds.get(category, {}).get(name, None)
        if sfx:
            sfx.set_volume(volume)
            Config.SOUND_VOLUMES[name] = volume
        else:
            logger.warning(f"Sound '{name}' in category '{category}' not found.")

    def set_music_volume(self, volume: float) -> None:
        if not self.audio_available:
            return
        volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(volume)
            Config.DEFAULT_SOUND_VOLUME = volume
            logger.info(f"Background music volume set to {volume}.")
        except pygame.error as e:
            logger.warning(f"Failed to set music volume: {e}")

sound_manager = SoundManager()
