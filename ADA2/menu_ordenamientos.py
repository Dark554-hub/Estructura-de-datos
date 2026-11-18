from shellsort import shell_sort
from quicksort import quicksort
from heapsort import heapsort
from radix import radix_sort


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
                num = int(input(f"  Ingresa el número {i + 1}: "))
                numeros.append(num)
                break
            except ValueError:
                print("  Entrada inválida. Ingresa un número entero.")
    return numeros


def main():
    numeros = pedir_numeros()

    while True:
        print("\n==========================================")
        print("      MENÚ DE MÉTODOS DE ORDENAMIENTO     ")
        print("==========================================")
        print(f"Lista actual ({len(numeros)} elementos): {numeros}")
        print("1. Ordenar por ShellSort")
        print("2. Ordenar por Quicksort")
        print("3. Ordenar por Heapsort")
        print("4. Ordenar por Radix Sort")
        print("5. Cambiar / ingresar nuevos números")
        print("6. Salir")
        opcion = input("Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            print("\n--- Método ShellSort ---")
            print("Lista original:", numeros)
            res = shell_sort(numeros)
            print("Resultado ordenado:", res)
        elif opcion == "2":
            print("\n--- Método Quicksort ---")
            print("Lista original:", numeros)
            res = quicksort(numeros)
            print("Resultado ordenado:", res)
        elif opcion == "3":
            print("\n--- Método Heapsort ---")
            print("Lista original:", numeros)
            res = heapsort(numeros)
            print("Resultado ordenado:", res)
        elif opcion == "4":
            print("\n--- Método Radix Sort ---")
            print("Lista original:", numeros)
            res = radix_sort(numeros)
            print("Resultado ordenado:", res)
        elif opcion == "5":
            numeros = pedir_numeros()
        elif opcion == "6":
            print("\nPrograma finalizado.")
            break
        else:
            print("\nOpción no válida. Elige entre 1 y 6.")


if __name__ == "__main__":
    main()
