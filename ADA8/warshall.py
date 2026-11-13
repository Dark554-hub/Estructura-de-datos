"""Algoritmo de Warshall: cerradura transitiva (alcanzabilidad) de un grafo."""


def warshall(adyacencia):
    n = len(adyacencia)
    r = [fila[:] for fila in adyacencia]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                r[i][j] = r[i][j] or (r[i][k] and r[k][j])
    return r


def imprimir(m, etiquetas):
    print("    " + " ".join(etiquetas))
    for e, fila in zip(etiquetas, m):
        print(f"{e}   " + " ".join(str(int(v)) for v in fila))


if __name__ == "__main__":
    etiquetas = ["A", "B", "C", "D"]
    m = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]
    print("=== Algoritmo de Warshall ===")
    print("Matriz de adyacencia:")
    imprimir(m, etiquetas)
    cierre = warshall(m)
    print("\nCerradura transitiva:")
    imprimir(cierre, etiquetas)
    print("\nAlcanzabilidad:")
    for i, e in enumerate(etiquetas):
        alc = [etiquetas[j] for j in range(len(m)) if cierre[i][j]]
        print(f"Desde {e} se puede llegar a: {', '.join(alc) if alc else 'ninguno'}")
