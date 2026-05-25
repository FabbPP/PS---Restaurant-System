"""Delivery validators."""

from validators.common import validate_non_empty_str, validate_phone


def validate_address(address: str) -> str:
    """Validate delivery address."""
    return validate_non_empty_str(address, "Dirección", min_len=5, max_len=120)


def validate_delivery_phone(phone: str) -> str:
    """Validate delivery phone."""
    return validate_phone(phone, "Teléfono")
