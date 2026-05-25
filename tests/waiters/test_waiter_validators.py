import pytest

from exceptions.validation import ValidationError
from waiters.validators import validate_waiter_name


def test_validate_waiter_name_valid() -> None:
    assert validate_waiter_name("Mario") == "Mario"


def test_validate_waiter_name_invalid() -> None:
    with pytest.raises(ValidationError):
        validate_waiter_name("  ")
