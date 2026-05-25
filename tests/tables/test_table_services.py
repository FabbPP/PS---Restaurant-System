"""Tests for TableService and Table model logic."""

import pytest
from src.tables.services import TableService
from src.tables.repository import TableRepository
from src.exceptions.domain import StateError, NotFoundError
from src.exceptions.validation import ValidationError

@pytest.fixture
def table_service() -> TableService:
    """Fresh TableService for each test."""
    return TableService(TableRepository())

def test_add_multiple_tables_incremental_ids(table_service: TableService) -> None:
    """Test: Generación incremental de IDs de mesas."""
    t1 = table_service.add_table()
    t2 = table_service.add_table()
    assert t1.id == 1
    assert t2.id == 2
    assert t1.is_available is True

def test_occupy_and_release_flow(table_service: TableService) -> None:
    """Test: Flujo completo de estado de una mesa."""
    table = table_service.add_table()
    
    # Ocupar
    table_service.occupy_table(table.id)
    assert table_service.get_table(table.id).is_available is False
    
    # Liberar
    table_service.release_table(table.id)
    assert table_service.get_table(table.id).is_available is True

def test_occupy_already_occupied_raises_error(table_service: TableService) -> None:
    """Test: Intento de ocupar una mesa ya ocupada (PE: Conflicto)."""
    table = table_service.add_table()
    table_service.occupy_table(table.id)
    
    with pytest.raises(StateError, match="ya está ocupada"):
        table_service.occupy_table(table.id)

def test_release_already_free_raises_error(table_service: TableService) -> None:
    """Test: Intento de liberar una mesa ya libre (PE: Conflicto)."""
    table = table_service.add_table()
    with pytest.raises(StateError, match="ya está libre"):
        table_service.release_table(table.id)

def test_get_non_existent_table(table_service: TableService) -> None:
    """Test: Búsqueda de mesa inexistente (PE: Referencia)."""
    with pytest.raises(NotFoundError):
        table_service.get_table(999)

@pytest.mark.parametrize("invalid_id", [0, -1, -99])
def test_table_id_validation_limits(table_service: TableService, invalid_id: int) -> None:
    """Test: IDs inválidos (AVL: Límites inferiores)."""
    # Dependiendo de si el repositorio o el servicio validan el ID al buscar
    with pytest.raises(ValidationError):
        table_service.get_table(invalid_id)

@pytest.mark.parametrize("bad_input", ["uno", None, 1.5])
def test_table_service_type_robustness(table_service: TableService, bad_input: any) -> None:
    """Test: Robustez ante tipos de ID incorrectos."""
    with pytest.raises((ValidationError, TypeError)):
        table_service.occupy_table(bad_input)

def test_ensure_available_logic(table_service: TableService) -> None:
    """Test: Validación de disponibilidad para procesos externos."""
    table = table_service.add_table()
    table_service.ensure_available(table.id)  # No debe lanzar nada
    
    table_service.occupy_table(table.id)
    with pytest.raises(Exception): # ConflictError o ValidationError según tu impl.
        table_service.ensure_available(table.id)