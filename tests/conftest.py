"""Shared fixtures and test configuration for the Restaurant System."""

import pytest
from decimal import Decimal
from typing import Dict, Any

from src.orders.models import Order, OrderItem, OrderType
from src.orders.states import OrderState
from src.orders.repository import OrderRepository
from src.orders.services import OrderService
from src.tables.models import Table
from src.tables.repository import TableRepository
from src.waiters.repository import WaiterRepository
from src.customers.repository import CustomerRepository
from src.tables.services import TableService
from src.waiters.services import WaiterService
from src.customers.services import CustomerService
from src.delivery.services import DeliveryService

# -------------------------------------------------------------------------
# REPOSITORY & SERVICE FIXTURES (Infrastructure & Application)
# -------------------------------------------------------------------------

@pytest.fixture
def order_repository() -> OrderRepository:
    """Provides a fresh in-memory order repository."""
    return OrderRepository()

@pytest.fixture
def table_service() -> TableService:
    """Provides a table service. 
    Inyectamos un TableRepository real para las pruebas."""
    return TableService(TableRepository())

@pytest.fixture
def waiter_service() -> WaiterService:
    """Provides a waiter service."""
    return WaiterService(WaiterRepository())

@pytest.fixture
def customer_service() -> CustomerService:
    """Provides a customer service."""
    return CustomerService(CustomerRepository())

@pytest.fixture
def delivery_service(customer_service) -> DeliveryService:
    """Provides a delivery service."""
    return DeliveryService(customer_service)

@pytest.fixture
def order_service(order_repository, table_service, delivery_service) -> OrderService:
    """Provides a fully wired OrderService."""
    return OrderService(
        repository=order_repository,
        table_service=table_service,
        delivery_service=delivery_service
    )

# -------------------------------------------------------------------------
# DOMAIN OBJECT FIXTURES (Entities)
# -------------------------------------------------------------------------

@pytest.fixture
def valid_table() -> Table:
    """Returns a valid Table instance (AVL: ID=1)."""
    return Table(id=1, is_available=True)

@pytest.fixture
def valid_order_item() -> OrderItem:
    """Returns a valid OrderItem (PE: Standard valid class)."""
    return OrderItem(name="Pizza Margarita", quantity=2, unit_price=Decimal("15.50"))

@pytest.fixture
def pending_dine_in_order() -> Order:
    """Returns a valid DINE_IN order in PENDING state."""
    return Order(id=101, order_type=OrderType.DINE_IN, table_id=1)

# -------------------------------------------------------------------------
# BLACK BOX TESTING DATA (PE + AVL)
# -------------------------------------------------------------------------

@pytest.fixture
def raw_data_pe_avl() -> Dict[str, Any]:
    """
    Centralized catalog of test data for Equivalence Partitioning and 
    Boundary Value Analysis. Used to feed @pytest.mark.parametrize.
    """
    return {
        "names": {
            "valid": "Sopa de Pollo",
            "boundary_min": "A",           # AVL: 1 char
            "boundary_max": "A" * 60,      # AVL: 60 chars
            "invalid_empty": "",           # PE: Invalid Empty
            "invalid_too_long": "A" * 61,  # AVL: Max + 1
            "invalid_whitespace": "   "    # PE: Blank string
        },
        "quantities": {
            "valid": 5,
            "boundary_min": 1,             # AVL: Min
            "boundary_max": 99,            # AVL: Max
            "invalid_zero": 0,             # AVL: Min - 1
            "invalid_negative": -1,        # PE: Negative
            "invalid_too_high": 100,       # AVL: Max + 1
            "invalid_type": "cinco"        # PE: Wrong Type
        },
        "prices": {
            "valid": Decimal("25.50"),
            "boundary_min": Decimal("0.01"),          # AVL: Minimum positive
            "boundary_max": Decimal("9999.99"),       # AVL: Logical Max
            "invalid_zero": Decimal("0.00"),          # PE: Zero price
            "invalid_negative": Decimal("-0.01"),     # PE: Negative
            "invalid_inf": Decimal('Infinity'),       # Robustness: Infinity
            "invalid_nan": Decimal('NaN')             # Robustness: Not a Number
        },
        "ids": {
            "valid": 1,
            "invalid_zero": 0,             # AVL: Boundary failure
            "invalid_negative": -5,        # PE: Invalid class
            "invalid_type": "id_string"    # PE: Wrong type
        },
        "phones": {
            "valid": "999888777",          # PE: 9 digits
            "boundary_max": "1" * 15,      # AVL: 15 digits
            "invalid_short": "12345678",   # AVL: 8 digits (too short)
            "invalid_long": "1" * 16,      # AVL: 16 digits (too long)
            "invalid_chars": "999-ABC-77"  # PE: Non-numeric
        }
    }

@pytest.fixture(autouse=True)
def clear_repositories(order_repository):
    """Ensures a clean state between tests for in-memory storage."""
    yield
    # Si los repositorios son singletons o persistentes en sesión,
    # aquí se limpiarían sus diccionarios internos.