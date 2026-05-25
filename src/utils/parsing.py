"""Safe parsing helpers for CLI inputs."""

from __future__ import annotations

import math
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


def parse_float(value: object, field_name: str) -> float:
    """Parse a float from text or numeric input."""
    if isinstance(value, bool):
        raise ValidationError(f"{field_name} debe ser un número válido.")

    parsed: float
    if isinstance(value, (int, float)):
        parsed = float(value)
    elif isinstance(value, str):
        text = value.strip()
        if text == "":
            raise ValidationError(f"{field_name} es obligatorio.")

        normalized = text.replace(",", ".")
        try:
            parsed = float(normalized)
        except ValueError as exc:
            raise ValidationError(
                f"{field_name} debe ser un número válido."
            ) from exc
    else:
        raise ValidationError(f"{field_name} debe ser texto o numérico.")

    if not math.isfinite(parsed):
        raise ValidationError(f"{field_name} debe ser un número finito.")
    return parsed
