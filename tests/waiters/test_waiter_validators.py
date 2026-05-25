"""Tests for waiter-specific validators using PE and AVL."""
import pytest
from src.exceptions.validation import ValidationError
from src.validators.common import validate_non_empty_str

def test_waiter_name_valid() -> None:
    """PE: Nombre estándar válido."""
    name = "Juan Perez"
    assert validate_non_empty_str(name, "Nombre") == name

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