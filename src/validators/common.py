"""Common validation functions."""

from typing import Optional

from exceptions.validation import ValidationError
from validators.base import ensure


def validate_non_empty_str(value: str, field_name: str, min_len: int = 1,
                           max_len: int = 60) -> str:
    """Validate a non-empty string within length bounds."""
    if value is None:
        raise ValidationError(f"{field_name} es obligatorio.")
    normalized = value.strip()
    ensure(normalized != "", f"{field_name} es obligatorio.")
    ensure(len(normalized) >= min_len,
           f"{field_name} debe tener al menos {min_len} caracteres.")
    ensure(len(normalized) <= max_len,
           f"{field_name} no debe exceder {max_len} caracteres.")
    return normalized


def validate_int_range(value: int, field_name: str, min_value: Optional[int] = None,
                       max_value: Optional[int] = None) -> int:
    """Validate integer range constraints."""
    if min_value is not None:
        ensure(value >= min_value,
               f"{field_name} debe ser >= {min_value}.")
    if max_value is not None:
        ensure(value <= max_value,
               f"{field_name} debe ser <= {max_value}.")
    return value


def validate_positive_int(value: int, field_name: str, min_value: int = 1,
                          max_value: Optional[int] = None) -> int:
    """Validate a positive integer within optional bounds."""
    return validate_int_range(value, field_name, min_value=min_value,
                              max_value=max_value)


def validate_price(value: float, field_name: str, min_value: float = 0.01,
                   max_value: float = 9999.99) -> float:
    """Validate a price within bounds."""
    ensure(value >= min_value,
           f"{field_name} debe ser >= {min_value}.")
    ensure(value <= max_value,
           f"{field_name} debe ser <= {max_value}.")
    return round(value, 2)


def validate_phone(value: str, field_name: str = "Teléfono",
                   min_len: int = 9, max_len: int = 15) -> str:
    """Validate a phone number composed only of digits."""
    normalized = validate_non_empty_str(value, field_name, min_len, max_len)
    ensure(normalized.isdigit(), f"{field_name} debe contener solo dígitos.")
    return normalized


def validate_id(value: int, field_name: str) -> int:
    """Validate a positive identifier."""
    return validate_positive_int(value, field_name, min_value=1)
