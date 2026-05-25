"""Tests for Customer models and data integrity."""

import pytest
from src.customers.models import DeliveryCustomer
from src.exceptions.validation import ValidationError

def test_customer_creation_valid() -> None:
    """Test: Creación válida de cliente."""
    customer = DeliveryCustomer(id=1, name="Ana Lopez", phone="999888777")
    assert customer.name == "Ana Lopez"
    assert customer.phone == "999888777"

def test_customer_name_normalization() -> None:
    """Test: Los nombres deben limpiarse de espacios (PE: Normalización)."""
    customer = DeliveryCustomer(id=1, name="  Pedro Pascal  ", phone="999888777")
    # Asumiendo que el __post_init__ o el validador limpia el string
    assert customer.name == "Pedro Pascal"

@pytest.mark.parametrize("invalid_phone", [
    "12345678",        # AVL: Muy corto (8 dígitos)
    "1" * 16,          # AVL: Muy largo (16 dígitos)
    "999-888-777",     # PE: Caracteres no permitidos (guiones)
    "999 888 777",     # PE: Espacios internos
    "abc999888",       # PE: Alfanumérico
    "",                # PE: Vacío
])
def test_customer_invalid_phones(invalid_phone: str) -> None:
    """Test: Validación estricta del formato de teléfono (PE + AVL)."""
    with pytest.raises(ValidationError):
        DeliveryCustomer(id=1, name="Cliente Test", phone=invalid_phone)

def test_customer_extreme_names() -> None:
    """Test: Límites de caracteres en nombres (AVL)."""
    # Límite superior: 60 caracteres (según IMPLEMENTS.md)
    long_name = "A" * 60
    customer = DeliveryCustomer(id=1, name=long_name, phone="999888777")
    assert len(customer.name) == 60

    with pytest.raises(ValidationError):
        DeliveryCustomer(id=1, name="A" * 61, phone="999888777")

@pytest.mark.parametrize("bad_id", [0, -5, "id1"])
def test_customer_id_robustness(bad_id: any) -> None:
    """Test: Validación de ID de cliente."""
    with pytest.raises((ValidationError, TypeError)):
        DeliveryCustomer(id=bad_id, name="Test", phone="999888777")

def test_customer_empty_name() -> None:
    """Test: El nombre no puede ser solo espacios o vacío."""
    with pytest.raises(ValidationError):
        DeliveryCustomer(id=1, name="   ", phone="999888777")