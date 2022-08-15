'''
Creates Dataset of Rectangular Mazes
(actually there are Squared)
'''
import math
import pprint

from src.algorithms.prims_randomized import PrimsRandomized
from src.algorithms.kruskal_randomized_rectangular import KruskalRectangular
from PIL import Image, ImageDraw
import time


class RectangularKruskal:

    def __init__(self, n, side_len):
        self.n = n
        self.side_len = side_len

    def create_maze_image(self):

        # create a spanning using Kruskal's Randomized to depict our maze
        algo = KruskalRectangular(self.n)
        spanning_tree, edges = algo.kruskal_spanning_tree()

        '''
        the indices of grid are 0, 1, 2, ...., 2*n
        between them, the cells that correspond to cells of maze (adjacency matrix) 
        have indices: 1, 3, 5, ... 2*n - 1

        in between these cells, we will insert 'filler' cells that will
        represent the connection / edge between these cells or the walls.
        that's why those gaps (even cells) exist
        '''

        grid_len = 2 * self.n + 1

        image_width = grid_len * self.side_len
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
                if col + 1 < self.n and spanning_tree[node][algo.RIGHT] == 1:
                    canvas.rectangle([(x+side, y), (x + 2*side, y + side)], width=side, fill='white')

                # if this cell has a bottom neighbour (i.e. this cell is not in the last row)
                # and is connected to the bottom neighbour
                if row + 1 < self.n and spanning_tree[node][algo.BOTTOM] == 1:
                    canvas.rectangle([(x, y+1), (x + side, y + 2*side)], width=side, fill='white')

        # the entrance to the maze is the box in our grid at 0,side
        canvas.rectangle([(0, side), (side, 2*side)], width=side, fill='white')

        # the exit to the maze is the box in last column and 2nd last row
        x = 2 * self.n * side
        y = (2 * self.n - 1) * side
        canvas.rectangle([(x, y), (x + side, y + side)], width=side, fill='white')

        maze_image.save(f'images/{math.floor(time.time())}.png')

        # sort the edges so they could be saved as graph representation and compared to avoid duplicate trees
        # each edge has a smaller indexed node at index 0. we will sort by using that vertex, all the edge tuples
        # and this convention will be used to detect duplicates.
        edges.sort(key=lambda edg: edg[0])

        print("Edges in the Graph:")
        pprint.pp(edges)


if __name__ == '__main__':
    row_size = 10
    side_length = 20

    # number of items in dataset
    num_items = 5

    # Plan:
    #  1. number of items to generate
    #  2. duplicates check and count at each iteration with named records
    #       2.a. generation_logs_TIME will have item_id
    #       2.b. duplicates_found_TIME will have these: item_id: duplicate_spanning_tree_as_adjacency?
    #  3. dataset directory rectangular_maze_dataset_TIME:
    #       will contain csv file with the spanning_tree for each image and images labeld from 0->n-1
    #  4. Publish on Kaggle?

    gr = RectangularKruskal(row_size, side_length)

    gr.create_maze_image()

