"""ID generator utility."""

from src.exceptions.validation import ValidationError

class IdGenerator:
    """Simple incremental ID generator."""

    def __init__(self, start: int = 1) -> None:
        if isinstance(start, bool) or not isinstance(start, int):
            raise ValidationError(
                "Valor inicial de ID debe ser un número entero."
            )
        if start < 1:
            raise ValidationError("Valor inicial de ID debe ser >= 1.")
        self._next_id = start

    def next_id(self) -> int:
        """Return a new unique integer ID."""
        value = self._next_id
        self._next_id += 1
        return value
