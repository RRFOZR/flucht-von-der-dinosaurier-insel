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
]
