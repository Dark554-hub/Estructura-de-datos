# Control de Ventas por Departamento

Este programa en Python gestiona las ventas mensuales de una tienda dividida en tres departamentos: Ropa, Deportes y Juguetería, a lo largo de los 12 meses del año.

La información se almacena utilizando una matriz bidimensional (arreglo 2D) donde cada fila representa un mes (de Enero a Diciembre) y cada columna representa uno de los departamentos.

## Estructura de los datos

La matriz tiene un tamaño de 12 x 3:

- Filas (12): Enero (índice 0) hasta Diciembre (índice 11).
- Columnas (3): Ropa (índice 0), Deportes (índice 1) y Juguetería (índice 2).

## Explicación de los métodos

### 1. Método para insertar o actualizar ventas (`insertar_venta`)
Este método recibe el mes, el departamento y la cantidad vendida. Se encarga de convertir el mes y el departamento a sus posiciones numéricas dentro de la matriz para guardar el valor correspondiente. Antes de registrar la venta, valida que el mes y el departamento existan y que el monto no sea negativo.

### 2. Método para buscar una venta (`buscar_venta`)
Permite consultar la venta registrada de un departamento en un mes específico. Recibe como parámetro el mes y el departamento a consultar, ubica la celda en la matriz y regresa o muestra en pantalla la cifra registrada.

### 3. Método para eliminar una venta (`eliminar_venta`)
Sirve para borrar el registro de una venta en particular. Al indicarle el mes y el departamento, la función ubica la posición en la matriz y reinicia su valor a cero.

## Cómo ejecutar el programa

Para correr el programa en la consola, ejecuta el siguiente comando:

```bash
python VentasDepartamentos.py
```
