
# NodoLab.py
# Listas enlazadas: programa interactivo para terminal
# Compatible con Python 3. No requiere instalar librerias.

class Nodo:
    def __init__(self, identificador, dato):
        self.id = identificador
        self.dato = dato
        self.liga = None


class NodoLab:
    def __init__(self):
        self.nodos = {}
        self.inicio = None
        self.contador = 1
        self.P = None
        self.Q = None
        self.T = None

    def crear_nodo(self, dato):
        identificador = self.contador
        self.contador += 1
        self.nodos[identificador] = Nodo(identificador, dato)
        return identificador

    def pedir_id(self, mensaje):
        try:
            identificador = int(input(mensaje))
            if identificador not in self.nodos:
                print("Error: ese nodo no existe.")
                return None
            return identificador
        except ValueError:
            print("Error: escribe un numero entero.")
            return None

    def mostrar_nodos(self):
        print("\n" + "=" * 58)
        print("                 NODOS REGISTRADOS")
        print("=" * 58)

        if not self.nodos:
            print("No hay nodos creados.")
            return

        alcanzables = self.recorrer_ids()
        alcanzables_set = set(alcanzables)

        for identificador, nodo in self.nodos.items():
            if nodo.liga is None:
                destino = "NULL"
            elif nodo.liga in self.nodos:
                destino = f"Nodo {nodo.liga}"
            else:
                destino = f"Destino inexistente ({nodo.liga})"

            if identificador == self.inicio:
                estado = "INICIO"
            elif identificador not in alcanzables_set:
                estado = "HUERFANO"
            else:
                estado = "Conectado"

            print(
                f"ID: {identificador:<4} | "
                f"DATO: {nodo.dato:<15} | "
                f"LIGA -> {destino:<24} | {estado}"
            )

        print("-" * 58)
        print(f"INICIO = {self.inicio if self.inicio is not None else 'NULL'}")
        print(f"P = {self.valor_apuntador(self.P)}")
        print(f"Q = {self.valor_apuntador(self.Q)}")
        print(f"T = {self.valor_apuntador(self.T)}")
        print("=" * 58)

    def valor_apuntador(self, identificador):
        if identificador is None:
            return "NULL"
        if identificador in self.nodos:
            return f"Nodo {identificador}"
        return "NULL"

    def recorrer_ids(self):
        recorrido = []
        visitados = set()
        actual = self.inicio

        while actual is not None and actual in self.nodos:
            if actual in visitados:
                break
            visitados.add(actual)
            recorrido.append(actual)
            actual = self.nodos[actual].liga

        return recorrido

    def mostrar_recorrido(self):
        print("\nRECORRIDO DE LA LISTA")
        print("-" * 40)

        if self.inicio is None:
            print("La lista esta vacia.")
            return

        actual = self.inicio
        visitados = set()
        elementos = []

        while actual is not None:
            if actual not in self.nodos:
                elementos.append(f"Destino inexistente ({actual})")
                break

            if actual in visitados:
                elementos.append(f"[CICLO al nodo {actual}]")
                break

            visitados.add(actual)
            nodo = self.nodos[actual]
            elementos.append(f"[{nodo.id}: {nodo.dato}]")
            actual = nodo.liga

        print(" -> ".join(elementos) + " -> NULL")

    def crear_al_inicio(self):
        dato = input("Dato del nuevo nodo: ").strip()
        if not dato:
            print("El dato no puede estar vacio.")
            return

        nuevo_id = self.crear_nodo(dato)
        self.nodos[nuevo_id].liga = self.inicio
        self.inicio = nuevo_id
        print(f"Nodo {nuevo_id} insertado al inicio.")

    def crear_al_final(self):
        dato = input("Dato del nuevo nodo: ").strip()
        if not dato:
            print("El dato no puede estar vacio.")
            return

        nuevo_id = self.crear_nodo(dato)

        if self.inicio is None:
            self.inicio = nuevo_id
        else:
            actual = self.inicio
            visitados = set()

            while self.nodos[actual].liga is not None:
                if actual in visitados:
                    print("La lista tiene un ciclo. No se puede insertar al final.")
                    del self.nodos[nuevo_id]
                    return
                visitados.add(actual)
                siguiente = self.nodos[actual].liga

                if siguiente not in self.nodos:
                    print("Hay un enlace roto. Corrigelo antes de continuar.")
                    del self.nodos[nuevo_id]
                    return

                actual = siguiente

            self.nodos[actual].liga = nuevo_id

        print(f"Nodo {nuevo_id} insertado al final.")

    def insertar_antes(self):
        objetivo = self.pedir_id("ID del nodo antes del cual insertar: ")
        if objetivo is None:
            return

        dato = input("Dato del nuevo nodo: ").strip()
        if not dato:
            print("El dato no puede estar vacio.")
            return

        nuevo_id = self.crear_nodo(dato)
        nuevo = self.nodos[nuevo_id]
        nuevo.liga = objetivo

        if self.inicio == objetivo:
            self.inicio = nuevo_id
        else:
            anterior = None
            actual = self.inicio
            visitados = set()

            while actual is not None and actual in self.nodos:
                if actual in visitados:
                    break
                visitados.add(actual)

                if self.nodos[actual].liga == objetivo:
                    anterior = actual
                    break

                actual = self.nodos[actual].liga

            if anterior is None:
                print("No se encontro el nodo anterior en la lista principal.")
                print(f"El nodo {nuevo_id} queda independiente.")
                return

            self.nodos[anterior].liga = nuevo_id

        print(f"Nodo {nuevo_id} insertado antes del nodo {objetivo}.")

    def insertar_despues(self):
        objetivo = self.pedir_id("ID del nodo despues del cual insertar: ")
        if objetivo is None:
            return

        dato = input("Dato del nuevo nodo: ").strip()
        if not dato:
            print("El dato no puede estar vacio.")
            return

        nuevo_id = self.crear_nodo(dato)
        nuevo = self.nodos[nuevo_id]
        nuevo.liga = self.nodos[objetivo].liga
        self.nodos[objetivo].liga = nuevo_id

        print(f"Nodo {nuevo_id} insertado despues del nodo {objetivo}.")

    def eliminar_nodo(self):
        identificador = self.pedir_id("ID del nodo que deseas eliminar: ")
        if identificador is None:
            return

        if self.inicio == identificador:
            self.inicio = self.nodos[identificador].liga
        else:
            actual = self.inicio
            visitados = set()

            while actual is not None and actual in self.nodos:
                if actual in visitados:
                    break
                visitados.add(actual)

                if self.nodos[actual].liga == identificador:
                    self.nodos[actual].liga = self.nodos[identificador].liga

                actual = self.nodos[actual].liga

        del self.nodos[identificador]

        # Ningun nodo debe conservar una liga hacia el nodo eliminado.
        for nodo in self.nodos.values():
            if nodo.liga == identificador:
                nodo.liga = None

        if self.P == identificador:
            self.P = None
        if self.Q == identificador:
            self.Q = None
        if self.T == identificador:
            self.T = None

        print(f"Nodo {identificador} eliminado.")

    def buscar_dato(self):
        dato = input("Dato que deseas buscar: ").strip()
        encontrados = [
            nodo.id for nodo in self.nodos.values()
            if nodo.dato == dato
        ]

        if encontrados:
            print("Encontrado en los nodos:", encontrados)
        else:
            print("No se encontro ese dato.")

    def asignar_enlace(self):
        origen = self.pedir_id("ID del nodo de origen: ")
        if origen is None:
            return

        entrada = input(
            "ID del destino (0 para NULL): "
        ).strip()

        try:
            destino = int(entrada)
        except ValueError:
            print("Debes introducir un ID numerico.")
            return

        if destino == 0:
            self.nodos[origen].liga = None
            print(f"LIGA del nodo {origen} ahora apunta a NULL.")
        elif destino in self.nodos:
            self.nodos[origen].liga = destino
            print(f"Nodo {origen} ahora apunta al nodo {destino}.")
        else:
            print("El nodo de destino no existe.")

    def dos_a_uno(self):
        print("\nDOS NODOS APUNTAN AL MISMO DESTINO")

        origen1 = self.pedir_id("ID del primer nodo de origen: ")
        if origen1 is None:
            return

        origen2 = self.pedir_id("ID del segundo nodo de origen: ")
        if origen2 is None:
            return

        if origen1 == origen2:
            print("Los dos nodos de origen deben ser distintos.")
            return

        destino = self.pedir_id("ID del nodo de destino compartido: ")
        if destino is None:
            return

        self.nodos[origen1].liga = destino
        self.nodos[origen2].liga = destino

        print(f"Nodo {origen1} -> Nodo {destino}")
        print(f"Nodo {origen2} -> Nodo {destino}")
        print("Ambos nodos apuntan al mismo destino.")

    def asignar_apuntador(self):
        nombre = input("Apuntador que deseas modificar (P, Q o T): ").upper()

        if nombre not in ("P", "Q", "T"):
            print("Apuntador no valido.")
            return

        entrada = input("ID del nodo (0 para NULL): ").strip()

        try:
            identificador = int(entrada)
        except ValueError:
            print("Debes escribir un numero entero.")
            return

        if identificador == 0:
            valor = None
        elif identificador in self.nodos:
            valor = identificador
        else:
            print("Ese nodo no existe.")
            return

        setattr(self, nombre, valor)
        print(f"{nombre} = {self.valor_apuntador(valor)}")

    def desconectar_nodo(self):
        identificador = self.pedir_id("ID del nodo que deseas desconectar: ")
        if identificador is None:
            return

        self.nodos[identificador].liga = None
        print(f"El nodo {identificador} ahora apunta a NULL.")

    def vaciar_lista(self):
        confirmacion = input(
            "Seguro que deseas eliminar todos los nodos? (s/n): "
        ).lower()

        if confirmacion == "s":
            self.nodos.clear()
            self.inicio = None
            self.P = self.Q = self.T = None
            print("Todos los nodos fueron eliminados.")

    def menu(self):
        while True:
            self.mostrar_recorrido()
            print("""
==========================================================
             NODOLAB - LISTAS ENLAZADAS
==========================================================
 1. Mostrar todos los nodos y sus enlaces
 2. Recorrer la lista desde INICIO
 3. Crear nodo al inicio
 4. Crear nodo al final
 5. Insertar nodo antes de otro
 6. Insertar nodo despues de otro
 7. Eliminar un nodo
 8. Buscar un dato
 9. Modificar una LIGA manualmente
10. Hacer que dos nodos apunten al mismo destino
11. Modificar apuntador P, Q o T
12. Desconectar un nodo (LIGA = NULL)
13. Vaciar la lista
 0. Salir
==========================================================
""")
            opcion = input("Selecciona una opcion: ").strip()

            if opcion == "1":
                self.mostrar_nodos()
            elif opcion == "2":
                self.mostrar_recorrido()
            elif opcion == "3":
                self.crear_al_inicio()
            elif opcion == "4":
                self.crear_al_final()
            elif opcion == "5":
                self.insertar_antes()
            elif opcion == "6":
                self.insertar_despues()
            elif opcion == "7":
                self.eliminar_nodo()
            elif opcion == "8":
                self.buscar_dato()
            elif opcion == "9":
                self.asignar_enlace()
            elif opcion == "10":
                self.dos_a_uno()
            elif opcion == "11":
                self.asignar_apuntador()
            elif opcion == "12":
                self.desconectar_nodo()
            elif opcion == "13":
                self.vaciar_lista()
            elif opcion == "0":
                print("Programa finalizado.")
                break
            else:
                print("Opcion no valida. Intenta de nuevo.")


if __name__ == "__main__":
    programa = NodoLab()
    programa.menu()
