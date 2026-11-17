"""Ejercicio 3 - Método de Ordenamiento por Selección (Selection Sort).

Problema: Ordenar el catálogo de productos de una tienda de tecnología del más económico
al más costoso seleccionando en cada paso el precio mínimo restante.
"""


def ordenamiento_seleccion(lista):
    """Ordena una lista de tuplas (producto, precio) por precio ascendente."""
    datos = lista[:]
    n = len(datos)
    comparaciones = 0

    for i in range(n - 1):
        idx_min = i
        for j in range(i + 1, n):
            comparaciones += 1
            if datos[j][1] < datos[idx_min][1]:
                idx_min = j
        if idx_min != i:
            datos[i], datos[idx_min] = datos[idx_min], datos[i]
        print(f"Paso {i + 1} (mínimo seleccionado: {datos[i][0]} ${datos[i][1]}): "
              f"{[f'{p}(${pr})' for p, pr in datos]}")

    return datos, comparaciones


if __name__ == "__main__":
    productos = [
        ("Monitor", 3200),
        ("Mouse", 350),
        ("Teclado", 780),
        ("Audífonos", 620),
        ("Webcam", 950),
        ("SSD 1TB", 1450),
    ]

    print("=== Ejercicio 3: Ordenamiento por Selección (Precios de Productos) ===")
    print("Catálogo original:", [f"{p}(${pr})" for p, pr in productos])
    print("\nProceso de selección:")
    catalogo_ordenado, comparaciones = ordenamiento_seleccion(productos)

    print("\nCatálogo ordenado por precio (menor a mayor):")
    for idx, (prod, precio) in enumerate(catalogo_ordenado, 1):
        print(f"  {idx}. {prod:<10} -> ${precio}")

    print(f"\nTotal de comparaciones realizadas: {comparaciones}")
