"""Tests for common/shared validators using PE and AVL."""
import pytest
from src.exceptions.validation import ValidationError
from src.validators.common import (validate_non_empty_str, validate_phone,
                                validate_price, validate_positive_int)

def test_validate_non_empty_str() -> None:
    """PE: Validación de limpieza de espacios y strings válidos."""
    assert validate_non_empty_str(" Juan ", "Nombre") == "Juan"

def test_validate_non_empty_str_empty() -> None:
    """PE: Detección de strings vacíos o solo espacios."""
    with pytest.raises(ValidationError, match="no puede estar vacío"):
        validate_non_empty_str("   ", "Nombre")

@pytest.mark.parametrize("invalid_str", [
    "A" * 61,  # AVL: Supera el máximo por defecto (60)
    "",        # PE: Vacío total
])
def test_validate_str_limits(invalid_str: str) -> None:
    """AVL: Verificación de límites de longitud."""
    with pytest.raises(ValidationError):
        validate_non_empty_str(invalid_str, "Test", min_len=1, max_len=60)

def test_validate_phone_valid() -> None:
    """PE: Formato de teléfono estándar."""
    assert validate_phone("987654321") == "987654321"

@pytest.mark.parametrize("bad_phone", [
    "98A",         # PE: Contiene letras
    "12345678",    # AVL: Muy corto (8 dígitos)
    "1" * 16       # AVL: Muy largo (16 dígitos)
])
def test_validate_phone_invalid(bad_phone: str) -> None:
    """PE/AVL: Teléfonos con formato incorrecto."""
    with pytest.raises(ValidationError, match="formato de teléfono"):
        validate_phone("98A")

def test_validate_price_bounds() -> None:
    """AVL: Verificación de precios positivos y límites mínimos."""
    assert validate_price(10.5, "Precio") == 10.5
    assert validate_price(0.01, "Precio") == 0.01
    with pytest.raises(ValidationError):
        validate_price(0.0, "Precio")
    with pytest.raises(ValidationError):
        validate_price(-1.0, "Precio")

def test_validate_positive_int_bounds() -> None:
    """AVL: Verificación de enteros positivos."""
    assert validate_positive_int(1, "Cantidad") == 1
    with pytest.raises(ValidationError):
        validate_positive_int(0, "Cantidad")
