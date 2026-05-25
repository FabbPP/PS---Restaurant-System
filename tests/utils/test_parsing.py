"""Tests for safe data parsing from raw string inputs."""
import pytest
from decimal import Decimal

from src.exceptions.validation import ValidationError
from src.utils.parsing import parse_decimal, parse_int

def test_parse_int_valid() -> None:
    """PE: Conversión exitosa con limpieza de espacios."""
    assert parse_int("10", "ID") == 10
    assert parse_int("  5  ", "ID") == 5


@pytest.mark.parametrize("bad_input", ["abc", "10.5", "None"])
def test_parse_int_invalid(bad_input: str) -> None:
    """PE: Entradas no numéricas o mal formadas para enteros."""
    with pytest.raises(ValidationError, match="debe ser un número entero"):
        parse_int(bad_input, "ID")

@pytest.mark.parametrize("empty_input", ["", " "])
def test_parse_int_empty(empty_input: str) -> None:
    """PE: Entradas vacías."""
    with pytest.raises(ValidationError, match="es obligatorio"):
        parse_int(empty_input, "ID")


def test_parse_decimal_valid() -> None:
    """PE: Conversión exitosa a Decimal."""
    assert parse_decimal("12.5", "Monto") == Decimal("12.5")
    assert parse_decimal("  0.99  ", "Monto") == Decimal("0.99")
    assert parse_decimal("12,5", "Monto") == Decimal("12.5")

@pytest.mark.parametrize("bad_input", ["x", "---", "inf", "nan"])
def test_parse_decimal_invalid(bad_input: str) -> None:
    """PE/Robustez: Entradas inválidas para montos monetarios."""
    with pytest.raises(ValidationError, match="Monto debe ser un número"):
        parse_decimal(bad_input, "Monto")


def test_parse_extreme_overflow() -> None:
    """Robustez: Manejo de números absurdamente grandes."""
    extreme = "9" * 1001
    with pytest.raises(ValidationError, match="demasiado largo"):
        parse_int(extreme, "Mucho")