"""Common validation functions."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Optional

from src.exceptions.validation import ValidationError
from src.validators.base import ensure


def _ensure_int(value: object, field_name: str) -> int:
    """Validate a strict integer (excluding bool)."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{field_name} debe ser un número entero.")
    return value


def _ensure_length_bounds(min_len: int, max_len: int) -> None:
    """Validate minimum and maximum string length bounds."""
    _ensure_int(min_len, "Longitud mínima")
    _ensure_int(max_len, "Longitud máxima")
    ensure(min_len >= 1, "Longitud mínima debe ser >= 1.")
    ensure(max_len >= min_len,
           "Longitud máxima debe ser mayor o igual que la mínima.")


def validate_non_empty_str(value: object, field_name: str, min_len: int = 1,
                           max_len: int = 60) -> str:
    """Validate non-empty text within explicit length bounds."""
    _ensure_length_bounds(min_len, max_len)
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} debe ser texto.")

    normalized = value.strip()
    ensure(normalized != "", f"{field_name} es obligatorio.")
    ensure(len(normalized) >= min_len,
           f"{field_name} debe tener al menos {min_len} caracteres.")
    ensure(len(normalized) <= max_len,
           f"{field_name} no debe exceder {max_len} caracteres.")
    return normalized


def validate_int_range(value: object, field_name: str,
                       min_value: Optional[int] = None,
                       max_value: Optional[int] = None) -> int:
    """Validate integer range constraints with strict typing."""
    parsed_value = _ensure_int(value, field_name)

    if min_value is not None:
        _ensure_int(min_value, f"Límite mínimo de {field_name}")
    if max_value is not None:
        _ensure_int(max_value, f"Límite máximo de {field_name}")
    if min_value is not None and max_value is not None:
        ensure(min_value <= max_value,
               f"Rango inválido para {field_name}: mínimo mayor a máximo.")

    if min_value is not None:
        ensure(parsed_value >= min_value,
               f"{field_name} debe ser >= {min_value}.")
    if max_value is not None:
        ensure(parsed_value <= max_value,
               f"{field_name} debe ser <= {max_value}.")
    return parsed_value


def validate_positive_int(value: object, field_name: str, min_value: int = 1,
                          max_value: Optional[int] = None) -> int:
    """Validate a positive integer within optional bounds."""
    return validate_int_range(value, field_name, min_value=min_value,
                              max_value=max_value)


def validate_price(value: object, field_name: str, 
                   min_value: Decimal = Decimal("0.01"),
                   max_value: Decimal = Decimal("9999.99")) -> Decimal:
    """Validate a price within bounds and ensure finite numeric input."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal, str)):
        raise ValidationError(f"{field_name} debe ser numérico.")

    try:
        parsed_value = Decimal(str(value)) if not isinstance(value, str) else Decimal(value.replace(",", "."))
    except (InvalidOperation, ValueError):
        raise ValidationError(f"{field_name} debe ser un número válido.")

    ensure(parsed_value.is_finite(), f"{field_name} debe ser finito.")
    ensure(min_value <= max_value,
           f"Rango inválido para {field_name}: mínimo mayor a máximo.")
    ensure(parsed_value >= min_value,
           f"{field_name} debe ser >= {min_value}.")
    ensure(parsed_value <= max_value,
           f"{field_name} debe ser <= {max_value}.")
    return parsed_value.quantize(Decimal("0.00"))


def validate_phone(value: object, field_name: str = "Teléfono",
                   min_len: int = 9, max_len: int = 15) -> str:
    """Validate a phone number composed only of digits."""
    normalized = validate_non_empty_str(value, field_name, min_len, max_len)
    ensure(normalized.isdigit(), f"{field_name} debe contener solo dígitos.")
    return normalized


def validate_id(value: object, field_name: str) -> int:
    """Validate a positive identifier."""
    return validate_positive_int(value, field_name, min_value=1)
