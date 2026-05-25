"""Customer validators."""

from src.validators.common import validate_non_empty_str, validate_phone


def validate_customer_name(name: str) -> str:
    """Validate customer name."""
    return validate_non_empty_str(name, "Nombre de cliente")


def validate_customer_phone(phone: str) -> str:
    """Validate customer phone."""
    return validate_phone(phone, "Teléfono")
