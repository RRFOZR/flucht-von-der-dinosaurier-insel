# engine/object_pool.py

from typing import List, Callable, TypeVar, Generic

T = TypeVar('T')

class ObjectPool(Generic[T]):
    """
    Object pooling system to reuse objects instead of creating/destroying.
    Improves performance and reduces memory churn.
    """

    def __init__(self, factory: Callable[[], T], initial_size: int = 50) -> None:
        """
        Initialize object pool.

        Args:
            factory: Function that creates new objects
            initial_size: Number of objects to pre-create
        """
        self.factory = factory
        self.available: List[T] = []
        self.in_use: List[T] = []

        # Pre-create initial objects
        for _ in range(initial_size):
            self.available.append(factory())

    def acquire(self) -> T:
        """
        Get an object from the pool.

        Returns:
            An object from the pool (reused or newly created)
        """
        if len(self.available) > 0:
            obj = self.available.pop()
        else:
            obj = self.factory()

        self.in_use.append(obj)
        return obj

    def release(self, obj: T) -> None:
        """
        Return an object to the pool.

        Args:
            obj: Object to return
        """
        if obj in self.in_use:
            self.in_use.remove(obj)
            self.available.append(obj)

    def release_all(self) -> None:
        """Return all in-use objects to the pool."""
        self.available.extend(self.in_use)
        self.in_use.clear()

    def get_stats(self) -> dict:
        """
        Get pool statistics.

        Returns:
            Dictionary with pool stats
        """
        return {
            'available': len(self.available),
            'in_use': len(self.in_use),
            'total': len(self.available) + len(self.in_use)
        }
