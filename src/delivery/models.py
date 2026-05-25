"""Delivery domain model."""

from dataclasses import dataclass

from validators.common import validate_id, validate_non_empty_str, validate_phone


@dataclass
class DeliveryInfo:
    """Delivery-specific information."""

    customer_id: int
    address: str
    phone: str

    def __post_init__(self) -> None:
        validate_id(self.customer_id, "ID de cliente")
        self.address = validate_non_empty_str(self.address, "Dirección", min_len=5,
                                              max_len=120)
        self.phone = validate_phone(self.phone, "Teléfono")
