class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, dato):
        self.items.append(dato)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.items.pop(0)

    def esta_vacia(self):
        return len(self.items) == 0

    def tamano(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)