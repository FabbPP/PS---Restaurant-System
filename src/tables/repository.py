"""Table repository (in-memory)."""

from typing import Dict, List

from src.exceptions.domain import ConflictError, NotFoundError
from src.tables.models import Table
from src.utils.id_generator import IdGenerator


class TableRepository:
    """In-memory repository for tables."""

    def __init__(self) -> None:
        self._items: Dict[int, Table] = {}
        self._id_gen = IdGenerator()

    def create(self) -> Table:
        """Create and store a new table."""
        table_id = self._id_gen.next_id()
        if table_id in self._items:
            raise ConflictError("ID de mesa duplicado.")
        table = Table(id=table_id)
        self._items[table_id] = table
        return table

    def add(self, table: Table) -> None:
        """Add an existing table to the repository."""
        if table.id in self._items:
            raise ConflictError("ID de mesa duplicado.")
        self._items[table.id] = table

    def get(self, table_id: int) -> Table:
        """Get a table by ID."""
        try:
            return self._items[table_id]
        except KeyError as exc:
            raise NotFoundError("Mesa no encontrada.") from exc

    def list_all(self) -> List[Table]:
        """List all tables."""
        return list(self._items.values())
