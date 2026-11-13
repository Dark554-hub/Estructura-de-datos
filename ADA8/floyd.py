"""Algoritmo de Floyd(-Warshall): caminos mas cortos entre todos los pares."""

INF = float("inf")


def floyd(matriz):
    n = len(matriz)
    dist = [fila[:] for fila in matriz]
    sig = [[j if matriz[i][j] != INF and i != j else None for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    sig[i][j] = sig[i][k]
    return dist, sig


def ruta(sig, i, j):
    if sig[i][j] is None:
        return [] if i != j else [i]
    r = [i]
    while i != j:
        i = sig[i][j]
        r.append(i)
    return r


def imprimir(m, etiquetas):
    print("     " + "".join(f"{e:>5}" for e in etiquetas))
    for e, fila in zip(etiquetas, m):
        print(f"{e:>4} " + "".join(f"{'INF' if v == INF else v:>5}" for v in fila))


if __name__ == "__main__":
    etiquetas = ["A", "B", "C", "D"]
    m = [
        [0, 3, INF, 7],
        [8, 0, 2, INF],
        [5, INF, 0, 1],
        [2, INF, INF, 0],
    ]
    print("=== Algoritmo de Floyd ===")
    print("Matriz inicial:")
    imprimir(m, etiquetas)
    dist, sig = floyd(m)
    print("\nMatriz de distancias minimas:")
    imprimir(dist, etiquetas)
    print("\nRutas:")
    for i in range(4):
        for j in range(4):
            if i != j:
                r = " -> ".join(etiquetas[x] for x in ruta(sig, i, j))
                print(f"{etiquetas[i]} a {etiquetas[j]}: costo {dist[i][j]}  ruta {r}")
