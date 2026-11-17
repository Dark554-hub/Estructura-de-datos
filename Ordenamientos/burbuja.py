"""Ejercicio 1 - Método de Ordenamiento Burbuja (Bubble Sort).

Problema: Ordenar las calificaciones finales de un grupo de alumnos de menor a mayor
y mostrar el proceso de pasadas, el promedio, la calificación más baja y la más alta.
"""


def ordenamiento_burbuja(lista):
    """Ordena una lista de tuplas (alumno, calificacion) por calificación de menor a mayor."""
    datos = lista[:]
    n = len(datos)
    intercambios_totales = 0

    for i in range(n - 1):
        hubo_intercambio = False
        for j in range(n - 1 - i):
            if datos[j][1] > datos[j + 1][1]:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                hubo_intercambio = True
                intercambios_totales += 1
        print(f"Pasada {i + 1}: {[f'{nombre}({cal})' for nombre, cal in datos]}")
        if not hubo_intercambio:
            break

    return datos, intercambios_totales


if __name__ == "__main__":
    alumnos = [
        ("Ana", 88),
        ("Luis", 72),
        ("Carlos", 95),
        ("Elena", 64),
        ("Sofía", 81),
        ("Diego", 77),
    ]

    print("=== Ejercicio 1: Ordenamiento Burbuja (Calificaciones de Alumnos) ===")
    print("Lista original:", [f"{n}({c})" for n, c in alumnos])
    print("\nProceso de ordenamiento:")
    ordenados, intercambios = ordenamiento_burbuja(alumnos)

    print("\nResultado final (menor a mayor):")
    for pos, (nombre, cal) in enumerate(ordenados, 1):
        print(f"  {pos}. {nombre:<8} -> {cal}")

    promedio = sum(c for _, c in ordenados) / len(ordenados)
    print(f"\nTotal de intercambios realizados: {intercambios}")
    print(f"Menor calificación: {ordenados[0][0]} ({ordenados[0][1]})")
    print(f"Mayor calificación: {ordenados[-1][0]} ({ordenados[-1][1]})")
    print(f"Promedio del grupo: {promedio:.2f}")
