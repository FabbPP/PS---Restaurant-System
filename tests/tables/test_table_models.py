import pytest

from src.exceptions.domain import StateError
from src.tables.models import Table


def test_table_occupy_and_release() -> None:
    table = Table(id=1)
    table.occupy()
    assert not table.is_available
    table.release()
    assert table.is_available


def test_table_occupy_twice() -> None:
    table = Table(id=1)
    table.occupy()
    with pytest.raises(StateError):
        table.occupy()
