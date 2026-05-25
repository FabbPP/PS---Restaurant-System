"""Tests for TableRepository integrity."""
import pytest
from src.tables.repository import TableRepository
from src.tables.models import Table
from src.exceptions.domain import NotFoundError

def test_table_repository_persistence() -> None:
    """Invariante: Los datos añadidos deben persistir y ser recuperables."""
    repo = TableRepository()
    table = Table(id=1, is_available=True)
    repo.save(table)
    
    fetched = repo.get_by_id(1)
    assert fetched == table
    assert len(repo.get_all()) == 1

def test_get_non_existent_table_raises_error() -> None:
    """PE: Buscar un ID que no existe debe lanzar NotFoundError."""
    repo = TableRepository()
    with pytest.raises(NotFoundError):
        repo.get_by_id(99)

def test_save_duplicate_id_overwrites_or_fails() -> None:
    """
    Invariante: La integridad de los IDs. 
    En repositorios in-memory simples, el segundo save suele sobreescribir.
    """
    repo = TableRepository()
    t1 = Table(id=1, is_available=True)
    t2 = Table(id=1, is_available=False)
    
    repo.save(t1)
    repo.save(t2)
    
    # Debe prevalecer el último estado guardado para ese ID
    assert len(repo.get_all()) == 1
    assert repo.get_by_id(1).is_available is False