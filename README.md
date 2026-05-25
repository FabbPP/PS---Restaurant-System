## 1. DESCRIPCIÓN DEL SISTEMA Y OBJETIVO
El **PS---Restaurant-System** es un sistema basado en interfaz de línea de comandos (CLI) diseñado para la gestión transaccional integral de restaurantes. Su objetivo principal es garantizar la integridad del flujo de pedidos, desde la asignación de mesas hasta el despacho de delivery, eliminando errores de precisión financiera y estados inconsistentes mediante un diseño modular y estrictamente validado.

## 2. FUNCIONALIDADES DETALLADAS
El sistema ofrece 12 operaciones reales accesibles desde el menú principal:

1.  **Añadir mesero:** Registra un nuevo miembro del personal de servicio validando obligatoriedad del nombre.
2.  **Listar meseros:** Despliega la colección completa de meseros activos en el sistema.
3.  **Añadir mesa:** Crea un nuevo recurso físico de atención con ID autoincremental.
4.  **Asignar mesa:** Vincula una mesa disponible a una orden de tipo "Dine-In" existente.
5.  **Crear orden:** Inicializador genérico para seleccionar el tipo de servicio deseado.
6.  **Pedido mesa (Dine-In):** Flujo de atención en local que bloquea la disponibilidad de una mesa física.
7.  **Pedido delivery:** Genera órdenes de despacho validando dirección (min. 5 chars) y teléfono (9-15 dígitos).
8.  **Pedido para llevar (Takeaway):** Crea órdenes directas que no consumen recursos físicos ni requieren logística de envío.
9.  **Cambiar estado:** Controla la Máquina de Estados (PENDING -> PREPARING -> READY -> DELIVERED).
10. **Cerrar orden:** Ejecuta el cierre administrativo, bloqueando ediciones y liberando recursos (mesas).
11. **Ver órdenes:** Reporte detallado del estado actual, ítems y totales de todas las comandas.
12. **Calcular total:** Ejecuta el cálculo financiero de precisión exacta sobre una orden específica.
0.  **Salir:** Finaliza la ejecución del sistema de forma segura.

## 3. ARQUITECTURA Y MÓDULOS
El sistema implementa una arquitectura de **Componentes Horizontales**, donde cada módulo es responsable de su propia lógica de negocio, persistencia y validación:

- **Módulos de Dominio:** Encapsulados en carpetas por componente (e.g., `orders/`, `tables/`), conteniendo sus propios modelos, servicios para casos de uso, repositorios in-memory y validadores locales.
- **Módulo de Excepciones:** Centraliza errores de dominio (`domain.py`) y fallos de entrada (`validation.py`).
- **Módulo de Utilidades:** Provee herramientas transversales de parsing seguro y generación de identidades únicas.
- **Capa de Presentación:** Ubicada en `menu/`, gestiona el flujo del controlador CLI y la renderización de vistas.

## 4. ESTRUCTURA DEL PROYECTO
```text
src/
├── customers/          # Gestión de base de datos de clientes
├── delivery/           # Lógica de despacho y logística
├── exceptions/         # domain.py, validation.py (Jerarquía de errores)
├── menu/               # controller.py, views.py (Orquestación CLI)
├── orders/             # models.py, services.py, states.py, validators.py
├── tables/             # Gestión de inventario de mesas y disponibilidad
├── utils/              # id_generator.py, parsing.py (Tools transversales)
└── waiters/            # Registro y control de meseros
tests/
├── conftest.py         # Fixtures globales y catálogo de datos PE/AVL
└── [componentes]/      # Pruebas unitarias parametrizadas (espejo de src)
```

## 5. TECNOLOGÍAS USADAS
- **Lenguaje:** Python 3.12+ con tipado estático (Type Hints).
- **Testing Framework:** `Pytest` para ejecución de pruebas unitarias e integrales.
- **QA Metrics:** `Pytest-cov` para auditoría de cobertura de código.


## 6. INSTALACIÓN Y EJECUCIÓN
Sigue los pasos correspondientes a tu sistema operativo para configurar el entorno de desarrollo.

