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

    def __init__(self, n, side_len):
        self.n = n
        self.side_len = side_len

    def create_maze_image(self):

        # create a spanning using Prims Randomized to depict our maze
        pr = PrimsRandomized(n)
        spanning_tree = pr.prims_mst()
        # print('Spanning Tree')
        # pprint.pp(spanning_tree)

        '''
        the indices of grid are 0, 1, 2, ...., 2*n
        between them, the cells that correspond to cells of maze (adjacency matrix) 
        have indices: 1, 3, 5, ... 2*n - 1

        in between these cells, we will insert 'filler' cells that will
        represent the connection / edge between these cells or the walls.
        that's why those gaps (even cells) exist
        '''

        grid_size = 2 * self.n + 1

        image_width = grid_size * self.side_len
        image_height = image_width
        print('Image Dimensions:', image_width, 'x', image_height)

        maze_image = Image.new(mode='1', size=(image_width, image_height), color=(0))
        canvas = ImageDraw.Draw(maze_image)

        # center of origin for PIL is upper left corner

        # length of the side of a box / square / cell. for easier access
        side = self.side_len

        # the image is black. just draw white boxes where the cells appear
        # or where a connection between two connected cell appears.
        # we only need to draw the right and bottom connection for the current cell.
        for row in range(self.n):
            for col in range(self.n):

                x = (2 * col + 1) * side
                y = (2 * row + 1) * side

                # draw this cell
                canvas.rectangle([(x, y), (x+side, y+side)], width=side, fill='white')

                # cell index in 1D form
                node = row * self.n + col

                # draw connections too (each cell checks right & bottom connections)

                # if the node has a right neighbour and is connected to it
                if col + 1 < self.n and spanning_tree[node][pr.RIGHT] == 1:
                    canvas.rectangle([(x+side, y), (x + 2*side, y + side)], width=side, fill='white')

                # if this cell has a bottom neighbour (i.e. this cell is not in the last row)
                # and is connected to the bottom neighbour
                if row + 1 < self.n and spanning_tree[node][pr.BOTTOM] == 1:
                    canvas.rectangle([(x, y+1), (x + side, y + 2*side)], width=side, fill='white')

        # the entrance to the maze is the box in our grid at 0,side
        canvas.rectangle([(0, side), (side, 2*side)], width=side, fill='white')

        # the exit to the maze is the box in last column and 2nd last row
        x = 2 * n * side
        y = (2 * n - 1) * side
        canvas.rectangle([(x, y), (x + side, y +side)], width=side, fill='white')

        maze_image.save(f'images/{math.floor(time.time())}.png')


if __name__ == '__main__':
    n = 10
    side_len = 20

    # number of items in dataset
    num_items = 5

    gr = GenerateRectangular(n, side_len)

    gr.create_maze_image()

