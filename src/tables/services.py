"""Table services (use cases)."""

from typing import List

from exceptions.domain import ConflictError
from tables.models import Table
from tables.repository import TableRepository
from tables.validators import validate_table_id


class TableService:
    """Application service for tables."""

    def __init__(self, repository: TableRepository) -> None:
        self._repository = repository

    def add_table(self) -> Table:
        """Create a new table."""
        return self._repository.create()

    def list_tables(self) -> List[Table]:
        """List all tables."""
        return self._repository.list_all()

    def get_table(self, table_id: int) -> Table:
        """Get a table by ID."""
        validate_table_id(table_id)
        return self._repository.get(table_id)

    def occupy_table(self, table_id: int) -> Table:
        """Mark a table as occupied."""
        table = self.get_table(table_id)
        table.occupy()
        return table

    def release_table(self, table_id: int) -> Table:
        """Mark a table as available."""
        table = self.get_table(table_id)
        table.release()
        return table

    def ensure_available(self, table_id: int) -> None:
        """Ensure the table is available."""
        table = self.get_table(table_id)
        if not table.is_available:
            raise ConflictError("La mesa no está disponible.")
