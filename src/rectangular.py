import math
from turtle import *
from algorithms.prims_randomized import PrimsRandomized
import time


class RectMaze:

    def __init__(self, n=10, sideLen=10):
        self.n = n
        self.sideLen = sideLen

    def create_square(self):
        side = self.sideLen * 5
        x = - side / 2
        y = side / 2

        penup()
        goto(x, y)
        pendown()

        for i in range(4):
            forward(side)
            right(90)

    def create_grid(self):

        x = - (self.n * self.sideLen) / 2
        y = - x
        penup()
        goto(x, y)

        for row in range(self.n):
            for col in range(self.n):
                pendown()

                forward(self.sideLen)
                right(90)
                forward(self.sideLen)
                right(90)
                forward(self.sideLen)
                right(90)
                forward(self.sideLen)
                right(90)
                penup()

                forward(self.sideLen)
            y -= self.sideLen
            goto(x, y)

    def create_maze(self):

        pr = PrimsRandomized(n)
        mst = pr.prims_mst()

        x = - (self.n / 2) * self.sideLen
        y = - x
        penup()
        goto(x, y)

        for row in range(self.n):
            for col in range(self.n):
                # node index in 1D form
                node = row * self.n + col

                pendown()

                # if node is connected to the node in TOP direction
                # do not draw the line
                if mst[node][pr.TOP] == 1:
                    penup()

                forward(self.sideLen)
                right(90)
                pendown()

                # if connected to the node on the right
                # or the current node is the last node, keep the right side open (for the exit gate)
                if mst[node][pr.RIGHT] == 1 or node == self.n ** 2 - 1:
                    penup()

                forward(self.sideLen)
                right(90)
                pendown()

                if mst[node][pr.BOTTOM] == 1:
                    penup()

                forward(self.sideLen)
                right(90)
                pendown()

                # for the first node, keep the left gate open (entrance)
                if mst[node][pr.LEFT] == 1 or node == 0:
                    penup()

                forward(self.sideLen)
                right(90)

                # keep the pen up while we go to the position to draw next square in line
                penup()
                forward(self.sideLen)
            y -= self.sideLen
            penup()
            goto(x, y)

    def save_screenshot(self):
        ts = getscreen()
        ts.getcanvas().postscript(file=f"gallery/{math.floor(time.time())}.eps")


if __name__ == '__main__':
    pensize(2)
    hideturtle()
    speed(0)

    n = 10
    sideLen = 15

    rm = RectMaze(n, sideLen)
    # rm.create_square()
    # rm.create_grid()
    rm.create_maze()

    done()
