# engine/render_layers.py

from typing import List, Tuple, Callable
import pygame

class RenderLayer:
    """
    Represents a single render layer with a z-index.
    """

    def __init__(self, name: str, z_index: int) -> None:
        """
        Initialize a render layer.

        Args:
            name: Layer name
            z_index: Z-order (higher = drawn on top)
        """
        self.name = name
        self.z_index = z_index
        self.render_calls: List[Callable] = []

    def add_render_call(self, render_func: Callable) -> None:
        """
        Add a render function to this layer.

        Args:
            render_func: Function to call for rendering
        """
        self.render_calls.append(render_func)

    def clear(self) -> None:
        """Clear all render calls for this frame."""
        self.render_calls.clear()

    def render(self, surface: pygame.Surface) -> None:
        """
        Execute all render calls for this layer.

        Args:
            surface: Surface to render to
        """
        for render_func in self.render_calls:
            render_func(surface)


class LayerManager:
    """
    Manages multiple render layers for proper z-ordering.
    """

    def __init__(self) -> None:
        """Initialize the layer manager."""
        self.layers: List[RenderLayer] = []

        # Create default layers
        self.add_layer("background", -100)
        self.add_layer("ground", 0)
        self.add_layer("items", 10)
        self.add_layer("entities", 20)
        self.add_layer("player", 30)
        self.add_layer("effects", 40)
        self.add_layer("particles", 50)
        self.add_layer("ui", 100)
        self.add_layer("debug", 200)

    def add_layer(self, name: str, z_index: int) -> RenderLayer:
        """
        Add a new render layer.

        Args:
            name: Layer name
            z_index: Z-order

        Returns:
            The created layer
        """
        layer = RenderLayer(name, z_index)
        self.layers.append(layer)
        self._sort_layers()
        return layer

    def get_layer(self, name: str) -> RenderLayer:
        """
        Get a layer by name.

        Args:
            name: Layer name

        Returns:
            The layer, or None if not found
        """
        for layer in self.layers:
            if layer.name == name:
                return layer
        return None

    def _sort_layers(self) -> None:
        """Sort layers by z-index."""
        self.layers.sort(key=lambda l: l.z_index)

    def clear_all(self) -> None:
        """Clear all render calls from all layers."""
        for layer in self.layers:
            layer.clear()

    def render_all(self, surface: pygame.Surface) -> None:
        """
        Render all layers in order.

        Args:
            surface: Surface to render to
        """
        for layer in self.layers:
            layer.render(surface)

    def render_to(self, layer_name: str, render_func: Callable) -> None:
        """
        Add a render call to a specific layer.

        Args:
            layer_name: Name of the layer
            render_func: Function to call for rendering
        """
        layer = self.get_layer(layer_name)
        if layer:
            layer.add_render_call(render_func)
