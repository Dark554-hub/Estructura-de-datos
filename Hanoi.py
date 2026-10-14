
import time


def torre_hanoi(n, origen, auxiliar, destino):
    """Resuelve la Torre de Hanoi y cuenta los movimientos."""
    if n == 1:
        return 1

    movimientos = torre_hanoi(n - 1, origen, destino, auxiliar)
    movimientos += 1
    movimientos += torre_hanoi(n - 1, auxiliar, origen, destino)

    return movimientos


def medir_tiempo(n):
    inicio = time.perf_counter()

    movimientos = torre_hanoi(n, "A", "B", "C")

    fin = time.perf_counter()
    return movimientos, fin - inicio


if __name__ == "__main__":
    discos_prueba = [5, 10, 30, 64]
    limite_practico = 1_000_000

    for n in discos_prueba:
        movimientos_teoricos = 2**n - 1

        print(f"\nDiscos: {n}")
        print(f"Movimientos necesarios: {movimientos_teoricos:,}")

        if movimientos_teoricos <= limite_practico:
            movimientos, tiempo = medir_tiempo(n)
            print(f"Tiempo medido: {tiempo:.8f} segundos")
            print(f"Movimientos realizados: {movimientos:,}")
        else:
            print(
                "Tiempo: no medido; "
                "se omite por el costo computacional."
            )
          
