import math
import random
from collections import deque
from typing import List, Tuple
from turtle import *


class CircularMaze:

    def __init__(self, n, r):

        self.num_levels = n
        self.line_length = r

        # list containing number of cells at each level
        self.num_cells_at_level = self.cell_count_by_level()

        self.total_cells = sum(self.num_cells_at_level)

    def cell_count_by_level(self) -> List[int]:
        '''
        level: 0,  1,  2,  3,  4,  5,  6,  7,  8,  9...
        cells: 1, 16, 16, 32, 32, 32, 32, 64, 64, 64...
        '''

        cells_by_level = [1]

        for level in range(1, self.num_levels):
            cells_by_level.append(int(math.pow(2, math.floor(math.log2(level + 1)) + 3)))

        return cells_by_level

    def index_1d_from_2d(self, level, cell):
        # takes the level & cell (the 2D indices) and converts them to their corresponding 1D index

        if level >= self.num_levels:
            raise Exception("level greater than maze levels")

        idx = 0
        for lvl in range(level):
            idx += self.num_cells_at_level[lvl]
        idx += cell

        return idx

    def index_2d_from_1d(self, idx) -> Tuple[int, int]:
        # takes index of cell in 1-D array form and converts to 2D
        if idx >= self.total_cells:
            raise Exception("1D index greater than total number of cells")

        level = 0
        while idx - self.num_cells_at_level[level] >= 0:
            idx -= self.num_cells_at_level[level]
            level += 1

        # the remaining cells give the index of cell at current level
        cell = idx

        return level, cell

    def parent_index_1d(self, level, cell):
        # takes 2D index of current cell and returns index of its parent in 1D
        if level <= 0:
            raise Exception(f'Level {level} has no parent')
        elif level == 1:
            return 0

        parent = self.index_1d_from_2d(level - 1, cell)

        # sometimes parent level has fewer cells than current level
        if self.num_cells_at_level[level - 1] < self.num_cells_at_level[level]:
            parent = self.index_1d_from_2d(level - 1, cell // 2)

        return parent

    def left_index_1d(self, level, cell):
        if level <= 0:
            raise Exception(f'Level {level} has no left cell')

        left = self.index_1d_from_2d(level, cell - 1)

        if cell == 0:
            # it is circular maze, the first cell's left would be the last cell
            left = self.index_1d_from_2d(level, self.num_cells_at_level[level] - 1)

        return left

    def right_index_1d(self, level, cell):
        if level <= 0:
            raise Exception(f'Level {level} has no left cell')

        right = self.index_1d_from_2d(level, cell + 1)

        if cell == self.num_cells_at_level[level] - 1:
            # it is last cell, its right is first cell
            right = self.index_1d_from_2d(level, 0)

        return right

    def create_dfs_tree(self):

        graph = {}

        # pick a random starting cell
        cell_1d = random.randint(0, self.total_cells - 1)

        visited = [cell_1d]

        # stack will help us do depth first search without recursion
        stack = deque()
        stack.append(cell_1d)

        while len(visited) < self.total_cells:
            level, cell = self.index_2d_from_1d(cell_1d)

            # neighbours of current cell
            connections = []

            if level == 0:
                # level-0 has 16 neighbours i.e. all the cells on level-1.
                # indexed [1-16] in 1D representation
                for idx in range(1, self.num_cells_at_level[1] + 1):
                    connections.append(idx)
            else:
                # all the cells except level-0 have 3, 4 or 5 neighbours.
                # cells in the last level (n-1) have no children.
                # So they have exactly 3 neighbours (parent, left, right).

                connections.append(self.parent_index_1d(level, cell))

                connections.append(self.left_index_1d(level, cell))

                connections.append(self.right_index_1d(level, cell))

                # the cells belonging to level-1 to 2nd last level (n-2) can have either 4 or 5 neighbours
                if level <= self.num_levels - 2:
                    if self.num_cells_at_level[level] < self.num_cells_at_level[level + 1]:
                        # since num cells at this level is less than num cells at next level
                        # then cells in this level have 5 neighbours (since 2 children)

                        # left child:
                        connections.append(self.index_1d_from_2d(level + 1, 2 * cell))
                        # right child:
                        connections.append(self.index_1d_from_2d(level + 1, 2 * cell + 1))
                    else:
                        # otherwise it has one child
                        connections.append(self.index_1d_from_2d(level + 1, cell))

            # only keep the neighbours that are not already visited
            unvisited_connections = []
            for conn in connections:
                if conn not in visited:
                    unvisited_connections.append(conn)

            if len(unvisited_connections) > 0:
                next_cell = random.choice(unvisited_connections)

                visited.append(next_cell)
                stack.append(next_cell)

                # add connection in both directions
                # cell_1d -> next_cell
                if cell_1d in graph:
                    graph[cell_1d].append(next_cell)
                else:
                    graph[cell_1d] = [next_cell]

                # next_cell -> cell_1d
                if next_cell in graph:
                    graph[next_cell].append(cell_1d)
                else:
                    graph[next_cell] = [cell_1d]

                cell_1d = next_cell
            else:
                cell_1d = stack.pop()

        return graph

    def draw_circular_pattern(self):

        for level in range(self.num_levels):

            radius = level * self.line_length

            # for this level, the circle would be divided into num_cells number of arcs
            arcAngle = 360 / self.num_cells_at_level[level]

            goto(radius, 0)

            for cell in range(self.num_cells_at_level[level]):

                # draw the vertical line
                forward(self.line_length)

                # come back to the drawing position
                penup()
                backward(self.line_length)
                pendown()

                # turn to draw the arch
                left(90)
                circle(radius, arcAngle)

                # undo that turn for the arc to face the direction of next vertical line
                right(90)

        # draw the outer boundary
        radius = self.num_levels * self.line_length

        penup()

        goto(radius, 0)
        setheading(90)

        pendown()

        num_cells = self.num_cells_at_level[-1]
        arcAngle = 360 / num_cells

        for cell in range(num_cells):
            circle(radius, arcAngle)

        # circle(radius)

    def draw_maze(self, graph):

        penup()

        '''
        while drawing maze, we draw 
        1. an arc between current cell & its parent cell
        2. a line between current cell & its left_cell (that appears just before current cell)

        if theres connections between current cell & these parent/left cell
        then skip the corresponding arc/line from drawing to keep an open path
        '''

        # we do not draw level-0 since its boundaries would be drawn by cells in level-1
        for level in range(1, self.num_levels):

            # draw level 1's bottom arc with bigger radius (that's why level+1)
            radius = level * self.line_length

            arcAngle = 360 / self.num_cells_at_level[level]

            penup()
            goto(radius, 0)
            setheading(0)

            for cell in range(self.num_cells_at_level[level]):

                # get 1D index from 2D representation for current cell
                cell_1d = self.index_1d_from_2d(level, cell)

                parent_cell = self.parent_index_1d(level, cell)
                left_cell = self.left_index_1d(level, cell)

                # draw vertical line between current cell and its left_cell if they are not connected
                if left_cell not in graph[cell_1d]:
                    pendown()
                    forward(self.line_length)
                    penup()

                    # come back to the starting position
                    backward(self.line_length)

                # if current cell & parent are connected, don't draw arc.
                # but do move the arc length to move the cursor to desired position for next cell
                if parent_cell not in graph[cell_1d]:
                    pendown()

                # turn for the arch
                left(90)
                circle(radius, arcAngle)

                # undo that turn for the arc
                right(90)
                penup()

        # draw the boundary circle while leaving entrance gate open
        radius = self.num_levels * self.line_length

        penup()
        goto(radius, 0)
        setheading(90)
        pendown()

        num_cells = self.num_cells_at_level[-1]
        arcAngle = 360 / num_cells

        skip_arc = random.randint(0, num_cells - 1)

        for cell in range(num_cells):
            if cell == skip_arc:
                penup()

            circle(radius, arcAngle)

            if cell == skip_arc:
                pendown()


if __name__ == '__main__':
    pensize(2)
    speed(100)
    hideturtle()

    n = 20
    r = 20
    maze = CircularMaze(n, r)

    # maze.draw_circular_pattern()

    tree = maze.create_dfs_tree()

    maze.draw_maze(tree)

    done()
