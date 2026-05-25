"""Safe parsing helpers for CLI inputs."""

from exceptions.validation import ValidationError


def parse_int(value: str, field_name: str) -> int:
    """Parse an integer from text."""
    if value is None:
        raise ValidationError(f"{field_name} es obligatorio.")
    text = value.strip()
    if text == "":
        raise ValidationError(f"{field_name} es obligatorio.")
    try:
        return int(text)
    except ValueError as exc:
        raise ValidationError(f"{field_name} debe ser un número entero.") from exc


def parse_float(value: str, field_name: str) -> float:
    """Parse a float from text."""
    if value is None:
        raise ValidationError(f"{field_name} es obligatorio.")
    text = value.strip()
    if text == "":
        raise ValidationError(f"{field_name} es obligatorio.")
    try:
        return float(text)
    except ValueError as exc:
        raise ValidationError(f"{field_name} debe ser un número válido.") from exc
