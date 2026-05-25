"""Integration tests for OrderService state machine and business logic."""

import pytest
from src.orders.services import OrderService
from src.orders.states import OrderState
from src.exceptions.domain import StateError, NotFoundError, ConflictError
from src.exceptions.validation import ValidationError

def test_create_dine_in_order_flow(order_service: OrderService, table_service) -> None:
    """PE: Creación de orden de mesa y sincronización de estado de mesa."""
    table = table_service.add_table() # ID 1
    
    order = order_service.create_dine_in_order(table.id)
    
    assert order.table_id == table.id
    assert order.state == OrderState.PENDING
    # La mesa debe quedar ocupada automáticamente
    assert table_service.get_table(table.id).is_available is False

def test_create_dine_in_occupied_table_fails(order_service: OrderService, table_service) -> None:
    """PE: Intento de abrir orden en mesa ya ocupada."""
    table = table_service.add_table()
    table_service.occupy_table(table.id)
    
    # Refactorizado: Especificidad absoluta en la excepción para evitar falsos positivos
    with pytest.raises(ConflictError, match="no está disponible"):
        order_service.create_dine_in_order(table.id)

def test_create_delivery_order_requires_info(order_service: OrderService, customer_service) -> None:
    """PE: Validación de requisitos para órdenes de Delivery."""
    customer_service.add_customer("Juan", "999888777")
    # Caso Válido
    order = order_service.create_delivery_order(
        customer_id=1, 
        address="Av. Siempre Viva 742", 
        phone="999888777"
    )
    assert order.delivery_info.address == "Av. Siempre Viva 742"
    
    # Caso Inválido: Teléfono mal formado (debe fallar en el validador del servicio o modelo)
    with pytest.raises(ValidationError):
        order_service.create_delivery_order(1, "Direccion", "abc")

@pytest.mark.parametrize("current, next_state, should_pass", [
    (OrderState.PENDING, OrderState.PREPARING, True),
    (OrderState.PENDING, OrderState.DELIVERED, False), # Salto ilegal
    (OrderState.PREPARING, OrderState.DELIVERED, True),
    (OrderState.PREPARING, OrderState.CANCELED, True),
    (OrderState.DELIVERED, OrderState.PENDING, False),  # Regresión ilegal
    (OrderState.CANCELED, OrderState.PREPARING, False), # Regresión ilegal
])
def test_order_state_transitions(order_service: OrderService, current, next_state, should_pass) -> None:
    """FSM: Validación exhaustiva de la máquina de estados."""
    order = order_service.create_takeaway_order()
    
    # Forzamos estado inicial para el test de transición
    order.state = current
    
    if should_pass:
        updated = order_service.change_state(order.id, next_state)
        assert updated.state == next_state
    else:
        with pytest.raises(StateError):
            order_service.change_state(order.id, next_state)

def test_close_order_and_release_table(order_service: OrderService, table_service) -> None:
    """PE: Al cerrar una orden de mesa, la mesa debe liberarse."""
    table = table_service.add_table()
    order = order_service.create_dine_in_order(table.id)
    order_service.add_item(order.id, "Pasta", 1, 20.0)
    
    # Avanzar a estado final para permitir cierre
    order_service.change_state(order.id, OrderState.PREPARING)
    order_service.change_state(order.id, OrderState.DELIVERED)
    
    # Cerrar
    order_service.close_order(order.id)
    
    # Verificaciones
    assert order_service.get_order(order.id).closed is True
    assert table_service.get_table(table.id).is_available is True

def test_close_order_invalid_states(order_service: OrderService) -> None:
    """Edge Case: No se puede cerrar una orden si no está en estado final."""
    order = order_service.create_takeaway_order()
    
    # Intentar cerrar en PENDING
    with pytest.raises(StateError, match="finalizada"):
        order_service.close_order(order.id)

def test_close_order_without_items_fails(order_service: OrderService) -> None:
    """Edge Case: No se puede cerrar una orden DELIVERED si no tiene ítems."""
    order = order_service.create_takeaway_order()
    order_service.change_state(order.id, OrderState.PREPARING)
    order_service.change_state(order.id, OrderState.DELIVERED)
    
    with pytest.raises(StateError, match="sin ítems"):
        order_service.close_order(order.id)

def test_calculate_total_non_existent_order(order_service: OrderService) -> None:
    """PE: Referencia a ID inexistente en cálculo."""
    with pytest.raises(NotFoundError):
        order_service.calculate_total(9999)

def test_assign_table_logic(order_service: OrderService, table_service) -> None:
    """PE: Asignación de mesa a una orden de mesa que no tenía una."""
    # Crear orden TAKEAWAY e intentar asignar mesa (debe fallar)
    tk_order = order_service.create_takeaway_order()
    table = table_service.add_table()
    with pytest.raises(StateError, match="Solo las órdenes de mesa"):
        order_service.assign_table(tk_order.id, table.id)
    
    # Crear orden DINE_IN sin mesa inicial (si el servicio lo permite) o reasignar
    # Nota: Tu OrderService.create_dine_in_order requiere table_id. 
    # Probamos reasignación conflictiva:
    table2 = table_service.add_table()
    dine_order = order_service.create_dine_in_order(table.id)
    with pytest.raises(ConflictError):
        order_service.assign_table(dine_order.id, table2.id)

def test_cannot_change_state_on_closed_order(order_service: OrderService):
    """Edge Case: Intentar manipular una orden que ya fue cerrada administrativamente."""
    order = order_service.create_takeaway_order()
    order.closed = True # Inyección manual de estado para forzar la regla de negocio
    with pytest.raises(StateError, match="cerrada"):
        order_service.change_state(order.id, OrderState.PREPARING)