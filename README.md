# Estructura de Datos - Gestión de Ventas Mensuales por Departamento

Este repositorio contiene las implementaciones en **Python** y **Java** de un sistema de gestión de ventas mensuales representadas mediante **arreglos bidimensionales (matrices 2D)**.

---

## 📌 Descripción del Programa

El programa gestiona una matriz de **12 filas** (correspondientes a los meses del año, de Enero a Diciembre) por **3 columnas** (correspondientes a los departamentos: *Ropa*, *Deportes* y *Juguetería*).

### Estructura de la Matriz:
| Mes | Ropa (Columna 0) | Deportes (Columna 1) | Juguetería (Columna 2) |
|---|---|---|---|
| **Enero (Fila 0)** | Ventas Ropa | Ventas Deportes | Ventas Juguetería |
| **Febrero (Fila 1)** | Ventas Ropa | Ventas Deportes | Ventas Juguetería |
| ... | ... | ... | ... |
| **Diciembre (Fila 11)** | Ventas Ropa | Ventas Deportes | Ventas Juguetería |

---

## ⚙️ Explicación de los Métodos Principales

### 1. Método para Insertar / Actualizar Elementos
* **Python:** `insertar_venta(mes, departamento, monto)`
* **Java:** `insertarVenta(String mes, String departamento, double monto)`
* **Funcionamiento:** Recibe el mes (por nombre o número 1-12), el departamento (por nombre o número 1-3) y la cantidad a registrar. Convierte los parámetros a los índices numéricos correspondientes de la matriz `[fila][columna]` y asigna el valor. Valida que los índices estén en rango y que el monto sea no negativo.

### 2. Método para Buscar un Elemento en Particular
* **Python:** `buscar_venta(mes, departamento)`
* **Java:** `buscarVenta(String mes, String departamento)`
* **Funcionamiento:** Localiza la celda correspondiente en la matriz `[índice_mes][índice_departamento]`, extrae el monto de venta acumulado/registrado y lo retorna o muestra en consola.

### 3. Método para Eliminar una Venta en Particular
* **Python:** `eliminar_venta(mes, departamento)`
* **Java:** `eliminarVenta(String mes, String departamento)`
* **Funcionamiento:** Ubica la celda `[índice_mes][índice_departamento]` especificada por el usuario y restablece su valor a `0.0`, dejando el registro del departamento sin ventas para ese mes.

---

## 🚀 Ejecución del Código

### En Python:
```bash
python VentasDepartamentos.py
```

### En Java:
```bash
javac VentasDepartamentos.java
java VentasDepartamentos
```
