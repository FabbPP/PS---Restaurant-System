"""Tests for table-specific validators using PE and AVL."""
import pytest
from src.exceptions.validation import ValidationError
from src.tables.validators import validate_table_id

def test_validate_table_id_valid() -> None:
    """AVL: ID mínimo válido (1)."""
    assert validate_table_id(1) == 1

@pytest.mark.parametrize("invalid_id", [
    0,      # AVL: Justo debajo del límite
    -1,     # PE: Número negativo
    -999    # PE: Negativo extremo
])
def test_validate_table_id_invalid(invalid_id: int) -> None:
    """PE/AVL: IDs fuera de rango permitido."""
    with pytest.raises(ValidationError, match="ID de mesa"):
        validate_table_id(invalid_id)
