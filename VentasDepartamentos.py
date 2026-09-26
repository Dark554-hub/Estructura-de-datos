"""
Programa de gestión de Ventas Mensuales por Departamento (Matriz 2D).
Departamentos: Ropa, Deportes, Juguetería (3 columnas)
Meses: Enero a Diciembre (12 filas)
"""

# Constantes para meses y departamentos
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]
DEPARTAMENTOS = ["Ropa", "Deportes", "Juguetería"]

class GestorVentas:
    def __init__(self):
        # Matriz de 12 filas (meses) x 3 columnas (departamentos) inicializada en 0.0
        self.matriz_ventas = [[0.0 for _ in range(len(DEPARTAMENTOS))] for _ in range(len(MESES))]

    def _obtener_indice_mes(self, mes_input):
        if isinstance(mes_input, int):
            if 1 <= mes_input <= 12:
                return mes_input - 1
        elif isinstance(mes_input, str):
            mes_str = mes_input.strip().capitalize()
            if mes_str in MESES:
                return MESES.index(mes_str)
        return -1

    def _obtener_indice_dep(self, dep_input):
        if isinstance(dep_input, int):
            if 1 <= dep_input <= 3:
                return dep_input - 1
        elif isinstance(dep_input, str):
            dep_str = dep_input.strip().capitalize()
            for idx, dep in enumerate(DEPARTAMENTOS):
                if dep.lower() == dep_str.lower():
                    return idx
        return -1

    def insertar_venta(self, mes, departamento, monto):
        """1. Método para insertar o actualizar un elemento en el arreglo bidimensional."""
        idx_mes = self._obtener_indice_mes(mes)
        idx_dep = self._obtener_indice_dep(departamento)

        if idx_mes == -1 or idx_dep == -1:
            print("Error: Mes o Departamento inválido.")
            return False
        if monto < 0:
            print("Error: El monto de venta no puede ser negativo.")
            return False

        self.matriz_ventas[idx_mes][idx_dep] = float(monto)
        print(f"ÉXITO: Se insertó la venta de ${monto:.2f} en {DEPARTAMENTOS[idx_dep]} ({MESES[idx_mes]}).")
        return True

    def buscar_venta(self, mes, departamento):
        """2. Método que permite buscar el valor de una venta en particular por mes y departamento."""
        idx_mes = self._obtener_indice_mes(mes)
        idx_dep = self._obtener_indice_dep(departamento)

        if idx_mes == -1 or idx_dep == -1:
            print("Error: Mes o Departamento inválido.")
            return None

        monto = self.matriz_ventas[idx_mes][idx_dep]
        print(f"RESULTADO: La venta de {DEPARTAMENTOS[idx_dep]} en {MESES[idx_mes]} es: ${monto:.2f}")
        return monto

    def eliminar_venta(self, mes, departamento):
        """3. Método que permite eliminar una venta en particular de algún departamento (establece en 0.0)."""
        idx_mes = self._obtener_indice_mes(mes)
        idx_dep = self._obtener_indice_dep(departamento)

        if idx_mes == -1 or idx_dep == -1:
            print("Error: Mes o Departamento inválido.")
            return False

        monto_anterior = self.matriz_ventas[idx_mes][idx_dep]
        self.matriz_ventas[idx_mes][idx_dep] = 0.0
        print(f"ÉXITO: Se eliminó la venta de {DEPARTAMENTOS[idx_dep]} en {MESES[idx_mes]} (Monto anterior: ${monto_anterior:.2f}).")
        return True

    def mostrar_tabla(self):
        """Muestra la matriz bidimensional de ventas formateada."""
        print("\n" + "=" * 60)
        print(f"{'TABLA DE VENTAS MENSUALES':^60}")
        print("=" * 60)
        header = f"{'Mes':<15}" + "".join([f"{dep:>15}" for dep in DEPARTAMENTOS])
        print(header)
        print("-" * 60)
        for i, mes in enumerate(MESES):
            fila_str = f"{mes:<15}" + "".join([f"${self.matriz_ventas[i][j]:>14.2f}" for j in range(len(DEPARTAMENTOS))])
            print(fila_str)
        print("=" * 60)


def menu_interactive():
    gestor = GestorVentas()

    # Cargar algunos datos iniciales de prueba
    datos_iniciales = [
        ("Enero", "Ropa", 15000.50),
        ("Enero", "Deportes", 23000.00),
        ("Enero", "Juguetería", 18500.25),
        ("Febrero", "Ropa", 12400.00),
        ("Diciembre", "Juguetería", 45000.00),
    ]
    for m, d, v in datos_iniciales:
        gestor.insertar_venta(m, d, v)

    while True:
        print("\n--- MENÚ DE GESTIÓN DE VENTAS ---")
        print("1. Insertar / Actualizar venta")
        print("2. Buscar venta")
        print("3. Eliminar venta")
        print("4. Mostrar tabla completa de ventas")
        print("5. Salir")

        opcion = input("Selecciona una opción (1-5): ").strip()

        if opcion == "1":
            mes = input("Ingresa el mes (Nombre o número 1-12): ")
            dep = input("Ingresa el departamento (Ropa, Deportes, Juguetería o 1-3): ")
            try:
                monto = float(input("Ingresa el monto de la venta: "))
                gestor.insertar_venta(mes, dep, monto)
            except ValueError:
                print("Error: Ingresa un número válido para el monto.")

        elif opcion == "2":
            mes = input("Ingresa el mes (Nombre o número 1-12): ")
            dep = input("Ingresa el departamento (Ropa, Deportes, Juguetería o 1-3): ")
            gestor.buscar_venta(mes, dep)

        elif opcion == "3":
            mes = input("Ingresa el mes (Nombre o número 1-12): ")
            dep = input("Ingresa el departamento (Ropa, Deportes, Juguetería o 1-3): ")
            gestor.eliminar_venta(mes, dep)

        elif opcion == "4":
            gestor.mostrar_tabla()

        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    menu_interactive()
