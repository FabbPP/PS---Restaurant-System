"""Waiter validators."""

from validators.common import validate_non_empty_str


def validate_waiter_name(name: str) -> str:
    """Validate waiter name."""
    return validate_non_empty_str(name, "Nombre de mesero")
