from cola import Cola


def sumar_colas(a, b):
    """Devuelve una nueva Cola con a[i] + b[i]. Las colas originales quedan intactas."""
    if a.tamano() != b.tamano():
        raise ValueError("Las colas deben tener el mismo tamaño")

    resultado = Cola()
    for _ in range(a.tamano()):
        x = a.desencolar()
        y = b.desencolar()
        resultado.encolar(x + y)
        a.encolar(x)  # se restauran los elementos
        b.encolar(y)
    return resultado


if __name__ == "__main__":
    cola_a = Cola()
    cola_b = Cola()

    for n in [3, 4, 2, 8, 12]:
        cola_a.encolar(n)
    for n in [6, 2, 9, 11, 3]:
        cola_b.encolar(n)

    resultado = sumar_colas(cola_a, cola_b)

    print("Cola A:        ", cola_a)
    print("Cola B:        ", cola_b)
    print("Cola Resultado:", resultado)