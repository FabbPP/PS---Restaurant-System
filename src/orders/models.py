"""Order domain models."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from delivery.models import DeliveryInfo
from exceptions.domain import StateError
from orders.states import OrderState, ensure_transition
from validators.common import (validate_id, validate_non_empty_str,
                                validate_positive_int, validate_price)


class OrderType(str, Enum):
    """Order type enum."""

    DINE_IN = "mesa"
    TAKEAWAY = "llevar"
    DELIVERY = "delivery"


@dataclass
class OrderItem:
    """Represents a single order item."""

    name: str
    quantity: int
    unit_price: float

    def __post_init__(self) -> None:
        self.name = validate_non_empty_str(self.name, "Nombre del ítem",
                                           min_len=1, max_len=60)
        self.quantity = validate_positive_int(self.quantity, "Cantidad",
                                              min_value=1, max_value=99)
        self.unit_price = validate_price(self.unit_price, "Precio unitario")

    def subtotal(self) -> float:
        """Compute subtotal for the item."""
        return round(self.quantity * self.unit_price, 2)


@dataclass
class Order:
    """Represents an order."""

    id: int
    order_type: OrderType
    state: OrderState = OrderState.PENDING
    items: List[OrderItem] = field(default_factory=list)
    table_id: Optional[int] = None
    delivery_info: Optional[DeliveryInfo] = None
    closed: bool = False

    def __post_init__(self) -> None:
        validate_id(self.id, "ID de orden")

    def add_item(self, item: OrderItem) -> None:
        """Add an item to the order."""
        if self.closed:
            raise StateError("La orden está cerrada.")
        if self.state in {OrderState.DELIVERED, OrderState.CANCELED}:
            raise StateError("No se pueden agregar ítems a una orden finalizada.")
        self.items.append(item)

    def total(self) -> float:
        """Calculate the total amount."""
        return round(sum(item.subtotal() for item in self.items), 2)

    def set_state(self, new_state: OrderState) -> None:
        """Change order state with validation."""
        if self.closed:
            raise StateError("La orden está cerrada.")
        ensure_transition(self.state, new_state)
        self.state = new_state
