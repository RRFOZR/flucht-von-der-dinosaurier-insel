# engine/particle_system.py

import pygame
import random
import math
from typing import Optional

class Particle:
    """
    Individual particle with physics and lifetime.
    """

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 lifetime: float, color: tuple[int, int, int],
                 size: float = 2.0, gravity: float = 0.0) -> None:
        """
        Initialize a particle.

        Args:
            x: Starting x position
            y: Starting y position
            vx: Velocity in x direction
            vy: Velocity in y direction
            lifetime: How long the particle lives (seconds)
            color: RGB color tuple
            size: Particle size in pixels
            gravity: Gravity acceleration (pixels/second²)
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.age = 0.0
        self.color = color
        self.size = size
        self.gravity = gravity
        self.alpha = 255

    def update(self, dt: float) -> bool:
        """
        Update particle physics and age.

        Args:
            dt: Delta time in seconds

        Returns:
            True if particle is still alive, False if expired
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt

        self.age += dt

        # Fade out as particle ages
        life_ratio = 1.0 - (self.age / self.lifetime)
        self.alpha = int(255 * life_ratio)

        return self.age < self.lifetime

    def render(self, surface: pygame.Surface, camera_offset_x: float = 0,
               camera_offset_y: float = 0) -> None:
        """
        Render the particle.

        Args:
            surface: Surface to render to
            camera_offset_x: Camera x offset for world-to-screen conversion
            camera_offset_y: Camera y offset for world-to-screen conversion
        """
        screen_x = int(self.x - camera_offset_x)
        screen_y = int(self.y - camera_offset_y)

        if self.alpha > 0:
            # Create a temporary surface with alpha
            temp_surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (*self.color, self.alpha),
                             (int(self.size), int(self.size)), int(self.size))
            surface.blit(temp_surf, (screen_x - int(self.size), screen_y - int(self.size)))


class ParticleSystem:
    """
    Manages multiple particles for visual effects.
    """

    def __init__(self) -> None:
        """Initialize the particle system."""
        self.particles: list[Particle] = []

    def emit(self, x: float, y: float, count: int = 10,
             color: tuple[int, int, int] = (255, 255, 255),
             speed_range: tuple[float, float] = (20, 50),
             lifetime_range: tuple[float, float] = (0.5, 1.5),
             size_range: tuple[float, float] = (2, 4),
             spread_angle: float = 360,
             direction: float = 0,
             gravity: float = 0) -> None:
        """
        Emit a burst of particles.

        Args:
            x: Emission x position
            y: Emission y position
            count: Number of particles to emit
            color: RGB color tuple
            speed_range: (min, max) speed in pixels/second
            lifetime_range: (min, max) lifetime in seconds
            size_range: (min, max) size in pixels
            spread_angle: Angle spread in degrees (360 = all directions)
            direction: Base direction in degrees (0 = right, 90 = down)
            gravity: Gravity acceleration
        """
        for _ in range(count):
            # Random angle within spread
            angle_offset = random.uniform(-spread_angle / 2, spread_angle / 2)
            angle = math.radians(direction + angle_offset)

            # Random speed
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            # Random lifetime and size
            lifetime = random.uniform(*lifetime_range)
            size = random.uniform(*size_range)

            # Create particle
            particle = Particle(x, y, vx, vy, lifetime, color, size, gravity)
            self.particles.append(particle)

    def update(self, dt: float) -> None:
        """
        Update all particles and remove expired ones.

        Args:
            dt: Delta time in seconds
        """
        self.particles = [p for p in self.particles if p.update(dt)]

    def render(self, surface: pygame.Surface, camera_offset_x: float = 0,
               camera_offset_y: float = 0) -> None:
        """
        Render all active particles.

        Args:
            surface: Surface to render to
            camera_offset_x: Camera x offset
            camera_offset_y: Camera y offset
        """
        for particle in self.particles:
            particle.render(surface, camera_offset_x, camera_offset_y)

    def clear(self) -> None:
        """Clear all particles."""
        self.particles.clear()

    def get_particle_count(self) -> int:
        """Get the number of active particles."""
        return len(self.particles)
