'''
code used for animation to explain the triangular pattern and graph
in the Triangular Maze video
'''

import pprint
from turtle import *
import math
import time
from src.color_scheme import ColorScheme


class TriangularAnimation:

    def __init__(self, side_len, num_levels):
        self.side_len = side_len
        self.num_levels = num_levels

        self.total_cells = int(num_levels * (num_levels + 1) / 2)

        self.triangle_height = self._compute_triangle_height()

        self.clr_scheme = ColorScheme()

        # key = level, value = list of tuples containing coordinates of centers of triangles
        self.node_coordinates = {
            lvl: [] for lvl in range(num_levels)
        }


    def _compute_triangle_height(self):
        # apply Pythagoras theorem
        base = self.side_len/2
        hypotenuse = self.side_len
        perpendicular = math.sqrt(hypotenuse**2 - base**2)
        return perpendicular

    def draw_triangle(self):
        setheading(0)

        for _ in range(3):
            forward(self.side_len)
            left(120)

    def draw_triangle_stack(self, ps=8, erase=False):
        pensize(ps)

        total_height = self.num_levels * self.triangle_height
        y = total_height / 2

        for lvl in range(self.num_levels):
            # number of triangles on this level
            num_triangles = lvl + 1

            x = - self.side_len * num_triangles / 2

            # all triangles on same level have same color
            self.clr_scheme.next_color(color)
            if erase:
                color('white')

            # draw all triangles on this level
            for n in range(num_triangles):
                penup()
                goto(x, y)
                pendown()

                self.draw_triangle()
                x += self.side_len

            y -= self.triangle_height

    def undo_triangles(self, ps):
        self.draw_triangle_stack(erase=True, ps=ps)

    # draws the nodes at the center of triangles
    def draw_nodes(self, ps):
        pensize(ps)

        total_height = self.num_levels * self.triangle_height

        # the y position first node is at the center of first triangle
        y = total_height / 2 + self.triangle_height / 2

        for lvl in range(self.num_levels):
            # number of triangles on this level
            # the number of triangles that actually appear at each level is 2*n+1 . but we only draw n+1
            # the middle triangle appears automatically due to surrounding walls
            num_triangles = 2 * lvl + 1

            x = - self.side_len * (lvl+1) / 2 + self.side_len / 2

            # draw all triangles on this level
            for n in range(num_triangles):
                penup()
                goto(x, y)
                pendown()

                # keep record of node / triangle centers for current level
                self.node_coordinates[lvl].append((x, y))

                self.clr_scheme.next_color(color)
                dot(14)

                x += self.side_len / 2

            y -= self.triangle_height

    def draw_edges_between_nodes(self, ps):
        pensize(ps)
        # indexing starts with 0
        # 1. every even numbered node is connected directly downward
        #   except last level by triangle_height lengthed edge
        # 2. every node is connected to its right node node by side_len/2 except last node of the level

        for lvl in self.node_coordinates.keys():

            num_triangles = len(self.node_coordinates[lvl])
            # for all triangle centers on current level
            for i in range(num_triangles):
                x, y = self.node_coordinates[lvl][i]

                penup()
                goto(x, y)

                # only draw downward connection for even indexed triangles before last level
                # because those triangles have their base connected to triangles below them
                if i % 2 == 0 and lvl < self.num_levels - 1:
                    # draw vertical line downwards of size triangle_height
                    setheading(-90)
                    pendown()
                    self.clr_scheme.next_color(color)
                    forward(self.triangle_height)
                    penup()

                if i < num_triangles - 1:
                    # draw line towards right of size side_len / 2
                    setheading(0)
                    goto(x, y)
                    pendown()
                    self.clr_scheme.next_color(color)
                    forward(self.side_len/2)
                    penup()


if __name__ == '__main__':
    hideturtle()
    # pensize
    ps = 8
    speed(5)

    # set full screen for canvas
    screen = Screen()
    screen.setup(width=1.0, height=1.0)

    side_len = 100
    num_levels = 4

    time.sleep(3)

    TA = TriangularAnimation(side_len, num_levels)
    TA.draw_triangle_stack(ps)

    TA.draw_nodes(ps)

    # draw edges a little thinner
    TA.draw_edges_between_nodes(ps=4)

    time.sleep(1)

    TA.undo_triangles(ps)

    # draw edges again to fix eraser effect
    TA.draw_edges_between_nodes(ps=4)

    # TA.draw_triangle_stack()

    # TODO
    # 1. find Spanning Tree through some algorithm
    # 2. draw spanning tree (remove all edges and then draw only ST edges)
    # 3. draw triangles on top
    # 4. now remove THOSE lines of triangles that intersect with edges of ST

    done()
