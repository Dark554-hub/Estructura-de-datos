"""Genera capturas (salidas, trazas, grafos y codigo) y arma el reporte Word completo."""
import contextlib
import heapq
import io
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from docx_min import Document, Inches  # noqa: E402
import dijkstra as mod_dij  # noqa: E402
import floyd as mod_floyd  # noqa: E402
import kruskal as mod_kru  # noqa: E402
import warshall as mod_war  # noqa: E402

CAPS = os.path.join(AQUI, "capturas")
os.makedirs(CAPS, exist_ok=True)
INF = float("inf")
FUENTE = "C:/Windows/Fonts/consola.ttf"


def correr(f, *a, **k):
    """Ejecuta f capturando lo que imprime."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = f(*a, **k)
    return buf.getvalue(), r


# ---------- imagenes ----------
def captura(texto, nombre, titulo="PowerShell - python", numerar=False):
    fuente = ImageFont.truetype(FUENTE, 18)
    lineas = texto.rstrip().splitlines()
    if numerar:
        lineas = [f"{i:>3} | {l}" for i, l in enumerate(lineas, 1)]
    w = int(max(fuente.getlength(l) for l in lineas) + 40)
    h = len(lineas) * 24 + 70
    img = Image.new("RGB", (max(w, 500), h), (30, 30, 30))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, 28], fill=(60, 60, 60))
    d.text((10, 4), titulo, fill=(220, 220, 220), font=fuente)
    for i, l in enumerate(lineas):
        d.text((20, 40 + i * 24), l, fill=(204, 204, 204), font=fuente)
    ruta = os.path.join(CAPS, nombre + ".png")
    img.save(ruta)
    return ruta


def grafo_img(nombre, pos, aristas, dirigido=False, resaltar=(), inicio=None, ancho=640, alto=420):
    """aristas: (u, v, etiqueta). resaltar: conjunto de (u, v)."""
    img = Image.new("RGB", (ancho, alto), "white")
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FUENTE, 20)
    clave = (lambda u, v: (u, v)) if dirigido else (lambda u, v: frozenset((u, v)))
    res = {clave(u, v) for u, v in resaltar}
    R = 24
    for u, v, et in aristas:
        (x1, y1), (x2, y2) = pos[u], pos[v]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        off = 9 if dirigido else 0
        x1o, y1o, x2o, y2o = x1 + nx * off, y1 + ny * off, x2 + nx * off, y2 + ny * off
        hl = clave(u, v) in res
        col = (0, 150, 60) if hl else (120, 120, 120)
        d.line([x1o, y1o, x2o, y2o], fill=col, width=5 if hl else 2)
        if dirigido:
            ux, uy = dx / L, dy / L
            tx, ty = x2o - ux * R, y2o - uy * R
            d.polygon([(tx, ty), (tx - ux * 14 + nx * 6, ty - uy * 14 + ny * 6),
                       (tx - ux * 14 - nx * 6, ty - uy * 14 - ny * 6)], fill=col)
        mx, my = (x1o + x2o) / 2 + nx * 14, (y1o + y2o) / 2 + ny * 14 - (0 if dirigido else 0)
        tag = str(et)
        d.rectangle([mx - 4 - 6 * len(tag), my - 12, mx + 4 + 6 * len(tag), my + 12], fill="white")
        d.text((mx - 6 * len(tag), my - 11), tag, fill=(180, 30, 30), font=f)
    for n, (x, y) in pos.items():
        col = (255, 215, 90) if n == inicio else (190, 215, 255)
        d.ellipse([x - R, y - R, x + R, y + R], fill=col, outline=(30, 60, 120), width=3)
        d.text((x - 6, y - 11), n, fill="black", font=f)
    ruta = os.path.join(CAPS, nombre + ".png")
    img.save(ruta)
    return ruta


# ---------- trazas (paso a paso) ----------
def traza_dijkstra(grafo, origen):
    dist = {n: INF for n in grafo}
    dist[origen] = 0
    cola = [(0, origen)]
    hecho = set()
    paso = 1
    print(f"Traza de Dijkstra desde {origen}\n")
    while cola:
        d, u = heapq.heappop(cola)
        if u in hecho:
            continue
        hecho.add(u)
        print(f"Paso {paso}: se extrae {u} con distancia {d}")
        for v, p in grafo[u]:
            if v in hecho:
                continue
            if d + p < dist[v]:
                ant = "INF" if dist[v] == INF else dist[v]
                print(f"   relajar {u}->{v}: {d}+{p}={d + p} < {ant}  => dist[{v}] = {d + p}")
                dist[v] = d + p
                heapq.heappush(cola, (d + p, v))
            else:
                print(f"   {u}->{v}: {d}+{p}={d + p} no mejora {dist[v]}")
        paso += 1
    print("\nDistancias finales:", dist)


def fmt(m, et):
    s = "     " + "".join(f"{e:>5}" for e in et) + "\n"
    for e, fila in zip(et, m):
        s += f"{e:>4} " + "".join(f"{'INF' if v == INF else int(v):>5}" for v in fila) + "\n"
    return s


def traza_floyd(m, et):
    n = len(m)
    d = [r[:] for r in m]
    print("Matriz inicial D0:\n" + fmt(d, et))
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    print(f"   k={et[k]}: {et[i]}->{et[j]} mejora a {d[i][k]}+{d[k][j]}={d[i][k] + d[k][j]}")
                    d[i][j] = d[i][k] + d[k][j]
        print(f"Matriz D{k + 1} (intermedio {et[k]}):\n" + fmt(d, et))


def traza_warshall(m, et):
    n = len(m)
    r = [f[:] for f in m]
    print("R0 (adyacencia):\n" + fmt(r, et))
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if not r[i][j] and r[i][k] and r[k][j]:
                    print(f"   k={et[k]}: {et[i]}->{et[k]} y {et[k]}->{et[j]} => nuevo camino {et[i]}->{et[j]}")
                r[i][j] = r[i][j] or (r[i][k] and r[k][j])
        print(f"R{k + 1} (intermedio {et[k]}):\n" + fmt(r, et))


# ---------- datos ----------
G = {
    "A": [("B", 4), ("C", 2)], "B": [("A", 4), ("C", 1), ("D", 5)],
    "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)], "D": [("B", 5), ("C", 8), ("E", 2), ("F", 6)],
    "E": [("C", 10), ("D", 2), ("F", 3)], "F": [("D", 6), ("E", 3)],
}
POS6 = {"A": (70, 210), "B": (220, 90), "C": (220, 330), "D": (410, 90), "E": (410, 330), "F": (570, 210)}
ARIS6 = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8),
         ("C", "E", 10), ("D", "E", 2), ("D", "F", 6), ("E", "F", 3)]
POS4 = {"A": (120, 110), "B": (440, 110), "C": (440, 320), "D": (120, 320)}
ET4 = ["A", "B", "C", "D"]
FL1 = [[0, 3, INF, 7], [8, 0, 2, INF], [5, INF, 0, 1], [2, INF, INF, 0]]
FL1_A = [("A", "B", 3), ("A", "D", 7), ("B", "A", 8), ("B", "C", 2), ("C", "A", 5), ("C", "D", 1), ("D", "A", 2)]
FL2 = [[0, 1, INF, INF], [INF, 0, -2, INF], [4, INF, 0, 3], [INF, INF, INF, 0]]
FL2_A = [("A", "B", 1), ("B", "C", -2), ("C", "A", 4), ("C", "D", 3)]
WA1 = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
WA1_A = [("A", "B", ""), ("B", "C", ""), ("C", "D", "")]
ET5 = ["A", "B", "C", "D", "E"]
POS5 = {"A": (90, 110), "B": (320, 80), "C": (540, 110), "D": (200, 330), "E": (480, 330)}
WA2 = [[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]]
WA2_A = [("A", "B", ""), ("B", "C", ""), ("C", "A", ""), ("D", "E", "")]
NODOS6 = list("ABCDEF")
AR_K1 = [(4, "A", "B"), (2, "A", "C"), (1, "B", "C"), (5, "B", "D"), (8, "C", "D"),
         (10, "C", "E"), (2, "D", "E"), (6, "D", "F"), (3, "E", "F")]
NODOS5 = list("ABCDE")
POS5K = {"A": (80, 110), "B": (300, 80), "C": (540, 110), "D": (160, 330), "E": (460, 330)}
AR_K2 = [(7, "A", "B"), (5, "A", "D"), (8, "B", "C"), (9, "B", "D"), (7, "B", "E"),
         (5, "C", "E"), (15, "D", "E")]


def ruta_codigo(arch):
    with open(os.path.join(AQUI, arch), encoding="utf-8") as f:
        return captura(f.read(), "codigo_" + arch[:-3], f"{arch} - codigo fuente", numerar=True)


# ---------- documento ----------
doc = Document()
AN = Inches(6.3)
ALTO = Inches(8.3)


def figura(ruta, pie):
    doc.add_picture(ruta, AN, max_height=ALTO)
    doc.add_caption(pie)


doc.add_heading("Reporte: Algoritmos de Grafos en Python", 0)
doc.add_paragraph("Materia: Estructura de Datos")
doc.add_paragraph("Actividad: ADA 8 - Algoritmos de Dijkstra, Floyd, Warshall y Kruskal")
doc.add_paragraph("Repositorio: https://github.com/Dark554-hub/Estructura-de-datos (carpeta ADA8)")
doc.add_paragraph("Lenguaje: Python 3")

doc.add_heading("1. Introducción", 1)
doc.add_paragraph(
    "Un grafo es una estructura de datos formada por nodos (vértices) conectados por aristas, que pueden "
    "tener un peso (costo, distancia, tiempo) y una dirección. Los grafos modelan problemas reales como "
    "mapas de carreteras, redes de computadoras, redes sociales o rutas de transporte.")
doc.add_paragraph(
    "En esta práctica se implementaron en Python cuatro algoritmos clásicos sobre grafos. Para cada uno se "
    "explica para qué sirve, cómo funciona, se muestra el código, se presentan capturas de su ejecución y de "
    "una traza paso a paso, y se analiza el resultado.")
doc.add_heading("Resumen comparativo", 2)
doc.add_table([
    ["Algoritmo", "Problema que resuelve", "Estructura", "Complejidad", "Pesos negativos"],
    ["Dijkstra", "Camino mínimo desde un origen a todos", "Lista de adyacencia + cola de prioridad", "O((V+E) log V)", "No"],
    ["Floyd", "Camino mínimo entre todos los pares", "Matriz de distancias", "O(V³)", "Sí (sin ciclos negativos)"],
    ["Warshall", "Alcanzabilidad (cerradura transitiva)", "Matriz booleana", "O(V³)", "No aplica"],
    ["Kruskal", "Árbol de expansión mínima", "Lista de aristas + Union-Find", "O(E log E)", "Sí"],
])

# ===== DIJKSTRA =====
doc.add_page_break()
doc.add_heading("2. Algoritmo de Dijkstra", 1)
doc.add_heading("2.1 ¿Para qué sirve?", 2)
doc.add_paragraph(
    "Encuentra el camino de menor costo desde un nodo origen hacia todos los demás nodos de un grafo con "
    "pesos no negativos. Fue propuesto por Edsger W. Dijkstra en 1956.")
doc.add_paragraph("Aplicaciones:")
for t in ["Navegación GPS y mapas (ruta más corta o más rápida).",
          "Enrutamiento en redes de computadoras (protocolos OSPF e IS-IS).",
          "Logística y planeación de rutas de entrega.",
          "Videojuegos (búsqueda de caminos de personajes)."]:
    doc.add_bullet(t)
doc.add_heading("2.2 ¿Cómo funciona?", 2)
for t in ["Se asigna distancia 0 al nodo origen e infinito a todos los demás.",
          "Se guarda el origen en una cola de prioridad (heapq) ordenada por distancia.",
          "Se extrae el nodo con menor distancia conocida; ese nodo ya tiene su distancia definitiva.",
          "Para cada vecino se calcula distancia_actual + peso de la arista. Si es menor que la distancia guardada, "
          "se actualiza (relajación) y se anota el nodo previo para reconstruir la ruta.",
          "Se repite hasta vaciar la cola. Siguiendo los nodos previos desde el destino se obtiene la ruta."]:
    doc.add_bullet(t)
doc.add_paragraph("Limitación: no funciona correctamente si existen aristas con peso negativo.")
doc.add_heading("2.3 Código", 2)
figura(ruta_codigo("dijkstra.py"), "Captura 1. Código de dijkstra.py")
doc.add_heading("2.4 Grafo de prueba", 2)
doc.add_paragraph("Se usó un grafo no dirigido de 6 nodos (A-F). Los números rojos son los pesos de las aristas. "
                  "El nodo amarillo es el origen.")
figura(grafo_img("dij_grafo", POS6, ARIS6, inicio="A"), "Captura 2. Grafo de prueba")
doc.add_heading("2.5 Ejecución", 2)
salida, _ = correr(lambda: mod_dij.dijkstra(G, "A"))
txt_a, _ = correr(lambda: [print(f"A -> {n}: distancia = {mod_dij.dijkstra(G, 'A')[0][n]:>2}  ruta = "
                                 f"{' -> '.join(mod_dij.camino(mod_dij.dijkstra(G, 'A')[1], n))}") for n in G])
figura(captura("=== Algoritmo de Dijkstra (origen: A) ===\n" + txt_a, "dij_salida"), "Captura 3. Salida del programa (origen A)")
doc.add_paragraph("Interpretación: el costo mínimo de A a B es 3 (A→C→B = 2+1), mejor que la arista directa A-B de peso 4. "
                  "La ruta más larga es A→F con costo 13, pasando por C, B, D y E.")
doc.add_heading("2.6 Traza paso a paso", 2)
t, _ = correr(traza_dijkstra, G, "A")
figura(captura(t, "dij_traza"), "Captura 4. Cada paso extrae el nodo más cercano y relaja a sus vecinos")
doc.add_heading("2.7 Ruta resaltada en el grafo", 2)
rutaAF = [("A", "C"), ("C", "B"), ("B", "D"), ("D", "E"), ("E", "F")]
figura(grafo_img("dij_ruta", POS6, ARIS6, resaltar=rutaAF, inicio="A"), "Captura 5. Camino mínimo A→F (en verde)")
doc.add_heading("2.8 Segunda prueba: otro origen", 2)
d2, p2 = mod_dij.dijkstra(G, "F")
txt, _ = correr(lambda: [print(f"F -> {n}: distancia = {d2[n]:>2}  ruta = {' -> '.join(mod_dij.camino(p2, n))}") for n in G])
figura(captura("=== Algoritmo de Dijkstra (origen: F) ===\n" + txt, "dij_salida2"), "Captura 6. Salida con origen F")
doc.add_paragraph("Al cambiar el origen cambia todo el árbol de caminos mínimos. Desde F, el nodo más cercano es E (3) y el más lejano es A (13).")

# ===== FLOYD =====
doc.add_page_break()
doc.add_heading("3. Algoritmo de Floyd (Floyd-Warshall)", 1)
doc.add_heading("3.1 ¿Para qué sirve?", 2)
doc.add_paragraph(
    "Calcula el camino de menor costo entre todos los pares de nodos de un grafo dirigido con pesos. A diferencia de "
    "Dijkstra, resuelve el problema para todos los orígenes a la vez y admite aristas negativas siempre que no "
    "existan ciclos negativos. Es un ejemplo de programación dinámica.")
for t in ["Tablas de distancias entre ciudades.", "Detección de ciclos negativos (diagonal con valores negativos).",
          "Cálculo de centralidad y diámetro de una red.", "Tablas de enrutamiento completas."]:
    doc.add_bullet(t)
doc.add_heading("3.2 ¿Cómo funciona?", 2)
for t in ["Se parte de una matriz D con el peso de cada arista, 0 en la diagonal e INF si no hay arista directa.",
          "Para cada nodo k (posible intermedio) y para cada par (i, j) se prueba si pasar por k mejora: "
          "D[i][k] + D[k][j] < D[i][j].",
          "Si mejora, se actualiza D[i][j] y se guarda el siguiente nodo en la matriz de rutas.",
          "Al terminar los tres ciclos anidados, D contiene las distancias mínimas entre todos los pares."]:
    doc.add_bullet(t)
doc.add_heading("3.3 Código", 2)
figura(ruta_codigo("floyd.py"), "Captura 7. Código de floyd.py")
doc.add_heading("3.4 Grafo de prueba 1", 2)
figura(grafo_img("flo_grafo1", POS4, FL1_A, dirigido=True), "Captura 8. Grafo dirigido de 4 nodos")
doc.add_heading("3.5 Ejecución", 2)
txt, _ = correr(lambda: __import__("runpy").run_path(os.path.join(AQUI, "floyd.py"), run_name="__main__"))
figura(captura(txt, "flo_salida"), "Captura 9. Matriz inicial, matriz final y rutas")
doc.add_paragraph("Interpretación: de A a C no existía arista directa (INF); después del algoritmo el costo mínimo es 5, "
                  "con la ruta A→B→C (3+2).")
doc.add_heading("3.6 Traza por cada nodo intermedio", 2)
t, _ = correr(traza_floyd, FL1, ET4)
figura(captura(t, "flo_traza"), "Captura 10. Matrices D1 a D4 y las mejoras encontradas")
doc.add_heading("3.7 Segunda prueba: con peso negativo", 2)
figura(grafo_img("flo_grafo2", POS4, FL2_A, dirigido=True), "Captura 11. Grafo con arista B→C de peso -2")
d, _s = mod_floyd.floyd(FL2)
figura(captura("Matriz inicial:\n" + fmt(FL2, ET4) + "\nMatriz de distancias mínimas:\n" + fmt(d, ET4), "flo_salida2"),
       "Captura 12. Resultado con aristas negativas")
doc.add_paragraph("Floyd maneja correctamente el peso negativo: de A a C el costo es -1 (A→B→C = 1-2), y de A a D es 2. "
                  "La diagonal permanece en 0, lo que indica que no hay ciclos negativos.")

# ===== WARSHALL =====
doc.add_page_break()
doc.add_heading("4. Algoritmo de Warshall", 1)
doc.add_heading("4.1 ¿Para qué sirve?", 2)
doc.add_paragraph(
    "Calcula la cerradura transitiva de un grafo dirigido: una matriz que indica si existe al menos un camino, de "
    "cualquier longitud, entre cada par de nodos. No considera costos, solo si se puede llegar o no.")
for t in ["Verificar conectividad entre nodos.", "Dependencias entre módulos o tareas (¿A depende indirectamente de C?).",
          "Bases de datos (consultas recursivas) y análisis de redes sociales (alcance de influencia)."]:
    doc.add_bullet(t)
doc.add_heading("4.2 ¿Cómo funciona?", 2)
for t in ["Se parte de la matriz de adyacencia booleana (1 = hay arista, 0 = no hay).",
          "Para cada nodo intermedio k, y cada par (i, j), se aplica R[i][j] = R[i][j] OR (R[i][k] AND R[k][j]).",
          "Es decir: si se puede ir de i a k y de k a j, entonces se puede ir de i a j.",
          "La matriz final tiene un 1 en cada par (i, j) donde j es alcanzable desde i."]:
    doc.add_bullet(t)
doc.add_paragraph("Es la misma estructura de Floyd, pero con operaciones lógicas en lugar de sumas y mínimos.")
doc.add_heading("4.3 Código", 2)
figura(ruta_codigo("warshall.py"), "Captura 13. Código de warshall.py")
doc.add_heading("4.4 Grafo de prueba 1", 2)
figura(grafo_img("war_grafo1", POS4, WA1_A, dirigido=True), "Captura 14. Cadena A→B→C→D")
doc.add_heading("4.5 Ejecución", 2)
txt, _ = correr(lambda: __import__("runpy").run_path(os.path.join(AQUI, "warshall.py"), run_name="__main__"))
figura(captura(txt, "war_salida"), "Captura 15. Matriz de adyacencia, cerradura transitiva y alcanzabilidad")
doc.add_paragraph("Interpretación: aunque A solo está conectado directamente con B, la cerradura muestra que desde A "
                  "se alcanza también C y D a través de caminos indirectos. D no llega a ningún nodo.")
doc.add_heading("4.6 Traza por cada nodo intermedio", 2)
t, _ = correr(traza_warshall, WA1, ET4)
figura(captura(t, "war_traza"), "Captura 16. Evolución de la matriz R0 a R4")
doc.add_heading("4.7 Segunda prueba: grafo con ciclo y componentes separadas", 2)
figura(grafo_img("war_grafo2", POS5, WA2_A, dirigido=True), "Captura 17. Ciclo A→B→C→A y componente aparte D→E")
cier = mod_war.warshall(WA2)
txt = "Cerradura transitiva:\n" + fmt(cier, ET5) + "\nAlcanzabilidad:\n"
for i, e in enumerate(ET5):
    a = [ET5[j] for j in range(5) if cier[i][j]]
    txt += f"Desde {e} se puede llegar a: {', '.join(a) if a else 'ninguno'}\n"
figura(captura(txt, "war_salida2"), "Captura 18. Resultado de la segunda prueba")
doc.add_paragraph("Los nodos A, B y C forman un ciclo, por lo que cada uno alcanza a los tres (incluso a sí mismo). "
                  "El grupo D, E es independiente: ninguno de ellos llega al ciclo ni viceversa.")

# ===== KRUSKAL =====
doc.add_page_break()
doc.add_heading("5. Algoritmo de Kruskal", 1)
doc.add_heading("5.1 ¿Para qué sirve?", 2)
doc.add_paragraph(
    "Obtiene el árbol de expansión mínima (MST) de un grafo no dirigido y ponderado: el subconjunto de aristas que "
    "conecta todos los nodos, sin formar ciclos, con el menor peso total posible. Un MST de V nodos tiene exactamente V-1 aristas.")
for t in ["Diseño de redes eléctricas, de telecomunicaciones o de tuberías con el menor costo de cableado.",
          "Construcción de carreteras que conecten todas las ciudades con la menor longitud total.",
          "Agrupamiento de datos (clustering) y aproximación del problema del viajante."]:
    doc.add_bullet(t)
doc.add_heading("5.2 ¿Cómo funciona?", 2)
for t in ["Se ordenan todas las aristas de menor a mayor peso.",
          "Se crea una estructura Union-Find donde cada nodo empieza en su propio conjunto.",
          "Se recorre la lista ordenada: si los extremos de la arista están en conjuntos distintos, la arista se acepta "
          "y se unen los conjuntos; si están en el mismo, formaría un ciclo y se rechaza.",
          "Se termina al aceptar V-1 aristas (o al agotar las aristas)."]:
    doc.add_bullet(t)
doc.add_paragraph("Union-Find usa compresión de caminos y unión por rango para que cada operación sea casi constante.")
doc.add_heading("5.3 Código", 2)
figura(ruta_codigo("kruskal.py"), "Captura 19. Código de kruskal.py")
doc.add_heading("5.4 Grafo de prueba 1", 2)
figura(grafo_img("kru_grafo1", POS6, ARIS6), "Captura 20. Grafo original de 6 nodos y 9 aristas")
doc.add_heading("5.5 Ejecución", 2)
txt, _ = correr(lambda: __import__("runpy").run_path(os.path.join(AQUI, "kruskal.py"), run_name="__main__"))
figura(captura(txt, "kru_salida"), "Captura 21. Aristas aceptadas y rechazadas, árbol y peso total")
doc.add_paragraph("Interpretación: se aceptan 5 aristas (V-1) con peso total 13. Las aristas A-B (4), C-D (8) y C-E (10) "
                  "se rechazan porque ya existía otro camino entre sus nodos y crearían un ciclo.")
doc.add_heading("5.6 Árbol resultante", 2)
mst1 = [("B", "C"), ("A", "C"), ("D", "E"), ("E", "F"), ("B", "D")]
figura(grafo_img("kru_mst1", POS6, ARIS6, resaltar=mst1), "Captura 22. Árbol de expansión mínima (en verde), peso 13")
doc.add_heading("5.7 Segunda prueba", 2)
figura(grafo_img("kru_grafo2", POS5K, [(u, v, p) for p, u, v in AR_K2]), "Captura 23. Grafo de 5 nodos y 7 aristas")
txt, (arb2, tot2) = correr(mod_kru.kruskal, NODOS5, AR_K2)
txt += "\nÁrbol de expansión mínima:\n" + "".join(f"  {u} - {v}  (peso {p})\n" for u, v, p in arb2) + f"Peso total: {tot2}\n"
figura(captura("=== Algoritmo de Kruskal (prueba 2) ===\n" + txt, "kru_salida2"), "Captura 24. Resultado de la segunda prueba")
figura(grafo_img("kru_mst2", POS5K, [(u, v, p) for p, u, v in AR_K2], resaltar=[(u, v) for u, v, _p in arb2]),
       f"Captura 25. MST en verde, peso total {tot2}")
doc.add_paragraph(f"El árbol conecta los 5 nodos con 4 aristas y un costo total de {tot2}; las demás aristas se descartan por formar ciclos.")

# ===== CIERRE =====
doc.add_page_break()
doc.add_heading("6. Conclusiones", 1)
for t in [
    "Dijkstra es la mejor opción cuando se necesita la ruta más corta desde un solo origen y los pesos no son negativos, "
    "gracias a su eficiencia con cola de prioridad.",
    "Floyd resuelve todos los pares de nodos con un código muy corto y soporta pesos negativos, pero su costo O(V³) "
    "lo hace adecuado solo para grafos pequeños o medianos.",
    "Warshall es la versión lógica de Floyd: no calcula costos, solo si existe conexión entre dos nodos.",
    "Kruskal no busca rutas, sino conectar todos los nodos con el menor costo; su clave es la estructura Union-Find "
    "para detectar ciclos rápidamente.",
    "Elegir el algoritmo depende del problema: rutas desde un punto (Dijkstra), rutas entre todos (Floyd), "
    "conectividad (Warshall) o red de costo mínimo (Kruskal).",
    "Representar los grafos con dibujos y trazas paso a paso facilitó comprobar que los resultados son correctos."]:
    doc.add_bullet(t)
doc.add_heading("7. Referencias", 1)
for t in ["Cormen, T., Leiserson, C., Rivest, R., Stein, C. Introduction to Algorithms. MIT Press.",
          "Documentación de Python: módulo heapq. https://docs.python.org/3/library/heapq.html",
          "Repositorio del proyecto: https://github.com/Dark554-hub/Estructura-de-datos"]:
    doc.add_bullet(t)

doc.save(os.path.join(AQUI, "Reporte_ADA8_Grafos.docx"))
print("Reporte generado:", len(doc.imgs), "imagenes")

