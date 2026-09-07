import random
import statistics


def calcular_estadisticas():
    # 1. Generar 50 números enteros aleatorios entre 1 y 100
    numeros = [random.randint(150, 250) for _ in range(50)]

    # 2. Cálculos estadísticos
    media = statistics.mean(numeros)
    mediana = statistics.median(numeros)
    moda = statistics.multimode(numeros)  # Lista con el/los valores más frecuentes
    varianza = statistics.variance(numeros)  # Varianza muestral (n - 1)
    desviacion_std = statistics.stdev(numeros)  # Desviación estándar muestral

    # 3. Mostrar resultados
    print("--- Datos generados (50 valores) ---")
    print(numeros)
    print("\n--- Resultados Estadísticos ---")
    print(f"Media:               {media:.2f}")
    print(f"Mediana:             {mediana}")
    print(f"Moda:                {moda}")
    print(f"Varianza:            {varianza:.2f}")
    print(f"Desviación estándar: {desviacion_std:.2f}")


if __name__ == "__main__":
    calcular_estadisticas()