def counting_por_digito(lista, exp):
    n = len(lista)
    salida = [0] * n
    conteo = [0] * 10

    for num in lista:
        indice = (num // exp) % 10
        conteo[indice] += 1

    for i in range(1, 10):
        conteo[i] += conteo[i - 1]

    for i in range(n - 1, -1, -1):
        indice = (lista[i] // exp) % 10
        salida[conteo[indice] - 1] = lista[i]
        conteo[indice] -= 1

    for i in range(n):
        lista[i] = salida[i]


def radix_sort(lista):
    if not lista:
        return []

    negativos = [-x for x in lista if x < 0]
    positivos = [x for x in lista if x >= 0]

    if positivos:
        max_pos = max(positivos)
        exp = 1
        while max_pos // exp > 0:
            counting_por_digito(positivos, exp)
            print(f"  Ordenando por posición decimal {exp}: {positivos}")
            exp *= 10

    if negativos:
        max_neg = max(negativos)
        exp = 1
        while max_neg // exp > 0:
            counting_por_digito(negativos, exp)
            exp *= 10
        negativos = [-x for x in reversed(negativos)]

    return negativos + positivos


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
        print("\n=== MENÚ RADIX SORT ===")
        print("1. Ingresar cantidad de números y capturar lista")
        print("2. Ordenar por método Radix Sort")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            numeros = pedir_numeros()
            print("Lista capturada:", numeros)
        elif opcion == "2":
            if not numeros:
                numeros = pedir_numeros()
            print("\nLista original:", numeros)
            ordenada = radix_sort(numeros)
            print("Lista ordenada con Radix Sort:", ordenada)
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()
