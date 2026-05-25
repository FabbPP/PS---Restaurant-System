# PS---Restaurant-System
[!Quality Assurance](https://docs.pytest.org/)
[!Python Version](https://www.python.org/)
[!License](LICENSE)

Sistema profesional de gestión de restaurante y despacho (Delivery) desarrollado bajo estándares de arquitectura limpia, diseñado para operar mediante una interfaz de línea de comandos (CLI) robusta y altamente confiable.

## 1. DESCRIPCIÓN Y OBJETIVO
El **PS---Restaurant-System** es una solución integral para la gestión operativa de establecimientos gastronómicos. Su objetivo principal es resolver la fragmentación en la toma de pedidos y la gestión de inventario/mesas mediante un sistema centralizado que garantiza la integridad de los datos. 

El sistema soluciona problemas críticos como:
- Errores de precisión financiera mediante el uso de aritmética de punto fijo.
- Inconsistencias de estado (ej. asignar pedidos a mesas ocupadas).
- Fallos por entradas de usuario inválidas o malformadas.
- Falta de trazabilidad en el ciclo de vida de una orden.

## 2. FUNCIONALIDADES
El sistema implementa las 12 funciones operativas obligatorias para un flujo de negocio completo:
1.  **Gestión de Meseros:** Registro y listado de personal de servicio.
2.  **Gestión de Mesas:** Control de inventario físico de mesas con estados dinámicos.
3.  **Registro de Clientes:** Base de datos para clientes frecuentes, esencial para el módulo de delivery.
4.  **Apertura de Órdenes de Mesa (Dine-in):** Vinculación automática entre mesa, orden y estado de ocupación.
5.  **Creación de Órdenes para Llevar (Takeaway):** Flujo simplificado sin asignación de recursos físicos.
6.  **Gestión de Delivery:** Creación de órdenes con validación de datos de contacto y dirección geográfica.
7.  **Catálogo Dinámico de Ítems:** Capacidad de añadir productos a cualquier orden activa.
8.  **Cálculo Financiero de Precisión:** Sumatoria de subtotales y totales utilizando la API `Decimal`.
9.  **Máquina de Estados de Órdenes:** Control estricto de transiciones (Pendiente -> Preparando -> Entregado).
10. **Sincronización de Recursos:** Liberación automática de mesas al cerrar o cancelar órdenes de comedor.
11. **Validación de Reglas de Negocio:** Restricciones que impiden, por ejemplo, añadir ítems a órdenes ya cerradas.
12. **Interfaz de Control (CLI):** Menú interactivo con manejo de excepciones para prevenir cierres inesperados.

## 3. ARQUITECTURA Y MÓDULOS
El proyecto sigue una arquitectura en capas basada en el principio de responsabilidad única (SRP), organizada dentro del directorio `src/`:

- **`src/domain/`**: El núcleo del sistema. Contiene las entidades (`Order`, `Table`, `OrderItem`) y la lógica de estados. Aquí residen las invariantes de negocio que no dependen de marcos externos.
- **`src/application/`**: Servicios (`OrderService`, `TableService`) que orquestan los casos de uso y coordinan la interacción entre el dominio y los repositorios.
- **`src/infrastructure/`**: Implementaciones de persistencia in-memory a través de Repositorios, asegurando que el acceso a datos sea agnóstico a la lógica de negocio.
- **`src/presentation/`**: El controlador del menú y las vistas de consola. Se encarga de la entrada/salida y el formateo de datos para el usuario final.
- **`src/validators/`**: Utilidades transversales para la normalización y validación de tipos, longitudes y formatos.

## 4. TECNOLOGÍAS
- **Lenguaje:** Python 3.12+ (aprovechando el tipado estático avanzado).
- **Aritmética:** `Decimal API` para evitar errores de redondeo de `float` en transacciones financieras.
- **Testing:** `Pytest` para pruebas unitarias e integrales.
- **Cobertura:** `Pytest-cov` para auditoría de rutas de código probadas.
- **Modelado:** `Dataclasses` para una representación de datos limpia y eficiente.

## 5. INSTALACIÓN Y EJECUCIÓN
Sigue los pasos correspondientes a tu sistema operativo para configurar el entorno de desarrollo.

### 5.1. Clonar el Repositorio (General)
```bash
git clone https://github.com/FabbPP/PS---Restaurant-System.git
cd PS---Restaurant-System
```

### 5.2. Guía para Linux / macOS (Basado en Debian/Ubuntu/Pop!_OS)
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

### 5.3. Guía para Windows (PowerShell / CMD)
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

## 6. CÓMO CORRER TESTS
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

## 7. ENFOQUE DE TESTING (CALIDAD DE SOFTWARE)
Se ha aplicado una metodología de **Black Box Testing** rigurosa para blindar el software contra comportamientos inesperados:

### Partición de Equivalencia (PE)
Se dividieron los dominios de entrada en grupos de comportamiento similar para optimizar la cantidad de tests:
- **Teléfonos:** Particiones válidas (9-15 dígitos), inválidas (letras), e incompletas (vacíos).
- **Precios:** Particiones positivas, negativas (rechazadas) y cero (rechazada para ítems).
- **Nombres:** Longitudes aceptadas (1-60 caracteres) vs desbordamientos.

### Análisis de Valores Límite (AVL)
Se testearon los bordes críticos para evitar errores de "fuera por uno":
- **Cantidades:** Se probaron los valores 0, 1, 99 y 100 para asegurar que el rango [1, 99] se respete estrictamente.
- **Precios:** Validación en 0.00, 0.01 y 9999.99.
- **IDs:** Validación de que solo IDs > 0 sean procesados por los repositorios.

## 8. EJEMPLOS DE USO Y RESTRICCIONES

### Migración a Decimal
A diferencia de otros sistemas que usan `float`, este sistema utiliza `from decimal import Decimal`. Esto garantiza que un precio de `19.99` sumado 100 veces sea exactamente `1999.00`, eliminando los residuos binarios indeseados.

### Restricciones Técnicas Clave
- **Invariante de Mesa:** Una mesa no puede pasar a estado `libre` si tiene una orden asociada con estado `PENDING` o `PREPARING`.
- **Integridad de Delivery:** No se permite la creación de una orden de despacho si el objeto `DeliveryInfo` no cumple con la validación de dirección (min 5 chars) y teléfono.
- **Cierre Administrativo:** Una vez que una orden se marca como `closed`, el sistema bloquea cualquier modificación de ítems o cambio de estado para preservar la auditoría.

---
*Desarrollado como parte del Laboratorio de Procesos de Software - Tarea 05.*
