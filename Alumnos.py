import timeit
import random
import csv

# Listas base para generar nombres aleatorios
nombres_base = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Elena", "Jorge", "Sofia", "Miguel", "Laura", "Pedro", "Lucia", "Diego", "Carmen", "Raul"]
apellidos_base = ["Perez", "Gomez", "Lopez", "Diaz", "Martinez", "Hernandez", "Garcia", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Cruz", "Reyes", "Ruiz"]

# Generamos 500 nombres unicos
nombres_alumnos = []
for _ in range(500):
    nombre = random.choice(nombres_base)
    apellido1 = random.choice(apellidos_base)
    apellido2 = random.choice(apellidos_base)
    nombres_alumnos.append(f"{nombre} {apellido1} {apellido2}")

# Nombres de las materias
nombres_materias = ["Matematicas", "Ciencias", "Historia", "Literatura", "Geografia", "Deportes"]

TOTAL_ALUMNOS = 5000
TOTAL_MATERIAS = 6

# 1. Generar matrices con calificaciones aleatorias
matriz_forma_alumnos_materias = []
for i in range(TOTAL_ALUMNOS):
    calificaciones = [random.randint(50, 100) for _ in range(TOTAL_MATERIAS)]
    matriz_forma_alumnos_materias.append(calificaciones)

matriz_forma_materias_alumnos = [[matriz_forma_alumnos_materias[a][m] for a in range(TOTAL_ALUMNOS)] for m in range(TOTAL_MATERIAS)]

def buscar_rendimiento_forma1():
    # Busca en estructura [Materia][Alumno] (Materia 5 es indice 4, Alumno 321 es indice 320)
    return matriz_forma_materias_alumnos[4][320]

def buscar_rendimiento_forma2():
    # Busca en estructura [Alumno][Materia]
    return matriz_forma_alumnos_materias[320][4]

if __name__ == "__main__":
    # --- 2. EXPORTAR A ARCHIVO PARA EXCEL (CSV) ---
    nombre_archivo = "calificaciones_alumnos.csv"
    with open(nombre_archivo, mode='w', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["No.", "Nombre del Alumno"] + nombres_materias)
        for a in range(TOTAL_ALUMNOS):
            fila = [a + 1, nombres_alumnos[a]] + matriz_forma_alumnos_materias[a]
            writer.writerow(fila)
            
    print(f"EXITO: Se exportaron los 500 alumnos al archivo '{nombre_archivo}'.")
    
    # --- 3. MEDICION DE RENDIMIENTO (Requisito original) ---
    iteraciones = 10000000
    tiempo_forma1 = timeit.timeit(buscar_rendimiento_forma1, number=iteraciones)
    tiempo_forma2 = timeit.timeit(buscar_rendimiento_forma2, number=iteraciones)
    
    print("\n--- PRUEBA DE VELOCIDAD (Alumno 321, Materia 5) ---")
    if tiempo_forma1 < tiempo_forma2:
        print("-> La primera forma (Materias x Alumnos) se ejecuto mas rapido.")
    else:
        print("-> La segunda forma (Alumnos x Materias) se ejecuto mas rapido.")

    # --- 4. BUSQUEDA INTERACTIVA DE CALIFICACIONES ---
    print("\n" + "="*50)
    print("SISTEMA DE BUSQUEDA DE CALIFICACIONES")
    print("="*50)
    
    # Mostramos las materias disponibles una sola vez como guia
    print("\nMaterias disponibles:")
    for i, mat in enumerate(nombres_materias):
        print(f" {i+1}. {mat}")
            
    while True:
        entrada_alumno = input("\nIngresa el numero de alumno (1-500) o escribe 'salir' para terminar: ")
        
        if entrada_alumno.lower() == 'salir':
            print("Saliendo del programa...")
            break
            
        try:
            num_alumno = int(entrada_alumno)
            if num_alumno < 1 or num_alumno > 500:
                print("Error: El numero de alumno debe estar entre 1 y 500.")
                continue
                
            entrada_materia = input("Ingresa el numero de materia (1-6): ")
            num_materia = int(entrada_materia)
            
            if num_materia < 1 or num_materia > 6:
                print("Error: El numero de materia debe estar entre 1 y 6.")
                continue
                
            # Ajustamos a base 0 para buscar correctamente en las listas de Python
            idx_alumno = num_alumno - 1
            idx_materia = num_materia - 1
            
            # Obtenemos los datos correspondientes
            nombre_encontrado = nombres_alumnos[idx_alumno]
            materia_encontrada = nombres_materias[idx_materia]
            calificacion = matriz_forma_alumnos_materias[idx_alumno][idx_materia]
            
            print("-" * 50)
            print(f"RESULTADO: El alumno {num_alumno} ({nombre_encontrado})")
            print(f"tiene una calificacion de {calificacion} en {materia_encontrada}.")
            print("-" * 50)
            
        except ValueError:
            print("Error: Por favor ingresa un numero entero valido.")