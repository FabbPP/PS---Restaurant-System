"""Customer services (use cases)."""

from typing import List

from customers.models import DeliveryCustomer
from customers.repository import CustomerRepository
from customers.validators import validate_customer_name, validate_customer_phone


class CustomerService:
    """Application service for delivery customers."""

    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    def add_customer(self, name: str, phone: str) -> DeliveryCustomer:
        """Create a new customer."""
        valid_name = validate_customer_name(name)
        valid_phone = validate_customer_phone(phone)
        return self._repository.create(valid_name, valid_phone)

    def get_customer(self, customer_id: int) -> DeliveryCustomer:
        """Get a customer by ID."""
        return self._repository.get(customer_id)

    def list_customers(self) -> List[DeliveryCustomer]:
        """List all customers."""
        return self._repository.list_all()
