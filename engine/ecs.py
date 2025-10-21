# engine/ecs.py

from typing import Dict, Set, List, Type, TypeVar, Optional, Any
from abc import ABC, abstractmethod

T = TypeVar('T', bound='Component')

class Component:
    """Base class for all ECS components."""
    pass


class Entity:
    """
    Lightweight entity that holds components.
    Entities are just IDs with attached components.
    """

    _next_id = 0

    def __init__(self) -> None:
        self.id = Entity._next_id
        Entity._next_id += 1
        self.components: Dict[Type[Component], Component] = {}
        self.active = True

    def add_component(self, component: Component) -> 'Entity':
        """
        Add a component to this entity.

        Args:
            component: Component instance to add

        Returns:
            Self for method chaining
        """
        self.components[type(component)] = component
        return self

    def get_component(self, component_type: Type[T]) -> Optional[T]:
        """
        Get a component of the specified type.

        Args:
            component_type: The component class to retrieve

        Returns:
            The component instance or None if not found
        """
        return self.components.get(component_type)

    def has_component(self, component_type: Type[Component]) -> bool:
        """
        Check if entity has a component of the specified type.

        Args:
            component_type: The component class to check

        Returns:
            True if component exists
        """
        return component_type in self.components

    def remove_component(self, component_type: Type[Component]) -> None:
        """
        Remove a component from this entity.

        Args:
            component_type: The component class to remove
        """
        if component_type in self.components:
            del self.components[component_type]


class System(ABC):
    """
    Base class for all systems.
    Systems process entities that have specific components.
    """

    def __init__(self) -> None:
        self.required_components: Set[Type[Component]] = set()

    @abstractmethod
    def update(self, entities: List[Entity], dt: float) -> None:
        """
        Update all entities with required components.

        Args:
            entities: List of all entities
            dt: Delta time in seconds
        """
        pass

    def get_matching_entities(self, entities: List[Entity]) -> List[Entity]:
        """
        Get entities that have all required components.

        Args:
            entities: List of all entities

        Returns:
            Filtered list of entities with required components
        """
        return [
            entity for entity in entities
            if entity.active and all(entity.has_component(comp) for comp in self.required_components)
        ]


class World:
    """
    Container for entities and systems.
    Manages entity lifecycle and system updates.
    """

    def __init__(self) -> None:
        self.entities: List[Entity] = []
        self.systems: List[System] = []
        self.entities_to_remove: Set[int] = set()

    def create_entity(self) -> Entity:
        """
        Create a new entity and add it to the world.

        Returns:
            The created entity
        """
        entity = Entity()
        self.entities.append(entity)
        return entity

    def remove_entity(self, entity: Entity) -> None:
        """
        Mark an entity for removal.

        Args:
            entity: Entity to remove
        """
        self.entities_to_remove.add(entity.id)
        entity.active = False

    def add_system(self, system: System) -> None:
        """
        Add a system to the world.

        Args:
            system: System to add
        """
        self.systems.append(system)

    def update(self, dt: float) -> None:
        """
        Update all systems.

        Args:
            dt: Delta time in seconds
        """
        # Update all systems
        for system in self.systems:
            system.update(self.entities, dt)

        # Remove marked entities
        if self.entities_to_remove:
            self.entities = [e for e in self.entities if e.id not in self.entities_to_remove]
            self.entities_to_remove.clear()

    def get_entities_with_component(self, component_type: Type[T]) -> List[Entity]:
        """
        Get all active entities with a specific component.

        Args:
            component_type: The component type to filter by

        Returns:
            List of entities with the component
        """
        return [e for e in self.entities if e.active and e.has_component(component_type)]

    def clear(self) -> None:
        """Remove all entities and systems."""
        self.entities.clear()
        self.systems.clear()
        self.entities_to_remove.clear()


# Common component types for this game

class TransformComponent(Component):
    """Position and facing direction."""

    def __init__(self, x: float, y: float, facing_left: bool = False) -> None:
        self.x = x
        self.y = y
        self.facing_left = facing_left


class HealthComponent(Component):
    """Health points."""

    def __init__(self, hp: int, max_hp: int) -> None:
        self.hp = hp
        self.max_hp = max_hp


class VelocityComponent(Component):
    """Movement velocity."""

    def __init__(self, vx: float = 0.0, vy: float = 0.0, speed: float = 1.0) -> None:
        self.vx = vx
        self.vy = vy
        self.speed = speed


class SpriteComponent(Component):
    """Sprite rendering data."""

    def __init__(self, frames_right: List[Any], frames_left: List[Any]) -> None:
        self.frames_right = frames_right
        self.frames_left = frames_left
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_interval = 0.15


class AIComponent(Component):
    """AI behavior state."""

    def __init__(self, state: str = "IDLE", aggressive: bool = False) -> None:
        self.state = state
        self.aggressive = aggressive
        self.just_attacked = False


class InventoryComponent(Component):
    """Inventory for items."""

    def __init__(self) -> None:
        self.items: Dict[str, int] = {}
