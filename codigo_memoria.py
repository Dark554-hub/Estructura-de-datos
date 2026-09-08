# =====================================================================
# EJEMPLOS DE MEMORIA ESTÁTICA Y MEMORIA DINÁMICA EN PYTHON
# Código limpio ideal para demostraciones académicas y diapositivas
# =====================================================================

def ejemplo_memoria_estatica():
    """
    Simulación de Memoria Estática.
    Define un tamaño fijo y rígido desde el inicio que no puede alterarse.
    """
    print("=== 1. DEMOSTRACIÓN DE MEMORIA ESTÁTICA ===")
    
    # 1. Definimos un tamaño fijo estricto (5 posiciones)
    TAMAÑO_FIJO = 5
    calificaciones = [None] * TAMAÑO_FIJO
    
    print(f"Memoria reservada inicialmente: {calificaciones}")
    print(f"Tamaño fijo inicial: {TAMAÑO_FIJO} posiciones.")
    
    # 2. Llenamos los espacios reservados por medio de asignación directa
    calificaciones[0] = 85
    calificaciones[1] = 90
    calificaciones[2] = 78
    calificaciones[3] = 92
    calificaciones[4] = 88
    
    print(f"Memoria después de asignar datos: {calificaciones}")
    
    # 3. Intento de desbordamiento de memoria (Lanzará un error)
    print("\nIntentando agregar un elemento extra en la posición [5]...")
    try:
        calificaciones[5] = 95  # Intentamos acceder a un índice no reservado
    except IndexError as error:
        print(f"-> [ERROR CONTROLADO]: {error}")
        print("-> Explicación: No podemos expandir la memoria estática una vez creada.")


def ejemplo_memoria_dinamica():
    """
    Simulación de Memoria Dinámica.
    Permite solicitar y liberar recursos de manera flexible en tiempo de ejecución.
    """
    print("\n=== 2. DEMOSTRACIÓN DE MEMORIA DINÁMICA ===")
    
    # 1. Inicializamos una estructura vacía sin tamaño predefinido (Tamaño = 0)
    frutas = []
    print(f"Memoria inicial vacía: {frutas} | Tamaño actual: {len(frutas)}")
    
    # 2. Agregamos elementos de forma dinámica (La memoria se expande)
    print("\n--- Agregando elementos (Expansión) ---")
    frutas.append("Mango")
    frutas.append("Manzana")
    frutas.append("Durazno")
    print(f"Memoria actual: {frutas} | Tamaño: {len(frutas)}")
    
    # 3. Removemos un elemento de forma dinámica (La memoria se contrae)
    print("\n--- Removiendo elemento (Contracción) ---")
    fruta_eliminada = fruits.pop(0) if 'fruits' in locals() else frutas.pop(0)  # Elimina el primer elemento ("Mango")
    print(f"Se eliminó '{fruta_eliminada}' de la memoria.")
    print(f"Memoria actual: {frutas} | Tamaño: {len(frutas)}")
    
    # 4. Agregamos otro elemento sobre la marcha
    print("\n--- Agregando nuevo elemento en ejecución ---")
    frutas.append("Sandía")
    print(f"Memoria final: {frutas} | Tamaño final: {len(frutas)}")


if __name__ == "__main__":
    ejemplo_memoria_estatica()
    ejemplo_memoria_dinamica()
