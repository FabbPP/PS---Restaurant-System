"""Order repository (in-memory)."""

from typing import Dict, List

from exceptions.domain import ConflictError, NotFoundError
from orders.models import Order
from utils.id_generator import IdGenerator


class OrderRepository:
    """In-memory repository for orders."""

    def __init__(self) -> None:
        self._items: Dict[int, Order] = {}
        self._id_gen = IdGenerator()

    def next_id(self) -> int:
        """Get a new unique order ID."""
        return self._id_gen.next_id()

    def add(self, order: Order) -> None:
        """Store a new order."""
        if order.id in self._items:
            raise ConflictError("ID de orden duplicado.")
        self._items[order.id] = order

    def get(self, order_id: int) -> Order:
        """Get an order by ID."""
        try:
            return self._items[order_id]
        except KeyError as exc:
            raise NotFoundError("Orden no encontrada.") from exc

    def list_all(self) -> List[Order]:
        """List all orders."""
        return list(self._items.values())
