'''
Creates Dataset of Rectangular Mazes
(actually there are Squared)
'''
import math
import pprint

from src.algorithms.prims_randomized import PrimsRandomized
from PIL import Image, ImageDraw
import time


class GenerateRectangular:

    def __init__(self, n, side_len, wall_width):
        self.n = n
        self.side_len = side_len
        self.wall_width = wall_width

    def draw_image(self):

        # create a spanning using Prims Randomized to depict our maze
        pr = PrimsRandomized(n)
        spanning_tree = pr.prims_mst()
        # print('Spanning Tree')
        # pprint.pp(spanning_tree)

        # n boxes, each has a side length = side_len and the there are n+1 walls that enclose n boxes:
        image_width = self.n * (self.side_len + self.wall_width)
        image_height = image_width
        print('Image Dimensions:', image_width, 'x', image_height)

        maze_image = Image.new(mode='1', size=(image_width, image_height), color=(1))
        canvas = ImageDraw.Draw(maze_image)

        # center of origin for PIL is upper left corner

        # x0, y0 is the starting point of each square. it starts with 0,0
        x0 = 0
        y0 = 0

        dimension = self.side_len + self.wall_width

        for row in range(self.n):
            for col in range(self.n):
                # node index in 1D form
                node = row * self.n + col

                # pendown()

                # if node is connected to the node in TOP direction
                # do not draw the line
                if spanning_tree[node][pr.TOP] == 0:
                    # draw the top line since this node is not connected to top
                    canvas.line([(x0, y0), (x0 + dimension, y0)], width=self.wall_width)
                    canvas.arc([(x0+dimension, y0), (x0+dimension, y0)], 0, 0, width=self.wall_width)

                # if connected to the node on the right
                # or the current node is the last node, keep the right side open (for the exit gate)
                if spanning_tree[node][pr.RIGHT] == 0 and node != self.n ** 2 - 1:
                    canvas.line([(x0 + dimension, y0), (x0 + dimension, y0 + dimension)],
                                width=self.wall_width)

                if spanning_tree[node][pr.BOTTOM] == 0:
                    canvas.line([(x0 + dimension, y0 + dimension), (x0, y0 + dimension)],
                                width=self.wall_width)

                # for the first node, keep the left gate open (entrance)
                if spanning_tree[node][pr.LEFT] == 0 and node != 0:
                    canvas.line([(x0, y0 + dimension), (x0, y0)],
                                width=self.wall_width)

                # go to the position to draw next square in the current row
                x0 += dimension

            # move to the next row
            y0 += dimension
            x0 = 0

            # TODO consider wall width
        maze_image.save(f'images/{math.floor(time.time())}.png')


if __name__ == '__main__':
    n = 10
    side_len = 20
    wall_width = 10

    gr = GenerateRectangular(n, side_len, wall_width)

    gr.draw_image()

