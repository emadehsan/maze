import pprint
import random


class PrimsRandomized:
    '''
    Creates a Minimum Spanning Tree for square grid like graph
    where each node has 4 neighbours (except boundary nodes)
    '''

    def __init__(self, row_len):
        self.row_len = row_len

        # it is a square maze, so:
        self.total_nodes = row_len**2

        # indices of the a node's neighbours in the adjacency list
        self.TOP = 0
        self.LEFT = 1
        self.BOTTOM = 2
        self.RIGHT = 3

    def prims_mst(self):
        # creates Minimum Spanning Tree using Randomized Prim's

        # the minimum spanning tree has no edges in the start
        # and it is represented like an adjacency list
        # each node can be connected to 4 of its neighbours, counted counter-clockwise
        # TOP, LEFT, BOTTOM, RIGHT
        mst = [
            [0, 0, 0, 0] for _ in range(self.total_nodes)
        ]

        # list of nodes to visit
        to_visit = [node for node in range(self.total_nodes)]

        # let's start Prims by visiting the first node
        node = to_visit[0]
        visited = [node]
        to_visit.remove(node)

        while len(to_visit) > 0:
            # for all the nodes in visited, pick one of the outgoing edge
            # at random, connecting to a new node that is not already in visited.

            edges_pool = self.edges_to_unvisited_nodes(visited)
            # pick a random edge
            edge = random.choice(edges_pool)
            node, next_node = edge

            # connect these two nodes in the minimum spanning tree
            direction = self.get_neighbour_dir(node, next_node)
            mst[node][direction] = 1

            # also set it for the neighbour
            neighbour_dir = self.get_neighbour_dir(next_node, node)
            mst[next_node][neighbour_dir] = 1

            # now remove this next_node from unvisited list and add to visited
            visited.append(next_node)
            to_visit.remove(next_node)

        return mst

    def edges_to_unvisited_nodes(self, visited):
        # returns all the edges originating from already visited nodes and going
        # towards unvisited nodes

        edges_pool = []

        for node in visited:
            # add this node's edges to the pool

            row = node // self.row_len
            col = node % self.row_len

            if row > 0:
                # all rows except top one has top neighbours
                # add the edge between node<>top_node to edges pool
                # if top_node is not already visited
                top_node = node - self.row_len
                if top_node not in visited:
                    edges_pool.append((node, top_node))

            if col > 0:
                # all columns except fist have left neighbours
                left_node = node - 1
                if left_node not in visited:
                    edges_pool.append((node, left_node))

            if row < self.row_len - 1:
                # all rows except last have bottom neighbours
                bottom_node = node + self.row_len
                if bottom_node not in visited:
                    edges_pool.append((node, bottom_node))

            if col < self.row_len - 1:
                # all columns except last have right neighbours
                right_node = node + 1
                if right_node not in visited:
                    edges_pool.append((node, right_node))

        return edges_pool

    def get_neighbour_dir(self, node, next_node):
        '''
        returns the direction in which next_node lies relative to node
        '''
        if node - self.row_len == next_node:
            # next_node is the top_node to node
            return self.TOP
        if node - 1 == next_node:
            return self.LEFT
        if node + self.row_len == next_node:
            return self.BOTTOM
        if node + 1 == next_node:
            return self.RIGHT


if __name__ == '__main__':
    # number of nodes in a row
    n = 4
    pr = PrimsRandomized(n)

    print("Prims Minimum Spanning Tree (as adjacency list):")
    pprint.pp(
        pr.prims_mst()
    )
