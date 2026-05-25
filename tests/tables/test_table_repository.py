"""Tests for TableRepository integrity."""
import pytest
from src.tables.repository import TableRepository
from src.tables.models import Table
from src.exceptions.domain import NotFoundError, ConflictError

def test_table_repository_persistence() -> None:
    """Invariante: Los datos añadidos deben persistir y ser recuperables."""
    repo = TableRepository()
    table = Table(id=1, is_available=True)
    repo.add(table)
    
    fetched = repo.get(1)
    assert fetched == table
    assert len(repo.list_all()) == 1

def test_get_non_existent_table_raises_error() -> None:
    """PE: Buscar un ID que no existe debe lanzar NotFoundError."""
    repo = TableRepository()
    with pytest.raises(NotFoundError):
        repo.get(99)

def test_save_duplicate_id_fails() -> None:
    """
    Invariante: La integridad de los IDs. 
    """
    repo = TableRepository()
    t1 = Table(id=1, is_available=True)
    t2 = Table(id=1, is_available=False)
    
    repo.add(t1)
    with pytest.raises(ConflictError):
        repo.add(t2)