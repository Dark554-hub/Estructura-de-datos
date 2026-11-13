"""Algoritmo de Kruskal: arbol de expansion minima usando Union-Find."""


class UnionFind:
    def __init__(self, nodos):
        self.padre = {n: n for n in nodos}
        self.rango = {n: 0 for n in nodos}

    def find(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.find(self.padre[x])  # compresion de caminos
        return self.padre[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False  # formaria un ciclo
        if self.rango[ra] < self.rango[rb]:
            ra, rb = rb, ra
        self.padre[rb] = ra
        if self.rango[ra] == self.rango[rb]:
            self.rango[ra] += 1
        return True


def kruskal(nodos, aristas):
    """aristas: lista de (peso, u, v). Devuelve (arbol, peso_total)."""
    uf = UnionFind(nodos)
    arbol, total = [], 0
    for peso, u, v in sorted(aristas):
        aceptada = uf.union(u, v)
        print(f"Arista {u}-{v} (peso {peso}): {'ACEPTADA' if aceptada else 'rechazada (ciclo)'}")
        if aceptada:
            arbol.append((u, v, peso))
            total += peso
    return arbol, total


if __name__ == "__main__":
    nodos = ["A", "B", "C", "D", "E", "F"]
    aristas = [
        (4, "A", "B"), (2, "A", "C"), (1, "B", "C"), (5, "B", "D"),
        (8, "C", "D"), (10, "C", "E"), (2, "D", "E"), (6, "D", "F"), (3, "E", "F"),
    ]
    print("=== Algoritmo de Kruskal ===")
    arbol, total = kruskal(nodos, aristas)
    print("\nArbol de expansion minima:")
    for u, v, p in arbol:
        print(f"  {u} - {v}  (peso {p})")
    print(f"Peso total: {total}")
