# ESPECIFICACIÓN FORMAL DE REQUERIMIENTOS DEL SISTEMA (REQUIREMENTS.md)

Este documento define los lineamientos técnicos, operativos y de calidad del **PS---Restaurant-System**. Su cumplimiento es obligatorio para garantizar la integridad transaccional y la robustez del software.

## 1. GUÍA DE CONFIGURACIÓN Y EJECUCIÓN LOCAL

Siga los pasos correspondientes a su sistema operativo para configurar el entorno de desarrollo.

### 1.1. Clonar el Repositorio (General)
```bash
git clone https://github.com/FabbPP/PS---Restaurant-System.git
cd PS---Restaurant-System
```

### 1.2. Guía para Linux / macOS (Basado en Debian/Ubuntu/Pop!_OS)
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

### 1.3. Guía para Windows (PowerShell / CMD)
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
``

## 2. REQUERIMIENTOS FUNCIONALES (RF)

Mapeo de las capacidades operativas del sistema CLI:

- **RF-01 (Añadir mesero):** Registra personal de servicio. El nombre debe ser puramente alfabético y con espacios. Dispara `ValidationError` ante números o caracteres especiales.
- **RF-02 (Listar meseros):** Recupera y visualiza la colección completa de meseros activos.
- **RF-03 (Añadir mesa):** Crea una nueva mesa con ID secuencial gestionado por `IdGenerator`.
- **RF-04 (Asignar mesa):** Vincula una orden "Dine-In" a una mesa libre. Debe listar previamente mesas disponibles y órdenes activas para facilitar la selección.
- **RF-05 (Crear orden):** Provee un sub-menú para seleccionar el tipo de servicio (Mesa, Delivery o Para llevar).
- **RF-06 (Pedido mesa):** Inicia flujo Dine-In. Permite asignar una mesa disponible al momento de la creación.
- **RF-07 (Pedido delivery):** Requiere cliente, dirección (mín. 5 caracteres) y teléfono numérico estrictamente entre 9 y 15 dígitos.
- **RF-08 (Pedido para llevar):** Genera una orden de tipo "Takeaway" sin dependencias físicas de mesa ni logística de envío.
- **RF-09 (Cambiar estado):** Controla la FSM de la orden. Valida transiciones legales: `PENDING` -> `PREPARING` -> `READY` -> `DELIVERED`.
- **RF-10 (Cerrar orden):** Ejecuta el cierre administrativo de la orden. Bloquea la adición de ítems, calcula el total final y libera automáticamente la mesa si era Dine-In.
- **RF-11 (Ver órdenes):** Genera un reporte tabular con el ID, tipo, estado, mesa y total de todas las comandas.
- **RF-12 (Calcular total):** Ejecuta la sumatoria de ítems de una orden específica con precisión decimal absoluta.
- **RF-00 (Salir):** Termina el bucle de ejecución de la CLI y cierra el proceso de forma segura.

## 3. REQUERIMIENTOS NO FUNCIONALES (RNF)

- **RNF-01 (Precisión Financiera):** Uso mandatorio de la API `Decimal` para evitar errores de coma flotante (IEEE 754). Se prohíben cálculos con `float` en montos.
- **RNF-02 (Robustez de la Interfaz):** Tolerancia a fallos contra entradas "basura" mediante validadores centrales en `src/utils/parsing.py`. El sistema no debe colapsar ante datos corruptos.
- **RNF-03 (Modularidad por Componentes):** Organización horizontal del código en paquetes independientes (`waiters`, `tables`, `orders`, `delivery`, `customers`).

## 4. REGLAS DE NEGOCIO Y RESTRICCIONES CRÍTICAS

- **Validación de Identidad:** El nombre del mesero no acepta valores numéricos; de lo contrario, relanza `ValidationError`.
- **Máquina de Estados (FSM):** Se prohíben saltos ilegales (ej: de `PENDING` a `DELIVERED`) y regresiones de estado.
- **Invariante de Inmutabilidad:** Una orden con `closed=True` no puede ser modificada bajo ninguna circunstancia (ni ítems ni estados).
- **Integridad de Mesa:** Una mesa ocupada no puede asignarse a una nueva orden hasta que la orden previa sea cerrada o cancelada.
- **Anti-crash CLI:** Toda excepción de negocio o validación debe ser atrapada por el `MenuController`, informando al usuario sin terminar el proceso.

## 5. MATRIZ DE DISEÑO DE ENTRADAS (PE / AVL)

| Campo | Rango Válido | Partición de Equivalencia (PE) | Análisis de Valores Límite (AVL) |
| :--- | :--- | :--- | :--- |
| **IDs** | Enteros > 0 | Válido: [1, n] / Inválido: 0, Negativos | 0 (Err), 1 (Ok) |
| **Nombre Mesero** | Alfabético | Válido: Letras y espacios / Inválido: Números, símbolos | "Luis" (Ok), "Luis123" (Err) |
| **Longitud Nombre** | [1, 60] chars | Válido: 1-60 / Inválido: Vacío, > 60 | 0 (Err), 1 (Ok), 60 (Ok), 61 (Err) |
| **Cant. Ítems** | [1, 99] | Válido: Enteros [1, 99] / Inválido: 0, > 99 | 0 (Err), 1 (Ok), 99 (Ok), 100 (Err) |
| **Precio Unitario** | [0.01, 9999.99] | Válido: Decimal > 0 / Inválido: 0.00, Negativos | 0.00 (Err), 0.01 (Ok), 9999.99 (Ok) |
| **Teléfono** | [9, 15] dígitos | Válido: Numérico 9-15 / Inválido: < 9, > 15, letras | 8 (Err), 9 (Ok), 15 (Ok), 16 (Err) |

## 6. CRITERIOS DE ACEPTACIÓN DE QA

Para que un requerimiento se considere aprobado, debe superar las siguientes aserciones en `pytest`:

1.  **Consistencia de Repositorio:** El objeto retornado debe coincidir con los datos de entrada y persistir en la colección interna.
2.  **Validación de Excepciones:** Los flujos inválidos (según la matriz PE/AVL) deben disparar exactamente `ValidationError` o `DomainError`.
3.  **Sincronización de Estados:** Al cerrar una orden de mesa, la consulta inmediata al `TableService` debe retornar `is_available = True`.
4.  **Exactitud Decimal:** Las pruebas de cálculo de total deben compararse contra objetos `Decimal`, nunca contra valores de punto flotante aproximados.
5.  **Cobertura Mínima:** Cada módulo de `src/` debe mantener una cobertura de líneas superior al 90%.