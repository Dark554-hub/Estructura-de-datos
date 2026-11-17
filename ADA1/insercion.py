"""Ejercicio 2 - Método de Ordenamiento por Inserción (Insertion Sort).

Problema: Ordenar los tiempos de llegada (en segundos) de corredores en una carrera
de 100 metros planos para determinar el podio del más rápido al más lento.
"""


def ordenamiento_insercion(lista):
    """Ordena una lista de tuplas (corredor, tiempo) de menor a mayor tiempo."""
    datos = lista[:]
    desplazamientos = 0

    for i in range(1, len(datos)):
        actual = datos[i]
        j = i - 1
        while j >= 0 and datos[j][1] > actual[1]:
            datos[j + 1] = datos[j]
            j -= 1
            desplazamientos += 1
        datos[j + 1] = actual
        print(f"Inserción {i} ({actual[0]} - {actual[1]}s): {[f'{c}({t}s)' for c, t in datos[:i + 1]]}")

    return datos, desplazamientos


if __name__ == "__main__":
    corredores = [
        ("Mateo", 11.42),
        ("Valeria", 10.85),
        ("Jorge", 12.10),
        ("Camila", 10.58),
        ("Andrés", 11.05),
        ("Lucía", 10.92),
    ]

    print("=== Ejercicio 2: Ordenamiento por Inserción (Tiempos de Carrera 100m) ===")
    print("Registro de llegada:", [f"{c}({t}s)" for c, t in corredores])
    print("\nProceso de inserción:")
    clasificacion, desplazamientos = ordenamiento_insercion(corredores)

    print("\nClasificación final:")
    medallas = {1: "Oro", 2: "Plata", 3: "Bronce"}
    for lugar, (nombre, tiempo) in enumerate(clasificacion, 1):
        extra = f" [{medallas[lugar]}]" if lugar in medallas else ""
        print(f"  {lugar}° lugar: {nombre:<8} - {tiempo:.2f} s{extra}")

    print(f"\nDesplazamientos realizados: {desplazamientos}")
