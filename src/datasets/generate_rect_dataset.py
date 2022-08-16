'''
Dataset that creates Rectangular Mazes
'''
import math
import time
from sys import argv

from hashlib import sha256
from pathlib import Path

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

from rectangular_kruskal_maze import RectangularKruskalMaze


class RectangularDataset:

    def __init__(self, row_len, side_len, num_mazes):
        self.n = row_len
        self.side_len = side_len
        self.num_mazes = num_mazes

    def create_dataset(self):
        start_time = time.time()

        seconds = math.floor(time.time())
        cwd_path = './'
        ds_name = f'rectangular_mazes_{seconds}'

        # create a folder for this dataset in current directory
        dataset_directory = cwd_path + ds_name
        Path(dataset_directory).mkdir(parents=True)

        # add logs.txt
        log_file_name = f'{dataset_directory}/logs.txt'
        log_file = open(log_file_name, 'a')

        # add spanning_trees.txt to record a spanning tree per line for every maze
        tree_file_name = f'{dataset_directory}/spanning_tree.txt'
        tree_file = open(tree_file_name, 'a')

        # a map whose key is a hash of a Maze's spanning tree and value is its maze_id
        # helpful in checking duplicates
        maze_hashes = {}

        # 0 <-> n-1
        maze_id = 0

        mazes_remaining = self.num_mazes

        generator = RectangularKruskalMaze(self.n, self.side_len)

        while mazes_remaining > 0:
            edges, maze_image = generator.create_maze_image()

            spanning_tree_str = str(edges)

            # check if a maze with similar structure was already created
            # edges follow a convention and are sorted. create a hash and use hash checking
            # for faster checking for duplicates
            key = sha256(spanning_tree_str.encode()).hexdigest()
            value = maze_id

            if key in maze_hashes:
                output_line = f"Duplicate found for Maze#{maze_id} with Maze#{maze_hashes[key]}\n"
                output_line += f"{spanning_tree_str}\n"
                output_line += "Generating again\n"
                log_file.write(output_line)

                print(output_line)
                print()
                continue

            # else this is a new maze

            # maze will be saved at this path
            maze_image_path = f'{dataset_directory}/{maze_id}.png'
            maze_image.save(maze_image_path)

            output_line = f'Maze created #{maze_id}, {key}\n'
            log_file.write(output_line)
            print(output_line, end='')

            maze_hashes[key] = maze_id
            tree_file.write(f'{maze_id}: {spanning_tree_str}\n')

            maze_id += 1
            mazes_remaining -= 1

        output_line = f'\nTime Taken: {time.time() - start_time} seconds'
        log_file.write(output_line)
        print(output_line)

        log_file.close()
        tree_file.close()


if __name__ == '__main__':
    # number of cells in a single row
    num_cells_in_row = 10
    side_length = 10

    # number of mazes to generate in the dataset
    num_items = 5

    ds = RectangularDataset(num_cells_in_row, side_length, num_items)

    ds.create_dataset()

    print('Task finished.')

    # if len(argv) == 4:
    #     num_cells_in_row = int(argv[1])
    #     side_length = int(argv[2])
    #     num_items = int(argv[3])
    #     ds = RectangularDataset(num_cells_in_row, side_length, num_items)
    #
    #     ds.create_dataset()
    #
    #     print('Task finished.')
    #
    # else:
    #     print('Usage:')
    #     print('python generate_rect_dataset.py NUM_CELLS CELL_SIDE_LEN NUM_MAZES')
