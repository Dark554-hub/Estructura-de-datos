"""MyLinkedList: implementación propia de una lista enlazada simple."""


class Node:
    """Nodo de la lista: guarda un dato y la referencia al siguiente."""

    __slots__ = ("data", "next")

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class MyLinkedList:
    """Lista enlazada simple con puntero a head y tail.

    Complejidades:
        append, prepend, extend (por elemento) ... O(1)
        insert, remove, pop, index, [i] ......... O(n)
        len ..................................... O(1)
    """

    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        self._size = 0
        if iterable is not None:
            self.extend(iterable)

    # ---------- Protocolos de Python ----------
    def __len__(self):
        return self._size

    def __iter__(self):
        cur = self.head
        while cur is not None:
            yield cur.data
            cur = cur.next

    def __contains__(self, value):
        return any(item == value for item in self)

    def __getitem__(self, index):
        return self._node_at(self._normalize(index)).data

    def __setitem__(self, index, value):
        self._node_at(self._normalize(index)).data = value

    def __delitem__(self, index):
        self.pop(index)

    def __eq__(self, other):
        if not isinstance(other, MyLinkedList) or len(self) != len(other):
            return False
        return all(a == b for a, b in zip(self, other))

    def __repr__(self):
        return "MyLinkedList([" + ", ".join(repr(x) for x in self) + "])"

    # ---------- Auxiliares ----------
    def _normalize(self, index):
        """Convierte índices negativos y valida el rango."""
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("índice fuera de rango")
        return index

    def _node_at(self, index):
        cur = self.head
        for _ in range(index):
            cur = cur.next
        return cur

    # ---------- Inserción ----------
    def append(self, value):
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, value):
        node = Node(value, self.head)
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1

    def insert(self, index, value):
        if index <= 0:
            self.prepend(value)
        elif index >= self._size:
            self.append(value)
        else:
            prev = self._node_at(index - 1)
            prev.next = Node(value, prev.next)
            self._size += 1

    def extend(self, iterable):
        for value in iterable:
            self.append(value)

    # ---------- Eliminación ----------
    def pop(self, index=-1):
        """Elimina y regresa el elemento en `index` (por defecto el último)."""
        if self._size == 0:
            raise IndexError("pop de lista vacía")
        index = self._normalize(index)
        if index == 0:
            removed = self.head
            self.head = removed.next
            if self.head is None:
                self.tail = None
        else:
            prev = self._node_at(index - 1)
            removed = prev.next
            prev.next = removed.next
            if removed is self.tail:
                self.tail = prev
        self._size -= 1
        return removed.data

    def remove(self, value):
        """Elimina la primera aparición de `value`."""
        prev, cur = None, self.head
        while cur is not None:
            if cur.data == value:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                if cur is self.tail:
                    self.tail = prev
                self._size -= 1
                return
            prev, cur = cur, cur.next
        raise ValueError(f"{value!r} no está en la lista")

    def clear(self):
        self.head = self.tail = None
        self._size = 0

    # ---------- Consulta ----------
    def index(self, value):
        for i, item in enumerate(self):
            if item == value:
                return i
        raise ValueError(f"{value!r} no está en la lista")

    def count(self, value):
        return sum(1 for item in self if item == value)

    def is_empty(self):
        return self._size == 0

    # ---------- Operaciones ----------
    def reverse(self):
        prev, cur = None, self.head
        self.tail = self.head
        while cur is not None:
            cur.next, prev, cur = prev, cur, cur.next
        self.head = prev

    def to_list(self):
        return list(self)


if __name__ == "__main__":
    ll = MyLinkedList([1, 2, 3])
    ll.append(4)
    ll.prepend(0)
    ll.insert(2, 99)
    assert ll.to_list() == [0, 1, 99, 2, 3, 4]

    assert ll[0] == 0 and ll[-1] == 4 and len(ll) == 6
    assert 99 in ll and ll.index(3) == 4 and ll.count(1) == 1

    ll.remove(99)
    assert ll.pop() == 4 and ll.pop(0) == 0
    assert ll.to_list() == [1, 2, 3]

    ll.reverse()
    assert ll.to_list() == [3, 2, 1]
    ll.append(10)
    assert ll.tail.data == 10

    ll[1] = 20
    assert ll.to_list() == [3, 20, 1, 10]

    ll.clear()
    assert ll.is_empty() and ll.head is None and ll.tail is None
    print("Todas las pruebas pasaron:", ll)