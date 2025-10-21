# engine/audio_manager.py

import pygame
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class AudioChannel:
    """
    Wrapper for pygame mixer channel with additional features.
    """

    def __init__(self, channel_id: int) -> None:
        """
        Initialize audio channel.

        Args:
            channel_id: Pygame mixer channel ID
        """
        self.channel_id = channel_id
        self.channel = pygame.mixer.Channel(channel_id)
        self.volume = 1.0
        self.paused = False
        self.current_sound: Optional[str] = None

    def play(self, sound: pygame.mixer.Sound, loops: int = 0, fade_ms: int = 0) -> None:
        """
        Play a sound on this channel.

        Args:
            sound: Pygame sound object
            loops: Number of loops (-1 for infinite)
            fade_ms: Fade in time in milliseconds
        """
        if fade_ms > 0:
            self.channel.play(sound, loops=loops, fade_ms=fade_ms)
        else:
            self.channel.play(sound, loops=loops)
        self.channel.set_volume(self.volume)

    def stop(self, fade_ms: int = 0) -> None:
        """
        Stop playback on this channel.

        Args:
            fade_ms: Fade out time in milliseconds
        """
        if fade_ms > 0:
            self.channel.fadeout(fade_ms)
        else:
            self.channel.stop()
        self.current_sound = None

    def pause(self) -> None:
        """Pause playback on this channel."""
        self.channel.pause()
        self.paused = True

    def unpause(self) -> None:
        """Unpause playback on this channel."""
        self.channel.unpause()
        self.paused = False

    def set_volume(self, volume: float) -> None:
        """
        Set channel volume.

        Args:
            volume: Volume (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        self.channel.set_volume(self.volume)

    def is_busy(self) -> bool:
        """Check if channel is playing a sound."""
        return self.channel.get_busy()


class AudioManager:
    """
    Enhanced audio manager with channel management and audio groups.
    Manages music, sound effects, and positional audio.
    """

    def __init__(self, num_channels: int = 16) -> None:
        """
        Initialize audio manager.

        Args:
            num_channels: Number of mixer channels to allocate
        """
        pygame.mixer.set_num_channels(num_channels)
        self.channels: List[AudioChannel] = [AudioChannel(i) for i in range(num_channels)]
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.channel_groups: Dict[str, List[int]] = {}
        self.master_volume = 1.0
        self.sfx_volume = 1.0
        self.music_volume = 1.0
        self.current_music: Optional[str] = None
        self.music_paused = False

        # Default channel groups
        self._setup_default_groups()

    def _setup_default_groups(self) -> None:
        """Set up default channel groups."""
        self.channel_groups = {
            "music": [0],
            "sfx": list(range(1, 8)),
            "ambient": [8, 9],
            "ui": [10, 11],
            "voice": [12, 13],
            "misc": [14, 15]
        }

    def load_sound(self, name: str, filepath: str) -> bool:
        """
        Load a sound file.

        Args:
            name: Sound identifier
            filepath: Path to sound file

        Returns:
            True if load was successful
        """
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sounds[name] = sound
            logger.info(f"Loaded sound: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to load sound {name}: {e}")
            return False

    def play_sound(
        self,
        name: str,
        group: str = "sfx",
        loops: int = 0,
        volume: float = 1.0,
        fade_ms: int = 0
    ) -> Optional[AudioChannel]:
        """
        Play a sound effect on the first available channel in a group.

        Args:
            name: Sound identifier
            group: Channel group to use
            loops: Number of loops (-1 for infinite)
            volume: Volume (0.0 to 1.0)
            fade_ms: Fade in time in milliseconds

        Returns:
            AudioChannel playing the sound, or None if failed
        """
        if name not in self.sounds:
            logger.warning(f"Sound not found: {name}")
            return None

        if group not in self.channel_groups:
            logger.warning(f"Channel group not found: {group}")
            return None

        sound = self.sounds[name]

        # Find available channel in group
        for channel_id in self.channel_groups[group]:
            channel = self.channels[channel_id]
            if not channel.is_busy():
                channel.set_volume(volume * self.sfx_volume * self.master_volume)
                channel.play(sound, loops=loops, fade_ms=fade_ms)
                channel.current_sound = name
                return channel

        # No available channel, use first channel in group anyway
        channel_id = self.channel_groups[group][0]
        channel = self.channels[channel_id]
        channel.set_volume(volume * self.sfx_volume * self.master_volume)
        channel.play(sound, loops=loops, fade_ms=fade_ms)
        channel.current_sound = name
        return channel

    def stop_sound(self, name: str, fade_ms: int = 0) -> None:
        """
        Stop all instances of a sound.

        Args:
            name: Sound identifier
            fade_ms: Fade out time in milliseconds
        """
        for channel in self.channels:
            if channel.current_sound == name:
                channel.stop(fade_ms=fade_ms)

    def stop_group(self, group: str, fade_ms: int = 0) -> None:
        """
        Stop all sounds in a channel group.

        Args:
            group: Channel group name
            fade_ms: Fade out time in milliseconds
        """
        if group not in self.channel_groups:
            return

        for channel_id in self.channel_groups[group]:
            self.channels[channel_id].stop(fade_ms=fade_ms)

    def play_music(self, filepath: str, loops: int = -1, fade_ms: int = 0) -> None:
        """
        Play background music.

        Args:
            filepath: Path to music file
            loops: Number of loops (-1 for infinite)
            fade_ms: Fade in time in milliseconds
        """
        try:
            pygame.mixer.music.load(filepath)
            if fade_ms > 0:
                pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            else:
                pygame.mixer.music.play(loops=loops)
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            self.current_music = filepath
            self.music_paused = False
            logger.info(f"Playing music: {filepath}")
        except Exception as e:
            logger.error(f"Failed to play music: {e}")

    def stop_music(self, fade_ms: int = 0) -> None:
        """
        Stop background music.

        Args:
            fade_ms: Fade out time in milliseconds
        """
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
        self.current_music = None
        self.music_paused = False

    def pause_music(self) -> None:
        """Pause background music."""
        pygame.mixer.music.pause()
        self.music_paused = True

    def unpause_music(self) -> None:
        """Unpause background music."""
        pygame.mixer.music.unpause()
        self.music_paused = False

    def set_master_volume(self, volume: float) -> None:
        """
        Set master volume for all audio.

        Args:
            volume: Volume (0.0 to 1.0)
        """
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_sfx_volume(self, volume: float) -> None:
        """
        Set volume for sound effects.

        Args:
            volume: Volume (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_music_volume(self, volume: float) -> None:
        """
        Set volume for music.

        Args:
            volume: Volume (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)

    def _update_volumes(self) -> None:
        """Update all channel volumes."""
        for channel in self.channels:
            if channel.is_busy():
                channel.set_volume(channel.volume * self.sfx_volume * self.master_volume)
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)

    def pause_all(self) -> None:
        """Pause all audio (music and sound effects)."""
        for channel in self.channels:
            if channel.is_busy():
                channel.pause()
        self.pause_music()

    def unpause_all(self) -> None:
        """Unpause all audio."""
        for channel in self.channels:
            if channel.paused:
                channel.unpause()
        self.unpause_music()

    def stop_all(self, fade_ms: int = 0) -> None:
        """
        Stop all audio.

        Args:
            fade_ms: Fade out time in milliseconds
        """
        for channel in self.channels:
            channel.stop(fade_ms=fade_ms)
        self.stop_music(fade_ms=fade_ms)

    def get_channel(self, channel_id: int) -> Optional[AudioChannel]:
        """
        Get a specific audio channel.

        Args:
            channel_id: Channel ID

        Returns:
            AudioChannel or None if invalid ID
        """
        if 0 <= channel_id < len(self.channels):
            return self.channels[channel_id]
        return None
