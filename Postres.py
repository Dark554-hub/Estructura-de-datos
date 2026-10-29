"""
POSTRES: arreglo ordenado alfabéticamente; cada elemento tiene una lista
ligada simple con los ingredientes del postre.
"""


class NodoIngrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.sig = None          # NIL = None


class Postre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cabeza = None       # lista de ingredientes (NIL si está vacía)


def norm(texto):
    return texto.strip().lower()


class Postres:
    def __init__(self):
        self.arreglo = []        # arreglo ordenado por nombre

    # ---------- utilidades ----------
    def _buscar(self, nombre):
        """Búsqueda binaria. Devuelve (indice, encontrado).
        Si no existe, indice es la posición donde debe insertarse."""
        izq, der = 0, len(self.arreglo) - 1
        while izq <= der:
            med = (izq + der) // 2
            actual = self.arreglo[med].nombre
            if actual == nombre:
                return med, True
            if actual < nombre:
                izq = med + 1
            else:
                der = med - 1
        return izq, False

    # ---------- a) imprimir ingredientes ----------
    def imprimir(self, nombre):
        nombre = norm(nombre)
        if not self.arreglo:
            print("El arreglo POSTRES está vacío.")
            return False
        i, ok = self._buscar(nombre)
        if not ok:
            print(f"El postre '{nombre}' no existe.")
            return False
        p = self.arreglo[i]
        if p.cabeza is None:
            print(f"'{p.nombre}' no tiene ingredientes (lista vacía).")
            return True
        print(f"Ingredientes de '{p.nombre}':")
        q = p.cabeza
        while q is not None:
            print(f"  - {q.nombre}")
            q = q.sig
        return True

    # ---------- b) insertar ingrediente ----------
    def insertar_ingrediente(self, postre, ingrediente):
        postre, ingrediente = norm(postre), norm(ingrediente)
        if not ingrediente:
            print("El ingrediente no puede ser vacío.")
            return False
        i, ok = self._buscar(postre)
        if not ok:
            print(f"El postre '{postre}' no existe.")
            return False
        p = self.arreglo[i]
        nuevo = NodoIngrediente(ingrediente)
        if p.cabeza is None:                 # lista vacía
            p.cabeza = nuevo
            return True
        q = p.cabeza
        while True:
            if q.nombre == ingrediente:      # ya existe
                print(f"'{ingrediente}' ya está en '{p.nombre}'.")
                return False
            if q.sig is None:
                break
            q = q.sig
        q.sig = nuevo                        # se inserta al final
        return True

    # ---------- c) eliminar ingrediente ----------
    def eliminar_ingrediente(self, postre, ingrediente):
        postre, ingrediente = norm(postre), norm(ingrediente)
        i, ok = self._buscar(postre)
        if not ok:
            print(f"El postre '{postre}' no existe.")
            return False
        p = self.arreglo[i]
        if p.cabeza is None:
            print(f"'{p.nombre}' no tiene ingredientes.")
            return False
        if p.cabeza.nombre == ingrediente:   # primero
            p.cabeza = p.cabeza.sig
            return True
        ant, q = p.cabeza, p.cabeza.sig
        while q is not None:
            if q.nombre == ingrediente:      # medio o último
                ant.sig = q.sig
                return True
            ant, q = q, q.sig
        print(f"'{ingrediente}' no está en '{p.nombre}'.")
        return False

    # ---------- d) alta de postre ----------
    def alta(self, postre, ingredientes):
        postre = norm(postre)
        if not postre:
            print("El nombre del postre no puede ser vacío.")
            return False
        i, ok = self._buscar(postre)
        if ok:
            print(f"El postre '{postre}' ya existe.")
            return False
        nuevo = Postre(postre)
        self.arreglo.insert(i, nuevo)        # conserva el orden alfabético
        for ing in ingredientes:             # duplicados se ignoran
            self.insertar_ingrediente(postre, ing)
        return True

    # ---------- e) baja de postre ----------
    def baja(self, postre):
        postre = norm(postre)
        if not self.arreglo:
            print("El arreglo POSTRES está vacío.")
            return False
        i, ok = self._buscar(postre)
        if not ok:
            print(f"El postre '{postre}' no existe.")
            return False
        self.arreglo[i].cabeza = None        # se libera la lista completa
        del self.arreglo[i]                  # se recorre el arreglo
        return True

    # ---------- Problema 2 ----------
    def eliminar_repetidos(self, fusionar=False):
        """Elimina postres repetidos (quedan adyacentes por estar ordenado).
        fusionar=False: se conserva la 1a aparición y la lista del repetido
                        se pierde.
        fusionar=True : antes de borrar, sus ingredientes se pasan al original.
        """
        i = 0
        while i < len(self.arreglo) - 1:
            if self.arreglo[i].nombre == self.arreglo[i + 1].nombre:
                if fusionar:
                    q = self.arreglo[i + 1].cabeza
                    while q is not None:
                        self.insertar_ingrediente(self.arreglo[i].nombre, q.nombre)
                        q = q.sig
                self.arreglo[i + 1].cabeza = None
                del self.arreglo[i + 1]
            else:
                i += 1

    def mostrar_todo(self):
        for p in self.arreglo:
            ings, q = [], p.cabeza
            while q is not None:
                ings.append(q.nombre)
                q = q.sig
            print(f"{p.nombre}: {ings}")


def cargar_sin_validar(postres, nombre, ingredientes):
    """Carga directa (permite repetidos) solo para probar el Problema 2."""
    p = Postre(norm(nombre))
    ultimo = None
    for ing in ingredientes:
        n = NodoIngrediente(norm(ing))
        if ultimo is None:
            p.cabeza = n
        else:
            ultimo.sig = n
        ultimo = n
    postres.arreglo.append(p)


def demo_problema_2():
    print("\n=== PROBLEMA 2 ===")
    P = Postres()
    cargar_sin_validar(P, "flan", ["huevo", "leche", "azúcar"])
    cargar_sin_validar(P, "flan", ["vainilla", "caramelo"])   # repetido
    cargar_sin_validar(P, "pastel", ["harina", "huevo"])
    cargar_sin_validar(P, "pastel", ["chocolate"])            # repetido
    print("Antes:")
    P.mostrar_todo()
    P.eliminar_repetidos()
    print("Después de eliminar repetidos:")
    P.mostrar_todo()


def menu():
    P = Postres()
    while True:
        print("\n1) Imprimir ingredientes  2) Insertar ingrediente  "
              "3) Eliminar ingrediente\n4) Alta de postre  5) Baja de postre  "
              "6) Mostrar todo  7) Problema 2 (demo)  0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            P.imprimir(input("Postre: "))
        elif op == "2":
            P.insertar_ingrediente(input("Postre: "), input("Ingrediente: "))
        elif op == "3":
            P.eliminar_ingrediente(input("Postre: "), input("Ingrediente: "))
        elif op == "4":
            nombre = input("Postre: ")
            ings = [x for x in input("Ingredientes (separados por coma): ").split(",")
                    if x.strip()]
            P.alta(nombre, ings)
        elif op == "5":
            P.baja(input("Postre: "))
        elif op == "6":
            P.mostrar_todo()
        elif op == "7":
            demo_problema_2()
        elif op == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
