"""Validation exceptions."""

from .domain import DomainError


class ValidationError(DomainError):
    """Raised when a validation rule is violated."""
