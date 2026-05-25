"""Console menu controller."""

from typing import Callable, Optional

from exceptions.domain import DomainError
from exceptions.validation import ValidationError
from menu import views
from orders.services import OrderService
from orders.states import OrderState
from orders.validators import parse_order_state
from tables.services import TableService
from utils.parsing import parse_float, parse_int
from validators.common import validate_int_range, validate_non_empty_str
from waiters.services import WaiterService
from customers.services import CustomerService
from delivery.services import DeliveryService


class MenuController:
    """Main menu controller for CLI interaction."""

    def __init__(self,
                 waiter_service: WaiterService,
                 table_service: TableService,
                 order_service: OrderService,
                 customer_service: CustomerService,
                 delivery_service: DeliveryService) -> None:
        self._waiter_service = waiter_service
        self._table_service = table_service
        self._order_service = order_service
        self._customer_service = customer_service
        self._delivery_service = delivery_service

    def run(self) -> None:
        """Run the main menu loop."""
        while True:
            views.show_main_menu()
            option = self._read_int("Seleccione una opción: ", min_value=0,
                                    max_value=12)
            if option == 0:
                views.print_success("Saliendo del sistema.")
                break
            self._handle_option(option)

    def _handle_option(self, option: int) -> None:
        handlers = {
            1: self._add_waiter,
            2: self._list_waiters,
            3: self._add_table,
            4: self._assign_table,
            5: self._create_dine_in_order,
            6: self._create_delivery_order,
            7: self._create_takeaway_order,
            8: self._change_order_state,
            9: self._close_order,
            10: self._list_orders,
            11: self._calculate_total,
            12: self._list_tables,
        }
        handler = handlers.get(option)
        if handler is None:
            views.print_error("Opción inválida.")
            return
        self._execute(handler)

    def _execute(self, action: Callable[[], None]) -> None:
        try:
            action()
        except DomainError as exc:
            views.print_error(str(exc))
        except ValidationError as exc:
            views.print_error(str(exc))

    def _add_waiter(self) -> None:
        name = self._read_str("Nombre del mesero: ")
        waiter = self._waiter_service.add_waiter(name)
        views.print_success(f"Mesero agregado con ID {waiter.id}.")

    def _list_waiters(self) -> None:
        waiters = self._waiter_service.list_waiters()
        views.show_waiters(waiters)

    def _add_table(self) -> None:
        table = self._table_service.add_table()
        views.print_success(f"Mesa agregada con ID {table.id}.")

    def _list_tables(self) -> None:
        tables = self._table_service.list_tables()
        views.show_tables(tables)

    def _assign_table(self) -> None:
        order_id = self._read_int("ID de orden: ", min_value=1)
        table_id = self._read_int("ID de mesa: ", min_value=1)
        order = self._order_service.assign_table(order_id, table_id)
        views.print_success(f"Mesa {order.table_id} asignada a orden {order.id}.")

    def _create_dine_in_order(self) -> None:
        table_id = self._read_int("ID de mesa: ", min_value=1)
        order = self._order_service.create_dine_in_order(table_id)
        views.print_success(f"Orden de mesa creada con ID {order.id}.")
        self._prompt_order_items(order.id)

    def _create_delivery_order(self) -> None:
        customer_id = self._resolve_customer()
        address = self._read_str("Dirección de entrega: ", min_len=5,
                                 max_len=120)
        phone = self._read_str("Teléfono de entrega: ", min_len=9,
                               max_len=15, digits_only=True)
        order = self._order_service.create_delivery_order(customer_id,
                                                          address, phone)
        views.print_success(f"Orden delivery creada con ID {order.id}.")
        self._prompt_order_items(order.id)

    def _create_takeaway_order(self) -> None:
        order = self._order_service.create_takeaway_order()
        views.print_success(f"Orden para llevar creada con ID {order.id}.")
        self._prompt_order_items(order.id)

    def _change_order_state(self) -> None:
        order_id = self._read_int("ID de orden: ", min_value=1)
        views.print_header("Estados válidos: pendiente, preparando, entregado, "
                           "cancelado")
        state_text = self._read_str("Nuevo estado: ", min_len=3, max_len=20)
        new_state = parse_order_state(state_text)
        order = self._order_service.change_state(order_id, new_state)
        views.print_success(
            f"Orden {order.id} ahora en estado {order.state.value}."
        )

    def _close_order(self) -> None:
        order_id = self._read_int("ID de orden: ", min_value=1)
        order = self._order_service.close_order(order_id)
        views.print_success(f"Orden {order.id} cerrada.")

    def _list_orders(self) -> None:
        orders = self._order_service.list_orders()
        views.show_orders(orders)

    def _calculate_total(self) -> None:
        order_id = self._read_int("ID de orden: ", min_value=1)
        total = self._order_service.calculate_total(order_id)
        views.print_success(f"Total de la orden {order_id}: {total}")

    def _prompt_order_items(self, order_id: int) -> None:
        while True:
            add_more = self._read_str("¿Agregar ítem? (s/n): ",
                                      min_len=1, max_len=1).lower()
            if add_more == "n":
                break
            if add_more != "s":
                views.print_error("Respuesta inválida. Use 's' o 'n'.")
                continue
            name = self._read_str("Nombre del ítem: ", min_len=1, max_len=60)
            quantity = self._read_int("Cantidad: ", min_value=1, max_value=99)
            price = self._read_float("Precio unitario: ", min_value=0.01,
                                     max_value=9999.99)
            self._order_service.add_item(order_id, name, quantity, price)
            views.print_success("Ítem agregado.")

    def _resolve_customer(self) -> int:
        customers = self._customer_service.list_customers()
        if customers:
            views.print_header("Clientes existentes")
            for customer in customers:
                print(f"- [{customer.id}] {customer.name} ({customer.phone})")
        use_existing = self._read_str("¿Usar cliente existente? (s/n): ",
                                      min_len=1, max_len=1).lower()
        if use_existing == "s":
            return self._read_int("ID de cliente: ", min_value=1)
        name = self._read_str("Nombre del cliente: ", min_len=2, max_len=60)
        phone = self._read_str("Teléfono del cliente: ", min_len=9,
                               max_len=15, digits_only=True)
        customer = self._customer_service.add_customer(name, phone)
        views.print_success(f"Cliente creado con ID {customer.id}.")
        return customer.id

    def _read_str(self, prompt: str, min_len: int = 1, max_len: int = 60,
                  digits_only: bool = False) -> str:
        while True:
            value = input(prompt)
            try:
                text = validate_non_empty_str(value, "Entrada",
                                              min_len=min_len,
                                              max_len=max_len)
                if digits_only and not text.isdigit():
                    raise ValidationError("Entrada debe contener solo dígitos.")
                return text
            except ValidationError as exc:
                views.print_error(str(exc))

    def _read_int(self, prompt: str, min_value: Optional[int] = None,
                  max_value: Optional[int] = None) -> int:
        while True:
            raw = input(prompt)
            try:
                value = parse_int(raw, "Número")
                validate_int_range(value, "Número", min_value, max_value)
                return value
            except ValidationError as exc:
                views.print_error(str(exc))

    def _read_float(self, prompt: str, min_value: float = 0.01,
                    max_value: float = 9999.99) -> float:
        while True:
            raw = input(prompt)
            try:
                value = parse_float(raw, "Monto")
                if value <= 0:
                    raise ValidationError("Monto debe ser positivo.")
                if value < min_value or value > max_value:
                    raise ValidationError("Monto fuera de rango.")
                return value
            except ValidationError as exc:
                views.print_error(str(exc))
