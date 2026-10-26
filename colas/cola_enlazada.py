"""
Práctica 1.2: Implementación de una cola con listas enlazadas.
Basado en la guía de la Universidad Carlos III de Madrid (UC3M).
Simulación de recepción de pedidos (Order) en una empresa.
"""


class Order:
    """
    Representa un pedido de un cliente con una cantidad determinada.
    """
    def __init__(self, qtty: int, customer: str):
        self.customer = customer
        self.qtty = qtty

    def get_customer(self) -> str:
        return self.customer

    def get_qtty(self) -> int:
        return self.qtty

    def print_order(self):
        print(f"     Customer: {self.get_customer()}")
        print(f"     Quantity: {self.get_qtty()}")
        print("     ------------")

    def __str__(self):
        return f"Order(Cliente: {self.customer}, Cantidad: {self.qtty})"


class Node:
    """
    Nodo de la lista enlazada.
    Contiene la información (info) y la referencia al siguiente nodo (next).
    """
    def __init__(self, info=None, next_node=None):
        self.info = info
        self.next = next_node

    def get_info(self):
        return self.info

    def set_info(self, info):
        self.info = info

    def get_next(self):
        return self.next

    def set_next(self, next_node):
        self.next = next_node


class LinkedQueue:
    """
    Implementación de una cola (Queue) mediante una lista enlazada simple.
    Sigue la política FIFO (First In, First Out).
    Mantiene referencias al primer elemento (top/cabeza) y al último (tail/cola).
    """
    def __init__(self):
        self.top = None   # Cabeza: por donde se extraen los elementos (dequeue)
        self.tail = None  # Cola: por donde se insertan los nuevos elementos (enqueue)
        self._size = 0    # Contador de elementos en la cola

    def size(self) -> int:
        """Devuelve el número de elementos en la cola."""
        return self._size

    def is_empty(self) -> bool:
        """Verifica si la cola está vacía."""
        return self.top is None

    def front(self):
        """
        Devuelve el primer elemento de la cola SIN extraerlo.
        Retorna None si la cola está vacía.
        """
        if self.is_empty():
            return None
        return self.top.get_info()

    def enqueue(self, info):
        """
        Inserta un nuevo elemento al final de la cola.
        Complejidad temporal O(1) gracias al puntero tail.
        """
        new_node = Node(info)
        if self.is_empty():
            self.top = new_node
            self.tail = new_node
        else:
            self.tail.set_next(new_node)
            self.tail = new_node
        self._size += 1

    def dequeue(self):
        """
        Extrae y devuelve el primer elemento de la cola.
        Retorna None si la cola está vacía.
        Complejidad temporal O(1).
        """
        if self.is_empty():
            return None
        
        info = self.top.get_info()
        self.top = self.top.get_next()
        self._size -= 1
        
        # Si la cola quedó vacía, tail también debe apuntar a None
        if self.top is None:
            self.tail = None
            
        return info

    def get_nth(self, pos: int):
        """
        Obtiene el n-ésimo elemento de la cola (índice 1-based) sin borrarlo.
        Devuelve None si se pide una posición no válida.
        """
        if pos <= 0 or pos > self._size:
            return None

        current = self.top
        current_pos = 1
        while current is not None:
            if current_pos == pos:
                return current.get_info()
            current_pos += 1
            current = current.get_next()
        return None

    def print_info(self):
        """
        Muestra en consola el estado actual de la cola recorriendo
        los nodos desde 'top' hasta el final.
        """
        print("********* QUEUE DUMP *********")
        print(f"   Size: {self.size()}")
        current = self.top
        count = 1
        while current is not None:
            print(f"   ** Element {count}")
            data = current.get_info()
            if isinstance(data, Order):
                data.print_order()
            else:
                print(f"     {data}")
                print("     ------------")
            count += 1
            current = current.get_next()
        print("******************************\n")


def test_queue():
    """
    Función de prueba solicitada en la práctica:
    1. Crear una cola enlazada.
    2. Crear al menos 3 pedidos (Order).
    3. Encolarlos e imprimir el estado tras cada inserción.
    4. Probar front() y dequeue(), mostrando el volcado de la cola.
    5. Probar getNth() con 4 elementos pidiendo el 3ro.
    """
    print("==================================================")
    print("  PRUEBA: COLA CON LISTAS ENLAZADAS (PRÁCTICA 1.2)")
    print("==================================================\n")

    cola = LinkedQueue()
    print(f"¿La cola está vacía al inicio?: {cola.is_empty()}")
    print(f"Tamaño inicial: {cola.size()}\n")

    # Creación de pedidos
    pedido1 = Order(20, "cust1")
    pedido2 = Order(30, "cust2")
    pedido3 = Order(40, "cust3")
    pedido4 = Order(50, "cust4")

    print("--- 1. Encolando pedidos ---")
    print("Encolando pedido 1 (cust1, 20)...")
    cola.enqueue(pedido1)
    cola.print_info()

    print("Encolando pedido 2 (cust2, 30)...")
    cola.enqueue(pedido2)
    cola.print_info()

    print("Encolando pedido 3 (cust3, 40)...")
    cola.enqueue(pedido3)
    cola.print_info()

    print("Encolando pedido 4 (cust4, 50)...")
    cola.enqueue(pedido4)
    cola.print_info()

    # Probar getNth
    print("--- 2. Probando getNth(pos) ---")
    pos = 3
    elemento_n = cola.get_nth(pos)
    print(f"Obteniendo el {pos}º elemento con getNth({pos}):")
    if elemento_n and isinstance(elemento_n, Order):
        elemento_n.print_order()
    else:
        print(f"Elemento: {elemento_n}")

    pos_invalida = 10
    print(f"Probando getNth({pos_invalida}) (posición fuera de rango): {cola.get_nth(pos_invalida)}\n")

    # Probar front()
    print("--- 3. Probando front() (primer elemento sin extraer) ---")
    primer_elemento = cola.front()
    print("Elemento en el frente (front):")
    if primer_elemento and isinstance(primer_elemento, Order):
        primer_elemento.print_order()
    print(f"Tamaño de la cola tras front(): {cola.size()} (no debe cambiar)\n")

    # Probar dequeue()
    print("--- 4. Probando dequeue() (atendiendo / extrayendo pedidos) ---")
    atendido = cola.dequeue()
    print(f"Pedido extraído con dequeue(): {atendido.get_customer()} (Cantidad: {atendido.get_qtty()})")
    cola.print_info()

    atendido2 = cola.dequeue()
    print(f"Pedido extraído con dequeue(): {atendido2.get_customer()} (Cantidad: {atendido2.get_qtty()})")
    cola.print_info()

    print(f"¿La cola está vacía?: {cola.is_empty()}")
    print(f"Tamaño restante: {cola.size()}\n")


if __name__ == "__main__":
    test_queue()
