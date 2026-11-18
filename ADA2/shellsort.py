def shell_sort(lista):
    datos = lista[:]
    n = len(datos)
    salto = n // 2
    paso = 1

    while salto > 0:
        for i in range(salto, n):
            temp = datos[i]
            j = i
            while j >= salto and datos[j - salto] > temp:
                datos[j] = datos[j - salto]
                j -= salto
            datos[j] = temp
        print(f"  Paso {paso} (salto = {salto}): {datos}")
        salto //= 2
        paso += 1

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
        print("\n=== MENÚ SHELLSORT ===")
        print("1. Ingresar cantidad de números y capturar lista")
        print("2. Ordenar por método ShellSort")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            numeros = pedir_numeros()
            print("Lista capturada:", numeros)
        elif opcion == "2":
            if not numeros:
                numeros = pedir_numeros()
            print("\nLista original:", numeros)
            ordenada = shell_sort(numeros)
            print("Lista ordenada con ShellSort:", ordenada)
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()
