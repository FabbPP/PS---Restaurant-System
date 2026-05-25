from waiters.repository import WaiterRepository
from waiters.services import WaiterService


def test_add_waiter() -> None:
    service = WaiterService(WaiterRepository())
    waiter = service.add_waiter("Luis")
    assert waiter.id == 1
    assert service.list_waiters()[0].name == "Luis"
