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

    def __init__(self, side_len, num_levels):
        self.side_len = side_len
        # TODO: ensure that levels are odd. for symmetric maze
        self.num_levels = num_levels

        # TODO: assumption, len(numCells) is odd
        self.middle_level = self.num_levels // 2
        self.num_cells_at_level = self.calc_num_cells_at_each_level()

        self.total_cells = sum(self.num_cells_at_level)

        # y component of single small hexagon. height above its center
        self.y_component = self.calc_y_comp()

        # edges counted counter clockwise start from bottom
        self.BOTTOM = 0
        self.RIGHT_BOTTOM = 1
        self.RIGHT_TOP = 2
        self.TOP = 3
        self.LEFT_TOP = 4
        self.LEFT_BOTTOM = 5

        self.graph = self.computeMaze()

    def calc_num_cells_at_each_level(self):
        num_cells = [0 for i in range(self.num_levels)]

        # the middle element of the maze will have cells = num_levels
        # number of cells will decrease towards for levels above and below
        # gradually, by one

        n = self.num_levels
        num_cells[self.middle_level] = n

        n -= 1
        above = self.middle_level - 1
        below = self.middle_level + 1
        while above >= 0 and below < len(num_cells):
            num_cells[above] = n
            num_cells[below] = n

            n -= 1
            above -= 1
            below += 1

        return num_cells

    def calc_y_comp(self):
        # the height of hexagon from its center. it is the same as the perpendicular
        # of a triangle with hypotenuse = side_len

        # a hexagon consists of 6 equilateral triangles
        # each have side length equal to the side length of hexagon
        # we will use those triangles' data to calculate the perpendicular through one of those triangles
        # this will give us the y comp (height of hexagon above origin, if origin was at center)
        base = self.side_len / 2
        hypotenuse = self.side_len
        perpendicular = math.sqrt(hypotenuse**2 - base**2)

        return perpendicular

    def index1dfrom2d(self, level, cell):
        # takes the level & cell (the 2D indices) and converts them to their corresponding 1D index
        if level >= self.num_levels:
            raise Exception("level greater than maze levels")
        return sum(self.num_cells_at_level[:level]) + cell

    def index2dfrom1d(self, idx) -> Tuple[int, int]:
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

    def have_num_cells_been_increasing(self, level):
        # number of cells increase up until middle level
        return level <= self.middle_level

    def is_last_cell(self, level, cell):
        return cell == self.num_cells_at_level[level] - 1

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
        if cell < self.num_cells_at_level[level] - 1:
            return self.index1dfrom2d(level, cell+1)
        return None

    def left_child_idx_1d(self, level, cell):
        # last level and first cell of cells after middle (inclusive) level have no left child
        if level == self.num_levels-1 or (cell == 0 and level >= self.middle_level):
            return None

        if level < self.middle_level:
            return self.index1dfrom2d(level + 1, cell)
        return self.index1dfrom2d(level + 1, cell-1)

    def right_child_idx_1d(self, level, cell):
        # last level and last cell of cells after middle (inclusive) level have no right child
        if level == self.num_levels - 1 or (self.is_last_cell(level, cell) and level >= self.middle_level):
            return None

        if level < self.middle_level:
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
        cell_1d = random.randint(0, self.total_cells - 1)

        visited = [cell_1d]
        stack = deque()
        stack.append(cell_1d)

        while len(visited) < self.total_cells:
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
        x = - self.side_len * (self.num_levels - self.num_cells_at_level[0] / 2)
        y = self.y_component * (self.num_levels - self.num_cells_at_level[0] - 1)

        for level in range(self.num_levels):
            prev_x = x
            prev_y = y

            for cell in range(self.num_cells_at_level[level]):
                # we will draw 3 edges of each hexagon
                # because inner hexagons share boundaries with others
                # but we will draw the boundary for all the boundary hexagons
                penup()
                setheading(0)
                goto(x, y)

                # draw bottom
                # to add gate, skip first cell of last level
                is_bottom_gate = cell == 0 and level == self.num_levels - 1
                if not self.is_connected_to(level, cell, self.BOTTOM) and not is_bottom_gate:
                    pendown()
                forward(self.side_len)
                penup()

                # draw bottom right edge
                if not self.is_connected_to(level, cell, self.RIGHT_BOTTOM):
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

                # draw top right edge
                if not self.is_connected_to(level, cell, self.RIGHT_TOP):
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

                '''
                for certain boundary cells, draw other edges too. Refer to 
                gallery/original-hexagon-for-maze-open-ends.PNG
                '''
                is_first_level = level == 0
                is_first_cell = cell == 0
                # is_last_cell = cell == self.numCellsAtLevel[level] - 1
                # number of cells increase in each level up until middle level
                is_num_cells_increasing = level <= self.middle_level

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
                forward(self.side_len)
                penup()

                # top left edge
                if should_draw_left_top and not self.is_connected_to(level, cell, self.LEFT_TOP):
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

                # bottom left edge
                if should_draw_left_bottom and not self.is_connected_to(level, cell, self.LEFT_BOTTOM):
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

                # x += self.sideLen + self.x_component
                x += 1.5 * self.side_len  # + self.x_component
                y += self.y_component

            # if cells in the next level are more than current level
            # starting x will stay the same
            if level < self.num_levels - 1 and self.num_cells_at_level[level] < self.num_cells_at_level[level + 1]:
                x = prev_x
                y = prev_y - 2 * self.y_component
            else:
                # otherwise, change x
                x = prev_x + 1.5 * self.side_len
                y = prev_y - self.y_component


    def draw_hexagons(self):
        # at origin 0,0
        goto(0, 0)
        dot(10)
        # also draw a line of height y_component
        setheading(90)
        forward(self.y_component * self.num_levels)

        # these equations are reached from trial and error:
        # relative to origin, the starting point of first hexagon (bottom-left vertex)
        x = - self.side_len * (self.num_levels - self.num_cells_at_level[0] / 2)
        y = self.y_component * (self.num_levels - self.num_cells_at_level[0] - 1)

        for level in range(self.num_levels):
            prev_x = x
            prev_y = y

            for cell in range(self.num_cells_at_level[level]):
                # we will draw 3 edges of each hexagon
                # because inner hexagons share boundaries with others
                # but we will draw the boundary for all the boundary hexagons
                penup()
                setheading(0)
                goto(x, y)

                # draw bottom
                pendown()
                forward(self.side_len)

                # draw bottom right edge
                left(60)
                forward(self.side_len)

                # draw top right edge
                left(60)
                forward(self.side_len)

                '''
                for certain boundary cells, draw other edges too. Refer to 
                gallery/original-hexagon-for-maze-open-ends.PNG
                '''
                is_first_level = level == 0
                is_first_cell = cell == 0
                # is_last_cell = cell == self.numCellsAtLevel[level] - 1
                # number of cells increase in each level up until middle level
                is_num_cells_increasing = level <= self.middle_level

                should_draw_top = is_first_level or (self.is_last_cell(level, cell) and is_num_cells_increasing)
                should_draw_left_top = is_first_level or (is_first_cell and is_num_cells_increasing)
                should_draw_left_bottom = is_first_cell

                penup()

                # top edge
                if should_draw_top:
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

                # top left edge
                if should_draw_left_top:
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

                # bottom left edge
                if should_draw_left_bottom:
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

                # x += self.sideLen + self.x_component
                x += 1.5 * self.side_len  # + self.x_component
                y += self.y_component

            # if cells in the next level are more than current level
            # starting x will stay the same
            if level < self.num_levels - 1 and self.num_cells_at_level[level] < self.num_cells_at_level[level + 1]:
                x = prev_x
                y = prev_y - 2 * self.y_component
            else:
                # otherwise, change x
                x = prev_x + 1.5 * self.side_len
                y = prev_y - self.y_component


if __name__ == '__main__':
    hideturtle()
    speed(100)
    pensize(2)
    bgcolor('#222')
    color('white')
    screen = Screen()
    screen.setup(width=1.0, height=1.0)


    # WARNING: numLevels must be odd
    # hm = HexagonalMaze(sideLen=12, numLevels=37)
    hm = HexagonalMaze(side_len=30, num_levels=13)

    # print("numCellsAtLevel:", hm.numCellsAtLevel)
    # print("Graph")
    # pprint.pp(hm.graph)
    # print("Total Cells", hm.totalCellsInMaze)
    # print("Total connections: ", len(hm.graph))

    hm.draw_hexagonal_maze()

    done()