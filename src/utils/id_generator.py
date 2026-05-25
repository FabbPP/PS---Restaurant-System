"""ID generator utility."""


class IdGenerator:
    """Simple incremental ID generator."""

    def __init__(self, start: int = 1) -> None:
        self._next_id = start

    def next_id(self) -> int:
        """Return a new unique integer ID."""
        value = self._next_id
        self._next_id += 1
        return value
