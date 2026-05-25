"""Safe parsing helpers for CLI inputs."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from src.exceptions.validation import ValidationError

def parse_int(value: object, field_name: str) -> int:
    """Parse an integer from text or integer input."""
    if isinstance(value, bool):
        raise ValidationError(f"{field_name} debe ser un número entero.")
    if isinstance(value, int):
        return value
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} debe ser texto o entero.")

    text = value.strip()
    if text == "":
        raise ValidationError(f"{field_name} es obligatorio.")

    if len(text) > 1000:
        raise ValidationError(f"{field_name} es demasiado largo.")

    try:
        return int(text)
    except ValueError as exc:
        raise ValidationError(f"{field_name} debe ser un número entero.") from exc


def parse_decimal(value: object, field_name: str) -> Decimal:
    """Parse a Decimal from text or numeric input."""
    if isinstance(value, bool):
        raise ValidationError(f"{field_name} debe ser un número válido.")

    parsed: Decimal
    if isinstance(value, (int, float, Decimal)):
        parsed = Decimal(str(value))
    elif isinstance(value, str):
        text = value.strip()
        if text == "":
            raise ValidationError(f"{field_name} es obligatorio.")

        normalized = text.replace(",", ".")
        try:
            parsed = Decimal(normalized)
        except (InvalidOperation, ValueError) as exc:
            raise ValidationError(
                f"{field_name} debe ser un número válido."
            ) from exc
    else:
        raise ValidationError(f"{field_name} debe ser texto o numérico.")

    if not parsed.is_finite():
        raise ValidationError(f"{field_name} debe ser un número finito.")
    return parsed
