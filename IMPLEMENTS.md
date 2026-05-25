# Arquitectura propuesta (MVP robusto por consola, modular y OOP)
Arquitectura en capas con dominio fuerte y validaciones en frontera: **Presentación (CLI) → Aplicación (casos de uso) → Dominio (entidades/estados/invariantes) → Infraestructura (repositorios in‑memory)**. El flujo principal siempre valida entradas antes de tocar el dominio y captura excepciones en la capa de presentación para evitar caídas.

## 1) Arquitectura completa (visión)
- **Presentación (CLI):** menús, captura de entrada, normalización (trim, lower), reintentos controlados, render de errores/éxitos.
- **Aplicación (Use Cases):** orquesta reglas, coordina repositorios, aplica validaciones cruzadas, maneja transiciones de estado.
- **Dominio:** entidades, value objects, invariantes, estado de órdenes, reglas de negocio (ej: una mesa no puede tener 2 órdenes abiertas).
- **Infraestructura:** repositorios en memoria, generadores de ID, almacenamiento temporal.
- **Cross‑cutting:** validadores, excepciones tipadas, utilitarios de parsing seguro.

## 2) Lista de módulos + responsabilidades
| Módulo | Responsabilidad principal | Notas clave |
|---|---|---|
| `domain/entities` | `Mesa`, `Mesero`, `ClienteDelivery`, `Orden`, `OrdenItem` | Invariantes y consistencia interna |
| `domain/states` | Estados y transiciones válidas | Máquina de estados por tipo de orden |
| `domain/policies` | Reglas de negocio | Restricciones (mesas, delivery, etc.) |
| `application/use_cases` | Casos de uso (CRUD + flujos) | Valida reglas cruzadas |
| `application/order_manager` | Módulo central de órdenes | Crea/actualiza órdenes mesa/llevar/delivery |
| `infrastructure/repositories` | Repositorios in‑memory | IDs únicos, búsquedas consistentes |
| `presentation/cli` | Menús, input/output | Nunca lanza excepción al usuario |
| `validation` | Validadores y normalizadores | PE + AVL en tests |
| `errors` | Excepciones tipadas | Errores de dominio / validación |
| `tests` | Pruebas unitarias y caja negra | Organizadas por módulo |

## 3) Flujo general del sistema
1. **CLI** muestra menú → captura entrada → normaliza → valida formato básico.
2. **Use case** recibe datos ya tipados → valida reglas cruzadas (existencia, estados, límites).
3. **Dominio** aplica invariantes y transiciones → crea/actualiza entidades.
4. **Repositorio** persiste en memoria → devuelve resultado.
5. **CLI** muestra resultado o error controlado.

## 4) Estructura de carpetas (propuesta)
```
/src
  /domain
    /entities
    /states
    /policies
  /application
    /use_cases
    order_manager.py
  /infrastructure
    /repositories
    id_generator.py
  /presentation
    /cli
      menus.py
      input_handlers.py
  /validation
  /errors
/tests
  /domain
  /application
  /presentation
  /validation
README.md
REQUIREMENTS.md
IMPLEMENTS.md
requirements.txt
```

## 5) Estrategia de validaciones (exhaustiva)
**Tipos de validación:**
- **Estructural:** tipo correcto (int, str), longitud mínima/máxima, formato (teléfono), rangos (cantidad > 0).
- **Referencial:** mesa/mesero/orden existen antes de asignar.
- **Estado:** transiciones válidas según tipo de orden.
- **Restrictiva:** una mesa no tiene más de una orden activa; delivery requiere dirección y teléfono.
- **Negocio:** límites de cantidad, ítems por orden, montos máximos.

**Ejemplos de restricciones clave:**
- `Mesa`: solo puede estar `libre/ocupada`; no se asigna si tiene orden activa.
- `Orden mesa`: requiere mesa asignada; no permite delivery fields.
- `Orden delivery`: requiere `cliente`, `dirección`, `teléfono`.
- `Orden llevar`: no mesa, no delivery.
- `Item`: cantidad 1..99, precio 0.01..9999.99, nombre 1..60 chars.

## 6) Estrategia de testing (pytest)
**Capas y cobertura:**
- **Dominio:** invariantes, estados, reglas puras.
- **Aplicación:** flujos de casos de uso (crear, asignar, cerrar, cancelar).
- **Validación:** pruebas negativas y límites.
- **CLI (mínimo):** parsing y manejo de error sin crash (simulando inputs).

**Tipos de pruebas:**
- **Caja negra (PE + AVL):** entradas válidas e inválidas.
- **Estados:** transiciones permitidas/prohibidas por tipo.
- **Persistencia:** IDs únicos y repositorio consistente.
- **Robustez:** entradas vacías, tipos incorrectos, overflow de límites.

## 7) Estrategia PE y AVL (black box)
### Partición de Equivalencia (PE)
- **IDs:** válidos (int>0), inválidos (0, negativo, no numérico).
- **Cantidad:** válida (1..99), inválida (0, <0, >99).
- **Nombre item:** válido (1..60), inválido (0, >60).
- **Teléfono:** válido (9..15 dígitos), inválido (letras, vacío, muy corto).

### Análisis de Valores Límite (AVL)
- **Cantidad:** 0,1,99,100
- **Precio:** 0.00,0.01,9999.99,10000
- **Longitud nombre:** 0,1,60,61
- **ID mesa:** -1,0,1,max_mesas,max_mesas+1

## 8) Riesgos potenciales y mitigación
- **Inconsistencia de estado** (orden cerrada con mesa “ocupada”):  
  → Validar transición y sincronizar estados en un solo caso de uso.
- **Órdenes huérfanas** (mesa eliminada con orden activa):  
  → Bloquear eliminación si hay orden activa.
- **Duplicidad de IDs**:  
  → Generador central único y repositorio controlado.
- **Entrada no numérica en menús**:  
  → Parse seguro + reintentos + mensajes claros.
- **Órdenes inválidas por tipo** (delivery sin dirección):  
  → Reglas de tipo en el `order_manager`.

## 9) Robustez ante entradas inválidas
- **Nunca fallar**: toda excepción de validación se captura en CLI.
- **Reintento controlado**: bucles de input con límite de intentos.
- **Mensajes consistentes**: códigos de error simples para el usuario.
- **Sin datos corruptos**: no se persiste nada si una validación falla.
- **Normalización**: trim, lower, conversión segura a int/float.

## 10) Módulo centralizado de órdenes (criterios)
- **Orden base** + **tipo** (`mesa`, `llevar`, `delivery`) con reglas específicas.
- **Estados comunes** (ejemplo): `CREATED → CONFIRMED → PREPARING → READY → CLOSED / CANCELED`.
- **Extensión por tipo**: delivery añade `OUT_FOR_DELIVERY → DELIVERED`.
- **Transiciones bloqueadas** si faltan requisitos o si el estado actual no lo permite.
