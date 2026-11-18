def heapify(lista, n, i):
    mayor = i
    izq = 2 * i + 1
    der = 2 * i + 2

    if izq < n and lista[izq] > lista[mayor]:
        mayor = izq
    if der < n and lista[der] > lista[mayor]:
        mayor = der

    if mayor != i:
        lista[i], lista[mayor] = lista[mayor], lista[i]
        heapify(lista, n, mayor)


def heapsort(lista):
    datos = lista[:]
    n = len(datos)

    for i in range(n // 2 - 1, -1, -1):
        heapify(datos, n, i)
    print(f"  Max-Heap inicial construido: {datos}")

    for i in range(n - 1, 0, -1):
        datos[0], datos[i] = datos[i], datos[0]
        heapify(datos, i, 0)
        print(f"  Extracción {n - i} (raíz colocada al final): {datos}")

    return datos


def pedir_numeros():
    while True:
        try:
            n = int(input("\n¿Cuántos números deseas ingresar?: "))
            if n > 0:
                break
            print("Ingresa una cantidad mayor a 0.")
        except ValueError:
            print("Entrada inválida. Ingresa un número entero.")

    numeros = []
    for i in range(n):
        while True:
            try:
                num = int(input(f"  Número {i + 1}: "))
                numeros.append(num)
                break
            except ValueError:
                print("  Entrada inválida. Ingresa un número entero.")
    return numeros


def main():
    numeros = []
    while True:
        print("\n=== MENÚ HEAPSORT ===")
        print("1. Ingresar cantidad de números y capturar lista")
        print("2. Ordenar por método Heapsort")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            numeros = pedir_numeros()
            print("Lista capturada:", numeros)
        elif opcion == "2":
            if not numeros:
                numeros = pedir_numeros()
            print("\nLista original:", numeros)
            ordenada = heapsort(numeros)
            print("Lista ordenada con Heapsort:", ordenada)
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()
