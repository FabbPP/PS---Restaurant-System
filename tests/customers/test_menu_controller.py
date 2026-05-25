"""Tests for MenuController navigation and robustness."""
import pytest
from unittest.mock import MagicMock, patch
from src.menu.controller import MenuController

@pytest.fixture
def mock_services():
    """Crea mocks para todos los servicios requeridos por el controlador."""
    return {
        "waiter": MagicMock(),
        "table": MagicMock(),
        "order": MagicMock(),
        "customer": MagicMock(),
        "delivery": MagicMock()
    }

@pytest.fixture
def controller(mock_services):
    return MenuController(
        waiter_service=mock_services["waiter"],
        table_service=mock_services["table"],
        order_service=mock_services["order"],
        customer_service=mock_services["customer"],
        delivery_service=mock_services["delivery"]
    )

def test_menu_exit_option(controller):
    """PE: Opción 0 debe terminar el bucle del menú."""
    with patch('builtins.input', return_value="0"):
        # El run() tiene un while True, si la opción 0 funciona, sale del loop.
        controller.run()
    # Si llega aquí, es que el break del option == 0 funcionó.
    assert True

def test_menu_invalid_numeric_option(controller):
    """AVL: Opción fuera de rango (13) seguida de opción de salida (0)."""
    # Simulamos: primero mete un 13 (error), luego un 0 (salir)
    with patch('builtins.input', side_effect=["13", "0"]):
        with patch('src.menu.views.print_error') as mock_error:
            controller.run()
            # Debería haber mostrado un error por el 13
            mock_error.assert_called()

def test_menu_non_numeric_input_robustness(controller):
    """PE: Ingresar una letra donde se espera una opción numérica."""
    # Simulamos: "letra" (error), luego "0" (salir)
    with patch('builtins.input', side_effect=["abc", "0"]):
        with patch('src.menu.views.print_error') as mock_error:
            controller.run()
            # El parse_int en _read_int debe capturar la letra y disparar print_error
            mock_error.assert_called()

def test_menu_add_waiter_flow(controller, mock_services):
    """Integration: Verificar que la opción 1 llama al servicio de meseros."""
    # Simulamos: "1" (Agregar mesero), "Ramon" (Nombre), "0" (Salir)
    with patch('builtins.input', side_effect=["1", "Ramon", "0"]):
        controller.run()
        # Verificar que el servicio recibió el nombre correcto
        mock_services["waiter"].add_waiter.assert_called_once_with("Ramon")