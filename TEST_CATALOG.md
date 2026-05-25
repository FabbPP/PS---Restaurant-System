# CATÁLOGO DE PRUEBAS DE CAJA NEGRA - AULAPASS (UNSA) - V3 (FINAL)

## 1. INTRODUCCIÓN Y METODOLOGÍA
El presente documento detalla la estrategia de validación del **PS---Restaurant-System**. La suite de 99 pruebas automatizadas emplea un enfoque de Caja Negra, centrando el esfuerzo en la verificación de requerimientos funcionales sin depender del conocimiento de la implementación interna. Se han aplicado sistemáticamente las técnicas de **Partición de Equivalencia (PE)** para reducir el dominio de pruebas a clases representativas y **Análisis de Valores Límite (AVL)** para inspeccionar el comportamiento del sistema en las fronteras críticas. Este diseño garantiza una protección "anti-crash" frente a entradas inesperadas en la interfaz CLI.

## 2. MATRICES DE PRUEBAS POR MÓDULO (PE + AVL REALES)
### 2.1. Módulo de Gestión de Meseros y Validadores Comunes (`tests/waiters/` y `tests/validators/`)
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-1.01 | `test_waiter_name_with_numbers` | Validar rechazo de nombres que contengan caracteres numéricos | PE | "Luis123" | Lanza ValidationError | PASSED |
| TC-1.02 | `test_waiter_name_valid` | Validar aceptación de nombre alfabético simple | PE | "Luis" | Éxito: Objeto Waiter creado | PASSED |
| TC-1.03 | `test_waiter_name_with_spaces` | Validar aceptación de nombre compuesto con espacios | PE | "Juan Perez" | Éxito: Retorna String validado | PASSED |
| TC-1.04 | `test_waiter_name_empty` | Validar rechazo de nombre vacío (límite inferior) | AVL | "" | Lanza ValidationError | PASSED |
| TC-1.05 | `test_waiter_name_too_long` | Validar rechazo de nombre excediendo 60 caracteres | AVL | "A" * 61 | Lanza ValidationError | PASSED |
| TC-1.06 | `test_waiter_model_init` | Verificar instanciación correcta del modelo Waiter | PE | id=1, name="Luis" | Atributos asignados | PASSED |
| TC-1.07 | `test_waiter_repo_create` | Verificar creación en repositorio in-memory | PE | name="Luis" | Retorna entidad con ID | PASSED |
| TC-1.08 | `test_waiter_repo_list` | Verificar recuperación de lista de meseros | PE | [Waiter1, Waiter2] | Lista no vacía | PASSED |
| TC-1.09 | `test_waiter_repo_get` | Verificar obtención por ID existente | PE | id=1 | Retorna mesero exacto | PASSED |
| TC-1.10 | `test_add_waiter_service` | Validar orquestación del servicio de meseros | PE | "Ramon" | Flujo completo exitoso | PASSED |
| TC-1.11 | `test_validate_non_empty_str_p1` | Parametrize: Validar string estándar | PE | "Valid" | Éxito | PASSED |
| TC-1.12 | `test_validate_non_empty_str_p2` | Parametrize: Validar longitud mínima 1 | AVL | "A" | Éxito | PASSED |
| TC-1.13 | `test_validate_non_empty_str_p3` | Parametrize: Validar longitud máxima 60 | AVL | "A"*60 | Éxito | PASSED |
| TC-1.14 | `test_validate_int_range_p1` | Parametrize: Entero dentro de rango [1, 10] | PE | 5 | Éxito | PASSED |
| TC-1.15 | `test_validate_int_range_p2` | Parametrize: Límite inferior exacto | AVL | 1 | Éxito | PASSED |
| TC-1.16 | `test_validate_int_range_p3` | Parametrize: Límite superior exacto | AVL | 10 | Éxito | PASSED |
| TC-1.17 | `test_validate_price_p1` | Parametrize: Precio mínimo positivo | AVL | 0.01 | Éxito | PASSED |
| TC-1.18 | `test_validate_price_p2` | Parametrize: Precio máximo lógico | AVL | 9999.99 | Éxito | PASSED |
| TC-1.19 | `test_validate_phone_p1` | Parametrize: Teléfono estándar 9 dígitos | PE | "999888777" | Éxito | PASSED |
| TC-1.20 | `test_validate_phone_p2` | Parametrize: Teléfono máximo 15 dígitos | AVL | "1"*15 | Éxito | PASSED |
| TC-1.21 | `test_validate_id_positive` | Validar que IDs sean siempre mayores a cero | PE | 1 | Éxito | PASSED |

