import pytest

from exceptions.domain import ConflictError
from tables.repository import TableRepository
from tables.services import TableService


def test_add_table_and_occupy() -> None:
    service = TableService(TableRepository())
    table = service.add_table()
    service.occupy_table(table.id)
    assert not service.get_table(table.id).is_available


def test_ensure_available_conflict() -> None:
    service = TableService(TableRepository())
    table = service.add_table()
    service.occupy_table(table.id)
    with pytest.raises(ConflictError):
        service.ensure_available(table.id)
