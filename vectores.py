def mostrar_vector(datos):
    for elemento in datos:
        print(elemento)


def media(datos):
    return sum(datos) / len(datos)


pares = [2, 4, 6, 8, 10]
impares = [1, 3, 5, 7, 9]

mostrar_vector(pares)
print("Media= ", media(pares))

mostrar_vector(impares)
print("Media= ", media(impares))