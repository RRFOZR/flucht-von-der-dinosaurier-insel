# engine/input_buffer.py

import time
from typing import Dict, Optional

class InputBuffer:
    """
    Input buffering system for better control feel.
    Remembers inputs for a short time window.
    """

    def __init__(self, buffer_time: float = 0.15) -> None:
        """
        Initialize input buffer.

        Args:
            buffer_time: How long to remember inputs (seconds)
        """
        self.buffer_time = buffer_time
        self.buffered_inputs: Dict[str, float] = {}

    def buffer_input(self, action: str) -> None:
        """
        Buffer an input action.

        Args:
            action: Name of the action (e.g., "jump", "attack")
        """
        self.buffered_inputs[action] = time.time()

    def consume_input(self, action: str) -> bool:
        """
        Check if action is buffered and consume it.

        Args:
            action: Name of the action

        Returns:
            True if action was buffered and is still valid
        """
        if action in self.buffered_inputs:
            timestamp = self.buffered_inputs[action]
            if time.time() - timestamp <= self.buffer_time:
                del self.buffered_inputs[action]
                return True
            else:
                # Expired, remove it
                del self.buffered_inputs[action]
        return False

    def is_buffered(self, action: str) -> bool:
        """
        Check if action is currently buffered (without consuming).

        Args:
            action: Name of the action

        Returns:
            True if action is buffered and valid
        """
        if action in self.buffered_inputs:
            timestamp = self.buffered_inputs[action]
            return time.time() - timestamp <= self.buffer_time
        return False

    def clear(self, action: Optional[str] = None) -> None:
        """
        Clear buffered inputs.

        Args:
            action: Specific action to clear, or None to clear all
        """
        if action:
            if action in self.buffered_inputs:
                del self.buffered_inputs[action]
        else:
            self.buffered_inputs.clear()

    def update(self) -> None:
        """Remove expired buffered inputs."""
        current_time = time.time()
        expired = [action for action, timestamp in self.buffered_inputs.items()
                   if current_time - timestamp > self.buffer_time]
        for action in expired:
            del self.buffered_inputs[action]
