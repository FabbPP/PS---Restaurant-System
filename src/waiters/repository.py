"""Waiter repository (in-memory)."""

from typing import Dict, List

from exceptions.domain import ConflictError, NotFoundError
from utils.id_generator import IdGenerator
from waiters.models import Waiter


class WaiterRepository:
    """In-memory repository for waiters."""

    def __init__(self) -> None:
        self._items: Dict[int, Waiter] = {}
        self._id_gen = IdGenerator()

    def create(self, name: str) -> Waiter:
        """Create and store a new waiter."""
        waiter_id = self._id_gen.next_id()
        if waiter_id in self._items:
            raise ConflictError("ID de mesero duplicado.")
        waiter = Waiter(id=waiter_id, name=name)
        self._items[waiter_id] = waiter
        return waiter

    def add(self, waiter: Waiter) -> None:
        """Add an existing waiter."""
        if waiter.id in self._items:
            raise ConflictError("ID de mesero duplicado.")
        self._items[waiter.id] = waiter

    def get(self, waiter_id: int) -> Waiter:
        """Get a waiter by ID."""
        try:
            return self._items[waiter_id]
        except KeyError as exc:
            raise NotFoundError("Mesero no encontrado.") from exc

    def list_all(self) -> List[Waiter]:
        """List all waiters."""
        return list(self._items.values())
