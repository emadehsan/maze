import pprint
import random
from typing import Tuple

from disjoint_set import DisjointSet


class KruskalRandomized:
    '''
    Creates a Spanning Tree for given graph while picking edges at random and including their vertices in the graph
    if not already in such a way that there are no cycles

    This implementation is specifc to Triangular Maze.
    '''

    def __init__(self, num_levels):

        self.num_levels = num_levels

        self.num_cells_at_level = [2 * lvl + 1 for lvl in range(num_levels)]

        self.total_cells = sum(self.num_cells_at_level)

        self.PARENT = 0
        self.LEFT = 1
        self.RIGHT = 2
        self.CHILD = 3

    def create_graph(self):
        # creates a graph aligned with triangular pattern

        graph = {
            cell: [0, 0, 0, 0] for cell in range(self.total_cells)
        }

        edges = []

        for lvl in range(self.num_levels):
            num_triangles = 2 * lvl + 1

            for tri in range(num_triangles):
                # sum all triangles in previous levels, add current level's triangle index
                index_1d = sum(self.num_cells_at_level[:lvl]) + tri

                if tri > 0:
                    graph[index_1d][self.LEFT] = 1
                    left_1d = index_1d - 1
                    edges.append((index_1d, left_1d))

                if tri < num_triangles - 1:
                    graph[index_1d][self.RIGHT] = 1
                    right_1d = index_1d + 1
                    edges.append((index_1d, right_1d))

                if tri % 2 == 0 and lvl < self.num_levels - 1:
                    # all even indexed triangles are connected downward
                    graph[index_1d][self.CHILD] = 1
                    child_1d = sum(self.num_cells_at_level[:lvl+1]) + tri + 1  # index of child
                    edges.append((index_1d, child_1d))

                elif tri % 2 != 0 and lvl > 0:
                    graph[index_1d][self.PARENT] = 1
                    parent_1d = sum(self.num_cells_at_level[:lvl - 1]) + tri - 1  # index of child
                    edges.append((index_1d, parent_1d))

        return graph, edges

    def kruskal_spanning_tree(self, edges):
        # creates Spanning Tree using Randomized Kruskal's

        # the minimum spanning tree has no edges in the start
        # PARENT, LEFT, RIGHT, CHILD
        spanning_tree = {
            cell: [0, 0, 0, 0] for cell in range(self.total_cells)
        }

        # list of nodes to visit
        to_visit = [node for node in range(self.total_cells)]

        # let's start Kruskal by visiting the first node
        visited = []

        # cell indices will be used in disjoint set and then to map back to real edge
        cells = [idx for idx in range(len(edges))]

        disjoint = DisjointSet(cells)

        while len(visited) < self.total_cells:
            # pick one edge at random, connecting to a new cell that is not already in visited.
            edge_idx = random.randint(0, len(edges)-1)
            edge = edges[edge_idx]
            cell1, cell2 = edge

            if cell1 in visited and cell2 in visited:
                # both cells already included, this edge is redundant
                edges.pop(edge_idx)
                continue

            # else, at least one of the cell is not part of spanning tree,
            # so connect both to include that
            disjoint.union(cell1, cell2)

            # connect these two nodes in the minimum spanning tree
            direction = self.get_neighbour_dir(cell1, cell2)
            spanning_tree[cell1][direction] = 1

            # also set it for the neighbour
            neighbour_dir = self.get_neighbour_dir(cell2, cell1)
            spanning_tree[cell2][neighbour_dir] = 1

            # add to visited
            if cell1 not in visited:
                visited.append(cell1)
            if cell2 not in visited:
                visited.append(cell2)

        return spanning_tree

    def index_2d(self, cell_1d) -> Tuple[int, int]:
        # takes index of cell in 1-D array form and converts to 2D
        if cell_1d >= self.total_cells:
            raise Exception("1D index greater than total number of cells")

        level = 0
        while cell_1d - self.num_cells_at_level[level] >= 0:
            cell_1d -= self.num_cells_at_level[level]
            level += 1

        # the remaining cells give the index of cell at current level
        cell = cell_1d

        return level, cell

    def get_neighbour_dir(self, cell1, cell2):
        '''
        returns the direction in which next_node lies relative to node.
        this method does not check the integrity of indices and whether this graph
        actually represents that triangular pattern.
        '''

        # convert to 2D indices
        cell1_level, cell1_idx = self.index_2d(cell1)
        cell2_level, cell2_idx = self.index_2d(cell2)

        if cell1_level == cell2_level:
            if cell1_idx < cell2_idx:
                return self.RIGHT
            else:
                return self.LEFT
        elif cell1_level < cell2_level:
            # cell2 is child of cell1
            return self.CHILD
        elif cell1_level > cell2_level:
            return self.PARENT


if __name__ == '__main__':
    # number of nodes in a row
    n = 4
    kr = KruskalRandomized(n)

    graph, edges = kr.create_graph()

    print("Kruskal Spanning Tree (as adjacency list):")
    pprint.pp(
        kr.kruskal_spanning_tree(edges)
    )
