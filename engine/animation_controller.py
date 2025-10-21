# engine/animation_controller.py

from typing import Dict, List, Callable, Optional, Any
import pygame


class Animation:
    """
    Represents a single animation sequence.
    """

    def __init__(
        self,
        frames: List[pygame.Surface],
        frame_duration: float = 0.1,
        loop: bool = True,
        on_complete: Optional[Callable] = None
    ) -> None:
        """
        Initialize animation.

        Args:
            frames: List of pygame surfaces (animation frames)
            frame_duration: Duration of each frame in seconds
            loop: Whether animation should loop
            on_complete: Callback when animation completes (for non-looping)
        """
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.on_complete = on_complete
        self.current_frame = 0
        self.timer = 0.0
        self.finished = False

    def reset(self) -> None:
        """Reset animation to first frame."""
        self.current_frame = 0
        self.timer = 0.0
        self.finished = False

    def update(self, dt: float) -> None:
        """
        Update animation timer and frame.

        Args:
            dt: Delta time in seconds
        """
        if self.finished:
            return

        self.timer += dt
        while self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    if self.on_complete:
                        self.on_complete()

    def get_current_frame(self) -> pygame.Surface:
        """
        Get the current animation frame.

        Returns:
            Current frame surface
        """
        return self.frames[self.current_frame]

    def is_finished(self) -> bool:
        """Check if animation has finished (for non-looping animations)."""
        return self.finished


class AnimationState:
    """
    Animation state with transition conditions.
    Part of an animation state machine.
    """

    def __init__(
        self,
        name: str,
        animation: Animation,
        transitions: Optional[Dict[str, Callable[[], bool]]] = None
    ) -> None:
        """
        Initialize animation state.

        Args:
            name: State name
            animation: Animation for this state
            transitions: Dictionary of {target_state_name: condition_function}
        """
        self.name = name
        self.animation = animation
        self.transitions = transitions or {}

    def check_transitions(self) -> Optional[str]:
        """
        Check if any transition conditions are met.

        Returns:
            Name of target state to transition to, or None
        """
        for target_state, condition in self.transitions.items():
            if condition():
                return target_state
        return None


class AnimationStateMachine:
    """
    State machine for managing animation transitions.
    Examples: idle -> walk -> run -> jump -> fall -> land -> idle
    """

    def __init__(self) -> None:
        self.states: Dict[str, AnimationState] = {}
        self.current_state: Optional[AnimationState] = None
        self.previous_state: Optional[str] = None

    def add_state(self, state: AnimationState) -> None:
        """
        Add a state to the state machine.

        Args:
            state: Animation state to add
        """
        self.states[state.name] = state

    def set_state(self, state_name: str, force: bool = False) -> None:
        """
        Set the current animation state.

        Args:
            state_name: Name of state to transition to
            force: Force transition even if already in this state
        """
        if state_name not in self.states:
            return

        # Don't transition to same state unless forced
        if not force and self.current_state and self.current_state.name == state_name:
            return

        self.previous_state = self.current_state.name if self.current_state else None
        self.current_state = self.states[state_name]
        self.current_state.animation.reset()

    def update(self, dt: float) -> None:
        """
        Update current animation and check for transitions.

        Args:
            dt: Delta time in seconds
        """
        if not self.current_state:
            return

        # Update current animation
        self.current_state.animation.update(dt)

        # Check for automatic transitions
        target_state = self.current_state.check_transitions()
        if target_state:
            self.set_state(target_state)

    def get_current_frame(self) -> Optional[pygame.Surface]:
        """
        Get the current animation frame.

        Returns:
            Current frame surface or None
        """
        if self.current_state:
            return self.current_state.animation.get_current_frame()
        return None

    def get_current_state_name(self) -> Optional[str]:
        """Get the name of the current state."""
        return self.current_state.name if self.current_state else None


class AnimationController:
    """
    High-level controller for entity animations.
    Manages multiple animation clips and transitions.
    """

    def __init__(self) -> None:
        self.animations: Dict[str, Animation] = {}
        self.current_animation: Optional[str] = None
        self.flip_horizontal = False
        self.flip_vertical = False
        self.tint_color: Optional[tuple] = None

    def add_animation(self, name: str, animation: Animation) -> None:
        """
        Add an animation clip.

        Args:
            name: Animation name
            animation: Animation object
        """
        self.animations[name] = animation

    def play(self, name: str, restart: bool = False) -> None:
        """
        Play an animation.

        Args:
            name: Animation name
            restart: Force restart if already playing
        """
        if name not in self.animations:
            return

        if self.current_animation != name or restart:
            self.current_animation = name
            self.animations[name].reset()

    def stop(self) -> None:
        """Stop the current animation."""
        self.current_animation = None

    def update(self, dt: float) -> None:
        """
        Update current animation.

        Args:
            dt: Delta time in seconds
        """
        if self.current_animation and self.current_animation in self.animations:
            self.animations[self.current_animation].update(dt)

    def get_current_frame(self) -> Optional[pygame.Surface]:
        """
        Get the current animation frame with transformations applied.

        Returns:
            Current frame surface or None
        """
        if not self.current_animation or self.current_animation not in self.animations:
            return None

        frame = self.animations[self.current_animation].get_current_frame()

        # Apply transformations
        if self.flip_horizontal or self.flip_vertical:
            frame = pygame.transform.flip(frame, self.flip_horizontal, self.flip_vertical)

        # Apply tint (if specified)
        if self.tint_color:
            tinted = frame.copy()
            tinted.fill(self.tint_color, special_flags=pygame.BLEND_MULT)
            frame = tinted

        return frame

    def is_playing(self, name: str) -> bool:
        """Check if a specific animation is currently playing."""
        return self.current_animation == name

    def is_finished(self) -> bool:
        """Check if current animation has finished."""
        if not self.current_animation or self.current_animation not in self.animations:
            return True
        return self.animations[self.current_animation].is_finished()
