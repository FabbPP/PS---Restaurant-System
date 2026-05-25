"""Delivery customer model."""

from dataclasses import dataclass

from validators.common import validate_id, validate_non_empty_str, validate_phone


@dataclass
class DeliveryCustomer:
    """Represents a delivery customer."""

    id: int
    name: str
    phone: str

    def __post_init__(self) -> None:
        validate_id(self.id, "ID de cliente")
        self.name = validate_non_empty_str(self.name, "Nombre de cliente")
        self.phone = validate_phone(self.phone, "Teléfono")