### 2.2. Módulo de Gestión de Mesas y Asignación (`tests/tables/`)
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-2.01 | `test_validate_table_id_valid` | Validar el límite inferior aceptado para IDs de mesa | AVL | 1 | Éxito: Retorna 1 | PASSED |
| TC-2.02 | `test_validate_table_id_invalid_p1` | Parametrize: Validar rechazo de ID cero | AVL | 0 | Lanza ValidationError | PASSED |
| TC-2.03 | `test_validate_table_id_invalid_p2` | Parametrize: Validar rechazo de ID negativo | PE | -1 | Lanza ValidationError | PASSED |
| TC-2.04 | `test_validate_table_id_invalid_p3` | Parametrize: Validar rechazo de ID negativo extremo | PE | -999 | Lanza ValidationError | PASSED |
| TC-2.05 | `test_table_model_init` | Verificar estado inicial de mesa (disponible) | PE | id=1, available=True | Atributos correctos | PASSED |
| TC-2.06 | `test_table_repr` | Verificar representación en string de la entidad mesa | PE | Table(id=1) | Formato esperado | PASSED |
| TC-2.07 | `test_table_repo_save` | Verificar persistencia de mesa en repositorio | PE | Table object | Almacenado exitosamente | PASSED |
| TC-2.08 | `test_table_repo_get_all` | Verificar listado de todas las mesas registradas | PE | N/A | Retorna colección | PASSED |
| TC-2.09 | `test_table_repo_delete` | Verificar eliminación física de mesa del repositorio | PE | id=1 | Remoción exitosa | PASSED |
| TC-2.10 | `test_table_service_add` | Validar lógica de negocio para añadir mesas | PE | N/A | ID autogenerado | PASSED |
| TC-2.11 | `test_table_service_occupy` | Validar cambio de estado a ocupado vía servicio | PE | id=1 | is_available = False | PASSED |
| TC-2.12 | `test_table_service_release` | Validar cambio de estado a libre vía servicio | PE | id=1 | is_available = True | PASSED |
| TC-2.13 | `test_table_service_list_available` | Filtrar solo mesas listas para atención | PE | N/A | Solo mesas libres | PASSED |
| TC-2.14 | `test_table_service_get_by_id` | Obtener mesa específica por ID | PE | 1 | Mesa encontrada | PASSED |
| TC-2.15 | `test_table_service_get_invalid` | Error al obtener mesa inexistente | PE | 99 | Lanza NotFoundError | PASSED |
| TC-2.16 | `test_table_service_delete_non_existent` | Error al borrar mesa inexistente | PE | 88 | Lanza NotFoundError | PASSED |
| TC-2.17 | `test_table_service_update_status` | Actualización manual de disponibilidad | PE | False -> True | Estado actualizado | PASSED |
| TC-2.18 | `test_table_service_capacity_p1` | Validar capacidad mínima | AVL | 1 | Aceptado | PASSED |
| TC-2.19 | `test_table_service_capacity_p2` | Validar capacidad máxima lógica | AVL | 20 | Aceptado | PASSED |
| TC-2.20 | `test_table_service_capacity_invalid` | Rechazar capacidad cero | AVL | 0 | Lanza ValidationError | PASSED |
| TC-2.21 | `test_table_service_capacity_neg` | Rechazar capacidad negativa | PE | -2 | Lanza ValidationError | PASSED |

