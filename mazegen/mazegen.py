#!/usr/bin/env python3

"""
Main module of the A-Maze-ing project.

This script is responsible for managing the cell data structure, running
the maze generation algorithms (perfect and imperfect Kruskal), calculating
the solution using breadth-first search (BFS), inserting the central '42' logo,
saving the formatted result to a file, and starting visual rendering.
"""

from .bfs import Bfs, BfsGenerator
from .kruskal import Kruskal
from .prim import Prim
from .maze_utils import Node
import random
from typing import Generator


class MazeGenerator:
    """
    Manages the complete lifecycle of the maze (creation, solving, and saving).

    Args:
        height (int): Maze height in number of cells.
        width (int): Maze width in number of cells.
        entry (tuple[int, int]): Entry coordinates (x, y).
        exit_maze (tuple[int, int]): Exit coordinates (x, y).
        seed (int | str): Pseudo-random number generator initialization.
        perfect (bool): Defines whether the maze should be perfect (True)
            or playable/imperfect (False).
        output_file (str): Path to the generated output file.

    Attributes:
        maze (list[list[Node]]): Grid containing the generated nodes.
        path (list[Node]): List of nodes forming the solution path.
        path_str (str): Textual representation of the path 'N', 'E', 'S', 'W'.
    """

    def __init__(
        self, height: int, width: int, entry: tuple[int, int],
        exit_maze: tuple[int, int], output_file: str,
        seed: int | str = "random", perfect: bool = False, algorithm_str: str = "kruskal"
    ) -> None:
        self.height = height
        self.width = width
        self.entry = entry
        self.exit_maze = exit_maze
        self.seed = seed
        self.perfect = perfect
        self.output_file = output_file
        self.maze: list[list[Node]] = []
        self.path: list[Node] = []
        self.path_str = ""
        self.algorithm_str = algorithm_str
        self.algorithm = None

    def build(self) -> None:
        """
        Generates the maze completely in a single run.

        Consumes the generator from `generate_maze` ignoring intermediate
        yields, useful for generating the full maze without step-by-step
        visual rendering.
        """
        for _ in self.generate_maze():
            pass

    def select_algorithm(self) -> Generator[tuple[Node, Node], None, None] | None:
        if self.algorithm_str.lower() == "prim" and self.perfect:
            return Prim.prim(self.maze, self.height, self.width)
        if self.algorithm_str.lower() == "prim" and not self.perfect:
            return Prim.prim_imperfect(self.maze, self.height, self.width)
        if self.algorithm_str.lower() == "kruskal" and self.perfect:
            return Kruskal.kruskal_perfect(self.maze, self.height, self.width)
        if self.algorithm_str.lower() == "kruskal" and not self.perfect:
            return Kruskal.kruskal_imperfect(self.maze, self.height, self.width)
        if self.algorithm_str.lower() == "bfs" and self.perfect:
            return BfsGenerator.bfs_perfect(
                    self.maze, self.entry[1], self.entry[0],
                    self.height, self.width
            )
        if self.algorithm_str.lower() == "bfs" and not self.perfect:
            return BfsGenerator.bfs_imperfect(
                    self.maze, self.entry[1], self.entry[0],
                    self.height, self.width
            )

    def generate_maze(self) -> Generator[tuple, None, None]:
        """
        Executes grid construction, logo application,
         Kruskal's algorithm and BFS.

        Yields:
            tuple: Intermediate states of the maze generation for rendering.
                   Yields an empty tuple after grid setup, and node pairs
                   during Kruskal generation.
        """
        self.validate_config()
        print("seed:", self.seed)
        if not self.maze:
            if self.seed != "random":
                random.seed(self.seed)
            self.maze = [
                [Node(j, i) for i in range(self.width)]
                for j in range(self.height)
            ]
            if self.width > 14 and self.height > 14:
                self.logo()
            yield ()
        self.algorithm = self.select_algorithm()
        while True:
            try:
                valor = next(self.algorithm)
                yield valor
            except StopIteration:
                break

        self.path = Bfs.short_path(self.maze, self.entry, self.exit_maze)
        for i in range(len(self.path) - 1):
            if self.path[i].cords[0] > self.path[i + 1].cords[0]:
                self.path_str += "N"
            if self.path[i].cords[0] < self.path[i + 1].cords[0]:
                self.path_str += "S"
            if self.path[i].cords[1] > self.path[i + 1].cords[1]:
                self.path_str += "W"
            if self.path[i].cords[1] < self.path[i + 1].cords[1]:
                self.path_str += "E"

    def logo(self) -> None:
        """
        Positions the '42' logo in the center of the maze if dimensions allow.

        Raises:
            ValueError: If the maze entry or exit overlaps with the fixed '42'
             logo area.
        """
        mid_h = int(self.height / 2)
        mid_w = int(self.width / 2)

        self.maze[mid_h][mid_w - 1].fix = True
        self.maze[mid_h][mid_w - 2].fix = True
        self.maze[mid_h][mid_w - 3].fix = True
        self.maze[mid_h - 1][mid_w - 3].fix = True
        self.maze[mid_h - 2][mid_w - 3].fix = True
        self.maze[mid_h + 1][mid_w - 1].fix = True
        self.maze[mid_h + 2][mid_w - 1].fix = True
        self.maze[mid_h][mid_w + 1].fix = True
        self.maze[mid_h][mid_w + 2].fix = True
        self.maze[mid_h][mid_w + 3].fix = True
        self.maze[mid_h - 1][mid_w + 3].fix = True
        self.maze[mid_h - 2][mid_w + 3].fix = True
        self.maze[mid_h - 2][mid_w + 2].fix = True
        self.maze[mid_h - 2][mid_w + 1].fix = True
        self.maze[mid_h + 1][mid_w + 1].fix = True
        self.maze[mid_h + 2][mid_w + 1].fix = True
        self.maze[mid_h + 2][mid_w + 2].fix = True
        self.maze[mid_h + 2][mid_w + 3].fix = True

        if self.maze[self.entry[1]][self.entry[0]].fix:
            raise ValueError("Maze entry is the same as 42 logo")

        if self.maze[self.exit_maze[1]][self.exit_maze[0]].fix:
            raise ValueError("Maze exit is the same as 42 logo")

    def new_seed(self) -> None:
        """
        Generates and applies a new random seed for the maze generation.
        """
        self.seed = random.randint(0, 100000)
        random.seed(self.seed)

    def save_file(self) -> None:
        """
        Writes the hexadecimal bit matrix, coordinates, and path to the
         output file.

        Prints a success message upon completion, or an error message if an
         OSError occurs.
        """
        try:
            with open(self.output_file, "w") as file:
                for row in range(self.height):
                    for node in range(self.width):
                        file.write(f"{self.maze[row][node].wall:x}")
                    file.write("\n")
                file.write("\n")
                file.write(f"{self.entry[0]},{self.entry[1]}\n")
                file.write(f"{self.exit_maze[0]},{self.exit_maze[1]}\n")
                file.write(self.path_str)
            print(f"Maze succesfully save in: {self.output_file}")

        except OSError:
            print("Error while tring to save output file.")

    def validate_config(self) -> None:
        try:
            if not isinstance(self.width, int):
                raise Exception("Type error: width")
            if not isinstance(self.height, int):
                raise Exception("Type error: height")
            if not isinstance(self.perfect, bool):
                raise Exception("Type error: perfect")
            if not isinstance(self.output_file, str):
                raise Exception("Type error: output_file")
            if not isinstance(self.algorithm_str, str):
                raise Exception("Type error: algorithm_str")
            if not isinstance(self.seed, (int)) and self.seed != "random":
                raise Exception("Invalid seed")
            if not self.output_file.endswith(".txt"):
                raise Exception("output_file incorret format")
            if not isinstance(self.entry[0], int):
                raise Exception("Type error: entry")
            if not isinstance(self.entry[1], int):
                raise Exception("Type error: entry")
            if not isinstance(self.exit_maze[0], int):
                raise Exception("Type error: exit_maze")
            if not isinstance(self.exit_maze[1], int):
                raise Exception("Type error: exit_maze")
            if len(self.entry) != 2 or len(self.exit_maze) != 2:
                raise Exception("entry or exit invalid")
            if not (
                int(self.entry[0]) <= self.height
                and int(self.entry[1]) <= self.width
                and int(self.exit_maze[0]) <= self.height
                and int(self.exit_maze[1]) <= self.width
                and int(self.entry[0]) >= 0
                and int(self.entry[1]) >= 0
                and int(self.exit_maze[0])
                and int(self.exit_maze[1]) >= 0
            ):
                raise Exception("Invalid coordinates")
                exit(1)
            if self.algorithm_str.lower() not in ["bfs", "kruskal", "prim"]:
                raise Exception("Invalid algorithm")
        except Exception as e:
            print(e)
            exit(1)
