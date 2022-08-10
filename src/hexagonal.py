import pprint
import random
from collections import deque
from turtle import *
import math
from typing import Tuple
from color_scheme import ColorScheme


class HexagonalMaze:
    '''
    the levels of Hexagon are not horizontal. They are sort of diagonal.
    Look at media/reference-hexagon-for-maze.PNG

    middle level has the most cell
    '''

    def __init__(self, side_len, num_levels):
        self.side_len = side_len

        # ensure that levels are odd. for symmetric maze
        if num_levels % 2 == 0:
            num_levels += 1

        self.num_levels = num_levels

        self.middle_level = self.num_levels // 2
        self.num_cells_at_level = self.calc_num_cells_at_each_level()

        self.total_cells = sum(self.num_cells_at_level)

        # y component of single small hexagon. height above its center
        self.y_component = self.calc_y_comp()

        # edges counted counter clockwise start from bottom
        self.BOTTOM = 0
        self.BOTTOM_RIGHT = 1
        self.TOP_RIGHT = 2
        self.TOP = 3
        self.TOP_LEFT = 4
        self.BOTTOM_LEFT = 5

        self.clr_scheme = ColorScheme()

        self.spanning_tree = []

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

    def index_1d(self, level, cell):
        # takes the level & cell (the 2D indices) and converts them to their corresponding 1D index
        if level >= self.num_levels:
            raise Exception("level greater than maze levels")
        return sum(self.num_cells_at_level[:level]) + cell

    def index_2d(self, idx) -> Tuple[int, int]:
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

    def left_parent_idx(self, level, cell):
        # cells of first level & left side of bigger hexagon have no left parent
        if level == 0 or (cell == 0 and self.have_num_cells_been_increasing(level)):
            return None

        if self.have_num_cells_been_increasing(level):
            return self.index_1d(level - 1, cell - 1)

        # else left parent has the same index
        return self.index_1d(level - 1, cell)

    def right_parent_idx(self, level, cell):
        # cells of first level & and last cells of first levels where num cells increase have no right parent
        if level == 0 or (self.is_last_cell(level, cell) and self.have_num_cells_been_increasing(level)):
            return None

        if self.have_num_cells_been_increasing(level):
            return self.index_1d(level - 1, cell)

        return self.index_1d(level - 1, cell + 1)

    def left_cell_idx(self, level, cell):
        return self.index_1d(level, cell - 1) if cell > 0 else None

    def right_cell_idx(self, level, cell):
        if cell < self.num_cells_at_level[level] - 1:
            return self.index_1d(level, cell + 1)
        return None

    def left_child_idx(self, level, cell):
        # last level and first cell of cells after middle (inclusive) level have no left child
        if level == self.num_levels-1 or (cell == 0 and level >= self.middle_level):
            return None

        if level < self.middle_level:
            return self.index_1d(level + 1, cell)
        return self.index_1d(level + 1, cell - 1)

    def right_child_idx(self, level, cell):
        # last level and last cell of cells after middle (inclusive) level have no right child
        if level == self.num_levels - 1 or (self.is_last_cell(level, cell) and level >= self.middle_level):
            return None

        if level < self.middle_level:
            return self.index_1d(level + 1, cell + 1)
        return self.index_1d(level + 1, cell)

    def create_dfs_tree(self):
        # using DFS randomized, creates a Spanning Tree

        # 0 means not connected, 1 means connected. order of neighbours:
        # BOTTOM, RIGHT_BOTTOM, RIGHT_TOP, TOP, LEFT_TOP, LEFT_BOTTOM
        spanning_tree = [
            [0, 0, 0, 0, 0, 0] for _ in range(self.total_cells)
        ]

        # pick a random starting cell
        cell_1d = random.randint(0, self.total_cells - 1)

        visited = [cell_1d]
        stack = deque()
        stack.append(cell_1d)

        while len(visited) < self.total_cells:
            # randomly pick a neighbour of current cell and go there

            # get 2D representation of current cell
            level, cell = self.index_2d(cell_1d)

            connections = [
                self.left_parent_idx(level, cell),
                self.right_parent_idx(level, cell),
                self.left_cell_idx(level, cell),
                self.right_cell_idx(level, cell),
                self.left_child_idx(level, cell),
                self.right_child_idx(level, cell),
            ]

            valid_connections = []
            for conn in connections:
                if conn is not None and conn not in visited:
                    valid_connections.append(conn)

            if len(valid_connections) > 0:
                next_cell = random.choice(valid_connections)

                visited.append(next_cell)
                stack.append(next_cell)

                # add this connection to the graph, for both cells
                # get direction of next_cell compared to cell_1d & vice versa
                direction = self.get_neighbour_dir(cell_1d, next_cell)
                spanning_tree[cell_1d][direction] = 1

                reverse_direction = self.get_neighbour_dir(next_cell, cell_1d)
                spanning_tree[next_cell][reverse_direction] = 1

                cell_1d = next_cell
            else:
                cell_1d = stack.pop()

        return spanning_tree

    def get_neighbour_dir(self, cell1, cell2):
        # gives the direction of cell2 with respect to cell1
        # reference: media/reference-hexagon-for-maze.PNG

        c1_level, c1_idx = self.index_2d(cell1)

        # using brute force approach, because using conditionals
        # to find direction of cell2 relative cell1 is too complex
        connection_indices = {
            self.BOTTOM: self.left_child_idx(c1_level, c1_idx),
            self.BOTTOM_RIGHT: self.right_child_idx(c1_level, c1_idx),
            self.TOP_RIGHT: self.right_cell_idx(c1_level, c1_idx),
            self.TOP: self.right_parent_idx(c1_level, c1_idx),
            self.TOP_LEFT: self.left_parent_idx(c1_level, c1_idx),
            self.BOTTOM_LEFT: self.left_cell_idx(c1_level, c1_idx)
        }

        # return the direction where the cell matches the other
        for direction, idx in connection_indices.items():
            if idx == cell2:
                return direction

    def is_connected_to(self, cell_1d, direction):
        return self.spanning_tree[cell_1d][direction] == 1

    def draw_hexagonal_maze(self):
        self.spanning_tree = self.create_dfs_tree()

        # relative to origin, the starting point of first hexagon (bottom-left vertex)
        x = - self.side_len * (self.num_levels - self.num_cells_at_level[0] / 2)
        y = self.y_component * (self.num_levels - self.num_cells_at_level[0] - 1)

        for level in range(self.num_levels):
            prev_x = x
            prev_y = y

            for cell in range(self.num_cells_at_level[level]):
                # we will draw 3 edges of each hexagon
                # because inner hexagons share boundaries with others.
                # but we will draw the boundary for all the boundary hexagons
                penup()
                setheading(0)
                goto(x, y)

                self.clr_scheme.next_color(color)

                # get 1d index of cell
                cell_1d = self.index_1d(level, cell)

                # draw bottom
                # to add gate, skip first cell of last level
                is_bottom_gate = cell == 0 and level == self.num_levels - 1

                # if cell is not connected to bottom cell or it is not a gate, draw the bottom line
                # to close the connection with bottom cell
                if not self.is_connected_to(cell_1d, self.BOTTOM) and not is_bottom_gate:
                    pendown()
                forward(self.side_len)
                penup()

                # draw bottom right edge
                if not self.is_connected_to(cell_1d, self.BOTTOM_RIGHT):
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

                # draw top right edge
                if not self.is_connected_to(cell_1d, self.TOP_RIGHT):
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

                # number of cells increase in each level up until middle level
                is_num_cells_increasing = level <= self.middle_level

                should_draw_top = is_first_level or (self.is_last_cell(level, cell) and is_num_cells_increasing)
                should_draw_left_top = is_first_level or (is_first_cell and is_num_cells_increasing)
                should_draw_left_bottom = is_first_cell

                penup()

                # top edge
                # for top gate too, top edge should be skipped
                is_top_gate = level == 0 and self.is_last_cell(level, cell)

                if should_draw_top and not self.is_connected_to(cell_1d, self.TOP) and not is_top_gate:
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

                # top left edge
                if should_draw_left_top and not self.is_connected_to(cell_1d, self.TOP_LEFT):
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

                # bottom left edge
                if should_draw_left_bottom and not self.is_connected_to(cell_1d, self.BOTTOM_LEFT):
                    pendown()
                left(60)
                forward(self.side_len)
                penup()

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
        # relative to origin, the starting point of first hexagon (bottom-left vertex)
        x = - self.side_len * (self.num_levels - self.num_cells_at_level[0] / 2)
        y = self.y_component * (self.num_levels - self.num_cells_at_level[0] - 1)

        for level in range(self.num_levels):
            prev_x = x
            prev_y = y

            # each level has a unique color
            self.clr_scheme.next_color(color)

            for cell in range(self.num_cells_at_level[level]):
                # we will draw 3 edges of each hexagon
                # because inner hexagons share boundaries with others
                # but we will draw the boundary for all the boundary hexagons
                penup()
                goto(x, y)
                setheading(0)

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

                x += 1.5 * self.side_len  # + self.x_component
                y += self.y_component

            # if cells in the next level are more than current level
            # x for first cell at each level will stay the same
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
    pensize(6)

    # set full screen for canvas
    screen = Screen()
    screen.setup(width=1.0, height=1.0)

    hm = HexagonalMaze(side_len=30, num_levels=15)

    bgcolor(hm.clr_scheme.bg_color)
    color(hm.clr_scheme.drawing_color)

    hm.draw_hexagonal_maze()

    done()
