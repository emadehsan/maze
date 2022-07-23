import pprint
import random
from collections import deque
from turtle import *
import math
from typing import Tuple


class HexagonalMaze:
    '''
    the levels of Hexagon are not horizontal. They are sort of diagonal.
    Look at gallery/reference-hexagon-for-maze.PNG

    middle level has the most cell
    '''

    def __init__(self, sideLen, numLevels):
        self.sideLen = sideLen
        # TODO: ensure that levels are odd. for symmetric maze
        self.numLevels = numLevels

        # TODO: assumption, len(numCells) is odd
        self.middle_level_idx = self.numLevels//2
        self.numCellsAtLevel = self._calcNumCellsAtLevel(self.numLevels, self.middle_level_idx)

        self.totalCellsInMaze = sum(self.numCellsAtLevel)

        # y component of single small hexagon. height above its center
        self.y_component = self._calc_y_comp(self.sideLen)

        # edges counted counter clockwise start from bottom
        self.BOTTOM = 0
        self.RIGHT_BOTTOM = 1
        self.RIGHT_TOP = 2
        self.TOP = 3
        self.LEFT_TOP = 4
        self.LEFT_BOTTOM = 5

        self.graph = self.computeMaze()

    def _calcNumCellsAtLevel(self, numLevels, middle):
        # create a list of length numLevels
        numCellsAtLevel = [0 for _ in range(numLevels)]

        # the middle element of the maze will have cells = numLevels
        # number of cells will decrease towards its left and write
        n = numLevels
        numCellsAtLevel[middle] = n

        n -= 1
        left = middle - 1
        right = middle + 1
        while left >= 0 and right < len(numCellsAtLevel):
            numCellsAtLevel[left] = n
            numCellsAtLevel[right] = n

            n -= 1
            left -= 1
            right += 1

        return numCellsAtLevel

    def _calc_y_comp(self, sideLen):
        # a hexagon consists of 6 equilateral triangles
        # each have side length equal to the side length of hexagon
        # we will use those triangles' data to calculate the perpendicular through one of those triangles
        # this will give up the y comp (height of hexagon above origin, if origin was at center)
        base = sideLen / 2
        hypotenuese = sideLen
        perpendicular = math.sqrt(hypotenuese**2 - base**2)

        return perpendicular

    def index1dfrom2d(self, level, cell):
        # takes the level & cell (the 2D indices) and converts them to their corresponding 1D index
        if level >= self.numLevels:
            raise Exception("level greater than maze levels")
        return sum(self.numCellsAtLevel[:level]) + cell

    def index2dfrom1d(self, idx) -> Tuple[int, int]:
        # takes index of cell in 1-D array form and converts to 2D
        if idx >= self.totalCellsInMaze:
            raise Exception("1D index greater than total number of cells")

        level = 0
        while idx - self.numCellsAtLevel[level] >= 0:
            idx -= self.numCellsAtLevel[level]
            level += 1

        # the remaining cells give the index of cell at current level
        cell = idx
        return level, cell

    def have_num_cells_been_increasing(self, level):
        # number of cells increase up until middle level
        return level <= self.middle_level_idx

    def is_last_cell(self, level, cell):
        return cell == self.numCellsAtLevel[level]-1

    def left_parent_idx_1d(self, level, cell):
        # cells of first level & left side of bigger hexagon have no left parent
        if level == 0 or (cell == 0 and self.have_num_cells_been_increasing(level)):
            return None

        if self.have_num_cells_been_increasing(level):
            return self.index1dfrom2d(level-1, cell-1)
        # else left parent has the same index
        return self.index1dfrom2d(level-1, cell)

    def right_parent_idx_1d(self, level, cell):
        # cells of first level & and last cells of first levels where num cells increase have no right parent
        if level == 0 or (self.is_last_cell(level, cell) and self.have_num_cells_been_increasing(level)):
            return None

        if self.have_num_cells_been_increasing(level):
            return self.index1dfrom2d(level-1, cell)
        return self.index1dfrom2d(level-1, cell+1)

    def left_cell_idx_1d(self, level, cell):
        if cell > 0:
            return self.index1dfrom2d(level, cell-1)
        return None

    def right_cell_idx_1d(self, level, cell):
        if cell < self.numCellsAtLevel[level] - 1:
            return self.index1dfrom2d(level, cell+1)
        return None

    def left_child_idx_1d(self, level, cell):
        # last level and first cell of cells after middle (inclusive) level have no left child
        if level == self.numLevels-1 or (cell == 0 and level >= self.middle_level_idx):
            return None

        if level < self.middle_level_idx:
            return self.index1dfrom2d(level + 1, cell)
        return self.index1dfrom2d(level + 1, cell-1)

    def right_child_idx_1d(self, level, cell):
        # last level and last cell of cells after middle (inclusive) level have no right child
        if level == self.numLevels - 1 or (self.is_last_cell(level, cell) and level >= self.middle_level_idx):
            return None

        if level < self.middle_level_idx:
            return self.index1dfrom2d(level + 1, cell + 1)
        return self.index1dfrom2d(level + 1, cell)

    def _make_graph_key(self, cell1, cell2):
        # the key of graph hashmap is from smaller indexed cell to higher indexed cell
        key = f'{cell1}:{cell2}'
        if cell2 < cell1:
            key = f'{cell2}:{cell1}'
        return key

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
                self.left_parent_idx_1d(level, cell),
                self.right_parent_idx_1d(level, cell),
                self.left_cell_idx_1d(level, cell),
                self.right_cell_idx_1d(level, cell),
                self.left_child_idx_1d(level, cell),
                self.right_child_idx_1d(level, cell),
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

    def is_connected_to(self, level, cell, direction):
        cell_1d = self.index1dfrom2d(level, cell)

        get_conn_id = {
            self.BOTTOM: self.left_child_idx_1d,
            self.RIGHT_BOTTOM: self.right_child_idx_1d,
            self.RIGHT_TOP: self.right_cell_idx_1d,
            self.TOP: self.right_parent_idx_1d,
            self.LEFT_TOP: self.left_parent_idx_1d,
            self.LEFT_BOTTOM: self.left_cell_idx_1d
        }

        conn_id = get_conn_id[direction](level, cell)

        if conn_id is None:
            return False

        key = self._make_graph_key(cell_1d, conn_id)
        return key in self.graph

    def draw_hexagonal_maze(self):
        # these equations are reached from trial and error:
        # relative to origin, the starting point of first hexagon (bottom-left vertex)
        x = - self.sideLen * (self.numLevels - self.numCellsAtLevel[0]/2)
        y = self.y_component * (self.numLevels - self.numCellsAtLevel[0] - 1)

        for level in range(self.numLevels):
            prev_x = x
            prev_y = y

            for cell in range(self.numCellsAtLevel[level]):
                # we will draw 3 edges of each hexagon
                # because inner hexagons share boundaries with others
                # but we will draw the boundary for all the boundary hexagons
                penup()
                setheading(0)
                goto(x, y)

                # draw bottom
                # to add gate, skip first cell of last level
                is_bottom_gate = cell == 0 and level == self.numLevels-1
                if not self.is_connected_to(level, cell, self.BOTTOM) and not is_bottom_gate:
                    pendown()
                forward(self.sideLen)
                penup()

                # draw bottom right edge
                if not self.is_connected_to(level, cell, self.RIGHT_BOTTOM):
                    pendown()
                left(60)
                forward(self.sideLen)
                penup()

                # draw top right edge
                if not self.is_connected_to(level, cell, self.RIGHT_TOP):
                    pendown()
                left(60)
                forward(self.sideLen)
                penup()

                '''
                for certain boundary cells, draw other edges too. Refer to 
                gallery/original-hexagon-for-maze-open-ends.PNG
                '''
                is_first_level = level == 0
                is_first_cell = cell == 0
                # is_last_cell = cell == self.numCellsAtLevel[level] - 1
                # number of cells increase in each level up until middle level
                is_num_cells_increasing = level <= self.middle_level_idx

                should_draw_top = is_first_level or (self.is_last_cell(level, cell) and is_num_cells_increasing)
                should_draw_left_top = is_first_level or (is_first_cell and is_num_cells_increasing)
                should_draw_left_bottom = is_first_cell

                penup()

                # top edge
                # for top gate too, top edge should be skipped
                is_top_gate = level == 0 and self.is_last_cell(level, cell)

                if should_draw_top and not self.is_connected_to(level, cell, self.TOP) and not is_top_gate:
                    pendown()
                left(60)
                forward(self.sideLen)
                penup()

                # top left edge
                if should_draw_left_top and not self.is_connected_to(level, cell, self.LEFT_TOP):
                    pendown()
                left(60)
                forward(self.sideLen)
                penup()

                # bottom left edge
                if should_draw_left_bottom and not self.is_connected_to(level, cell, self.LEFT_BOTTOM):
                    pendown()
                left(60)
                forward(self.sideLen)
                penup()

                # x += self.sideLen + self.x_component
                x += 1.5 * self.sideLen  # + self.x_component
                y += self.y_component

            # if cells in the next level are more than current level
            # starting x will stay the same
            if level < self.numLevels - 1 and self.numCellsAtLevel[level] < self.numCellsAtLevel[level+1]:
                x = prev_x
                y = prev_y - 2 * self.y_component
            else:
                # otherwise, change x
                x = prev_x + 1.5 * self.sideLen
                y = prev_y - self.y_component


    def draw_hexagons(self):
        # at origin 0,0
        goto(0, 0)
        dot(10)
        # also draw a line of height y_component
        setheading(90)
        forward(self.y_component * self.numLevels)

        # these equations are reached from trial and error:
        # relative to origin, the starting point of first hexagon (bottom-left vertex)
        x = - self.sideLen * (self.numLevels - self.numCellsAtLevel[0]/2)
        y = self.y_component * (self.numLevels - self.numCellsAtLevel[0] - 1)

        for level in range(self.numLevels):
            prev_x = x
            prev_y = y

            for cell in range(self.numCellsAtLevel[level]):
                # we will draw 3 edges of each hexagon
                # because inner hexagons share boundaries with others
                # but we will draw the boundary for all the boundary hexagons
                penup()
                setheading(0)
                goto(x, y)

                # draw bottom
                pendown()
                forward(self.sideLen)

                # draw bottom right edge
                left(60)
                forward(self.sideLen)

                # draw top right edge
                left(60)
                forward(self.sideLen)

                '''
                for certain boundary cells, draw other edges too. Refer to 
                gallery/original-hexagon-for-maze-open-ends.PNG
                '''
                is_first_level = level == 0
                is_first_cell = cell == 0
                # is_last_cell = cell == self.numCellsAtLevel[level] - 1
                # number of cells increase in each level up until middle level
                is_num_cells_increasing = level <= self.middle_level_idx

                should_draw_top = is_first_level or (self.is_last_cell(level, cell) and is_num_cells_increasing)
                should_draw_left_top = is_first_level or (is_first_cell and is_num_cells_increasing)
                should_draw_left_bottom = is_first_cell

                penup()

                # top edge
                if should_draw_top:
                    pendown()
                left(60)
                forward(self.sideLen)
                penup()

                # top left edge
                if should_draw_left_top:
                    pendown()
                left(60)
                forward(self.sideLen)
                penup()

                # bottom left edge
                if should_draw_left_bottom:
                    pendown()
                left(60)
                forward(self.sideLen)
                penup()

                # x += self.sideLen + self.x_component
                x += 1.5 * self.sideLen  # + self.x_component
                y += self.y_component

            # if cells in the next level are more than current level
            # starting x will stay the same
            if level < self.numLevels - 1 and self.numCellsAtLevel[level] < self.numCellsAtLevel[level+1]:
                x = prev_x
                y = prev_y - 2 * self.y_component
            else:
                # otherwise, change x
                x = prev_x + 1.5 * self.sideLen
                y = prev_y - self.y_component


if __name__ == '__main__':
    hideturtle()
    speed(100)
    pensize(2)

    # WARNING: numLevels must be odd
    # hm = HexagonalMaze(sideLen=12, numLevels=37)
    hm = HexagonalMaze(sideLen=30, numLevels=13)

    # print("numCellsAtLevel:", hm.numCellsAtLevel)
    # print("Graph")
    # pprint.pp(hm.graph)
    # print("Total Cells", hm.totalCellsInMaze)
    # print("Total connections: ", len(hm.graph))

    hm.draw_hexagonal_maze()

    done()