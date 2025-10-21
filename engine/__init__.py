# engine/__init__.py

from engine.camera import Camera
from engine.spatial_grid import SpatialGrid
from engine.asset_manager import AssetManager, asset_manager
from engine.event_bus import EventBus, event_bus
from engine.particle_system import Particle, ParticleSystem
from engine.state_machine import State, StateMachine
from engine.config_watcher import ConfigWatcher
from engine.transitions import Transition
from engine.easing import Easing, Tween
from engine.debug_overlay import DebugOverlay
from engine.input_buffer import InputBuffer
from engine.delta_smoother import DeltaSmoother
from engine.object_pool import ObjectPool
from engine.sprite_trail import SpriteTrail
from engine.post_processing import PostProcessing
from engine.render_layers import LayerManager, RenderLayer
from engine.audio_3d import Audio3D

# New fundamental engine systems
from engine.ecs import (
    Component, Entity, System, World,
    TransformComponent, HealthComponent, VelocityComponent,
    SpriteComponent, AIComponent, InventoryComponent
)
from engine.state_stack import GameStateBase, StateStack
from engine.save_load import SaveLoadSystem, serialize_player, serialize_dinosaur, serialize_game_state
from engine.animation_controller import Animation, AnimationState, AnimationStateMachine, AnimationController
from engine.audio_manager import AudioChannel, AudioManager
from engine.resource_preloader import ResourcePreloader

__all__ = [
    # Core systems
    'Camera',
    'SpatialGrid',
    'AssetManager',
    'asset_manager',
    'EventBus',
    'event_bus',

    # Particles & Effects
    'Particle',
    'ParticleSystem',
    'SpriteTrail',
    'PostProcessing',

    # AI & State
    'State',
    'StateMachine',

    # Rendering
    'LayerManager',
    'RenderLayer',

    # Animation & Transitions
    'Transition',
    'Easing',
    'Tween',

    # Input & Performance
    'InputBuffer',
    'DeltaSmoother',
    'ObjectPool',

    # Audio
    'Audio3D',

    # Debug & Tools
    'DebugOverlay',
    'ConfigWatcher',

    # Entity Component System
    'Component',
    'Entity',
    'System',
    'World',
    'TransformComponent',
    'HealthComponent',
    'VelocityComponent',
    'SpriteComponent',
    'AIComponent',
    'InventoryComponent',

    # State Stack
    'GameStateBase',
    'StateStack',

    # Save/Load System
    'SaveLoadSystem',
    'serialize_player',
    'serialize_dinosaur',
    'serialize_game_state',

    # Animation Controller
    'Animation',
    'AnimationState',
    'AnimationStateMachine',
    'AnimationController',

    # Enhanced Audio Manager
    'AudioChannel',
    'AudioManager',

    # Resource Preloader
    'ResourcePreloader',
]
