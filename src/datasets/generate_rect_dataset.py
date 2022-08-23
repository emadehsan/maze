'''
Dataset that creates Rectangular Mazes
'''
import math
import time
from sys import argv
import argparse, sys

from hashlib import sha256
from pathlib import Path

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

from rectangular_kruskal_maze import RectangularKruskalMaze


class RectangularDataset:

    def __init__(self, row_len, side_len, num_mazes, verbose_output):
        self.n = row_len
        self.side_len = side_len
        self.num_mazes = num_mazes

        self.verbose_output = verbose_output

    def create_dataset(self):
        start_time = time.time()

        seconds = math.floor(time.time())
        cwd_path = './'
        ds_name = f'rectangular_mazes_{seconds}'

        # create a folder for this dataset in current directory
        dataset_directory = cwd_path + ds_name
        dataset_images_dir = f'{dataset_directory}/images/'
        Path(dataset_directory).mkdir(parents=True)
        Path(dataset_images_dir).mkdir()

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
                output_line = f"[info] Duplicate found for Maze#{maze_id} with Maze#{maze_hashes[key]}\n"
                output_line += f"{spanning_tree_str}\n"
                output_line += "[info] Generating again\n"
                log_file.write(output_line)

                print(output_line)
                print()
                continue

            # else this is a new maze

            # maze will be saved at this path
            maze_image_path = f'{dataset_images_dir}/{maze_id}.png'
            maze_image.save(maze_image_path)

            if self.verbose_output:
                # output_line = f'Maze created #{maze_id}, {key}\n' # no need to print hash (key)
                output_line = f'Maze created #{maze_id}\n'
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

        # return the directory of dataset
        return Path(dataset_directory).absolute()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-rows', help='Number of row (or cells per row)')
    parser.add_argument('-width', help='Wall width in pixels')
    parser.add_argument('-items', help='Dataset size (number of images to generate)')
    parser.add_argument("-verbose", action=argparse.BooleanOptionalAction, help="Verbose output")

    args = parser.parse_args()

    if args.rows is None or args.width is None or args.items is None:
        print("Please provide all optional arguments:")
        parser.print_help()
        exit(1)

    # number of cells in a single row
    num_rows = int(args.rows)
    side_length = int(args.width)
    # number of mazes to generate in the dataset
    num_items = int(args.items)
    is_verbose = True if args.verbose else False

    ds = RectangularDataset(num_rows, side_length, num_items, is_verbose)

    ds_folder = ds.create_dataset()

    print(f'Task finished. Created {num_items} Maze images {ds_folder}')

