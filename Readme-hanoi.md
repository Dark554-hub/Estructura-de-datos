Torre de Hanoi en Python
Descripción
Este proyecto implementa el problema clásico de la Torre de Hanoi utilizando recursividad en Python. El programa calcula cuántos movimientos se necesitan para resolver el problema con distintas cantidades de discos y mide el tiempo de ejecución cuando la cantidad de movimientos permite realizar una prueba práctica.
Objetivo
Implementar la Torre de Hanoi en Python, identificar las funciones utilizadas, analizar el crecimiento del número de movimientos y comparar el rendimiento para 5, 10, 30 y 64 discos.
¿Cómo funciona?
El problema consiste en trasladar una torre de discos desde una varilla de origen hasta una varilla de destino, utilizando una varilla auxiliar.
Reglas:
Solo se puede mover un disco a la vez.
Solo se puede retirar el disco que está en la parte superior de una varilla.
Nunca se puede colocar un disco grande encima de uno más pequeño.
La solución recursiva sigue estos pasos:
Mover los n - 1 discos superiores desde el origen hasta la varilla auxiliar.
Mover el disco más grande hasta el destino.
Mover los n - 1 discos desde la varilla auxiliar hasta el destino.
El caso base ocurre cuando queda un solo disco: se necesita un movimiento.
Funciones utilizadas
El programa maneja dos funciones principales:
torre_hanoi(n, origen, auxiliar, destino): resuelve recursivamente el problema y devuelve el número total de movimientos.
medir_tiempo(n): mide cuánto tarda la ejecución con time.perf_counter() y devuelve el total de movimientos y el tiempo transcurrido.
El bloque if __name__ == "__main__": sirve como punto de entrada del programa; no es una función ni un método.
Fórmula de movimientos
El número mínimo de movimientos para n discos es:
M(n) = 2ⁿ − 1
Por eso, el número de movimientos aumenta exponencialmente al incrementar los discos.
Código
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

        print(f"\\nDiscos: {n}")
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
Pruebas y resultados
La tabla muestra el número exacto de movimientos que requiere la solución. Los tiempos de ejecución deben completarse después de correr el programa en el equipo utilizado.
Número de discos
Movimientos mínimos
Estado de la prueba
5
31
Se ejecuta y mide el tiempo
10
1,023
Se ejecuta y mide el tiempo
30
1,073,741,823
Se omite la ejecución por su costo computacional
64
18,446,744,073,709,551,615
Se omite la ejecución por su costo computacional
Nota: este programa no registra ni imprime cada movimiento de forma individual; cuenta los movimientos mediante la estructura recursiva. Esto evita que el tiempo de impresión en pantalla afecte la medición. Para 30 y 64 discos, el programa calcula la cantidad teórica de movimientos y omite la ejecución completa, porque implicaría realizar una cantidad excesiva de operaciones. Por ello, no se presentan tiempos inventados para esos casos.
Cómo ejecutar el programa
Se necesita tener Python 3 instalado.
Guarda el código en un archivo llamado torre_hanoi.py.
Abre una terminal en la carpeta del archivo.
Ejecuta:
python torre_hanoi.py
Copia los tiempos reales que aparezcan para 5 y 10 discos en la tabla de resultados si se requiere entregar la medición del equipo.
Conclusiones
La Torre de Hanoi permite comprender cómo funciona la recursividad, ya que un problema grande se divide en problemas más pequeños hasta llegar a un caso base. La implementación utiliza dos funciones principales: una para resolver recursivamente el problema y contar los movimientos, y otra para medir el tiempo de ejecución.
Los resultados teóricos muestran un crecimiento exponencial. Con 5 discos se necesitan 31 movimientos y con 10 discos, 1,023. Con 30 discos se requieren más de mil millones de movimientos y con 64 discos se necesitan 18,446,744,073,709,551,615 movimientos.
Por lo tanto, aunque el algoritmo es sencillo de implementar y correcto para resolver el problema, el costo de ejecución crece rápidamente con el número de discos. Este ejemplo demuestra la importancia de analizar la complejidad de los algoritmos y no solamente verificar que produzcan el resultado esperado.
Estructura del repositorio
Torre-de-Hanoi-Python/
├── README.md
└── torre_hanoi.py
