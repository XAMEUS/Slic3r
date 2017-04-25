"""
AVL module
"""

class Avl:
    """
    The main class
    """
    def __init__(self):
        self.size = 0
        self.node = None

    def __str__(self):
        if self.size:
            return str(self.node)
        return ""

    def __iter__(self):
        if self.size:
            yield from iter(self.node)

    def add(self, n_value): #TODO key
        """
        Add a new value in the AVL
        """
        if self.size:
            self.node.add(n_value)
        else:
            self.node = self.node(n_value)
        self.size += 1

    def delete(self, node_to_remove):
        """
        Delete the node in parameter
        """
        if node_to_remove is not self.node:
            node_to_remove.delete()
        else:
            pass
        self.size -= 1

    def search(self, value): #TODO key
        """
        Search the right cell and return if the cell is present
        """
        assert self.size
        return self.node.search(value)

    def min(self):
        """
        Find min
        """
        assert self.size
        return self.node.min()
    def max(self):
        """
        Find max
        """
        assert self.size
        return self.node.max()

class Node:  #TODO: transform this class into real AVL.
    """
    The node class
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
            yield from iter(self.childs[0])
        yield self.value
        if self.childs[1] is not None:
            yield from iter(self.childs[1])

    def add(self, n_value, key=lambda x: x):
        """
        Add a new value in the AVL
        """
        current = self
        while True:
            tmp = key(n_value) > key(current.value)
            if current.childs[tmp] is None:
                current.childs[tmp] = Node(n_value, current)
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
            if successor.childs[1]:
                successor.childs[1].father = successor.father
        else:
            if child_l or child_r:
                self.childs[child_r].father = self.father
            self.father.childs[child_number] = self.childs[child_r]