### 6.1. Clonar el Repositorio (General)
```bash
git clone https://github.com/FabbPP/PS---Restaurant-System.git
cd PS---Restaurant-System
```

### 6.2. Guía para Linux / macOS (Basado en Debian/Ubuntu/Pop!_OS)
1. **Crear entorno virtual:**
   ```bash
   python3 -m venv .venv
   ```
2. **Activar entorno virtual:**
   ```bash
   source .venv/bin/activate
   ```
3. **Instalar dependencias:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Ejecución de la Aplicación:**
   ```bash
   python3 app.py
   ```

### 6.3. Guía para Windows (PowerShell / CMD)
1. **Crear entorno virtual:**
   ```powershell
   python -m venv .venv
   ```
2. **Activar entorno virtual:**
   - **PowerShell:** `.\.venv\Scripts\Activate.ps1`
   - **Command Prompt (CMD):** `.\.venv\Scripts\activate.bat`
3. **Instalar dependencias:**
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Ejecución de la Aplicación:**
   ```powershell
   python app.py
   ```

## 7. CÓMO CORRER TESTS
La suite de pruebas es el pilar de la estabilidad de este sistema.

### Ejecución Básica
```bash
# Gracias al archivo pytest.ini, puedes correrlo directamente:
pytest

# Alternativamente, si no deseas usar el .ini:
python3 -m pytest
```

### Reporte de Cobertura Detallado
Para verificar qué porcentaje del código está cubierto por pruebas:
```bash
pytest --cov=src --cov-report=term-missing
```
*Nota: El sistema mantiene una cobertura superior al 90% en lógica de negocio y servicios.*
## 8. VALIDACIONES IMPLEMENTADAS Y MANEJO DE ERRORES
El sistema utiliza una jerarquía de excepciones personalizadas para garantizar la robustez:
- **`ValidationError`**: Disparada por validators locales ante datos malformados (e.g., teléfonos con letras).
- **`StateError`**: Previene transiciones ilegales en la Máquina de Estados (e.g., saltar de 'Pendiente' a 'Entregado').
- **`ConflictError`**: Evita inconsistencias de recursos (e.g., asignar una mesa ya ocupada).
- **`NotFoundError`**: Gestiona referencias a IDs inexistentes.

Cada entrada es procesada a través de `validators.py` específicos por módulo antes de alcanzar la capa de servicio.

## 9. ENFOQUE DE TESTING (PE Y AVL)
Se ha aplicado **Black Box Testing** basado en metodologías formales de QA:
- **Partición de Equivalencia (PE):** División de entradas en clases válidas e inválidas (e.g., cantidades permitidas [1, 99] vs negativas o superiores).
- **Análisis de Valores Límite (AVL):** Pruebas exhaustivas en los bordes críticos (0, 1, 99, 100) para asegurar que no existan errores de "off-by-one".
- **Tests Parametrizados:** Uso de `@pytest.mark.parametrize` para inyectar múltiples casos de prueba sobre una misma lógica de transición o cálculo.

## 10. RESTRICCIONES, FLUJO Y DECISIONES TÉCNICAS
- **Precisión Financiera:** Se descartó el uso de `float` debido al error IEEE 754. Toda operación monetaria utiliza `Decimal` para garantizar que `0.1 + 0.2` sea exactamente `0.3`.
- **Inmutabilidad Post-Cierre:** Una vez que una orden es marcada como `closed`, el sistema bloquea cualquier adición de ítems o cambio de estado, preservando la integridad histórica de la transacción.
- **Parsing Robusto:** Mediante `utils/parsing.py`, el sistema intercepta datos corruptos o "basura" en la consola, solicitando reingreso sin provocar la caída del proceso (`Exception handling` preventivo).
- **Sincronización Automática:** El sistema vincula el ciclo de vida de la orden con el estado de la mesa física, liberando el recurso automáticamente tras el cierre administrativo.

---
*Laboratorio de Procesos de Software - Ingeniería de Software.*