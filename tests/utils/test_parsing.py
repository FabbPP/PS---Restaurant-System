import pytest

from exceptions.validation import ValidationError
from utils.parsing import parse_float, parse_int


def test_parse_int_valid() -> None:
    assert parse_int("10", "ID") == 10


def test_parse_int_invalid() -> None:
    with pytest.raises(ValidationError):
        parse_int("abc", "ID")


def test_parse_float_valid() -> None:
    assert parse_float("12.5", "Monto") == 12.5


def test_parse_float_invalid() -> None:
    with pytest.raises(ValidationError):
        parse_float("x", "Monto")
