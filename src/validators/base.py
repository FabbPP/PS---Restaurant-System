"""Base validation helpers."""

from typing import Iterable, TypeVar

from src.exceptions.validation import ValidationError

T = TypeVar("T")


def ensure(condition: bool, message: str) -> None:
    """Ensure a condition is true or raise ValidationError."""
    if not condition:
        raise ValidationError(message)


def ensure_in(value: T, allowed: Iterable[T], field_name: str) -> None:
    """Ensure value is within allowed options."""
    if value not in allowed:
        raise ValidationError(f"{field_name} inválido: {value}")
