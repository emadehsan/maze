'''
Disjoint Set data structure
Also known as Union Find
'''

from typing import List, Any


class DisjointSet:
    def __init__(self, items: List[Any]):
        # 1. assign a mapping to items
        # since it is a list, let's assume each item is mapped to its index
        self.items = items

        # make every item its own parent
        self.parent = [idx for idx in range(len(items))]

        # size of each set/tree is one at the start (set containing the item itself).
        self.size = [1 for _ in range(len(items))]

    def find(self, x: int) -> int:
        # find root node for give node x
        item = x
        while item != self.parent[item]:
            item = self.parent[item]
        root = item

        # path compression (optional): makes subsequent finds faster:
        # point all the nodes from x till root directly to root
        while x != root:
            parent = self.parent[x]
            self.parent[x] = root
            x = parent

        return root

    def union(self, a: int, b: int) -> int:
        # takes two nodes and combines their parent into a single tree

        # we keep track of items in sets using indices. so get indices of provided items
        # a = self.items.index(item_a)
        # b = self.items.index(item_b)

        # find parents of both items
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a != root_b:
            # add the smaller set to the larger one
            # this keeps the depth of larger tree minimum
            if self.size[root_a] < self.size[root_b]:
                self.size[root_b] += self.size[root_a]
                self.parent[root_a] = root_b
            else:
                self.size[root_a] += self.size[root_b]
                self.parent[root_b] = root_a

        # both a & b are part of the same set (if they weren't already)
        # and the root of both is root_a
        return root_a


if __name__ == '__main__':
    # test

    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'
    I = 'I'
    J = 'J'
    K = 'K'
    L = 'L'
    arr = [A, B, C, D, E, F, G, H, I, J, K, L]
    uf = DisjointSet(arr)

    uf.union(D, E)
    uf.union(C, D)
    uf.union(B, C)
    uf.union(A, B)
    uf.union(F, A)

    uf.union(K, L)
    uf.union(J, K)
    uf.union(I, J)
    uf.union(H, I)
    uf.union(G, H)

    print('Items:', arr)
    print('Parents', uf.parent)

    # the path compression is done by find method. And the compressed-path also depends which nodes of
    # two different sets were provided to be union into a single one. E.g. here we are combining
    # the lowest two nodes two different trees. So they'll do the path compression along the way for
    # all midway nodes
    uf.union(E, L)

    print('Items:', arr)
    print('Parents', uf.parent)



