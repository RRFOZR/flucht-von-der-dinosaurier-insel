# engine/state_stack.py

from typing import List, Optional
from abc import ABC, abstractmethod
import pygame


class GameStateBase(ABC):
    """
    Base class for game states in a state stack.
    States can be pushed/popped like a stack for layered UI.
    """

    def __init__(self) -> None:
        self.next_state: Optional[str] = None
        self.is_transparent = False  # If True, render state below this one
        self.is_blocking = True  # If False, update state below this one

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame events.

        Args:
            event: Pygame event to handle
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update state logic.

        Args:
            dt: Delta time in seconds
        """
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """
        Render state to screen.

        Args:
            surface: Surface to render to
        """
        pass

    def on_enter(self) -> None:
        """Called when state becomes active (pushed to top)."""
        pass

    def on_exit(self) -> None:
        """Called when state is removed from stack."""
        pass

    def on_pause(self) -> None:
        """Called when another state is pushed on top."""
        pass

    def on_resume(self) -> None:
        """Called when state above is popped."""
        pass


class StateStack:
    """
    Manages a stack of game states.
    Useful for pause menus, inventory screens, dialog boxes, etc.
    """

    def __init__(self) -> None:
        self.states: List[GameStateBase] = []
        self.pending_actions: List[tuple] = []

    def push(self, state: GameStateBase) -> None:
        """
        Push a new state onto the stack.

        Args:
            state: State to push
        """
        self.pending_actions.append(('push', state))

    def pop(self) -> None:
        """Pop the top state from the stack."""
        self.pending_actions.append(('pop', None))

    def clear(self) -> None:
        """Clear all states from the stack."""
        self.pending_actions.append(('clear', None))

    def replace(self, state: GameStateBase) -> None:
        """
        Replace the current top state with a new one.

        Args:
            state: State to replace with
        """
        self.pending_actions.append(('replace', state))

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Pass events to the top state (and non-blocking states below).

        Args:
            event: Pygame event to handle
        """
        # Events are only sent to active (non-blocked) states
        for i in range(len(self.states) - 1, -1, -1):
            state = self.states[i]
            state.handle_event(event)
            if state.is_blocking:
                break

    def update(self, dt: float) -> None:
        """
        Update active states.

        Args:
            dt: Delta time in seconds
        """
        # Update from top to bottom, stopping at first blocking state
        for i in range(len(self.states) - 1, -1, -1):
            state = self.states[i]
            state.update(dt)
            if state.is_blocking:
                break

        # Apply pending actions
        self._apply_pending_actions()

    def render(self, surface: pygame.Surface) -> None:
        """
        Render visible states.

        Args:
            surface: Surface to render to
        """
        # Find the lowest visible state
        start_index = len(self.states) - 1
        for i in range(len(self.states) - 1, -1, -1):
            if not self.states[i].is_transparent:
                start_index = i
                break

        # Render from bottom to top
        for i in range(start_index, len(self.states)):
            self.states[i].render(surface)

    def _apply_pending_actions(self) -> None:
        """Apply all pending state stack actions."""
        for action, data in self.pending_actions:
            if action == 'push':
                if self.states:
                    self.states[-1].on_pause()
                self.states.append(data)
                data.on_enter()

            elif action == 'pop':
                if self.states:
                    state = self.states.pop()
                    state.on_exit()
                    if self.states:
                        self.states[-1].on_resume()

            elif action == 'clear':
                for state in self.states:
                    state.on_exit()
                self.states.clear()

            elif action == 'replace':
                if self.states:
                    old_state = self.states.pop()
                    old_state.on_exit()
                self.states.append(data)
                data.on_enter()

        self.pending_actions.clear()

    def is_empty(self) -> bool:
        """Check if the state stack is empty."""
        return len(self.states) == 0

    def peek(self) -> Optional[GameStateBase]:
        """Get the top state without removing it."""
        return self.states[-1] if self.states else None

    def size(self) -> int:
        """Get the number of states in the stack."""
        return len(self.states)
