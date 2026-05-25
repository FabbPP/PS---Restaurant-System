"""Order validators and parsers."""

from exceptions.validation import ValidationError
from orders.models import OrderType
from orders.states import OrderState
from validators.base import ensure_in


def parse_order_type(value: str) -> OrderType:
    """Parse order type from text."""
    if value is None:
        raise ValidationError("Tipo de orden es obligatorio.")
    text = value.strip().lower()
    mapping = {
        "mesa": OrderType.DINE_IN,
        "llevar": OrderType.TAKEAWAY,
        "delivery": OrderType.DELIVERY,
    }
    if text not in mapping:
        raise ValidationError("Tipo de orden inválido.")
    return mapping[text]


def parse_order_state(value: str) -> OrderState:
    """Parse order state from text."""
    if value is None:
        raise ValidationError("Estado es obligatorio.")
    text = value.strip().lower()
    for state in OrderState:
        if state.value == text:
            return state
    raise ValidationError("Estado inválido.")


def validate_state_value(state: OrderState) -> OrderState:
    """Validate the state is a valid OrderState."""
    ensure_in(state, list(OrderState), "Estado")
    return state
