"""Console views for rendering output."""

from typing import Iterable, List

from src.orders.models import Order
from src.tables.models import Table
from src.waiters.models import Waiter


def print_header(title: str) -> None:
    """Print a simple header."""
    print(f"\n=== {title} ===")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"[ERROR] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"[OK] {message}")


def show_main_menu() -> None:
    """Display the main menu options."""
    print_header("Menú Principal")
    print("1. Añadir mesero")
    print("2. Listar meseros")
    print("3. Añadir mesa")
    print("4. Asignar mesa")
    print("5. Crear orden")
    print("6. Pedido mesa")
    print("7. Pedido delivery")
    print("8. Pedido para llevar")
    print("9. Cambiar estado")
    print("10. Cerrar orden")
    print("11. Ver órdenes")
    print("12. Calcular total")
    print("0. Salir")


def show_waiters(waiters: Iterable[Waiter]) -> None:
    """Display a list of waiters."""
    waiter_list: List[Waiter] = list(waiters)
    print_header("Meseros")
    if not waiter_list:
        print("No hay meseros registrados.")
        return

    for waiter in waiter_list:
        print(f"- [{waiter.id}] {waiter.name}")


def show_tables(tables: Iterable[Table]) -> None:
    """Display a list of tables."""
    table_list: List[Table] = list(tables)
    print_header("Mesas")
    if not table_list:
        print("No hay mesas registradas.")
        return

    for table in table_list:
        status = "Libre" if table.is_available else "Ocupada"
        print(f"- [{table.id}] {status}")


def show_orders(orders: Iterable[Order]) -> None:
    """Display a list of orders."""
    order_list: List[Order] = list(orders)
    print_header("Órdenes")
    if not order_list:
        print("No hay órdenes registradas.")
        return

    for order in order_list:
        table_info = f"Mesa {order.table_id}" if order.table_id else "Sin mesa"
        total = order.total()
        closed = "Cerrada" if order.closed else "Abierta"
        print(
            f"- [{order.id}] {order.order_type.value} | "
            f"{order.state.value} | {table_info} | Total: {total} | {closed}"
        )
