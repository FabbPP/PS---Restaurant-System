"""Delivery services (use cases)."""

from src.customers.services import CustomerService
from src.delivery.models import DeliveryInfo
from src.delivery.validators import validate_address, validate_delivery_phone
from src.validators.common import validate_id


class DeliveryService:
    """Application service for delivery data."""

    def __init__(self, customer_service: CustomerService) -> None:
        self._customer_service = customer_service

    def create_info(self, customer_id: int, address: str, phone: str) -> DeliveryInfo:
        """Create validated delivery info."""
        valid_customer_id = validate_id(customer_id, "ID de cliente")
        self._customer_service.get_customer(valid_customer_id)
        valid_address = validate_address(address)
        valid_phone = validate_delivery_phone(phone)
        return DeliveryInfo(customer_id=valid_customer_id,
                            address=valid_address,
                            phone=valid_phone)
