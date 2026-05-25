import pytest

from exceptions.validation import ValidationError
from validators.common import (validate_non_empty_str, validate_phone,
                                validate_price, validate_positive_int)


def test_validate_non_empty_str() -> None:
    assert validate_non_empty_str(" Juan ", "Nombre") == "Juan"


def test_validate_non_empty_str_empty() -> None:
    with pytest.raises(ValidationError):
        validate_non_empty_str("   ", "Nombre")


def test_validate_phone_valid() -> None:
    assert validate_phone("987654321") == "987654321"


def test_validate_phone_invalid() -> None:
    with pytest.raises(ValidationError):
        validate_phone("98A")


def test_validate_price_bounds() -> None:
    assert validate_price(10.5, "Precio") == 10.5
    with pytest.raises(ValidationError):
        validate_price(0.0, "Precio")


def test_validate_positive_int_bounds() -> None:
    assert validate_positive_int(1, "Cantidad") == 1
    with pytest.raises(ValidationError):
        validate_positive_int(0, "Cantidad")
