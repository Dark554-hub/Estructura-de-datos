"""Algoritmo de Dijkstra: caminos mas cortos desde un origen (pesos >= 0)."""
import heapq

INF = float("inf")


def dijkstra(grafo, origen):
    """grafo: dict {nodo: [(vecino, peso), ...]}. Devuelve (distancias, previos)."""
    dist = {n: INF for n in grafo}
    previo = {n: None for n in grafo}
    dist[origen] = 0
    cola = [(0, origen)]  # cola de prioridad (distancia, nodo)
    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:
            continue  # entrada obsoleta
        for v, peso in grafo[u]:
            nueva = d + peso
            if nueva < dist[v]:
                dist[v] = nueva
                previo[v] = u
                heapq.heappush(cola, (nueva, v))
    return dist, previo


def camino(previo, destino):
    ruta = []
    while destino is not None:
        ruta.append(destino)
        destino = previo[destino]
    return ruta[::-1]


if __name__ == "__main__":
    grafo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2), ("F", 6)],
        "E": [("C", 10), ("D", 2), ("F", 3)],
        "F": [("D", 6), ("E", 3)],
    }
    origen = "A"
    dist, previo = dijkstra(grafo, origen)
    print(f"=== Algoritmo de Dijkstra (origen: {origen}) ===")
    for nodo in grafo:
        print(f"{origen} -> {nodo}: distancia = {dist[nodo]:>2}  ruta = {' -> '.join(camino(previo, nodo))}")
