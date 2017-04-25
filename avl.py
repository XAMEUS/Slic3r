"""
AVL module
"""

class Avl:  #TODO: transform this class into real AVL.
    """
    The main class
    """
    def __init__(self, value, father=None):
        self.father = father
        self.value = value
        self.childs = [None, None]

    def __str__(self):
        chain = ""
        if self.childs[0] is not None:
            chain = str(self.childs[0]) + ", "
        chain += str(self.value)
        if self.childs[1] is not None:
            chain += ", " + str(self.childs[1])
        return chain

    def __iter__(self):
        if self.childs[0] is not None:
            yield from self.childs[0].__iter__()
        yield self.value
        if self.childs[1] is not None:
            yield from self.childs[1].__iter__()

    def add(self, n_value, key=lambda x: x):
        """
        Add a new value in the AVL
        """
        current = self
        while True:
            tmp = key(n_value) > key(current.value)
            if current.childs[tmp] is None:
                current.childs[tmp] = Avl(n_value, current)
                return current.childs[tmp]
            current = current.childs[tmp]

    def search(self, value, key=lambda x: x):
        """
        Search the right cell and return if the cell is present
        """
        current = self
        while current is not None:
            if current.value == value:
                return current
            current = current.childs[key(value) > key(current.value)]
        return

    def min(self):
        """
        Find min
        """
        current = self
        while current is not None and current.childs[0] is not None:
            current = current.childs[0]
        return current

    def max(self):
        """
        Find max
        """
        current = self
        while current is not None and current.childs[1] is not None:
            current = current.childs[1]
        return current

    def successor(self):
        """
        Find the successor
        """
        current = self
        if current.childs[1] is not None:
            return current.childs[1].min()
        while current.father is not None and current.father.childs[0] is not current:
            current = current.father
        return current.father

    def predecessor(self):
        """
        Find the predecessor
        """
        current = self
        if current.childs[0] is not None:
            return current.childs[0].max()
        while current.father is not None and current.father.childs[1] is not current:
            current = current.father
        return current.father

    def delete(self):
        """
        Remove this cell
        """
        child_l = self.childs[0] != None
        child_r = self.childs[1] != None
        child_number = self.father.childs[1] is self

        if child_l and child_r:
            successor = self.successor()
            self.value = successor.value
            successor.father.childs[successor.father.childs[1] is successor] = successor.childs[1]
        else:
            if child_l or child_r:
                self.childs[child_r].father = self.father
            self.father.childs[child_number] = self.childs[child_r]
if __name__ == '__main__':
    a = Avl(10)
    a.add(5)
    a.add(2)
    a.add(7)
    print(a, "\t", a.childs[0].value)
    a.add(9)
    print(a, "\t", a.childs[0].value)
    a.childs[0].delete()
    print(a, "\t", a.childs[0].value)
    a.childs[0].delete()
    print(a, "\t", a.childs[0].value)
