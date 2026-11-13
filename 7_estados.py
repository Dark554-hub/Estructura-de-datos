"""7_estados: Grafo de 7 estados de la República Mexicana (ventana Tkinter).

Funciones:
  - Muestra los estados y sus relaciones (lista lateral y grafo dibujado con costos).
  - Tú eliges el estado donde INICIA y donde TERMINA (o "Cualquiera").
  - Tú cambias las ponderaciones (costos): clic sobre el número de una arista.
  - a) Recorrido de los 7 estados sin repetir ninguno (animado). Si desde ese
       inicio/final no es posible, no te deja.
  - b) Recorrido de los 7 estados repitiendo al menos uno (animado).
  - Sobre cada línea recorrida aparece el número de movimiento (1, 2, 3...).
  - Costo total de cada recorrido (costo = distancia aproximada en km).

Uso: python 7_estados.py
  Clic izquierdo sobre un estado = inicio | Clic derecho = final
  Clic sobre el número de una arista = cambiar su costo
"""
import math
import tkinter as tk
from tkinter import messagebox, simpledialog

# Aristas: [estado1, estado2, costo en km aprox. por carretera]
ARISTAS = [
    ["Jalisco", "Guanajuato", 300],
    ["Jalisco", "Querétaro", 450],
    ["Guanajuato", "Querétaro", 120],
    ["Guanajuato", "CDMX", 380],
    ["Querétaro", "CDMX", 220],
    ["CDMX", "Puebla", 130],
    ["Puebla", "Veracruz", 300],
    ["Puebla", "Oaxaca", 410],
    ["Veracruz", "Oaxaca", 440],
]

# Posiciones relativas (0-1) para que se parezca a un mapa
POS_REL = {
    "Jalisco": (0.10, 0.60), "Guanajuato": (0.28, 0.25), "Querétaro": (0.45, 0.50),
    "CDMX": (0.58, 0.78), "Puebla": (0.76, 0.78), "Veracruz": (0.90, 0.35),
    "Oaxaca": (0.82, 0.95),
}

ESTADOS = sorted(POS_REL)
N = len(ESTADOS)
CUALQUIERA = "Cualquiera"

# ---------- paleta y tipografía ----------
FUENTE = "Segoe UI"
BG = "#0f172a"          # fondo del grafo
PANEL = "#1e293b"       # barras y paneles
PANEL2 = "#273449"
TEXTO = "#e2e8f0"
TEXTO_SUAVE = "#94a3b8"
ACENTO = "#38bdf8"
ARISTA = "#475569"
ARISTA_ACT = "#f43f5e"
NODO = "#334155"
NODO_BORDE = "#94a3b8"
NODO_VISITADO = "#22c55e"
NODO_ACTUAL = "#f59e0b"
COLOR_INICIO = "#f43f5e"
COLOR_FIN = "#38bdf8"

grafo = {}


def reconstruir_grafo():
    """Reconstruye el diccionario de adyacencia con los costos actuales."""
    grafo.clear()
    for a, b, c in ARISTAS:
        grafo.setdefault(a, {})[b] = c
        grafo.setdefault(b, {})[a] = c


reconstruir_grafo()


def costo(ruta):
    return sum(grafo[ruta[i]][ruta[i + 1]] for i in range(len(ruta) - 1))


def sin_repetir(inicio, fin=None):
    """Mejor camino que visita los 7 estados exactamente una vez, de 'inicio' a
    'fin' (si fin es None, termina donde sea). Devuelve (None, inf) si no existe."""
    mejor = [None, math.inf]

    def dfs(ruta):
        if len(ruta) == N:
            if fin is None or ruta[-1] == fin:
                c = costo(ruta)
                if c < mejor[1]:
                    mejor[0], mejor[1] = ruta[:], c
            return
        for v in grafo[ruta[-1]]:
            if v not in ruta:
                ruta.append(v)
                dfs(ruta)
                ruta.pop()

    dfs([inicio])
    return mejor


def con_repeticion(inicio, fin=None, max_pasos=N + 3):
    """Mejor recorrido que visita los 7 estados repitiendo al menos uno, de
    'inicio' a 'fin' (si fin es None, termina donde sea)."""
    mejor = [None, math.inf]

    def dfs(ruta):
        if len(set(ruta)) == N and len(ruta) > N and (fin is None or ruta[-1] == fin):
            c = costo(ruta)
            if c < mejor[1]:
                mejor[0], mejor[1] = ruta[:], c
        if len(ruta) >= max_pasos:
            return
        for v in grafo[ruta[-1]]:
            ruta.append(v)
            dfs(ruta)
            ruta.pop()

    dfs([inicio])
    return mejor


