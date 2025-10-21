# engine/state_machine.py

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

class State:
    """
    Base state class for state machine.
    Override enter(), update(), and exit() methods in subclasses.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the state.

        Args:
            name: Name of the state for debugging
        """
        self.name = name

    def enter(self, entity: Any) -> None:
        """
        Called when entering this state.

        Args:
            entity: The entity this state belongs to
        """
        pass

    def update(self, entity: Any, dt: float, **kwargs: Any) -> Optional[str]:
        """
        Update the state logic.

        Args:
            entity: The entity this state belongs to
            dt: Delta time in seconds
            **kwargs: Additional context (e.g., player, game_map, night)

        Returns:
            Name of next state to transition to, or None to stay in current state
        """
        return None

    def exit(self, entity: Any) -> None:
        """
        Called when exiting this state.

        Args:
            entity: The entity this state belongs to
        """
        pass


class StateMachine:
    """
    Finite state machine for managing entity behavior.
    """

    def __init__(self, initial_state: Optional[State] = None) -> None:
        """
        Initialize the state machine.

        Args:
            initial_state: The starting state (optional)
        """
        self.states: dict[str, State] = {}
        self.current_state: Optional[State] = initial_state
        self.entity: Optional[Any] = None

    def add_state(self, state: State) -> None:
        """
        Add a state to the state machine.

        Args:
            state: The state to add
        """
        self.states[state.name] = state

    def set_initial_state(self, state_name: str, entity: Any) -> None:
        """
        Set the initial state and entity.

        Args:
            state_name: Name of the initial state
            entity: The entity this state machine controls
        """
        if state_name not in self.states:
            logger.error(f"State '{state_name}' not found in state machine")
            return

        self.entity = entity
        self.current_state = self.states[state_name]
        self.current_state.enter(entity)
        logger.debug(f"State machine initialized with state '{state_name}'")

    def change_state(self, state_name: str) -> None:
        """
        Transition to a different state.

        Args:
            state_name: Name of the state to transition to
        """
        if state_name not in self.states:
            logger.error(f"Cannot transition to unknown state '{state_name}'")
            return

        if self.current_state:
            self.current_state.exit(self.entity)
            logger.debug(f"Exiting state '{self.current_state.name}'")

        self.current_state = self.states[state_name]
        self.current_state.enter(self.entity)
        logger.debug(f"Entered state '{state_name}'")

    def update(self, dt: float, **kwargs: Any) -> None:
        """
        Update the current state.

        Args:
            dt: Delta time in seconds
            **kwargs: Additional context passed to state's update method
        """
        if self.current_state and self.entity:
            next_state = self.current_state.update(self.entity, dt, **kwargs)

            # Auto-transition if state returns a new state name
            if next_state and next_state in self.states:
                self.change_state(next_state)

    def get_current_state_name(self) -> Optional[str]:
        """
        Get the name of the current state.

        Returns:
            Current state name, or None if no state is set
        """
        return self.current_state.name if self.current_state else None
