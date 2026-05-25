"""Customer repository (in-memory)."""

from typing import Dict, List

from exceptions.domain import ConflictError, NotFoundError
from customers.models import DeliveryCustomer
from utils.id_generator import IdGenerator


class CustomerRepository:
    """In-memory repository for delivery customers."""

    def __init__(self) -> None:
        self._items: Dict[int, DeliveryCustomer] = {}
        self._id_gen = IdGenerator()

    def create(self, name: str, phone: str) -> DeliveryCustomer:
        """Create and store a new customer."""
        customer_id = self._id_gen.next_id()
        if customer_id in self._items:
            raise ConflictError("ID de cliente duplicado.")
        customer = DeliveryCustomer(id=customer_id, name=name, phone=phone)
        self._items[customer_id] = customer
        return customer

    def add(self, customer: DeliveryCustomer) -> None:
        """Add an existing customer."""
        if customer.id in self._items:
            raise ConflictError("ID de cliente duplicado.")
        self._items[customer.id] = customer

    def get(self, customer_id: int) -> DeliveryCustomer:
        """Get a customer by ID."""
        try:
            return self._items[customer_id]
        except KeyError as exc:
            raise NotFoundError("Cliente no encontrado.") from exc

    def list_all(self) -> List[DeliveryCustomer]:
        """List all customers."""
        return list(self._items.values())
