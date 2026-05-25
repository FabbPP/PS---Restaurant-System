# CATÁLOGO DE PRUEBAS DE CAJA NEGRA - AULAPASS (UNSA) - V3 (FINAL)

## 1. INTRODUCCIÓN Y METODOLOGÍA
El presente documento detalla la estrategia de validación técnica del **PS---Restaurant-System**. Este catálogo se basa estrictamente en las funciones de prueba implementadas en el directorio `tests/`, empleando **Partición de Equivalencia (PE)** y **Análisis de Valores Límite (AVL)**. Se garantiza la trazabilidad entre el código de prueba y los requerimientos funcionales.

## 2. MATRICES DE PRUEBAS POR MÓDULO (PE + AVL REALES)

### 2.1. Módulo de Gestión de Meseros 
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-1.01 | `test_waiter_name_valid` | Validar nombre alfabético con espacios | PE | "Juan Perez" | Éxito (str) | PASSED |
| TC-1.02 | `test_waiter_name_with_numbers` | Rechazar nombres con dígitos | PE | "Luis123" | ValidationError | PASSED |
| TC-1.03 | `test_waiter_name_invalid` (p1) | Validar rechazo de nombre vacío | AVL | "" | ValidationError | PASSED |
| TC-1.04 | `test_waiter_name_invalid` (p2) | Validar rechazo de solo espacios | PE | "   " | ValidationError | PASSED |
| TC-1.05 | `test_waiter_name_invalid` (p3) | Validar límite superior excedido | AVL | "A" * 61 | ValidationError | PASSED |
| TC-1.06 | `test_waiter_name_boundary_limits` | Validar límite inferior exacto | AVL | "X" | Éxito (len=1) | PASSED |
| TC-1.07 | `test_waiter_name_boundary_limits` | Validar límite superior exacto | AVL | "M" * 60 | Éxito (len=60) | PASSED |
| TC-1.08 | `test_add_waiter` | Integración: Creación vía servicio | PE | "Ramon" | Objeto Waiter | PASSED |

### 2.2. Módulo de Servicios de Orden 
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-2.01 | `test_create_dine_in_order_flow` | Abrir orden en mesa y ocupar recurso | PE | table_id=1 | is_available=False | PASSED |
| TC-2.02 | `test_create_dine_in_occupied_table_fails` | Bloquear orden en mesa ocupada | PE | table_id=ocupada | ConflictError | PASSED |
| TC-2.03 | `test_create_delivery_order_requires_info` | Validar teléfono numérico en despacho | PE | Phone="abc" | ValidationError | PASSED |
| TC-2.04 | `test_order_state_transitions` (p1) | Transición legal FSM | PE | PENDING -> PREPARING | Éxito | PASSED |
| TC-2.05 | `test_order_state_transitions` (p2) | Bloquear salto de estado ilegal | PE | PENDING -> DELIVERED | StateError | PASSED |
| TC-2.06 | `test_close_order_and_release_table` | Liberar mesa tras cierre de orden | PE | close_order(id) | is_available=True | PASSED |
| TC-2.07 | `test_close_order_invalid_states` | Impedir cierre de orden no finalizada | PE | state=PENDING | StateError | PASSED |
| TC-2.08 | `test_close_order_without_items_fails` | Impedir cierre de orden vacía | PE | items=[] | StateError | PASSED |
| TC-2.09 | `test_calculate_total_non_existent_order` | Manejo de ID inexistente en totales | PE | ID=9999 | NotFoundError | PASSED |
| TC-2.10 | `test_assign_table_logic` | Restringir mesas a órdenes Dine-In | PE | Takeaway + MesaID | StateError | PASSED |
| TC-2.11 | `test_cannot_change_state_on_closed_order`| Blindaje de órdenes cerradas | PE | closed=True | StateError | PASSED |

### 2.3. Módulo de Validadores de Orden
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-3.01 | `test_parse_order_state_valid` | Normalización de estados (mayúsculas) | PE | "PREPARANDO" | OrderState.PREPARING| PASSED |
| TC-3.02 | `test_parse_order_state_invalid` | Rechazo de estados inexistentes | PE | "cocinando" | ValidationError | PASSED |
| TC-3.03 | `test_validate_order_item_price_boundary`| Validar precisión mínima de precio | AVL | price=0.01 | Éxito (Decimal) | PASSED |
| TC-3.04 | `test_validate_order_item_empty_name`| Rechazo de ítems con nombre vacío | PE | name="   " | ValidationError | PASSED |

### 2.4. Módulo de Clientes y Delivery
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-4.01 | `test_menu_exit_option` | Salida segura del sistema | PE | "0" | Break Loop | PASSED |
| TC-4.02 | `test_menu_invalid_numeric_option` | Manejo de opción fuera de rango | AVL | "13" | print_error() | PASSED |
| TC-4.03 | `test_menu_non_numeric_input_robustness` | Entrada alfabética en menú | PE | "abc" | Captura Exception | PASSED |
| TC-4.04 | `test_menu_add_waiter_flow` | Inyección de datos en Opción 1 | Integración | "1", "Ramon" | add_waiter() call | PASSED |
| TC-4.05 | `test_customer_repository_save_and_get` | Persistencia de cliente Delivery | PE | ID=1, Ana | Repo Match | PASSED |
| TC-4.06 | `test_delivery_info_invalid_phone` | Rechazo de teléfonos cortos | AVL | "12345678" | ValidationError | PASSED |
| TC-4.07 | `test_customer_invalid_phones` (p1) | Rechazo de teléfono con letras | PE | "999-ABC" | ValidationError | PASSED |

### 2.5. Módulo de Utilidades y Robustez 
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-5.01 | `test_parse_int_valid` | Limpieza de espacios en enteros | PE | "  5  " | 5 (int) | PASSED |
| TC-5.02 | `test_parse_int_invalid` (p1) | Rechazo de entrada alfabética | PE | "abc" | ValidationError | PASSED |
| TC-5.03 | `test_parse_int_invalid` (p2) | Rechazo de entrada flotante | PE | "10.5" | ValidationError | PASSED |
| TC-5.04 | `test_parse_int_empty` | Rechazo de entrada vacía obligatoria | PE | "" | ValidationError | PASSED |
| TC-5.05 | `test_parse_decimal_valid` | Conversión exacta a Decimal | PE | "12.5" | Decimal("12.5") | PASSED |
| TC-5.06 | `test_parse_decimal_invalid` (p1) | Rechazo de valor no finito (NaN) | Robustez | "nan" | ValidationError | PASSED |
| TC-5.07 | `test_parse_decimal_invalid` (p2) | Rechazo de valor no finito (Inf) | Robustez | "inf" | ValidationError | PASSED |
| TC-5.08 | `test_parse_extreme_overflow` | Protección contra DoS (String largo) | Robustez | "9" * 1001 | ValidationError | PASSED |