### 2.3. Módulo de Órdenes y Precisión Financiera (`tests/tables/test_order_services.py`)
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-3.01 | `test_create_dine_in_order_flow` | Creación de orden presencial y bloqueo de mesa | PE | table_id=1 | Mesa is_available=False | PASSED |
| TC-3.02 | `test_create_dine_in_occupied_table_fails` | Prevención de duplicidad de órdenes en una misma mesa | PE | table_id=ocupada | Lanza ConflictError | PASSED |
| TC-3.03 | `test_create_delivery_order_requires_info` | Validación de datos mandatorios para despacho | PE | Juan, Dirección, 999... | Orden Delivery creada | PASSED |
| TC-3.04 | `test_order_state_transitions_p1` | FSM: Transición legal de pendiente a preparando | PE | PENDING -> PREPARING | Éxito (True) | PASSED |
| TC-3.05 | `test_order_state_transitions_p2` | FSM: Bloqueo de salto directo a entregado | PE | PENDING -> DELIVERED | Lanza StateError | PASSED |
| TC-3.06 | `test_order_state_transitions_p3` | FSM: Transición legal de preparando a entregado | PE | PREPARING -> DELIVERED | Éxito (True) | PASSED |
| TC-3.07 | `test_order_state_transitions_p4` | FSM: Cancelación permitida durante preparación | PE | PREPARING -> CANCELED | Éxito (True) | PASSED |
| TC-3.08 | `test_order_state_transitions_p5` | FSM: Bloqueo de regresión a pendiente | PE | DELIVERED -> PENDING | Lanza StateError | PASSED |
| TC-3.09 | `test_order_state_transitions_p6` | FSM: Bloqueo de reactivación de orden cancelada | PE | CANCELED -> PREPARING | Lanza StateError | PASSED |
| TC-3.10 | `test_close_order_and_release_table` | Cierre administrativo y liberación automática de mesa | PE | order_id=1 | Mesa is_available=True | PASSED |
| TC-3.11 | `test_close_order_invalid_states` | Impedir cierre de órdenes que no han sido entregadas | PE | PENDING -> Close | Lanza StateError | PASSED |
| TC-3.12 | `test_close_order_without_items_fails` | Impedir cierre de órdenes con cuenta en cero (sin ítems) | PE | items=[] | Lanza StateError | PASSED |
| TC-3.13 | `test_calculate_total_non_existent_order` | Error al consultar finanzas de ID inexistente | PE | 9999 | Lanza NotFoundError | PASSED |
| TC-3.14 | `test_assign_table_logic` | Validar que solo órdenes Dine-In acepten mesas | PE | Takeaway + TableID | Lanza StateError | PASSED |
| TC-3.15 | `test_cannot_change_state_on_closed_order` | Validar inmutabilidad absoluta de órdenes cerradas | PE | closed=True | Lanza StateError | PASSED |

### 2.4. Módulo de Clientes y Delivery (`tests/customers/`)
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-4.01 | `test_customer_model_name` | Validar atributo nombre en DeliveryCustomer | PE | "Ana" | Asignado | PASSED |
| TC-4.02 | `test_customer_model_phone` | Validar atributo teléfono en DeliveryCustomer | PE | "999888777" | Asignado | PASSED |
| TC-4.03-15 | `test_customer_attributes` | Desglose de 11 sub-tests de validación de modelos (13 total) | PE/AVL | Varios | Éxito | PASSED |
| TC-4.14 | `test_customer_repository_save` | Verificar guardado de cliente en repo | PE | DeliveryCustomer | Persistido | PASSED |
| TC-4.15 | `test_customer_not_found` | Manejo de error en búsqueda fallida | PE | ID=500 | Lanza NotFoundError | PASSED |
| TC-4.16 | `test_delivery_service_init` | Inicialización de servicio de despacho | PE | N/A | Instanciado | PASSED |
| TC-4.17 | `test_delivery_create_info` | Creación de objeto DeliveryInfo | PE | Dir, Tel | Objeto válido | PASSED |
| TC-4.18 | `test_delivery_validate_dir_p1` | Validar dirección mínima (5 chars) | AVL | "Calle" | Aceptado | PASSED |
| TC-4.19 | `test_delivery_validate_dir_invalid` | Rechazar dirección corta (4 chars) | AVL | "Urb." | Lanza ValidationError | PASSED |
| TC-4.20 | `test_delivery_phone_num_p1` | Validar teléfono numérico 9 dígitos | AVL | "900000000" | Aceptado | PASSED |
| TC-4.21 | `test_delivery_phone_num_p2` | Validar teléfono numérico 15 dígitos | AVL | "9"*15 | Aceptado | PASSED |
| TC-4.22 | `test_delivery_phone_invalid_chars` | Rechazar caracteres especiales en teléfono | PE | "999-888" | Lanza ValidationError | PASSED |
| TC-4.23 | `test_delivery_get_info` | Recuperar info de despacho por ID | PE | id=1 | Retorna Info | PASSED |
| TC-4.24 | `test_delivery_delete_info` | Eliminar registro de despacho | PE | id=1 | Eliminado | PASSED |

| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-5.01 | `test_menu_exit_option` | Validar cierre seguro del sistema (Opción 0) | PE | "0" | Break loop / Salida | PASSED |
| TC-5.02 | `test_menu_invalid_numeric_option` | Robustez: Opción fuera de rango (13) | AVL | "13", "0" | Captura print_error | PASSED |
| TC-5.03 | `test_menu_non_numeric_input_robustness` | Robustez: Entrada alfabética en menú | PE | "abc", "0" | Captura print_error | PASSED |
| TC-5.04 | `test_menu_add_waiter_flow` | Integración: Opción 1 llama al servicio correcto | PE | "1", "Ramon", "0" | add_waiter ejecutado | PASSED |
| TC-5.05 | `test_id_generator_unique` | Garantizar IDs correlativos únicos | PE | N/A | ID1 != ID2 | PASSED |
| TC-5.06 | `test_id_generator_reset` | Reinicio seguro del generador | PE | N/A | Empieza en 1 | PASSED |
| TC-5.07 | `test_parse_int_valid` | Conversión exitosa con limpieza de espacios | PE | "  10  " | 10 (int) | PASSED |
| TC-5.08 | `test_parse_int_invalid_p1` | Parametrize: Rechazar entrada alfabética | PE | "abc" | Lanza ValidationError | PASSED |
| TC-5.09 | `test_parse_int_invalid_p2` | Parametrize: Rechazar flotante en campo entero | PE | "10.5" | Lanza ValidationError | PASSED |
| TC-5.10 | `test_parse_int_invalid_p3` | Parametrize: Rechazar string "None" | PE | "None" | Lanza ValidationError | PASSED |
| TC-5.11 | `test_parse_int_empty_p1` | Parametrize: Rechazar nulo | AVL | "" | Lanza ValidationError | PASSED |
| TC-5.12 | `test_parse_int_empty_p2` | Parametrize: Rechazar solo espacios | PE | " " | Lanza ValidationError | PASSED |
| TC-5.13 | `test_parse_decimal_valid` | Conversión exitosa a Decimal (Precisión) | PE | "12.5" | Decimal("12.5") | PASSED |
| TC-5.14 | `test_parse_decimal_invalid_p1` | Parametrize: Rechazar basura alfanumérica | PE | "x" | Lanza ValidationError | PASSED |
| TC-5.15 | `test_parse_decimal_invalid_p2` | Parametrize: Rechazar guiones | PE | "---" | Lanza ValidationError | PASSED |
| TC-5.16 | `test_parse_decimal_invalid_p3` | Parametrize: Rechazar Infinity | Robustez | "inf" | Lanza ValidationError | PASSED |
| TC-5.17 | `test_parse_decimal_invalid_p4` | Parametrize: Rechazar NaN | Robustez | "nan" | Lanza ValidationError | PASSED |
| TC-5.18 | `test_parse_extreme_overflow` | Protección contra DoS/Strings masivos | Robustez | "9" * 1001 | Lanza ValidationError | PASSED |

## 3. RESUMEN MÉTRICO DE EJECUCIÓN

La ejecución de la suite de pruebas se realizó mediante el comando `pytest --cov=src` en un entorno virtual aislado, obteniendo los siguientes resultados finales:

| Métrica | Valor |
| :--- | :--- |
| **Total de casos ejecutados** | 99 |
| **Total de casos exitosos** | 99 |
| **Porcentaje de éxito (Pass Rate)** | 100% |

---
*Laboratorio de Procesos de Software - Ingeniería de Software.*