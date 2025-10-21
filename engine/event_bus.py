# engine/event_bus.py

import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class EventBus:
    """
    Event-driven message bus for decoupled system communication.
    Allows systems to communicate without direct dependencies.
    """

    def __init__(self) -> None:
        """Initialize the event bus with empty listener registry."""
        self.listeners: dict[str, list[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        Subscribe to an event type.

        Args:
            event_type: The type/name of the event to listen for
            callback: Function to call when event is emitted
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []

        if callback not in self.listeners[event_type]:
            self.listeners[event_type].append(callback)
            logger.debug(f"Subscribed to event '{event_type}'")

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """
        Unsubscribe from an event type.

        Args:
            event_type: The type/name of the event
            callback: The callback function to remove
        """
        if event_type in self.listeners and callback in self.listeners[event_type]:
            self.listeners[event_type].remove(callback)
            logger.debug(f"Unsubscribed from event '{event_type}'")

    def emit(self, event_type: str, **kwargs: Any) -> None:
        """
        Emit an event to all subscribers.

        Args:
            event_type: The type/name of the event
            **kwargs: Event data to pass to callbacks
        """
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                try:
                    callback(**kwargs)
                except Exception as e:
                    logger.error(f"Error in event handler for '{event_type}': {e}")

    def clear_all(self) -> None:
        """Clear all event listeners."""
        self.listeners.clear()
        logger.debug("All event listeners cleared")


# Global singleton instance
event_bus = EventBus()
