"""Console menu controller.

Central module for CLI interaction. Captures all user input, validates
through service layer, and renders output through views. Every handler
is wrapped in a safe executor that catches domain and validation errors
plus any unexpected exception to prevent system crashes.
"""

import logging
from typing import Callable, Optional


from src.exceptions.domain import DomainError
from src.exceptions.validation import ValidationError
from src.menu import views
from src.orders.services import OrderService
from src.orders.states import OrderState
from src.orders.validators import parse_order_state
from src.tables.services import TableService
from src.utils.parsing import parse_float, parse_int
from src.validators.common import validate_int_range, validate_non_empty_str
from src.waiters.services import WaiterService
from src.customers.services import CustomerService
from src.delivery.services import DeliveryService

logger = logging.getLogger(__name__)

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

    # ------------------------------------------------------------------ #
    #  Main loop
    # ------------------------------------------------------------------ #

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
        """Dispatch to the corresponding handler."""
        handlers = {
            1: self._add_waiter,
            2: self._list_waiters,
            3: self._add_table,
            4: self._assign_table,
            5: self._create_order,
            6: self._create_dine_in_order,
            7: self._create_delivery_order,
            8: self._create_takeaway_order,
            9: self._change_order_state,
            10: self._close_order,
            11: self._list_orders,
            12: self._calculate_total,
        }
        handler = handlers.get(option)
        if handler is None:
            views.print_error("Opción inválida.")
            return
        self._execute(handler)

    def _execute(self, action: Callable[[], None]) -> None:
        """Run a handler, catching all expected and unexpected errors."""
        try:
            action()
        except (DomainError, ValidationError) as exc:
            views.print_error(str(exc))
        except KeyboardInterrupt:
            views.print_error("Operación cancelada por el usuario.")
        except Exception as exc:  # noqa: BLE001
            logger.exception("Error inesperado")
            views.print_error(f"Error inesperado: {exc}")

    # ------------------------------------------------------------------ #
    #  1. Añadir mesero
    # ------------------------------------------------------------------ #

    def _add_waiter(self) -> None:
        name = self._read_str("Nombre del mesero: ")
        waiter = self._waiter_service.add_waiter(name)
        views.print_success(f"Mesero agregado con ID {waiter.id}.")

    # ------------------------------------------------------------------ #
    #  2. Listar meseros
    # ------------------------------------------------------------------ #

    def _list_waiters(self) -> None:
        waiters = self._waiter_service.list_waiters()
        views.show_waiters(waiters)

    # ------------------------------------------------------------------ #
    #  3. Añadir mesa
    # ------------------------------------------------------------------ #

    def _add_table(self) -> None:
        table = self._table_service.add_table()
        views.print_success(f"Mesa agregada con ID {table.id}.")

    # ------------------------------------------------------------------ #
    #  4. Asignar mesa
    # ------------------------------------------------------------------ #

    def _assign_table(self) -> None:
        """Assign a table to an existing dine-in order without one."""
        # Show available tables for context
        available = self._table_service.list_available_tables()
        if available:
            views.print_header("Mesas disponibles")
            for table in available:
                print(f"  [{table.id}] Libre")
        else:
            views.print_error("No hay mesas disponibles.")
            return

        order_id = self._read_int("ID de orden: ", min_value=1)
        table_id = self._read_int("ID de mesa: ", min_value=1)
        order = self._order_service.assign_table(order_id, table_id)
        views.print_success(
            f"Mesa {order.table_id} asignada a orden {order.id}."
        )

    # ------------------------------------------------------------------ #
    #  5. Crear orden (genérico — elige tipo)
    # ------------------------------------------------------------------ #

    def _create_order(self) -> None:
        """Create an order by choosing its type."""
        views.print_header("Tipo de orden")
        print("1. Mesa")
        print("2. Delivery")
        print("3. Para llevar")
        order_type = self._read_int("Seleccione tipo: ", min_value=1,
                                    max_value=3)
        if order_type == 1:
            self._create_dine_in_order()
        elif order_type == 2:
            self._create_delivery_order()
        else:
            self._create_takeaway_order()

    # ------------------------------------------------------------------ #
    #  6. Pedido mesa
    # ------------------------------------------------------------------ #

    def _create_dine_in_order(self) -> None:
        """Create a dine-in order, optionally assigning a table."""
        assign = self._read_str("¿Asignar mesa ahora? (s/n): ",
                                min_len=1, max_len=1).lower()
        table_id = None
        if assign == "s":
            available = self._table_service.list_available_tables()
            if available:
                views.print_header("Mesas disponibles")
                for table in available:
                    print(f"  [{table.id}] Libre")
            table_id = self._read_int("ID de mesa: ", min_value=1)

        order = self._order_service.create_dine_in_order(table_id)
        views.print_success(f"Orden de mesa creada con ID {order.id}.")
        self._prompt_order_items(order.id)

    # ------------------------------------------------------------------ #
    #  7. Pedido delivery
    # ------------------------------------------------------------------ #

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

    # ------------------------------------------------------------------ #
    #  8. Pedido para llevar
    # ------------------------------------------------------------------ #

    def _create_takeaway_order(self) -> None:
        order = self._order_service.create_takeaway_order()
        views.print_success(f"Orden para llevar creada con ID {order.id}.")
        self._prompt_order_items(order.id)

    # ------------------------------------------------------------------ #
    #  9. Cambiar estado
    # ------------------------------------------------------------------ #

    def _change_order_state(self) -> None:
        order_id = self._read_int("ID de orden: ", min_value=1)
        views.print_header(
            "Estados válidos: pendiente, preparando, entregado, cancelado"
        )
        state_text = self._read_str("Nuevo estado: ", min_len=3, max_len=20)
        new_state = parse_order_state(state_text)
        order = self._order_service.change_state(order_id, new_state)
        views.print_success(
            f"Orden {order.id} ahora en estado {order.state.value}."
        )

    # ------------------------------------------------------------------ #
    #  10. Cerrar orden
    # ------------------------------------------------------------------ #

    def _close_order(self) -> None:
        order_id = self._read_int("ID de orden: ", min_value=1)
        order = self._order_service.close_order(order_id)
        total = order.total()
        views.print_success(f"Orden {order.id} cerrada. Total: {total}")

    # ------------------------------------------------------------------ #
    #  11. Ver órdenes
    # ------------------------------------------------------------------ #

    def _list_orders(self) -> None:
        orders = self._order_service.list_orders()
        views.show_orders(orders)

    # ------------------------------------------------------------------ #
    #  12. Calcular total
    # ------------------------------------------------------------------ #

    def _calculate_total(self) -> None:
        order_id = self._read_int("ID de orden: ", min_value=1)
        total = self._order_service.calculate_total(order_id)
        views.print_success(f"Total de la orden {order_id}: {total}")

    # ------------------------------------------------------------------ #
    #  Helpers: ítems y clientes
    # ------------------------------------------------------------------ #

    def _prompt_order_items(self, order_id: int) -> None:
        """Prompt the user to add items to an order."""
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
            try:
                self._order_service.add_item(order_id, name, quantity, price)
                views.print_success("Ítem agregado.")
            except (DomainError, ValidationError) as exc:
                views.print_error(str(exc))

    def _resolve_customer(self) -> int:
        """Select an existing customer or create a new one."""
        customers = self._customer_service.list_customers()
        if customers:
            views.print_header("Clientes existentes")
            for customer in customers:
                print(f"  [{customer.id}] {customer.name} ({customer.phone})")
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

    # ------------------------------------------------------------------ #
    #  Input readers with built-in validation & retry
    # ------------------------------------------------------------------ #

    def _read_str(self, prompt: str, min_len: int = 1, max_len: int = 60,
                  digits_only: bool = False) -> str:
        """Read a validated string from stdin, retrying on error."""
        while True:
            try:
                value = input(prompt)
            except EOFError:
                raise KeyboardInterrupt from None
            try:
                text = validate_non_empty_str(value, "Entrada",
                                              min_len=min_len,
                                              max_len=max_len)
                if digits_only and not text.isdigit():
                    raise ValidationError(
                        "Entrada debe contener solo dígitos."
                    )
                return text
            except ValidationError as exc:
                views.print_error(str(exc))

    def _read_int(self, prompt: str, min_value: Optional[int] = None,
                  max_value: Optional[int] = None) -> int:
        """Read a validated integer from stdin, retrying on error."""
        while True:
            try:
                raw = input(prompt)
            except EOFError:
                raise KeyboardInterrupt from None
            try:
                value = parse_int(raw, "Número")
                validate_int_range(value, "Número", min_value, max_value)
                return value
            except ValidationError as exc:
                views.print_error(str(exc))

    def _read_float(self, prompt: str, min_value: float = 0.01,
                    max_value: float = 9999.99) -> float:
        """Read a validated float from stdin, retrying on error."""
        while True:
            try:
                raw = input(prompt)
            except EOFError:
                raise KeyboardInterrupt from None
            try:
                value = parse_float(raw, "Monto")
                if value < min_value or value > max_value:
                    raise ValidationError(
                        f"Monto debe estar entre {min_value} y {max_value}."
                    )
                return value
            except ValidationError as exc:
                views.print_error(str(exc))
