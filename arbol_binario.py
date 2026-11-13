"""Implementación de un Árbol Binario de Búsqueda (ABB) con clases Nodo y Arbol."""
from collections import deque


class Nodo:
    """Representa un nodo del árbol binario."""

    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None


class Arbol:
    """Árbol Binario de Búsqueda con operaciones de inserción, búsqueda,
    eliminación, recorridos y métricas estructurales."""

    def __init__(self):
        self.raiz = None

    def esta_vacio(self):
        return self.raiz is None

    # ---------- Inserción ----------
    def insertar(self, valor):
        """Inserta un valor respetando el orden ABB (sin duplicados)."""
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izq = self._insertar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._insertar(nodo.der, valor)
        return nodo

    # ---------- Búsqueda ----------
    def buscar(self, valor):
        """Devuelve True si el valor existe en el árbol, False en caso contrario."""
        actual = self.raiz
        while actual is not None:
            if valor == actual.valor:
                return True
            actual = actual.izq if valor < actual.valor else actual.der
        return False

    def minimo(self, nodo=None):
        """Devuelve el valor mínimo del árbol (o subárbol dado)."""
        actual = self.raiz if nodo is None else nodo
        if actual is None:
            return None
        while actual.izq is not None:
            actual = actual.izq
        return actual.valor

    def maximo(self):
        """Devuelve el valor máximo del árbol."""
        actual = self.raiz
        if actual is None:
            return None
        while actual.der is not None:
            actual = actual.der
        return actual.valor

    # ---------- Eliminación ----------
    def eliminar(self, valor):
        """Elimina un nodo por su valor manteniendo la propiedad ABB."""
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return None
        if valor < nodo.valor:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            # Caso 1 y 2: sin hijos o con un solo hijo
            if nodo.izq is None:
                return nodo.der
            if nodo.der is None:
                return nodo.izq
            # Caso 3: dos hijos -> reemplaza con el sucesor inorden
            sucesor = self.minimo(nodo.der)
            nodo.valor = sucesor
            nodo.der = self._eliminar(nodo.der, sucesor)
        return nodo

    # ---------- Recorridos ----------
    def preorden(self):
        """Raíz -> Izquierda -> Derecha."""
        res = []
        self._preorden(self.raiz, res)
        return res

    def _preorden(self, nodo, res):
        if nodo is not None:
            res.append(nodo.valor)
            self._preorden(nodo.izq, res)
            self._preorden(nodo.der, res)

    def inorden(self):
        """Izquierda -> Raíz -> Derecha (devuelve los elementos ordenados)."""
        res = []
        self._inorden(self.raiz, res)
        return res

    def _inorden(self, nodo, res):
        if nodo is not None:
            self._inorden(nodo.izq, res)
            res.append(nodo.valor)
            self._inorden(nodo.der, res)

    def posorden(self):
        """Izquierda -> Derecha -> Raíz."""
        res = []
        self._posorden(self.raiz, res)
        return res

    def _posorden(self, nodo, res):
        if nodo is not None:
            self._posorden(nodo.izq, res)
            self._posorden(nodo.der, res)
            res.append(nodo.valor)

    def por_niveles(self):
        """Recorrido en amplitud (BFS) nivel por nivel."""
        if self.raiz is None:
            return []
        res = []
        cola = deque([self.raiz])
        while cola:
            actual = cola.popleft()
            res.append(actual.valor)
            if actual.izq:
                cola.append(actual.izq)
            if actual.der:
                cola.append(actual.der)
        return res

    # ---------- Métricas y visualización ----------
    def altura(self):
        """Altura del árbol (árbol vacío = 0)."""
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izq), self._altura(nodo.der))

    def contar_nodos(self):
        """Cantidad total de nodos en el árbol."""
        return self._contar_nodos(self.raiz)

    def _contar_nodos(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_nodos(nodo.izq) + self._contar_nodos(nodo.der)

    def contar_hojas(self):
        """Cantidad de nodos hoja (sin hijos)."""
        return self._contar_hojas(self.raiz)

    def _contar_hojas(self, nodo):
        if nodo is None:
            return 0
        if nodo.izq is None and nodo.der is None:
            return 1
        return self._contar_hojas(nodo.izq) + self._contar_hojas(nodo.der)

    def mostrar(self, nodo=None, nivel=0, prefijo="Raíz: ", inicio=True):
        """Imprime el árbol de forma jerárquica en consola."""
        if inicio:
            if self.raiz is None:
                print("(Árbol vacío)")
                return
            nodo = self.raiz
        if nodo is None:
            return
        print("   " * nivel + prefijo + str(nodo.valor))
        if nodo.izq or nodo.der:
            if nodo.izq:
                self.mostrar(nodo.izq, nivel + 1, "Izq- ", False)
            else:
                print("   " * (nivel + 1) + "Izq- None")
            if nodo.der:
                self.mostrar(nodo.der, nivel + 1, "Der- ", False)
            else:
                print("   " * (nivel + 1) + "Der- None")


def demostracion():
    arbol = Arbol()
    valores = [50, 30, 70, 20, 40, 60, 80]
    for v in valores:
        arbol.insertar(v)

    print("=== Árbol Binario de Búsqueda ===")
    arbol.mostrar()

    print("\nRecorridos:")
    print("  Preorden   :", arbol.preorden())
    print("  Inorden    :", arbol.inorden())
    print("  Posorden   :", arbol.posorden())
    print("  Por niveles:", arbol.por_niveles())

    print("\nPropiedades:")
    print("  Total nodos:", arbol.contar_nodos())
    print("  Hojas      :", arbol.contar_hojas())
    print("  Altura     :", arbol.altura())
    print("  Mínimo     :", arbol.minimo())
    print("  Máximo     :", arbol.maximo())

    print("\nBúsquedas:")
    print("  ¿Existe 40?:", arbol.buscar(40))
    print("  ¿Existe 99?:", arbol.buscar(99))

    print("\nEliminando el nodo raíz (50)...")
    arbol.eliminar(50)
    arbol.mostrar()
    print("  Inorden tras eliminar 50:", arbol.inorden())


if __name__ == "__main__":
    demostracion()
