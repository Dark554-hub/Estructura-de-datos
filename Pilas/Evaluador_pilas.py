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
        raise IndexError("La pila está vacía")

    def ver_tope(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None


def operar(operador, a, b):
    if operador == '+': return a + b
    elif operador == '-': return a - b
    elif operador == '*': return a * b
    elif operador == '/': return a / b
    elif operador == '^': return a ** b
    else: raise ValueError(f"Operador no válido: {operador}")


def evaluar_posfija(expresion):
    """
    Evalúa expresiones donde el operador va DESPUÉS de los operandos.
    Ejemplo: '3 4 + 2 *' -> (3 + 4) * 2 = 14
    """
    pila = Pila()
    tokens = expresion.split()

    for token in tokens:
        if token.lstrip('-').replace('.', '', 1).isdigit():
            pila.apilar(float(token))
        else:
            # El primer desapilado es el operando derecho (b)
            b = pila.desapilar()
            a = pila.desapilar()
            resultado = operar(token, a, b)
            pila.apilar(resultado)

    return pila.desapilar()


def evaluar_prefija(expresion):
    """
    Evalúa expresiones donde el operador va ANTES de los operandos.
    Ejemplo: '* + 3 4 2' -> (3 + 4) * 2 = 14
    """
    pila = Pila()
    # Se lee de derecha a izquierda invirtiendo la lista de tokens
    tokens = expresion.split()[::-1]

    for token in tokens:
        if token.lstrip('-').replace('.', '', 1).isdigit():
            pila.apilar(float(token))
        else:
            # Al leer al revés, el primer desapilado es el operando izquierdo (a)
            a = pila.desapilar()
            b = pila.desapilar()
            resultado = operar(token, a, b)
            pila.apilar(resultado)

    return pila.desapilar()


if __name__ == "__main__":
    print("--- EVALUADOR DE EXPRESIONES CON PILAS ---")
    exp_posfija = "5 3 + 8 2 - *"  # Equivalente a (5 + 3) * (8 - 2) = 48
    print(f"Expresión Posfija: '{exp_posfija}'")
    print(f"Resultado: {evaluar_posfija(exp_posfija)}\n")

    exp_prefija = "* + 5 3 - 8 2"  # Equivalente a (5 + 3) * (8 - 2) = 48
    print(f"Expresión Prefija: '{exp_prefija}'")
    print(f"Resultado: {evaluar_prefija(exp_prefija)}")