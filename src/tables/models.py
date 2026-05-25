"""Table domain model."""

from dataclasses import dataclass

from exceptions.domain import StateError
from validators.common import validate_id


@dataclass
class Table:
    """Represents a restaurant table."""

    id: int
    is_available: bool = True

    def __post_init__(self) -> None:
        validate_id(self.id, "ID de mesa")

    def occupy(self) -> None:
        """Mark the table as occupied."""
        if not self.is_available:
            raise StateError("La mesa ya está ocupada.")
        self.is_available = False

    def release(self) -> None:
        """Mark the table as available."""
        if self.is_available:
            raise StateError("La mesa ya está libre.")
        self.is_available = True
