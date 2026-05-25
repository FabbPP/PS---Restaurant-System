from src.waiters.models import Waiter


def test_waiter_name_normalization() -> None:
    waiter = Waiter(id=1, name=" Ana ")
    assert waiter.name == "Ana"
