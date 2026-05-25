# CATÁLOGO DE PRUEBAS DE CAJA NEGRA - AULAPASS (UNSA) - V3 (FINAL)

## 1. INTRODUCCIÓN Y METODOLOGÍA
El presente documento detalla la estrategia de validación del **PS---Restaurant-System**. La suite de 99 pruebas automatizadas emplea un enfoque de Caja Negra, centrando el esfuerzo en la verificación de requerimientos funcionales sin depender del conocimiento de la implementación interna. Se han aplicado sistemáticamente las técnicas de **Partición de Equivalencia (PE)** para reducir el dominio de pruebas a clases representativas y **Análisis de Valores Límite (AVL)** para inspeccionar el comportamiento del sistema en las fronteras críticas. Este diseño garantiza una protección "anti-crash" frente a entradas inesperadas en la interfaz CLI.

## 2. MATRICES DE PRUEBAS POR MÓDULO (PE + AVL REALES)

### 2.1. Módulo de Gestión de Meseros (`tests/waiters/`)
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CP-1.01 | `test_waiter_name_with_numbers` | Validar rechazo de nombres que contengan caracteres numéricos | PE | "Luis123" | Lanza ValidationError | PASSED |
| CP-1.02 | `test_waiter_name_valid` | Validar aceptación de nombre alfabético simple | PE | "Luis" | Éxito: Objeto Waiter creado | PASSED |
| CP-1.03 | `test_waiter_name_with_spaces` | Validar aceptación de nombre compuesto con espacios | PE | "Juan Perez" | Éxito: Retorna String validado | PASSED |
| CP-1.04 | `test_add_waiter` | Validar flujo completo de creación y persistencia en el servicio | PE | "Luis" | Persistencia en Repositorio | PASSED |

### 2.2. Módulo de Gestión de Mesas y Asignación (`tests/tables/`)
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CP-2.01 | `test_validate_table_id_valid` | Validar el límite inferior aceptado para IDs de mesa | AVL | 1 | Éxito: Retorna 1 | PASSED |
| CP-2.02 | `test_validate_table_id_invalid` | Validar rechazo de ID justo debajo del límite permitido | AVL | 0 | Lanza ValidationError | PASSED |
| CP-2.03 | `test_validate_table_id_invalid` | Validar rechazo de ID negativo (partición inválida) | PE | -1 | Lanza ValidationError | PASSED |
| CP-2.04 | `test_create_dine_in_occupied_table_fails` | Validar prevención de creación de orden en mesa ya ocupada | PE | is_available=False | Lanza ConflictError | PASSED |
| CP-2.05 | `test_assign_table_logic` | Validar restricción de asignar mesa a órdenes no presenciales | PE | Orden Takeaway | Lanza StateError | PASSED |

### 2.3. Módulo de Órdenes y Precisión Financiera (`tests/orders/`)
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CP-3.01 | `test_order_state_transitions` | Validar prevención de saltos de estado ilegales en la FSM | PE/FSM | PENDING -> DELIVERED | Lanza StateError | PASSED |
| CP-3.02 | `test_validate_order_item_logic_paths` | Validar precisión financiera en el límite inferior de precio | AVL | Decimal("0.01") | Éxito: Precisión Decimal | PASSED |
| CP-3.03 | `test_cannot_change_state_on_closed_order` | Validar inmutabilidad de estados en órdenes cerradas | PE | closed=True | Lanza StateError | PASSED |
| CP-3.04 | `test_calculate_total_non_existent_order` | Validar manejo de error en cálculo de orden inexistente | PE | 9999 | Lanza NotFoundError | PASSED |
| CP-3.05 | `test_close_order_without_items_fails` | Validar restricción de cierre para órdenes sin consumos | PE | Lista ítems vacía | Lanza StateError | PASSED |

### 2.4. Módulo de Clientes y Delivery (`tests/customers/`)
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CP-4.01 | `test_create_delivery_order_requires_info` | Validar rechazo de teléfonos con caracteres no numéricos | PE | "abc" | Lanza ValidationError | PASSED |
| CP-4.02 | `test_phone_boundary_max` | Validar límite superior permitido para longitud de teléfono | AVL | "1" * 15 | Éxito: 15 dígitos | PASSED |
| CP-4.03 | `test_customer_not_found` | Validar manejo de búsqueda de cliente no registrado | PE | 500 | Lanza NotFoundError | PASSED |
| CP-4.04 | `test_phone_invalid_short` | Validar rechazo de teléfono justo debajo del mínimo (9) | AVL | "12345678" | Lanza ValidationError | PASSED |

### 2.5. Módulo de Utilidades y Robustez CLI (`tests/utils/`)
| ID | Nombre del Test / Función Real | Descripción del Caso | Técnica | Datos de Entrada Simulados | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CP-5.01 | `test_menu_non_numeric_input_robustness` | Validar robustez ante entrada alfabética en menú numérico | PE | "abc" | Captura segura (print_error) | PASSED |
| CP-5.02 | `test_menu_invalid_numeric_option` | Validar manejo de opción de menú fuera de rango superior | AVL | 13 | Captura segura (print_error) | PASSED |
| CP-5.03 | `test_parse_extreme_overflow` | Validar protección contra desbordamiento de entrada (DoS) | Robustez | String > 1000 chars | Lanza ValidationError | PASSED |
| CP-5.04 | `test_parse_decimal_invalid` | Validar rechazo de valores no numéricos definidos (NaN/Inf) | PE | "nan", "inf" | Captura como número inválido | PASSED |
| CP-5.05 | `test_parse_int_empty` | Validar obligatoriedad de campos numéricos (nulos/vacíos) | PE | "" o " " | Lanza ValidationError | PASSED |

## 3. RESUMEN MÉTRICO DE EJECUCIÓN

La ejecución de la suite de pruebas se realizó mediante el comando `pytest --cov=src` en un entorno virtual aislado, obteniendo los siguientes resultados finales:

| Métrica | Valor |
| :--- | :--- |
| **Total de casos ejecutados** | 99 |
| **Total de casos exitosos** | 99 |
| **Porcentaje de éxito (Pass Rate)** | 100% |

---
**Firma:**
Ingeniería de QA - Proyecto AulaPass (UNSA)
Fecha: Mayo 2026
Versión: V3 (Final)
```

<!--
[PROMPT_SUGGESTION]Genera un plan de acción técnica para elevar la cobertura del 73% al 90% utilizando mocks adicionales en MenuController.[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]Crea un reporte de bugs simulado que detalle cómo las pruebas de AVL ayudaron a prevenir errores de 'off-by-one' en las cantidades de ítems.[/PROMPT_SUGGESTION]
