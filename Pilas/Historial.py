class Pila:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, item):
        self.items.append(item)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        return None

    def ver_tope(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None

    def obtener_elementos(self):
        return self.items.copy()


class NavegadorWeb:
    def __init__(self):
        self.historial_atras = Pila()
        self.historial_adelante = Pila()
        self.pagina_actual = None

    def visitar_sitio(self, url):
        if self.pagina_actual is not None:
            self.historial_atras.apilar(self.pagina_actual)
        self.pagina_actual = url
        # Al visitar una nueva página, se limpia el historial de "Adelante"
        self.historial_adelante = Pila()
        print(f"🌐 Visitando: {self.pagina_actual}")

    def ir_atras(self):
        if self.historial_atras.esta_vacia():
            print("⚠️ No hay páginas anteriores en el historial.")
        else:
            self.historial_adelante.apilar(self.pagina_actual)
            self.pagina_actual = self.historial_atras.desapilar()
            print(f"⬅️ Volviendo a: {self.pagina_actual}")

    def ir_adelante(self):
        if self.historial_adelante.esta_vacia():
            print("⚠️ No hay páginas siguientes para avanzar.")
        else:
            self.historial_atras.apilar(self.pagina_actual)
            self.pagina_actual = self.historial_adelante.desapilar()
            print(f"➡️ Avanzando a: {self.pagina_actual}")

    def mostrar_historial(self):
        print("\n--- ESTADO DEL NAVEGADOR ---")
        print(f"📍 Página actual: {self.pagina_actual}")
        atras = self.historial_atras.obtener_elementos()
        print(f"📚 Historial atrás (Pila): {atras if atras else 'Vacío'}")
        print("----------------------------\n")


if __name__ == "__main__":
    navegador = NavegadorWeb()

    # Simulación de navegación
    navegador.visitar_sitio("google.com")
    navegador.visitar_sitio("github.com")
    navegador.visitar_sitio("stackoverflow.com")
    navegador.visitar_sitio("python.org")

    navegador.mostrar_historial()

    # Uso del botón "Atrás" y "Adelante"
    navegador.ir_atras()
    navegador.ir_atras()
    navegador.mostrar_historial()

    navegador.ir_adelante()
    navegador.mostrar_historial()