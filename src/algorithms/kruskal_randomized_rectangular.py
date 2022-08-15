import pprint
import random
from typing import Tuple

from src.algorithms.disjoint_set import DisjointSet


class KruskalRectangular:
    '''
    Creates a Spanning Tree for given graph while picking edges at random and including their vertices in the graph
    if not already in such a way that there are no cycles

    This implementation is specific to Squared Maze from a Squared Grid Graph (nxn).
    '''

    def __init__(self, n):

        self.n = n
        self.total_cells = n ** 2

        self.TOP = 0
        self.RIGHT = 1
        self.BOTTOM = 2
        self.LEFT = 3

    def create_graph(self):
        # creates a graph aligned with squared grid pattern

        # we do not need adjacency list for Kruskal's, only the list of edges
        # but code is there for adjacency list for Grid graph, if we need it in the future
        # graph = {
        #     cell: [0, 0, 0, 0] for cell in range(self.n ** 2)
        # }

        edges = []

        # create a Grid graph where every node/cell is connected in all 4 directions
        # except the boundary cells
        for row in range(self.n):
            for col in range(self.n):
                # convert to 1D index
                node = self.n * row + col

                # only add connection to the right and bottom cells for each cell
                # this avoid duplication

                if col < self.n - 1:
                    # graph[node][self.RIGHT] = 1

                    right_node = node + 1
                    # write the smaller node first
                    edges.append((node, right_node))

                if row < self.n - 1:
                    # graph[node][self.BOTTOM] = 1
                    bottom_node = node + self.n
                    edges.append((node, bottom_node))

        # return graph, edges
        return edges

    def kruskal_spanning_tree(self):
        # creates s Spanning Tree using Randomized Kruskal's for given graph while picking edges at random and
        # including their vertices in the graph if not already in such a way that there are no cycles

        edges_of_graph = self.create_graph()

        # the minimum spanning tree has no edges in the start
        # PARENT, LEFT, RIGHT, CHILD
        spanning_tree = {
            cell: [0, 0, 0, 0] for cell in range(self.total_cells)
        }

        # record all the edges involved in Spanning Tree
        edges = []

        # cell indices will be used in disjoint set and then to map back to real edge
        cells = [idx for idx in range(self.total_cells)]

        disjoint = DisjointSet(cells)

        random.shuffle(edges_of_graph)

        for edge in edges_of_graph:
            # pick one edge at random, connecting to a new cell that is not already in visited.
            cell1, cell2 = edge

            # if these cells are not part of the same set, then they are separate trees and we need to combine them
            if disjoint.find(cell1) != disjoint.find(cell2):
                disjoint.union(cell1, cell2)

                # connect these two nodes in the spanning tree
                direction = self.get_neighbour_dir(cell1, cell2)
                spanning_tree[cell1][direction] = 1

                # also set it vice versa
                neighbour_dir = self.get_neighbour_dir(cell2, cell1)
                spanning_tree[cell2][neighbour_dir] = 1

                # also add to the list of edges for our spanning tree
                edges.append(edge)

        return spanning_tree, edges

    def index_2d(self, cell_1d):

        row = cell_1d // self.n
        col = cell_1d % self.n

        return row, col

    def get_neighbour_dir(self, cell1, cell2):
        '''
        returns the direction in which next_node lies relative to node.
        this method does not check the integrity of indices and whether this graph
        actually represents a grid pattern.
        '''
        if cell1 == cell2 + self.n:
            return self.TOP
        elif cell1 == cell2 - 1:
            return self.RIGHT
        elif cell1 == cell2 + 1:
            return self.LEFT
        elif cell1 == cell2 - self.n:
            return self.BOTTOM


if __name__ == '__main__':
    # number of nodes in a row
    n = 4
    kr = KruskalRectangular(n)

    graph, edges = kr.create_graph()

    print("Kruskal Spanning Tree (as adjacency list):")
    pprint.pp(
        kr.kruskal_spanning_tree(edges)
    )
