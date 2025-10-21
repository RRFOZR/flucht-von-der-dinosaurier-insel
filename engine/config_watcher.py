# engine/config_watcher.py

import os
import time
import logging
from typing import Callable, List

logger = logging.getLogger(__name__)

class ConfigWatcher:
    """
    Watches configuration files for changes and triggers reload callbacks.
    Useful for live-tweaking game parameters during development.
    """

    def __init__(self, watch_files: List[str] = None) -> None:
        """
        Initialize the config watcher.

        Args:
            watch_files: List of file paths to watch for changes
        """
        self.watch_files = watch_files or ['config.py']
        self.last_modified = {}
        self.callbacks: List[Callable] = []
        self.enabled = False

        # Initialize modification times
        for filepath in self.watch_files:
            if os.path.exists(filepath):
                self.last_modified[filepath] = os.path.getmtime(filepath)
            else:
                logger.warning(f"Config watch file not found: {filepath}")

    def add_callback(self, callback: Callable) -> None:
        """
        Add a callback to be called when config changes.

        Args:
            callback: Function to call on config reload
        """
        self.callbacks.append(callback)

    def enable(self) -> None:
        """Enable config watching."""
        self.enabled = True
        logger.info("Config hot-reload enabled")

    def disable(self) -> None:
        """Disable config watching."""
        self.enabled = False
        logger.info("Config hot-reload disabled")

    def check_reload(self) -> bool:
        """
        Check if any watched files have changed and trigger reload if needed.

        Returns:
            True if config was reloaded, False otherwise
        """
        if not self.enabled:
            return False

        for filepath in self.watch_files:
            if not os.path.exists(filepath):
                continue

            current_mtime = os.path.getmtime(filepath)
            last_mtime = self.last_modified.get(filepath, 0)

            if current_mtime > last_mtime:
                logger.info(f"Config file changed: {filepath}")
                self.last_modified[filepath] = current_mtime
                self._reload_config(filepath)
                return True

        return False

    def _reload_config(self, filepath: str) -> None:
        """
        Reload the configuration and call all callbacks.

        Args:
            filepath: Path to the changed config file
        """
        logger.info(f"Reloading configuration from {filepath}")

        # In Python, we can't easily reload a module at runtime without importlib
        # For now, just trigger callbacks which can re-read values
        for callback in self.callbacks:
            try:
                callback(filepath)
            except Exception as e:
                logger.error(f"Error in config reload callback: {e}")

        logger.info("Configuration reloaded successfully")


# Example usage in game code:
# config_watcher = ConfigWatcher(['config.py'])
# config_watcher.add_callback(lambda path: logger.info(f"Config {path} changed!"))
# config_watcher.enable()
#
# # In game loop:
# if config_watcher.check_reload():
#     # Re-read config values
#     pass
