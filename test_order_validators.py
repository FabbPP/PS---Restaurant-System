"""Tests for Order Validators to cover logic paths and FSM constraints."""
from decimal import Decimal
import pytest
from src.orders.models import OrderItem
from src.orders.validators import parse_order_state
from src.orders.states import OrderState
from src.exceptions.validation import ValidationError

@pytest.mark.parametrize("input_text, expected_state", [
    ("pendiente", OrderState.PENDING),
    ("PREPARANDO", OrderState.PREPARING),
    ("  entregado  ", OrderState.DELIVERED),
    ("cancelado", OrderState.CANCELED),
])
def test_parse_order_state_valid(input_text, expected_state):
    """PE: Entradas válidas para estados, incluyendo variaciones de mayúsculas/espacios."""
    assert parse_order_state(input_text) == expected_state

@pytest.mark.parametrize("invalid_input", [
    "cocinando",
    "123",
    "",
    "nulo",
    "ready" # Asumiendo que usamos español según el controlador
])
def test_parse_order_state_invalid(invalid_input):
    """AVL/PE: Entradas que no mapean a la máquina de estados."""
    with pytest.raises(ValidationError, match="Estado inválido"):
        parse_order_state(invalid_input)

def test_validate_order_item_price_boundary():
    """TC-3.03: Validar precisión mínima de precio (AVL)."""
    item = OrderItem(name="Test", quantity=1, unit_price=Decimal("0.01"))
    assert item.unit_price == Decimal("0.01")

def test_validate_order_item_empty_name():
    """TC-3.04: Rechazo de ítems con nombre vacío (PE)."""
    with pytest.raises(ValidationError):
        OrderItem(name="   ", quantity=1, unit_price=Decimal("10.00"))