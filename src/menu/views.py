"""Console views for rendering output."""

from typing import Iterable

from orders.models import Order
from tables.models import Table
from waiters.models import Waiter


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
    print("4. Asignar mesa a orden")
    print("5. Crear orden mesa")
    print("6. Crear orden delivery")
    print("7. Crear orden llevar")
    print("8. Cambiar estado de orden")
    print("9. Cerrar orden")
    print("10. Ver órdenes")
    print("11. Calcular total de orden")
    print("12. Listar mesas")
    print("0. Salir")


def show_waiters(waiters: Iterable[Waiter]) -> None:
    """Display a list of waiters."""
    print_header("Meseros")
    for waiter in waiters:
        print(f"- [{waiter.id}] {waiter.name}")


def show_tables(tables: Iterable[Table]) -> None:
    """Display a list of tables."""
    print_header("Mesas")
    for table in tables:
        status = "Libre" if table.is_available else "Ocupada"
        print(f"- [{table.id}] {status}")


def show_orders(orders: Iterable[Order]) -> None:
    """Display a list of orders."""
    print_header("Órdenes")
    for order in orders:
        table_info = f"Mesa {order.table_id}" if order.table_id else "Sin mesa"
        total = order.total()
        closed = "Cerrada" if order.closed else "Abierta"
        print(
            f"- [{order.id}] {order.order_type.value} | "
            f"{order.state.value} | {table_info} | Total: {total} | {closed}"
        )
