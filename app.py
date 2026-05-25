"""Entry point for the restaurant system CLI."""

import os
import sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(CURRENT_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from customers.repository import CustomerRepository  # noqa: E402
from customers.services import CustomerService  # noqa: E402
from delivery.services import DeliveryService  # noqa: E402
from menu.controller import MenuController  # noqa: E402
from orders.repository import OrderRepository  # noqa: E402
from orders.services import OrderService  # noqa: E402
from tables.repository import TableRepository  # noqa: E402
from tables.services import TableService  # noqa: E402
from waiters.repository import WaiterRepository  # noqa: E402
from waiters.services import WaiterService  # noqa: E402


def main() -> None:
    """Initialize services and start the CLI."""
    table_repo = TableRepository()
    waiter_repo = WaiterRepository()
    customer_repo = CustomerRepository()
    order_repo = OrderRepository()

    table_service = TableService(table_repo)
    waiter_service = WaiterService(waiter_repo)
    customer_service = CustomerService(customer_repo)
    delivery_service = DeliveryService(customer_service)
    order_service = OrderService(order_repo, table_service, delivery_service)

    controller = MenuController(waiter_service, table_service, order_service,
                                customer_service, delivery_service)
    controller.run()


if __name__ == "__main__":
    main()
