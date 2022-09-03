import math
import pprint
import random
from turtle import *
from typing import Tuple

from algorithms.disjoint_set import DisjointSet
from src.color_scheme import ColorScheme


class TriangularMaze:

    def __init__(self, side_len, num_levels):

        self.side_len = side_len
        self.num_levels = num_levels

        self.TOP = 0
        self.LEFT = 1
        self.RIGHT = 2
        self.BOTTOM = 3

        '''
        at each level, actual number of triangles is 2*level + 1. i.e.
        level: 0, 1, 2, 3, 4, 
        cells: 1, 3, 5, 7, 9, 

        but the triangles to be drawn are just level+1. the gap between drawn triangles 
        appears as inverted triangle. but that inverted one is not explicitly drawn

        so, 
        level: 0, 1, 2, 3, 
        cells: 1, 2, 3, 4, 
        '''
        self.num_cells_at_level = [2 * lvl + 1 for lvl in range(num_levels)]
        self.total_cells = sum(self.num_cells_at_level)

        # compute the length of perpendicular dividing the equilateral triangle into
        # 2 right angled triangles.
        self.triangle_height = self.compute_triangle_height(self.side_len)

        self.clr_scheme = ColorScheme()

    def compute_triangle_height(self, side):
        # apply Pythagoras theorem
        base = side / 2
        hypotenuse = side
        perpendicular = math.sqrt(hypotenuse**2 - base**2)

        return perpendicular

    def get_graph_edges(self):
        # creates a graph aligned with triangular pattern
        # exactly what's required for our Maze algorithm
        # only returns the edges involved

        edges = []

        for lvl in range(self.num_levels):
            num_triangles = 2 * lvl + 1

            for tri in range(num_triangles):
                # sum all triangles in previous levels, add current level's triangle index
                cell_1d = self.index_1d(lvl, tri)

                if tri > 0:
                    left_1d = cell_1d - 1
                    edges.append((cell_1d, left_1d))

                if tri % 2 == 0 and lvl < self.num_levels - 1:
                    # all even indexed triangles are connected downward
                    child_1d = sum(self.num_cells_at_level[:lvl + 1]) + tri + 1  # index of child
                    edges.append((cell_1d, child_1d))

        return edges

    def kruskal_spanning_tree(self, edges):
        # creates Spanning Tree using Randomized Kruskal's:
        # Creates a Spanning Tree for given graph while picking edges at random and
        # including their vertices in the graph if not already in such a way that there are no cycles

        # the minimum spanning tree has no edges in the start
        # PARENT, LEFT, RIGHT, CHILD
        spanning_tree = {
            cell: [0, 0, 0, 0] for cell in range(self.total_cells)
        }

        # cell indices will be used in disjoint set and then to map back to real edge
        cells = [idx for idx in range(self.total_cells)]

        disjoint = DisjointSet(cells)

        random.shuffle(edges)

        for edge in edges:
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
            return self.BOTTOM
        elif cell1_level > cell2_level:
            return self.TOP

    def index_1d(self, level, cell):
        # takes the level & cell (the 2D indices) and converts them to their corresponding 1D index
        if level >= self.num_levels:
            raise Exception("level greather than maze levels")

        return sum(self.num_cells_at_level[:level]) + cell

    def draw_triangular_maze(self, spanning_tree):

        # the highest point of diagram, top tip of level-0 triangle
        y = self.num_levels * self.triangle_height / 2

        for level in range(self.num_levels):
            level_width = (level + 1) * self.side_len
            x = - level_width / 2

            # we start drawing a triangle from bottom edge, so drop down that much
            y -= self.triangle_height

            '''
            at ever level, there are 2*level+1 cells. 
            but only (level+1) of them are drawn which are odd indexed 
            '''
            for cell in range(self.num_cells_at_level[level]):
                # only draw even indexed cells
                if cell % 2 != 0:
                    continue

                # convert to 1d index
                cell_1d = self.index_1d(level, cell)

                penup()
                setposition(x, y)
                setheading(0)

                # draw the edge between cell and its child if cell is not connected to it
                # if not self.is_connected_to(level, cell, self.CHILD):
                #     pendown()
                # draw bottom line if cell is not connected to its child
                if spanning_tree[cell_1d][self.BOTTOM] == 0:
                    pendown()

                # draw bottom
                self.clr_scheme.next_color(color)
                forward(self.side_len)
                penup()

                # draw right edge
                if spanning_tree[cell_1d][self.RIGHT] == 0:
                    pendown()

                left(120)
                self.clr_scheme.next_color(color)
                forward(self.side_len)
                penup()

                # draw left edge

                # add gates for top & left most cells. don't draw left edge for these cells
                is_first_cell = level == 0 and cell == 0
                is_left_most_cell = level == self.num_levels - 1 and cell == 0

                # if not self.is_connected_to(level, cell, self.LEFT) and not is_first_cell and not is_left_most_cell:
                if spanning_tree[cell_1d][self.LEFT] == 0 and not is_first_cell and not is_left_most_cell:
                    pendown()

                left(120)
                self.clr_scheme.next_color(color)
                forward(self.side_len)

                # now draw the triangle towards its right
                x += self.side_len

    def draw_pyramid_of_triangles(self):
        # to visualize the initial state of diagram before maze edges are opened

        # the highest point of diagram, top tip of level-0 triangle
        y = self.num_levels * self.triangle_height / 2

        for level in range(self.num_levels):
            level_width = (level + 1) * self.side_len
            x = -level_width / 2

            # we start drawing a triangle from bottom edge, so drop down that much
            y -= self.triangle_height

            # print(x, y)

            for cell in range(level + 1):
                penup()
                setposition(x, y)
                setheading(0)
                pendown()
                # draw bottom
                forward(self.side_len)

                # draw right edge
                left(120)
                forward(self.side_len)

                # draw left edge
                left(120)
                forward(self.side_len)
                penup()

                # now draw the triangle towards its right
                x += self.side_len


if __name__ == '__main__':
    hideturtle()
    speed(100)
    pensize(5)

    # set full screen for canvas
    screen = Screen()
    screen.setup(width=1.0, height=1.0)

    tm = TriangularMaze(side_len=30, num_levels=25)

    edges = tm.get_graph_edges()

    spanning_tree = tm.kruskal_spanning_tree(edges)

    tm.draw_triangular_maze(spanning_tree)

    done()

