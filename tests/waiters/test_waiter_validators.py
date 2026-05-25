"""Tests for waiter-specific validators using PE and AVL."""
import pytest
from src.exceptions.validation import ValidationError
from src.validators.common import validate_non_empty_str
from src.waiters.validators import validate_waiter_name

def test_waiter_name_valid() -> None:
    """PE: Nombre estándar válido."""
    name = "Juan Perez"
    # Verificamos tanto la limpieza de espacios como la validación de caracteres
    cleansed = validate_non_empty_str(name, "Nombre")
    assert validate_waiter_name(cleansed) == name

def test_waiter_name_with_numbers() -> None:
    """CP-1.01: Validar rechazo de nombres que contengan caracteres numéricos."""
    with pytest.raises(ValidationError, match="solo debe contener letras y espacios"):
        validate_waiter_name("Luis123")

@pytest.mark.parametrize("invalid_name", [
    "",             # PE: Vacío
    "   ",          # PE: Solo espacios
    "A" * 61,       # AVL: Max + 1
])
def test_waiter_name_invalid(invalid_name: str) -> None:
    """PE/AVL: Validación de longitudes y contenido de nombres."""
    with pytest.raises(ValidationError):
        validate_non_empty_str(invalid_name, "Nombre", min_len=1, max_len=60)

def test_waiter_name_boundary_limits() -> None:
    """AVL: Verificación de límites exactos."""
    # Mínimo 1 carácter
    assert len(validate_non_empty_str("X", "Nombre", min_len=1)) == 1
    # Máximo 60 caracteres
    max_str = "M" * 60
    assert validate_non_empty_str(max_str, "Nombre", max_len=60) == max_str