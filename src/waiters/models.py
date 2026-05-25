"""Waiter domain model."""

from dataclasses import dataclass

from src.validators.common import validate_id, validate_non_empty_str


@dataclass
class Waiter:
    """Represents a waiter."""

    id: int
    name: str

    def __post_init__(self) -> None:
        validate_id(self.id, "ID de mesero")
        self.name = validate_non_empty_str(self.name, "Nombre de mesero")
