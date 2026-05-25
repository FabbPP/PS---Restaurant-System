"""Order validators and parsers."""

from exceptions.validation import ValidationError
from orders.models import OrderType
from orders.states import OrderState
from validators.base import ensure_in


def parse_order_type(value: object) -> OrderType:
    """Parse order type from text."""
    if not isinstance(value, str):
        raise ValidationError("Tipo de orden debe ser texto.")

    text = value.strip().lower()
    if text == "":
        raise ValidationError("Tipo de orden es obligatorio.")

    mapping = {
        "mesa": OrderType.DINE_IN,
        "llevar": OrderType.TAKEAWAY,
        "delivery": OrderType.DELIVERY,
    }
    if text not in mapping:
        raise ValidationError("Tipo de orden inválido.")
    return mapping[text]


def parse_order_state(value: object) -> OrderState:
    """Parse order state from text."""
    if not isinstance(value, str):
        raise ValidationError("Estado debe ser texto.")

    text = value.strip().lower()
    if text == "":
        raise ValidationError("Estado es obligatorio.")

    for state in OrderState:
        if state.value == text:
            return state
    raise ValidationError("Estado inválido.")


def validate_state_value(state: OrderState) -> OrderState:
    """Validate the state is a valid OrderState."""
    ensure_in(state, list(OrderState), "Estado")
    return state
