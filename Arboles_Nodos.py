"""Visualizador de árboles binarios (ventana de escritorio con Tkinter).

Funciones:
  - Crear árboles: insertar como ABB, o como hijo izquierdo/derecho del nodo seleccionado.
  - Recorridos animados: preorden, inorden y posorden.
  - Eliminar un nodo (los hijos se reacomodan) o un subárbol completo.

Uso: python Arboles_Nodos.py   (clic sobre un nodo para seleccionarlo)
"""
import tkinter as tk
from tkinter import messagebox


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None


class Arbol:
    def __init__(self):
        self.raiz = None

    # ---------- inserción ----------
    def existe(self, valor):
        return any(n.valor == valor for n in self.nodos())

    def insertar_abb(self, valor):
        nuevo = Nodo(valor)
        if self.raiz is None:
            self.raiz = nuevo
            return
        act = self.raiz
        while True:
            if valor < act.valor:
                if act.izq is None:
                    act.izq = nuevo
                    return
                act = act.izq
            else:
                if act.der is None:
                    act.der = nuevo
                    return
                act = act.der

    def insertar_hijo(self, padre, lado, valor):
        """Inserta como hijo 'izq' o 'der'. Devuelve False si el lado está ocupado."""
        if getattr(padre, lado) is not None:
            return False
        setattr(padre, lado, Nodo(valor))
        return True

    # ---------- recorridos ----------
    def preorden(self, n=None, primero=True):
        if primero:
            n = self.raiz
        if n is None:
            return []
        return [n] + self.preorden(n.izq, False) + self.preorden(n.der, False)

    def inorden(self, n=None, primero=True):
        if primero:
            n = self.raiz
        if n is None:
            return []
        return self.inorden(n.izq, False) + [n] + self.inorden(n.der, False)

    def posorden(self, n=None, primero=True):
        if primero:
            n = self.raiz
        if n is None:
            return []
        return self.posorden(n.izq, False) + self.posorden(n.der, False) + [n]

    def nodos(self):
        return self.preorden()

    # ---------- eliminación ----------
    def _padre(self, objetivo):
        for n in self.nodos():
            if n.izq is objetivo:
                return n, "izq"
            if n.der is objetivo:
                return n, "der"
        return None, None

    def eliminar_subarbol(self, objetivo):
        """Quita el nodo con todos sus descendientes."""
        if objetivo is self.raiz:
            self.raiz = None
            return
        padre, lado = self._padre(objetivo)
        setattr(padre, lado, None)

    def eliminar_nodo(self, objetivo):
        """Quita solo el nodo; sus hijos se reacomodan.
        0 hijos: se borra. 1 hijo: el hijo lo reemplaza.
        2 hijos: toma el valor del sucesor inorden y se borra el sucesor."""
        if objetivo.izq and objetivo.der:
            suc = objetivo.der
            while suc.izq:
                suc = suc.izq
            objetivo.valor = suc.valor
            self.eliminar_nodo(suc)
            return
        hijo = objetivo.izq or objetivo.der
        if objetivo is self.raiz:
            self.raiz = hijo
        else:
            padre, lado = self._padre(objetivo)
            setattr(padre, lado, hijo)


