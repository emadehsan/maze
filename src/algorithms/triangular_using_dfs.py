'''
THIS CODE IS NOT OPTIMIZED
'''

import math
import pprint
import random
from collections import deque
from turtle import *
from typing import Tuple


class TriangularMaze:

    def __init__(self, sideLen, numLevels):
        self.sideLen = sideLen
        self.numLevels = numLevels

        self.PARENT = 0
        self.LEFT = 1
        self.CHILD = 2
        self.RIGHT = 3

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
        self.numCellsAtLevel = [2 * level + 1 for level in range(self.numLevels)]
        self.totalCellsInMaze = sum(self.numCellsAtLevel)

        # compute the length of perpendicular dividing the equilateral triangle into
        # 2 right angled triangles.
        self.triangleHeight = self._compute_triangle_height(self.sideLen)

        self.graph = self.computeMaze()


    def _compute_triangle_height(self, side):
        # apply Pythagoras theorem
        base = side/2
        hypotenuse = side
        perpendicular = math.sqrt(hypotenuse**2 - base**2)
        return perpendicular

    def index1dfrom2d(self, level, cell):
        # takes the level & cell (the 2D indices) and converts them to their corresponding 1D index
        if level >= self.numLevels:
            raise Exception("level greather than maze levels")
            return

        idx = 0
        for l in range(level):
            idx += self.numCellsAtLevel[l]
        idx += cell

        return idx

    def index2dfrom1d(self, idx) -> Tuple[int, int]:
        # takes index of cell in 1-D array form and converts to 2D
        if idx >= self.totalCellsInMaze:
            raise Exception("1D index greater than total number of cells")
            return

        level = 0
        while idx - self.numCellsAtLevel[level] >= 0:
            idx -= self.numCellsAtLevel[level]
            level += 1

        # the remaining cells give the index of cell at current level
        cell = idx

        return level, cell

    def parent_idx_1d(self, level, cell):
        # takes 2D coordinates of current cell/triangle and returns parent's index in 1d representation
        # an even indexed cell has no parent
        if cell % 2 == 0 or level <= 0:
            return None
        return self.index1dfrom2d(level-1, cell-1)

    def left_idx_1d(self, level, cell):
        if cell > 0:
            return self.index1dfrom2d(level, cell-1)
        return None

    def right_idx_1d(self, level, cell):
        if cell < self.numCellsAtLevel[level] - 1:
            return self.index1dfrom2d(level, cell+1)
        return None

    def child_idx_1d(self, level, cell):
        # an odd indexed cell has no child. it is inverted equilateral with its tip pointing downards
        if cell % 2 != 0 or level >= self.numLevels-1:
            return None
        return self.index1dfrom2d(level+1, cell+1)


    def computeMaze(self):
        # DFS randomized

        # hashmap with each entry corresponding to the connectiong between cells
        # format of key: "smaller_id_cell:larger_id_cell"
        graph = {}

        # pick a random starting cell
        cell_1d = random.randint(0, self.totalCellsInMaze - 1)

        visited = [cell_1d]
        stack = deque()
        stack.append(cell_1d)

        while len(visited) < self.totalCellsInMaze:
            # randomly pick a neighbour of current cell and go there

            # get 2D representation of current cell
            level, cell = self.index2dfrom1d(cell_1d)

            connections = [
                self.parent_idx_1d(level, cell),
                self.left_idx_1d(level, cell),
                self.child_idx_1d(level, cell),
                self.right_idx_1d(level, cell)
            ]

            validConnections = []
            for conn in connections:
                if conn is not None and conn not in visited:
                    validConnections.append(conn)

            if len(validConnections) > 0:
                nextCell = random.choice(validConnections)

                visited.append(nextCell)
                stack.append(nextCell)

                # add this connection to the graph
                # the key represents connection from lower indexed cell to higher indexed cell
                key = self._make_graph_key(cell_1d, nextCell)
                graph[key] = True

                cell_1d = nextCell
            else:
                cell_1d = stack.pop()

        return graph

    def _make_graph_key(self, cell1, cell2):
        # the key of graph hashmap is from smaller indexed cell to higher indexed cell
        key = f'{cell1}:{cell2}'
        if cell2 < cell1:
            key = f'{cell2}:{cell1}'
        return key

    def is_connected_to(self, level, cell, direction):
        cell_1d = self.index1dfrom2d(level, cell)

        get_conn_id = {
            self.PARENT: self.parent_idx_1d,
            self.LEFT: self.left_idx_1d,
            self.CHILD: self.child_idx_1d,
            self.RIGHT: self.right_idx_1d
        }

        conn_id = get_conn_id[direction](level, cell)

        # if direction == self.PARENT:
        #     conn_id = self.parent_idx_1d(level, cell)
        # elif direction == self.LEFT:
        #     conn_id = self.left_idx_1d(level, cell)
        # elif direction == self.CHILD:
        #     conn_id = self.child_idx_1d(level, cell)
        # elif direction == self.RIGHT:
        #     conn_id = self.right_idx_1d(level, cell)
        # else:
        #     raise Exception("Invalid direction provided")

        if conn_id is None:
            return False

        key = self._make_graph_key(cell_1d, conn_id)
        return key in self.graph

    def draw_triangular_maze(self):

        # the highest point of diagram, top tip of level-0 triangle
        y = self.numLevels * self.triangleHeight / 2

        # TODO set random entry points
        # pick entry and exit points
        # gates = [
        #     (0, 0),  # top cell of maze
        #     (self.numLevels-1, 0),  # left most cell
        #     (self.numLevels, self.numLevels)  # right most cell
        # ]
        # entry_point = random.choice(gates)
        # gates.remove(entry_point)
        # exit_point = random.choice(gates)
        #
        # # level == entry_point[0] and cell == entry_point[1]

        for level in range(self.numLevels):
            level_width = (level + 1) * self.sideLen
            x = -level_width / 2

            # we start drawing a triangle from bottom edge, so drop down that much
            y -= self.triangleHeight

            '''
            at ever level, there are 2*level+1 cells. 
            but only (level+1) of them are drawn which are odd indexed 
            '''
            for cell in range(self.numCellsAtLevel[level]):
                # only draw even indexed cells
                if cell % 2 != 0:
                    continue

                penup()

                # draw bottom edge. it connects a cell to its child.
                setposition(x, y)
                setheading(0)
                # draw the edge between cell and its child if cell is not connected to it
                if not self.is_connected_to(level, cell, self.CHILD):
                    pendown()
                # draw bottom
                forward(self.sideLen)
                penup()

                # draw right edge
                left(120)
                if not self.is_connected_to(level, cell, self.RIGHT):
                    pendown()
                forward(self.sideLen)
                penup()

                # draw left edge
                left(120)

                # add gates for top & left most cells. don't draw left edge for these cells
                is_first_cell = level == 0 and cell == 0
                is_left_most_cell = level == self.numLevels-1 and cell == 0

                if not self.is_connected_to(level, cell, self.LEFT) and not is_first_cell and not is_left_most_cell:
                    pendown()
                forward(self.sideLen)

                # now draw the triangle towards its right
                x += self.sideLen

    def draw_pyramid_of_triangles(self):
        # to visualize the initial state of diagram before maze edges are opened

        # the highest point of diagram, top tip of level-0 triangle
        y = self.numLevels * self.triangleHeight / 2

        for level in range(self.numLevels):
            level_width = (level + 1) * self.sideLen
            x = -level_width / 2

            # we start drawing a triangle from bottom edge, so drop down that much
            y -= self.triangleHeight

            # print(x, y)

            for cell in range(level + 1):
                penup()
                setposition(x, y)
                setheading(0)
                pendown()
                # draw bottom
                forward(self.sideLen)

                # draw right edge
                left(120)
                forward(self.sideLen)

                # draw left edge
                left(120)
                forward(self.sideLen)
                penup()

                # now draw the triangle towards its right
                x += self.sideLen


if __name__ == '__main__':
    hideturtle()
    speed(100)
    pensize(2)

    tm = TriangularMaze(sideLen=30, numLevels=30)
    # tm = TriangularMaze(sideLen=16, numLevels=58)
    # print("numLevels", tm.numLevels)
    # print("sideLen", tm.sideLen)

    # tm.draw_pyramid_of_triangles()
    # pprint.pp(tm.computeMaze())
    # pprint.pp(tm.graph)
    tm.draw_triangular_maze()

    done()

