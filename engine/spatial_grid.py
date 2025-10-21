# engine/spatial_grid.py

from typing import Any

class SpatialGrid:
    """
    Spatial partitioning grid for efficient proximity queries.
    Divides the world into cells to optimize collision detection and entity queries.
    """

    def __init__(self, cell_size: int = 10) -> None:
        """
        Initialize the spatial grid.

        Args:
            cell_size: Size of each grid cell in world units (tiles)
        """
        self.cell_size = cell_size
        self.grid: dict[tuple[int, int], list[Any]] = {}

    def clear(self) -> None:
        """Clear all entities from the grid."""
        self.grid.clear()

    def insert(self, entity: Any) -> None:
        """
        Insert an entity into the grid based on its position.

        Args:
            entity: Entity with x and y attributes
        """
        cell_x = int(entity.x // self.cell_size)
        cell_y = int(entity.y // self.cell_size)
        key = (cell_x, cell_y)

        if key not in self.grid:
            self.grid[key] = []
        self.grid[key].append(entity)

    def query_nearby(self, x: float, y: float, radius: int = 1) -> list[Any]:
        """
        Get all entities in nearby cells around a position.

        Args:
            x: World x position in tiles
            y: World y position in tiles
            radius: How many cells to search in each direction (default: 1)

        Returns:
            List of entities in nearby cells
        """
        cell_x = int(x // self.cell_size)
        cell_y = int(y // self.cell_size)
        nearby = []

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                key = (cell_x + dx, cell_y + dy)
                if key in self.grid:
                    nearby.extend(self.grid[key])

        return nearby

    def query_range(self, start_x: float, start_y: float,
                    end_x: float, end_y: float) -> list[Any]:
        """
        Get all entities within a rectangular range.

        Args:
            start_x: Start x position in tiles
            start_y: Start y position in tiles
            end_x: End x position in tiles
            end_y: End y position in tiles

        Returns:
            List of entities in the specified range
        """
        start_cell_x = int(start_x // self.cell_size)
        start_cell_y = int(start_y // self.cell_size)
        end_cell_x = int(end_x // self.cell_size)
        end_cell_y = int(end_y // self.cell_size)

        entities = []
        for cy in range(start_cell_y, end_cell_y + 1):
            for cx in range(start_cell_x, end_cell_x + 1):
                key = (cx, cy)
                if key in self.grid:
                    entities.extend(self.grid[key])

        return entities