class App:
    R = 36  # radio del nodo

    def __init__(self, root):
        self.root = root
        root.title("7 Estados - Grafo, recorridos y costos")
        root.geometry("1200x740")
        root.configure(bg=PANEL)
        self.sel = None              # estado de inicio resaltado
        self.fin_sel = None          # estado final resaltado
        self.visitados = set()       # estados ya recorridos
        self.actual = None           # estado visitándose
        self.movs = {}               # frozenset(arista) -> [(n.º movimiento, desde, hasta)]
        self.pos = {}
        self.anim = None

        # --- encabezado ---
        tk.Label(root, text="Grafo de 7 estados de México", bg=PANEL, fg=TEXTO,
                 font=(FUENTE, 18, "bold"), anchor="w", padx=12).pack(fill="x", pady=(8, 0))

        # --- panel superior ---
        top = tk.Frame(root, bg=PANEL, padx=10, pady=8)
        top.pack(fill="x")
        self._etiqueta(top, "Inicia en")
        self.inicio = tk.StringVar(value="")
        self._menu(top, self.inicio, ESTADOS, self.elegir_inicio, COLOR_INICIO)
        self._etiqueta(top, "   Termina en")
        self.fin = tk.StringVar(value=CUALQUIERA)
        self._menu(top, self.fin, [CUALQUIERA] + ESTADOS, self.elegir_fin, COLOR_FIN)

        self._boton(top, "a) Sin repetir", "#0ea5e9",
                    lambda: self.recorrer("a) Sin repetir", sin_repetir)).pack(side="left", padx=(24, 4))
        self._boton(top, "b) Repitiendo al menos uno", "#8b5cf6",
                    lambda: self.recorrer("b) Con repetición", con_repeticion)).pack(side="left", padx=4)
        self._boton(top, "Limpiar", "#64748b", self.limpiar).pack(side="left", padx=4)

        self._etiqueta(top, "   Velocidad")
        self.vel = tk.Scale(top, from_=200, to=2000, orient="horizontal", length=130,
                            bg=PANEL, fg=TEXTO, troughcolor=PANEL2, highlightthickness=0,
                            activebackground=ACENTO, font=(FUENTE, 8), showvalue=False)
        self.vel.set(900)
        self.vel.pack(side="left")

        tk.Label(root, text="Clic izquierdo: inicio   •   Clic derecho: final   •   "
                            "Clic en un número amarillo: cambiar costo",
                 bg=PANEL, fg=TEXTO_SUAVE, font=(FUENTE, 9), anchor="w",
                 padx=12).pack(fill="x")

        # --- cuerpo: lista de relaciones + canvas ---
        cuerpo = tk.Frame(root, bg=PANEL)
        cuerpo.pack(fill="both", expand=True, padx=10, pady=8)

        lado = tk.Frame(cuerpo, bg=PANEL)
        lado.pack(side="left", fill="y")
        tk.Label(lado, text="Estados y relaciones", bg=PANEL, fg=ACENTO,
                 font=(FUENTE, 12, "bold")).pack(anchor="w", pady=(0, 4))
        self.lista = tk.Text(lado, width=32, font=("Consolas", 10), bg=PANEL2, fg=TEXTO,
                             relief="flat", padx=10, pady=8, highlightthickness=0)
        self.lista.pack(fill="y", expand=True)
        self.lista.tag_config("t", font=(FUENTE, 11, "bold"), foreground=ACENTO,
                              spacing1=6)
        self.llenar_lista()

        self.canvas = tk.Canvas(cuerpo, bg=BG, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self.canvas.bind("<Button-1>", self.clic)
        self.canvas.bind("<Button-3>", self.clic_derecho)
        self.canvas.bind("<Configure>", lambda e: self.dibujar())

        self.estado = tk.StringVar(value="Elige inicio y final, y luego un recorrido (a o b).")
        tk.Label(root, textvariable=self.estado, anchor="w", font=(FUENTE, 11, "bold"),
                 bg="#0b1220", fg="#fde68a", padx=12, pady=8).pack(fill="x", side="bottom")

    # ---------- widgets con estilo ----------
    def _etiqueta(self, padre, texto):
        tk.Label(padre, text=texto, bg=PANEL, fg=TEXTO_SUAVE,
                 font=(FUENTE, 10, "bold")).pack(side="left")

    def _menu(self, padre, var, opciones, cmd, color):
        m = tk.OptionMenu(padre, var, *opciones, command=cmd)
        m.config(bg=PANEL2, fg=color, activebackground=color, activeforeground="white",
                 font=(FUENTE, 10, "bold"), relief="flat", highlightthickness=0, width=11)
        m["menu"].config(bg=PANEL2, fg=TEXTO, font=(FUENTE, 10))
        m.pack(side="left", padx=6)

    def _boton(self, padre, texto, color, cmd):
        b = tk.Button(padre, text=texto, command=cmd, bg=color, fg="white",
                      activebackground=ACENTO, activeforeground="white", relief="flat",
                      font=(FUENTE, 10, "bold"), padx=12, pady=4, cursor="hand2",
                      borderwidth=0)
        return b

    # ---------- utilidades ----------
    def llenar_lista(self):
        self.lista.config(state="normal")
        self.lista.delete("1.0", "end")
        for e in ESTADOS:
            self.lista.insert("end", f"{e}\n", "t")
            for v, c in sorted(grafo[e].items()):
                self.lista.insert("end", f"   ↔ {v} ({c} km)\n")
        self.lista.config(state="disabled")

    def fin_actual(self):
        f = self.fin.get()
        return None if f == CUALQUIERA else f

    def detener_anim(self):
        if self.anim:
            self.root.after_cancel(self.anim)
            self.anim = None
        self.visitados.clear()
        self.movs.clear()
        self.actual = None

    def limpiar(self):
        self.detener_anim()
        self.sel = None
        self.fin_sel = None
        self.inicio.set("")
        self.fin.set(CUALQUIERA)
        self.estado.set("Grafo limpio.")
        self.dibujar()

    def elegir_inicio(self, e):
        self.detener_anim()
        self.inicio.set(e)
        self.sel = e
        self.informar()
        self.dibujar()

    def elegir_fin(self, e):
        self.detener_anim()
        self.fin.set(e)
        self.fin_sel = None if e == CUALQUIERA else e
        self.informar()
        self.dibujar()

    def informar(self):
        ini, fin = self.inicio.get(), self.fin_actual()
        if ini not in grafo:
            self.estado.set(f"Final: {fin or CUALQUIERA}. Falta elegir el inicio.")
            return
        ok = sin_repetir(ini, fin)[0] is not None
        self.estado.set(f"Inicio: {ini} | Final: {fin or CUALQUIERA} → " +
                        ("sirve para a) y b)." if ok else
                         "solo sirve para b) (en a) no se puede sin repetir)."))

    # ---------- acciones ----------
    def recorrer(self, nombre, fn):
        self.detener_anim()
        inicio, fin = self.inicio.get(), self.fin_actual()
        if inicio not in grafo:
            messagebox.showinfo("Inicio", "Elige primero el estado donde inicia.")
            return
        ruta, total = fn(inicio, fin)
        if ruta is None:
            if fn is sin_repetir:
                validos = [e for e in ESTADOS if sin_repetir(e, fin)[0]]
                messagebox.showwarning(
                    "Combinación no válida",
                    f"De {inicio} a {fin or CUALQUIERA} NO se pueden recorrer los 7 estados "
                    f"sin repetir ninguno.\n\n"
                    f"Inicios válidos para a) con final {fin or CUALQUIERA}: "
                    f"{', '.join(validos) if validos else 'ninguno'}.\n"
                    f"Cambia inicio/final o usa el recorrido b).")
            else:
                messagebox.showwarning(
                    "Sin recorrido",
                    f"No se encontró un recorrido b) de {inicio} a {fin or CUALQUIERA}. "
                    f"Prueba con otro final.")
            self.estado.set(f"{nombre}: imposible de {inicio} a {fin or CUALQUIERA}.")
            self.dibujar()
            return
        self.sel = inicio
        self.fin_sel = fin
        self.paso(nombre, ruta, total, 0)

    def paso(self, nombre, ruta, total, i):
        if self.actual:
            self.visitados.add(self.actual)
        if i >= len(ruta):
            self.actual = None
            self.anim = None
            rep = sorted({e for e in ruta if ruta.count(e) > 1})
            extra = f"  | Repetidos: {', '.join(rep)}" if rep else ""
            self.estado.set(f"{nombre}: " + " → ".join(ruta) +
                            f"  | {len(ruta) - 1} movimientos | COSTO TOTAL: {total} km{extra}")
            self.dibujar()
            return
        if i > 0:
            self.movs.setdefault(frozenset((ruta[i - 1], ruta[i])), []).append(
                (i, ruta[i - 1], ruta[i]))
        self.actual = ruta[i]
        self.estado.set(f"{nombre}: " + " → ".join(ruta[:i + 1]) +
                        f"  | Movimiento {i} | Costo parcial: {costo(ruta[:i + 1])} km")
        self.dibujar()
        self.anim = self.root.after(self.vel.get(), self.paso, nombre, ruta, total, i + 1)

    def editar_arista(self, arista):
        a, b, c = arista
        nuevo = simpledialog.askinteger(
            "Ponderación", f"Nuevo costo (km) de {a} ↔ {b}:",
            initialvalue=c, minvalue=1, maxvalue=100000, parent=self.root)
        if nuevo is None:
            return
        self.detener_anim()
        arista[2] = nuevo
        reconstruir_grafo()
        self.llenar_lista()
        self.estado.set(f"Costo de {a} ↔ {b} cambiado a {nuevo} km.")
        self.dibujar()

    # ---------- dibujo ----------
    def calcular_pos(self):
        w = max(self.canvas.winfo_width(), 300)
        h = max(self.canvas.winfo_height(), 300)
        m = self.R + 22
        self.pos = {e: (m + x * (w - 2 * m), m + y * (h - 2 * m))
                    for e, (x, y) in POS_REL.items()}

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        self.calcular_pos()
        # líneas
        for a, b, costo_ab in ARISTAS:
            (x1, y1), (x2, y2) = self.pos[a], self.pos[b]
            activa = frozenset((a, b)) in self.movs
            if activa:
                c.create_line(x1, y1, x2, y2, width=11, fill="#4c1d2e", capstyle="round")
            c.create_line(x1, y1, x2, y2, width=4 if activa else 2,
                          fill=ARISTA_ACT if activa else ARISTA, capstyle="round")
        # costos (pastilla amarilla en el centro)
        for a, b, costo_ab in ARISTAS:
            (x1, y1), (x2, y2) = self.pos[a], self.pos[b]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            c.create_rectangle(mx - 19, my - 11, mx + 19, my + 11, fill="#fde68a",
                               outline="#f59e0b", width=1)
            c.create_text(mx, my, text=str(costo_ab), fill="#1e293b",
                          font=(FUENTE, 10, "bold"))
        # números de movimiento sobre las líneas
        for movs in self.movs.values():
            for k, (n, desde, hasta) in enumerate(movs):
                (x1, y1), (x2, y2) = self.pos[desde], self.pos[hasta]
                t = min(0.22 + 0.11 * k, 0.40)
                bx, by = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
                c.create_oval(bx - 13, by - 13, bx + 13, by + 13, fill=ARISTA_ACT,
                              outline="white", width=2)
                c.create_text(bx, by, text=str(n), fill="white", font=(FUENTE, 10, "bold"))
        # nodos
        for e, (x, y) in self.pos.items():
            color = NODO
            if e in self.visitados:
                color = NODO_VISITADO
            if e == self.actual:
                color = NODO_ACTUAL
            borde, ancho = NODO_BORDE, 2
            if e == self.sel:
                borde, ancho = COLOR_INICIO, 4
            elif e == self.fin_sel:
                borde, ancho = COLOR_FIN, 4
            if e == self.sel and e == self.fin_sel:
                borde = "#a855f7"
            c.create_oval(x - self.R - 5, y - self.R - 5, x + self.R + 5, y + self.R + 5,
                          fill="", outline=color, width=1)  # halo
            c.create_oval(x - self.R, y - self.R, x + self.R, y + self.R,
                          fill=color, outline=borde, width=ancho)
            c.create_text(x, y, text=e, fill="white", font=(FUENTE, 10, "bold"))
            if e == self.sel:
                c.create_text(x, y - self.R - 16, text="▶ INICIO", fill=COLOR_INICIO,
                              font=(FUENTE, 9, "bold"))
            if e == self.fin_sel:
                c.create_text(x, y + self.R + 16, text="■ FINAL", fill=COLOR_FIN,
                              font=(FUENTE, 9, "bold"))

    def nodo_en(self, ev):
        for e, (x, y) in self.pos.items():
            if (ev.x - x) ** 2 + (ev.y - y) ** 2 <= self.R ** 2:
                return e
        return None

    def clic(self, ev):
        e = self.nodo_en(ev)
        if e:
            self.elegir_inicio(e)
            return
        for arista in ARISTAS:
            (x1, y1), (x2, y2) = self.pos[arista[0]], self.pos[arista[1]]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            if abs(ev.x - mx) <= 19 and abs(ev.y - my) <= 11:
                self.editar_arista(arista)
                return

    def clic_derecho(self, ev):
        e = self.nodo_en(ev)
        if e:
            self.elegir_fin(e)


if __name__ == "__main__":
    ventana = tk.Tk()
    App(ventana)
    ventana.mainloop()
