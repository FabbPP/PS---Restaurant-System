"""Tests for CustomerRepository integrity."""
import pytest
from src.customers.repository import CustomerRepository
from src.customers.models import DeliveryCustomer
from src.exceptions.domain import NotFoundError

def test_customer_repository_save_and_get() -> None:
    """PE: Persistencia de clientes de delivery."""
    repo = CustomerRepository()
    customer = DeliveryCustomer(id=1, name="Ana", phone="999888777")
    repo.save(customer)
    
    fetched = repo.get_by_id(1)
    assert fetched.name == "Ana"
    assert fetched.phone == "999888777"

def test_customer_not_found() -> None:
    """PE: Error al buscar cliente inexistente."""
    repo = CustomerRepository()
    with pytest.raises(NotFoundError):
        repo.get_by_id(500)