def quicksort(lista, profundidad=0):
    if len(lista) <= 1:
        return lista

    pivote = lista[len(lista) // 2]
    menores = [x for x in lista if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista if x > pivote]

    print(f"  {'  ' * profundidad}Pivote={pivote} -> menores={menores}, iguales={iguales}, mayores={mayores}")
    return quicksort(menores, profundidad + 1) + iguales + quicksort(mayores, profundidad + 1)


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
        print("\n=== MENÚ QUICKSORT ===")
        print("1. Ingresar cantidad de números y capturar lista")
        print("2. Ordenar por método Quicksort")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            numeros = pedir_numeros()
            print("Lista capturada:", numeros)
        elif opcion == "2":
            if not numeros:
                numeros = pedir_numeros()
            print("\nLista original:", numeros)
            ordenada = quicksort(numeros)
            print("Lista ordenada con Quicksort:", ordenada)
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()
