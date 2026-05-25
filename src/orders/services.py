"""Order services (use cases)."""

from typing import List

from delivery.services import DeliveryService
from exceptions.domain import ConflictError, StateError
from orders.models import Order, OrderItem, OrderType
from orders.repository import OrderRepository
from orders.states import OrderState
from tables.services import TableService
from validators.common import validate_id


class OrderService:
    """Application service for orders."""

    def __init__(self, repository: OrderRepository,
                 table_service: TableService,
                 delivery_service: DeliveryService) -> None:
        self._repository = repository
        self._table_service = table_service
        self._delivery_service = delivery_service

    def list_orders(self) -> List[Order]:
        """List all orders."""
        return self._repository.list_all()

    def get_order(self, order_id: int) -> Order:
        """Get an order by ID."""
        valid_id = validate_id(order_id, "ID de orden")
        return self._repository.get(valid_id)

    def create_dine_in_order(self, table_id: int) -> Order:
        """Create a dine-in order for a table."""
        valid_table_id = validate_id(table_id, "ID de mesa")
        self._table_service.ensure_available(valid_table_id)
        order_id = self._repository.next_id()
        order = Order(id=order_id, order_type=OrderType.DINE_IN,
                      table_id=valid_table_id)
        self._repository.add(order)
        self._table_service.occupy_table(valid_table_id)
        return order

    def create_takeaway_order(self) -> Order:
        """Create a takeaway order."""
        order_id = self._repository.next_id()
        order = Order(id=order_id, order_type=OrderType.TAKEAWAY)
        self._repository.add(order)
        return order

    def create_delivery_order(self, customer_id: int, address: str,
                              phone: str) -> Order:
        """Create a delivery order with delivery info."""
        delivery_info = self._delivery_service.create_info(customer_id,
                                                           address,
                                                           phone)
        order_id = self._repository.next_id()
        order = Order(id=order_id, order_type=OrderType.DELIVERY,
                      delivery_info=delivery_info)
        self._repository.add(order)
        return order

    def assign_table(self, order_id: int, table_id: int) -> Order:
        """Assign a table to an existing dine-in order."""
        order = self.get_order(order_id)
        if order.order_type != OrderType.DINE_IN:
            raise StateError("Solo las órdenes de mesa pueden asignar mesa.")
        if order.table_id is not None:
            raise ConflictError("La orden ya tiene una mesa asignada.")
        valid_table_id = validate_id(table_id, "ID de mesa")
        self._table_service.ensure_available(valid_table_id)
        order.table_id = valid_table_id
        self._table_service.occupy_table(valid_table_id)
        return order

    def add_item(self, order_id: int, name: str, quantity: int,
                 unit_price: float) -> Order:
        """Add an item to an order."""
        order = self.get_order(order_id)
        item = OrderItem(name=name, quantity=quantity, unit_price=unit_price)
        order.add_item(item)
        return order

    def change_state(self, order_id: int, new_state: OrderState) -> Order:
        """Change order state."""
        order = self.get_order(order_id)
        order.set_state(new_state)
        return order

    def close_order(self, order_id: int) -> Order:
        """Close an order and release related resources."""
        order = self.get_order(order_id)
        if order.closed:
            raise StateError("La orden ya está cerrada.")
        if order.state not in {OrderState.DELIVERED, OrderState.CANCELED}:
            raise StateError("Solo se puede cerrar una orden finalizada.")
        if order.state == OrderState.DELIVERED and not order.items:
            raise StateError("No se puede cerrar una orden sin ítems.")
        order.closed = True
        if order.order_type == OrderType.DINE_IN and order.table_id is not None:
            self._table_service.release_table(order.table_id)
        return order

    def calculate_total(self, order_id: int) -> float:
        """Calculate total amount for an order."""
        order = self.get_order(order_id)
        return order.total()
