"""Table-specific validators."""

from src.validators.common import validate_id


def validate_table_id(table_id: int) -> int:
    """Validate table ID."""
    return validate_id(table_id, "ID de mesa")
