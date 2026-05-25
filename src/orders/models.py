"""Order domain models."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from delivery.models import DeliveryInfo
from exceptions.domain import StateError
from exceptions.validation import ValidationError
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
        """Validate invariants after initialization."""
        validate_id(self.id, "ID de orden")

        if not isinstance(self.order_type, OrderType):
            raise ValidationError("Tipo de orden inválido.")
        if not isinstance(self.state, OrderState):
            raise ValidationError("Estado de orden inválido.")
        if not isinstance(self.closed, bool):
            raise ValidationError("Indicador de cierre inválido.")

        if self.table_id is not None:
            self.table_id = validate_id(self.table_id, "ID de mesa")
        if self.delivery_info is not None and not isinstance(self.delivery_info,
                                                             DeliveryInfo):
            raise ValidationError("Información de delivery inválida.")

        for item in self.items:
            if not isinstance(item, OrderItem):
                raise ValidationError(
                    "La lista de ítems contiene elementos inválidos."
                )

        self._validate_type_invariants()
        if self.closed and self.state not in {
                OrderState.DELIVERED,
                OrderState.CANCELED,
        }:
            raise ValidationError("Una orden cerrada debe estar finalizada.")

    def _validate_type_invariants(self) -> None:
        """Enforce consistency between order type and associated fields."""
        if self.order_type == OrderType.DINE_IN:
            if self.delivery_info is not None:
                raise ValidationError(
                    "La orden de mesa no puede incluir datos de delivery."
                )
            return

        if self.order_type == OrderType.TAKEAWAY:
            if self.table_id is not None:
                raise ValidationError(
                    "La orden para llevar no puede tener mesa asignada."
                )
            if self.delivery_info is not None:
                raise ValidationError(
                    "La orden para llevar no puede incluir delivery."
                )
            return

        if self.order_type == OrderType.DELIVERY:
            if self.delivery_info is None:
                raise ValidationError(
                    "La orden delivery requiere información de entrega."
                )
            if self.table_id is not None:
                raise ValidationError(
                    "La orden delivery no puede tener mesa asignada."
                )

    def add_item(self, item: OrderItem) -> None:
        """Add an item to the order."""
        if not isinstance(item, OrderItem):
            raise ValidationError("Ítem de orden inválido.")
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
        if not isinstance(new_state, OrderState):
            raise ValidationError("Estado inválido.")
        if self.closed:
            raise StateError("La orden está cerrada.")
        ensure_transition(self.state, new_state)
        self.state = new_state