class App:
    R = 20  # radio del nodo

    def __init__(self, root):
        self.root = root
        root.title("Árboles binarios - Preorden, Inorden y Posorden")
        root.geometry("1000x680")
        self.arbol = Arbol()
        self.sel = None
        self.resaltados = set()      # nodos ya visitados en el recorrido
        self.actual = None           # nodo visitándose
        self.pos = {}                # Nodo -> (x, y)
        self.anim = None

        # --- panel superior ---
        top = tk.Frame(root, padx=6, pady=6)
        top.pack(fill="x")
        tk.Label(top, text="Valor:").pack(side="left")
        self.entry = tk.Entry(top, width=8)
        self.entry.pack(side="left", padx=4)
        self.entry.bind("<Return>", lambda e: self.insertar_abb())
        for txt, cmd in [("Insertar (ABB)", self.insertar_abb),
                         ("Hijo izq.", lambda: self.insertar_hijo("izq")),
                         ("Hijo der.", lambda: self.insertar_hijo("der")),
                         ("Eliminar nodo", self.eliminar_nodo),
                         ("Eliminar subárbol", self.eliminar_subarbol),
                         ("Ejemplo", self.ejemplo),
                         ("Limpiar", self.limpiar)]:
            tk.Button(top, text=txt, command=cmd).pack(side="left", padx=2)

        rec = tk.Frame(root, padx=6)
        rec.pack(fill="x")
        tk.Label(rec, text="Recorridos:").pack(side="left")
        for txt, fn in [("Preorden", self.arbol.preorden),
                        ("Inorden", self.arbol.inorden),
                        ("Posorden", self.arbol.posorden)]:
            tk.Button(rec, text=txt, bg="#cfe8ff",
                      command=lambda t=txt, f=fn: self.recorrer(t, f)).pack(side="left", padx=2)
        tk.Label(rec, text="  Velocidad (ms):").pack(side="left")
        self.vel = tk.Scale(rec, from_=100, to=1500, orient="horizontal", length=140)
        self.vel.set(600)
        self.vel.pack(side="left")

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas.bind("<Button-1>", self.clic)
        self.canvas.bind("<Configure>", lambda e: self.dibujar())

        self.estado = tk.StringVar(value="Inserta valores. Clic en un nodo para seleccionarlo.")
        tk.Label(root, textvariable=self.estado, anchor="w", font=("Consolas", 11),
                 relief="sunken").pack(fill="x", side="bottom")

    # ---------- utilidades ----------
    def leer_valor(self):
        txt = self.entry.get().strip()
        if not txt:
            messagebox.showinfo("Valor", "Escribe un valor.")
            return None
        try:
            v = int(txt)
        except ValueError:
            v = txt
        if self.arbol.existe(v):
            messagebox.showinfo("Valor", f"El valor {v} ya existe.")
            return None
        return v

    def detener_anim(self):
        if self.anim:
            self.root.after_cancel(self.anim)
            self.anim = None
        self.resaltados.clear()
        self.actual = None

    # ---------- acciones ----------
    def insertar_abb(self):
        v = self.leer_valor()
        if v is None:
            return
        try:
            self.detener_anim()
            self.arbol.insertar_abb(v)
        except TypeError:
            messagebox.showerror("Error", "No se pueden mezclar números y texto en un ABB.")
            return
        self.entry.delete(0, "end")
        self.estado.set(f"Insertado {v} (ABB).")
        self.dibujar()

    def insertar_hijo(self, lado):
        if self.arbol.raiz is None:
            v = self.leer_valor()
            if v is not None:
                self.arbol.insertar_abb(v)
                self.entry.delete(0, "end")
                self.dibujar()
            return
        if not self.sel:
            messagebox.showinfo("Selección", "Selecciona primero un nodo (clic).")
            return
        v = self.leer_valor()
        if v is None:
            return
        self.detener_anim()
        if not self.arbol.insertar_hijo(self.sel, lado, v):
            messagebox.showinfo("Ocupado", f"El nodo {self.sel.valor} ya tiene hijo {lado}.")
            return
        self.entry.delete(0, "end")
        self.estado.set(f"{v} agregado como hijo {lado}. de {self.sel.valor}.")
        self.dibujar()

    def _objetivo(self):
        if self.sel:
            return self.sel
        txt = self.entry.get().strip()
        for n in self.arbol.nodos():
            if str(n.valor) == txt:
                return n
        messagebox.showinfo("Selección", "Selecciona un nodo con clic o escribe su valor.")
        return None

    def eliminar_nodo(self):
        n = self._objetivo()
        if n is None:
            return
        self.detener_anim()
        v = n.valor
        self.arbol.eliminar_nodo(n)
        self.sel = None
        self.entry.delete(0, "end")
        self.estado.set(f"Nodo {v} eliminado (sus hijos se reacomodaron).")
        self.dibujar()

    def eliminar_subarbol(self):
        n = self._objetivo()
        if n is None:
            return
        self.detener_anim()
        cantidad = len(self.arbol.preorden(n, False))
        v = n.valor
        self.arbol.eliminar_subarbol(n)
        self.sel = None
        self.entry.delete(0, "end")
        self.estado.set(f"Subárbol de {v} eliminado ({cantidad} nodo(s)).")
        self.dibujar()

    def limpiar(self):
        self.detener_anim()
        self.arbol.raiz = None
        self.sel = None
        self.estado.set("Árbol vacío.")
        self.dibujar()

    def ejemplo(self):
        self.limpiar()
        for v in [50, 30, 70, 20, 40, 60, 80, 35, 45]:
            self.arbol.insertar_abb(v)
        self.estado.set("Árbol de ejemplo cargado.")
        self.dibujar()

    def recorrer(self, nombre, fn):
        self.detener_anim()
        orden = fn()
        if not orden:
            self.estado.set("El árbol está vacío.")
            return
        self.paso(nombre, orden, 0)

    def paso(self, nombre, orden, i):
        if self.actual:
            self.resaltados.add(self.actual)
        if i >= len(orden):
            self.actual = None
            self.anim = None
            self.estado.set(f"{nombre}: " + " → ".join(str(n.valor) for n in orden))
            self.dibujar()
            return
        self.actual = orden[i]
        self.estado.set(f"{nombre}: " + " → ".join(str(n.valor) for n in orden[:i + 1]))
        self.dibujar()
        self.anim = self.root.after(self.vel.get(), self.paso, nombre, orden, i + 1)

    # ---------- dibujo ----------
    def calcular_pos(self):
        self.pos = {}
        orden = self.arbol.inorden()
        if not orden:
            return
        w = max(self.canvas.winfo_width(), 200)
        paso_x = min(60, (w - 60) / max(len(orden), 1))
        x0 = (w - paso_x * (len(orden) - 1)) / 2

        def prof(n, d):
            if n is None:
                return 0
            return max(d, prof(n.izq, d + 1), prof(n.der, d + 1))

        alto = prof(self.arbol.raiz, 1)
        h = max(self.canvas.winfo_height(), 200)
        paso_y = min(80, (h - 80) / max(alto, 1))

        def asignar(n, d):
            if n is None:
                return
            self.pos[n] = (x0 + orden.index(n) * paso_x, 40 + d * paso_y)
            asignar(n.izq, d + 1)
            asignar(n.der, d + 1)

        asignar(self.arbol.raiz, 0)

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        self.calcular_pos()
        if not self.pos:
            c.create_text(c.winfo_width() / 2, c.winfo_height() / 2,
                          text="Árbol vacío", fill="gray", font=("Arial", 16))
            return
        for n, (x, y) in self.pos.items():
            for h in (n.izq, n.der):
                if h:
                    hx, hy = self.pos[h]
                    c.create_line(x, y, hx, hy, width=2, fill="#555")
        for n, (x, y) in self.pos.items():
            color = "#f9f3a0"
            if n in self.resaltados:
                color = "#9be39b"
            if n is self.actual:
                color = "#ff9d5c"
            borde = "red" if n is self.sel else "black"
            c.create_oval(x - self.R, y - self.R, x + self.R, y + self.R,
                          fill=color, outline=borde, width=3 if n is self.sel else 1)
            c.create_text(x, y, text=str(n.valor), font=("Arial", 11, "bold"))

    def clic(self, ev):
        self.sel = None
        for n, (x, y) in self.pos.items():
            if (ev.x - x) ** 2 + (ev.y - y) ** 2 <= self.R ** 2:
                self.sel = n
                self.estado.set(f"Seleccionado: {n.valor}")
                break
        self.dibujar()


if __name__ == "__main__":
    ventana = tk.Tk()
    App(ventana)
    ventana.mainloop()
