import pytest

from exceptions.validation import ValidationError
from tables.validators import validate_table_id


def test_validate_table_id_valid() -> None:
    assert validate_table_id(1) == 1


def test_validate_table_id_invalid() -> None:
    with pytest.raises(ValidationError):
        validate_table_id(0)
