"""Order states and transitions."""

from enum import Enum
from typing import Dict, Set

from exceptions.domain import StateError


class OrderState(str, Enum):
    """Order state enum."""

    PENDING = "pendiente"
    PREPARING = "preparando"
    DELIVERED = "entregado"
    CANCELED = "cancelado"


ALLOWED_TRANSITIONS: Dict[OrderState, Set[OrderState]] = {
    OrderState.PENDING: {OrderState.PREPARING, OrderState.CANCELED},
    OrderState.PREPARING: {OrderState.DELIVERED, OrderState.CANCELED},
    OrderState.DELIVERED: set(),
    OrderState.CANCELED: set(),
}


def ensure_transition(current_state: OrderState, new_state: OrderState) -> None:
    """Ensure a state transition is valid."""
    allowed = ALLOWED_TRANSITIONS.get(current_state, set())
    if new_state not in allowed:
        raise StateError(
            f"Transición inválida: {current_state.value} → {new_state.value}."
        )
