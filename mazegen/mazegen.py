#!/usr/bin/env python3
"""Maze generation core of the A-Maze-ing project.

This module provides :class:`MazeGenerator`, which manages the cell grid,
runs the selected generation algorithm (BFS, Kruskal or Prim, in perfect or
imperfect variants), stamps the central '42' logo, computes the shortest
solution with a breadth-first search (BFS), and saves the formatted result
to a text file.
"""

from .bfs import Bfs, BfsGenerator
from .kruskal import Kruskal
from .prim import Prim
from .maze_utils import Node
import random
from typing import Generator, Any


class MazeGenerator:
    """Manage the complete lifecycle of a maze: build, solve and save.

    The generator works step by step: :meth:`generate_maze` is a generator
    that yields intermediate states so a renderer can animate the
    construction, while :meth:`build` consumes it in one go.

    Attributes:
        height (int): Maze height in number of cells (rows).
        width (int): Maze width in number of cells (columns).
        entry (tuple[int, int]): Entry coordinates as (x, y).
        exit_maze (tuple[int, int]): Exit coordinates as (x, y).
        seed (int | str): Seed of the pseudo-random number generator, or
            the string "random" for a non-deterministic maze.
        perfect (bool): True for a perfect maze (exactly one path between
            any two cells), False for an imperfect one (with loops).
        output_file (str): Path of the file written by :meth:`save_file`.
        maze (list[list[Node]]): Grid of nodes, indexed as ``maze[row][col]``.
        path (list[Node]): Nodes of the shortest path from entry to exit.
        path_str (str): Solution path as a string of 'N', 'E', 'S', 'W'.
        algorithm_str (str): Name of the algorithm: "bfs", "kruskal" or
            "prim" (case-insensitive).
        algorithm (Generator[tuple[Node, Node], None, None] | None): The
            active algorithm generator, or None before generation starts.
    """

    def __init__(
        self,
        height: int,
        width: int,
        entry: tuple[int, int],
        exit_maze: tuple[int, int],
        output_file: str,
        seed: int | str = "random",
        perfect: bool = False,
        algorithm_str: str = "kruskal",
    ) -> None:
        """Initialize the generator with the maze configuration.

        No validation or generation happens here; both are deferred to
        :meth:`generate_maze`.

        Args:
            height (int): Maze height in number of cells.
            width (int): Maze width in number of cells.
            entry (tuple[int, int]): Entry coordinates (x, y).
            exit_maze (tuple[int, int]): Exit coordinates (x, y).
            output_file (str): Path of the output file; must end in '.txt'.
            seed (int | str): Seed for the random number generator, or
                "random" to leave it unseeded. Defaults to "random".
            perfect (bool): Whether the maze must be perfect. Defaults to
                False.
            algorithm_str (str): Generation algorithm: "bfs", "kruskal" or
                "prim". Defaults to "kruskal".
        """
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
        self.algorithm: Generator[tuple[Node, Node], None, None] | None = None

    def build(self) -> None:
        """Generate the whole maze in a single run.

        Consume the generator returned by :meth:`generate_maze`, discarding
        every intermediate yield. Useful when no step-by-step rendering is
        needed.

        Raises:
            ValueError: If the algorithm cannot be loaded, or if the entry
                or exit overlaps the '42' logo.
        """
        for _ in self.generate_maze():
            pass

    def select_algorithm(
        self,
    ) -> Any:
        """Return the generator for the configured algorithm and mode.

        The choice depends on ``algorithm_str`` (case-insensitive) and on
        ``perfect``. Must be called after the grid has been created.

        Returns:
            Generator: A generator that carves the maze one step at a time,
            yielding pairs of nodes. It comes from ``Prim.prim``,
            ``Prim.prim_imperfect``, ``Kruskal.kruskal_perfect``,
            ``Kruskal.kruskal_imperfect``, ``BfsGenerator.bfs_perfect`` or
            ``BfsGenerator.bfs_imperfect``.

        Raises:
            ValueError: If ``algorithm_str`` is not a supported algorithm.
        """
        if self.algorithm_str.lower() == "prim" and self.perfect:
            return Prim.prim(self.maze, self.height, self.width)
        if self.algorithm_str.lower() == "prim" and not self.perfect:
            return Prim.prim_imperfect(self.maze, self.height, self.width)
        if self.algorithm_str.lower() == "kruskal" and self.perfect:
            return Kruskal.kruskal_perfect(self.maze, self.height, self.width)
        if self.algorithm_str.lower() == "kruskal" and not self.perfect:
            return Kruskal.kruskal_imperfect(
                self.maze, self.height, self.width
            )
        if self.algorithm_str.lower() == "bfs" and self.perfect:
            return BfsGenerator.bfs_perfect(
                self.maze,
                self.entry[1],
                self.entry[0],
                self.height,
                self.width,
            )
        if self.algorithm_str.lower() == "bfs" and not self.perfect:
            return BfsGenerator.bfs_imperfect(
                self.maze,
                self.entry[1],
                self.entry[0],
                self.height,
                self.width,
            )
        raise ValueError("Invalid algorithm selected: {self.algorithm_str}")

    def generate_maze(
        self,
    ) -> Generator[tuple[Node, Node] | tuple[()], None, None]:
        """Create the grid, carve the maze and compute the solution.

        Steps performed, in order: validate the configuration, seed the
        random generator, build the node grid, stamp the '42' logo (only
        when both dimensions exceed 14), run the selected algorithm, find
        the shortest path with BFS, and convert it to ``path_str``.

        Yields:
            tuple: An empty tuple once the grid is set up (only when the
            maze was not already created), followed by the ``(Node, Node)``
            pairs produced by the algorithm at each step.

        Raises:
            ValueError: If the algorithm cannot be loaded, or if the entry
                or exit overlaps the '42' logo.
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
        algo_generator = self.select_algorithm()
        if algo_generator is None:
            raise ValueError("It is not possible to load a valid algorithm")
        self.algorithm = algo_generator
        while True:
            try:
                valor = next(algo_generator)
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
        """Mark the cells that form the '42' logo at the maze center.

        Set the ``fix`` flag on the fixed cells so that generation
        algorithms leave them untouched. Called only when the maze is
        large enough to contain the logo.

        Raises:
            ValueError: If the maze entry or exit overlaps the fixed '42'
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
        """Generate and apply a new random seed.

        Pick an integer between 0 and 100000, store it in ``seed`` and
        reseed the random number generator with it, so the next maze
        differs from the previous one.
        """
        self.seed = random.randint(0, 100000)
        random.seed(self.seed)

    def save_file(self) -> None:
        """Write the maze to ``output_file``.

        The file contains, in order: one line per maze row with each cell's
        wall bitmask as a hexadecimal digit, a blank line, the entry
        coordinates ("x,y"), the exit coordinates ("x,y") and the solution
        path string.

        Print a success message when done. An ``OSError`` is caught and
        reported with an error message instead of being propagated.
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
        """Check that every configuration attribute is valid.

        Verify the types of ``width``, ``height``, ``perfect``,
        ``output_file`` and ``algorithm_str``, that ``seed`` is an integer
        or "random", that ``output_file`` ends in '.txt', that entry and
        exit are pairs of integers within the allowed range, and that the
        algorithm is one of "bfs", "kruskal" or "prim".

        Errors are not propagated: any ``TypeError`` or ``ValueError`` is
        printed and the program is terminated.

        Raises:
            SystemExit: With status 1 when any check fails.
        """
        try:
            if not isinstance(self.width, int):
                raise TypeError("Type error: width")
            if not isinstance(self.height, int):
                raise TypeError("Type error: height")
            if not isinstance(self.perfect, bool):
                raise TypeError("Type error: perfect")
            if not isinstance(self.output_file, str):
                raise TypeError("Type error: output_file")
            if not isinstance(self.algorithm_str, str):
                raise TypeError("Type error: algorithm_str")

            if not isinstance(self.seed, (int)) and self.seed != "random":
                raise ValueError("Invalid seed")
            if not self.output_file.endswith(".txt"):
                raise ValueError("output_file incorret format")

            if not isinstance(self.entry[0], int):
                raise TypeError("Type error: entry")
            if not isinstance(self.entry[1], int):
                raise TypeError("Type error: entry")
            if not isinstance(self.exit_maze[0], int):
                raise TypeError("Type error: exit_maze")
            if not isinstance(self.exit_maze[1], int):
                raise TypeError("Type error: exit_maze")

            if len(self.entry) != 2 or len(self.exit_maze) != 2:
                raise ValueError("entry or exit invalid")

            if not (
                int(self.entry[0]) <= self.height
                and int(self.entry[1]) <= self.width
                and int(self.exit_maze[0]) <= self.height
                and int(self.exit_maze[1]) <= self.width
                and int(self.entry[0]) >= 0
                and int(self.entry[1]) >= 0
                and int(self.exit_maze[0]) >= 0
                and int(self.exit_maze[1]) >= 0
            ):
                raise ValueError("Invalid coordinates")
                exit(1)
            if self.algorithm_str.lower() not in ["bfs", "kruskal", "prim"]:
                raise ValueError("Invalid algorithm")
        except (TypeError, ValueError) as e:
            print(e)
            exit(1)
