"""Tests for WaiterRepository integrity."""
import pytest
from src.waiters.repository import WaiterRepository
from src.waiters.models import Waiter
from src.exceptions.domain import NotFoundError

def test_waiter_repository_crud() -> None:
    """PE: Flujo básico de almacenamiento de meseros."""
    repo = WaiterRepository()
    waiter = Waiter(id=1, name="Luis")
    repo.save(waiter)
    
    assert repo.get_by_id(1).name == "Luis"
    assert len(repo.get_all()) == 1

def test_waiter_not_found() -> None:
    """PE: Error al buscar mesero inexistente."""
    repo = WaiterRepository()
    with pytest.raises(NotFoundError):
        repo.get_by_id(404)

def test_list_waiters_empty() -> None:
    """Estado inicial: Lista vacía."""
    repo = WaiterRepository()
    assert repo.get_all() == []