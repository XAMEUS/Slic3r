#!/usr/bin/env python3
"""
SL Structure
"""

# pylint:disable=C0111,C0301,C0103

class Node:
    def __init__(self, value, parent=None, left=None, right=None):
        self.value = value
        self.parent = parent
        self.children = [left, right]

    def insert(self, value):
        current = self
        while True:
            tmp = value > current.value
            if current.children[tmp] is None:
                current.children[tmp] = Node(value, current)
                return current.children[tmp]
            current = current.children[tmp]

    def lookup(self, value, parent=None):
        if value < self.value:
            if self.children[0] is None:
                return None, None
            return self.children[0].lookup(value, self)
        elif value > self.value:
            if self.children[1] is None:
                return None, None
            return self.children[1].lookup(value, self)
        else:
            return self, parent

    def delete(self, node):
        node, parent = node, node.parent
        if node is not None:
            if not (node.children[0] or node.children[1]):
                if parent:
                    if parent.children[0] is node:
                        parent.children[0] = None
                    else:
                        parent.children[1] = None
                else:
                    self.value = None
            elif node.children[0] and node.children[1]:
                parent = node
                successor = node.children[1]
                while successor.children[0]:
                    parent = successor
                    successor = successor.children[0]
                node.value = successor.value
                if parent.children[0] == successor:
                    parent.children[0] = successor.children[1]
                else:
                    parent.children[1] = successor.children[1]
                if successor.children[1]:
                    successor.children[1].parent = parent
            else:
                if node.children[0]:
                    n = node.children[0]
                else:
                    n = node.children[1]
                if parent:
                    if parent.children[0] is node:
                        parent.children[0] = n
                        if n:
                            n.parent = parent
                    else:
                        parent.children[1] = n
                        if n:
                            n.parent = parent
                else:
                    self.children[0] = n.children[0]
                    self.children[1] = n.children[1]
                    self.value = n.value
                    n.parent = None
                    if self.children[0]:
                        self.children[0].parent = self
                    if self.children[1]:
                        self.children[1].parent = self

    def __str__(self):
        chain = ""
        if self.children[0] is not None:
            chain = str(self.children[0]) + ", "
        chain += str(self.value)
        if self.children[1] is not None:
            chain += ", " + str(self.children[1])
        return chain

    def __iter__(self):
        if self.children[0] is not None:
            yield from iter(self.children[0])
        yield self
        if self.children[1] is not None:
            yield from iter(self.children[1])

    def min(self):
        """
        Find min
        """
        current = self
        while current is not None and current.children[0] is not None:
            current = current.children[0]
        return current

    def max(self):
        """
        Find max
        """
        current = self
        while current is not None and current.children[1] is not None:
            current = current.children[1]
        return current

    def successor(self):
        """
        Find the successor
        """
        current = self
        if current.children[1] is not None:
            return current.children[1].min()
        while current.parent is not None and current.parent.children[0] is not current:
            current = current.parent
        return current.parent

    def predecessor(self):
        """
        Find the predecessor
        """
        current = self
        if current.children[0] is not None:
            return current.children[0].max()
        while current.parent is not None and current.parent.children[1] is not current:
            current = current.parent
        return current.parent

class SweepLines:
    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def __str__(self):
        return "{" + str(self.root) + "}"

    def __iter__(self):
        if self.size:
            yield from iter(self.root)

    def put(self, val):
        self.size += 1
        if self.root:
            return self.root.insert(val)
        else:
            self.root = Node(val)
            return self.root

    def search(self, value):
        if self.root:
            return self.root.lookup(value)[0]

    def delete(self, value):
        if self.size > 1:
            node, _ = self.root.lookup(value)
            if node:
                self.root.delete(node)
                self.size -= 1
            else:
                raise KeyError('Error '+str(value)+' not in SL')
        elif self.size == 1 and self.root.value == value:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('Error, empty SL')

from random import randint
if __name__ == "__main__":
    SL = SweepLines()
    r = []
    while len(r) < 10:
        a = randint(1, 100)
        if a not in r:
            r.append(a)
    print(r)
    for e in r:
        SL.put(e)
    print(SL)
    n = SL.search(r[2])
    print(r[2], n.value)
    print(n.predecessor().value)
    print(n.successor().value)


"""
if __name__ == "__main__":
    stop = False
    c = 0
    while not stop:
        SL = SweepLines()
        N = Node(50)
        r = []
        while len(r) < 200:
            a = randint(1, 1000)
            if a not in r:
                r.append(a)
        for e in r:
            SL.put(e)
        for i in r:
            try:
                SL.delete(i)
            except Exception as e:
                stop = True
                print(r)
        if len(SL) > 0:
            stop = True
            print(len(SL), SL)
        c += 1
        print(c)
"""
