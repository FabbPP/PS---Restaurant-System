"""Common validation functions."""

from __future__ import annotations

import math
from typing import Optional

from exceptions.validation import ValidationError
from validators.base import ensure


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


def validate_price(value: object, field_name: str, min_value: float = 0.01,
                   max_value: float = 9999.99) -> float:
    """Validate a price within bounds and ensure finite numeric input."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{field_name} debe ser numérico.")
    if isinstance(min_value, bool) or not isinstance(min_value, (int, float)):
        raise ValidationError(f"Límite mínimo de {field_name} inválido.")
    if isinstance(max_value, bool) or not isinstance(max_value, (int, float)):
        raise ValidationError(f"Límite máximo de {field_name} inválido.")

    parsed_value = float(value)
    parsed_min = float(min_value)
    parsed_max = float(max_value)

    ensure(math.isfinite(parsed_value), f"{field_name} debe ser finito.")
    ensure(math.isfinite(parsed_min),
           f"Límite mínimo de {field_name} debe ser finito.")
    ensure(math.isfinite(parsed_max),
           f"Límite máximo de {field_name} debe ser finito.")
    ensure(parsed_min <= parsed_max,
           f"Rango inválido para {field_name}: mínimo mayor a máximo.")
    ensure(parsed_value >= parsed_min,
           f"{field_name} debe ser >= {parsed_min}.")
    ensure(parsed_value <= parsed_max,
           f"{field_name} debe ser <= {parsed_max}.")
    return round(parsed_value, 2)


def validate_phone(value: object, field_name: str = "Teléfono",
                   min_len: int = 9, max_len: int = 15) -> str:
    """Validate a phone number composed only of digits."""
    normalized = validate_non_empty_str(value, field_name, min_len, max_len)
    ensure(normalized.isdigit(), f"{field_name} debe contener solo dígitos.")
    return normalized


def validate_id(value: object, field_name: str) -> int:
    """Validate a positive identifier."""
    return validate_positive_int(value, field_name, min_value=1)
