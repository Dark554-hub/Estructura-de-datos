import time


def fib_iterativo(n):
    a = 0
    b = 1
    for i in range(n):
        temp = a + b
        a = b
        b = temp
    return a


def fib_recursivo(n):
    if n < 2:
        return n
    return fib_recursivo(n - 1) + fib_recursivo(n - 2)


n = int(input("Ingresa un numero n: "))

inicio = time.time()
resultado = fib_iterativo(n)
fin = time.time()
print("Iterativo:", resultado)
print("Tiempo iterativo:", fin - inicio, "segundos")

inicio = time.time()
resultado = fib_recursivo(n)
fin = time.time()
print("Recursivo:", resultado)
print("Tiempo recursivo:", fin - inicio, "segundos")