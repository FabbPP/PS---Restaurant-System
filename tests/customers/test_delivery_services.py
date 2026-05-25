"""Tests for DeliveryService and DeliveryInfo logic."""
import pytest
from src.delivery.services import DeliveryService
from src.delivery.models import DeliveryInfo
from src.exceptions.validation import ValidationError
from src.customers.services import CustomerService
from src.customers.repository import CustomerRepository

@pytest.fixture
def delivery_service() -> DeliveryService:
    return DeliveryService(CustomerService(CustomerRepository()))

def test_create_delivery_info_valid() -> None:
    """PE: Datos de entrega correctos."""
    info = DeliveryInfo(customer_id=1, address="Calle Falsa 123", phone="987654321")
    assert info.address == "Calle Falsa 123"
    assert info.phone == "987654321"

@pytest.mark.parametrize("bad_phone", [
    "12345678",        # AVL: < 9 dígitos
    "1" * 16,          # AVL: > 15 dígitos
    "tele-fono1",      # PE: Caracteres no numéricos
    "",                # PE: Vacío
])
def test_delivery_info_invalid_phone(bad_phone: str) -> None:
    """PE/AVL: Validación rigurosa de teléfonos de despacho."""
    with pytest.raises(ValidationError):
        DeliveryInfo(customer_id=1, address="Calle Valida 123", phone=bad_phone)

@pytest.mark.parametrize("bad_address", [
    "ABC",             # AVL: < 5 caracteres
    "A" * 121,         # AVL: > 120 caracteres
    "   ",             # PE: Solo espacios
])
def test_delivery_info_invalid_address(bad_address: str) -> None:
    """PE/AVL: Validación de longitud de dirección."""
    with pytest.raises(ValidationError):
        DeliveryInfo(customer_id=1, address=bad_address, phone="999888777")

def test_delivery_assignment(delivery_service: DeliveryService) -> None:
    """Test: Simulación de flujo de asignación (si aplica al servicio)."""
    # Asumiendo que el servicio maneja estados de despacho
    # Este es un placeholder para la lógica específica de tu delivery_service
    pass