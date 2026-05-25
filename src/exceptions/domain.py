"""Domain-level exceptions."""


class DomainError(Exception):
    """Base class for domain errors."""


class NotFoundError(DomainError):
    """Raised when an entity is not found."""


class ConflictError(DomainError):
    """Raised when a requested operation conflicts with current state."""


class StateError(DomainError):
    """Raised when a state transition or operation is invalid."""
