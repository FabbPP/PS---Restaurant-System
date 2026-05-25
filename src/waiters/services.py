"""Waiter services (use cases)."""

from typing import List

from waiters.models import Waiter
from waiters.repository import WaiterRepository
from waiters.validators import validate_waiter_name


class WaiterService:
    """Application service for waiters."""

    def __init__(self, repository: WaiterRepository) -> None:
        self._repository = repository

    def add_waiter(self, name: str) -> Waiter:
        """Create a new waiter."""
        valid_name = validate_waiter_name(name)
        return self._repository.create(valid_name)

    def list_waiters(self) -> List[Waiter]:
        """List all waiters."""
        return self._repository.list_all()

    def get_waiter(self, waiter_id: int) -> Waiter:
        """Get a waiter by ID."""
        return self._repository.get(waiter_id)
