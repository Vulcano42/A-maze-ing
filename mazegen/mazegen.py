#!/usr/bin/env python3

"""
Main module of the A-Maze-ing project.

This script is responsible for managing the cell data structure, running
the maze generation algorithms (perfect and imperfect Kruskal), calculating
the solution using breadth-first search (BFS), inserting the central '42' logo,
saving the formatted result to a file, and starting visual rendering.
"""

import random
from typing import Any, Generator


class Node:
    """
    Represents an individual cell within the maze grid.

    Attributes:
        parent (Node): Reference to the cell itself (used in the Union-Find algorithm).
        rank (int): Hierarchical level of the tree (used for Union-Find optimization).
        wall (int): Bitmask encoding the state of the 4 walls (N, E, S, W).
        cords (tuple[int, int]): Coordinates (x, y) of the cell in the matrix.
        fix (bool): Indicates whether the cell is part of the fixed '42' logo.
    """

    def __init__(self, x: int, y: int) -> None:
        """Initializes a node (cell) with walls closed in all directions."""
        self.parent = self
        self.rank = 0
        self.wall = 15
        self.cords = (x, y)
        self.fix = False


class Bfs:
    """Implements the Breadth-First Search algorithm."""

    @staticmethod
    def short_path(
        maze: list[list[Any]],
        entry: tuple[int, int],
        exit_maze: tuple[int, int]
    ) -> Any:
        """
        Calculates the shortest path between the maze entry and exit.

        Args:
            maze (list[list[Any]]): 2D matrix containing the maze nodes.
            entry (tuple[int, int]): Entry coordinates (x, y).
            exit_maze (tuple[int, int]): Exit coordinates (x, y).

        Returns:
            list: A list of ordered nodes making up the correct path.
        """
        start_node: Node = maze[entry[1]][entry[0]]
        visited: set[Node] = {start_node}

        queue: list = [(start_node, [start_node])]
        max_y: int = len(maze)
        max_x: int = len(maze[0])

        while queue:
            current, path = queue.pop(0)

            if current.cords == (exit_maze[1], exit_maze[0]):
                return path

            y, x = current.cords

            if (current.wall & 1) == 0 and y > 0:
                neighbor = maze[y - 1][x]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

            if (current.wall & 2) == 0 and x < max_x - 1:
                neighbor = maze[y][x + 1]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

            if (current.wall & 4) == 0 and y < max_y - 1:
                neighbor = maze[y + 1][x]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

            if (current.wall & 8) == 0 and x > 0:
                neighbor = maze[y][x - 1]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []


class Kruskal:
    """Implements Kruskal's algorithm for minimum spanning tree generation."""

    @staticmethod
    def link(x: Node, y: Node) -> None:
        """Unites two disjoint sets based on their ranks."""
        if x.rank > y.rank:
            y.parent = x
        else:
            x.parent = y
            if x.rank == y.rank:
                y.rank += 1

    @staticmethod
    def find_set(x: Node) -> Node:
        """Finds the root of the set to which the node belongs (with path compression)."""
        if x.parent != x:
            x.parent = Kruskal.find_set(x.parent)
        return x.parent

    @staticmethod
    def union(x: Node, y: Node) -> None:
        """Performs the union of the sets of two nodes."""
        Kruskal.link(Kruskal.find_set(x), Kruskal.find_set(y))

    @staticmethod
    def create_edge(
        maze: list[list[Node]],
        height: int, width: int
    ) -> list[tuple[Node, Node]]:
        """Generates and shuffles all possible edges between neighboring cells."""
        adjacency_list: list = []
        random.shuffle(adjacency_list)
        for i in range(height):
            for j in range(width - 1):
                adjacency_list.append((maze[i][j], maze[i][j + 1]))
        for i in range(width):
            for j in range(height - 1):
                adjacency_list.append((maze[j][i], maze[j + 1][i]))
        random.shuffle(adjacency_list)
        return adjacency_list

    @staticmethod
    def kruskal_perfect(
        maze: list[list[Node]],
        height: int, width: int
    ) -> Generator[tuple[Node, Node], None, None]:
        """Generates a perfect maze (no loops and no isolated areas)."""
        n = 0
        adjacency_list = Kruskal.create_edge(maze, height, width)
        for t in adjacency_list:
            if (Kruskal.find_set(t[0]) != Kruskal.find_set(t[1]) and not
                    (t[0].fix or t[1].fix)):
                if t[0].cords[0] > t[1].cords[0]:
                    t[0].wall = t[0].wall - 2**0
                    t[1].wall = t[1].wall - 2**2
                if t[0].cords[0] < t[1].cords[0]:
                    t[0].wall = t[0].wall - 2**2
                    t[1].wall = t[1].wall - 2**0
                if t[0].cords[1] > t[1].cords[1]:
                    t[0].wall = t[0].wall - 2**3
                    t[1].wall = t[1].wall - 2**1
                if t[0].cords[1] < t[1].cords[1]:
                    t[0].wall = t[0].wall - 2**1
                    t[1].wall = t[1].wall - 2**3
                # mst.append((t[0], t[1]))
                Kruskal.union(t[0], t[1])
                n += 1
                yield t
        # return mst

    @staticmethod
    def kruskal_imperfect(
        maze: list[list[Node]],
        height: int, width: int
    ) -> Generator[tuple[Node, Node], None, None]:
        """Generates an imperfect maze (with loops for game/Pac-Man mode)."""
        yield from Kruskal.kruskal_perfect(maze, height, width)
        max_y = len(maze)
        max_x = len(maze[0])
        while Kruskal.verify(maze, max_x, max_y):
            for y in range(max_y):
                for x in range(max_x):
                    options = []
                    if maze[y][x].wall.bit_count() == 3 and not maze[y][x].fix:
                        if (
                            maze[y][x].wall & 1 == 1
                            and y > 0
                            and y - 1 > 0
                            and not maze[y - 1][x].fix
                        ):
                            options.append(maze[y - 1][x])
                        if (
                            maze[y][x].wall & 2 == 2
                            and x < max_x - 1
                            and not maze[y][x + 1].fix
                        ):
                            options.append(maze[y][x + 1])
                        if (
                            maze[y][x].wall & 4 == 4
                            and y < max_y - 1
                            and not maze[y + 1][x].fix
                        ):
                            options.append((maze[y + 1][x]))
                        if (
                            maze[y][x].wall & 8 == 8
                            and x > 0
                            and x - 1 >= 0
                            and not maze[y][x - 1].fix
                        ):
                            options.append(maze[y][x - 1])
                        if options:
                            neighbor = random.choice(options)
                            if maze[y][x].cords[0] > neighbor.cords[0]:
                                maze[y][x].wall = maze[y][x].wall - 2**0
                                neighbor.wall = neighbor.wall - 2**2
                            if maze[y][x].cords[0] < neighbor.cords[0]:
                                maze[y][x].wall = maze[y][x].wall - 2**2
                                neighbor.wall = neighbor.wall - 2**0
                            if maze[y][x].cords[1] > neighbor.cords[1]:
                                maze[y][x].wall = maze[y][x].wall - 2**3
                                neighbor.wall = neighbor.wall - 2**1
                            if maze[y][x].cords[1] < neighbor.cords[1]:
                                maze[y][x].wall = maze[y][x].wall - 2**1
                                neighbor.wall = neighbor.wall - 2**3
                            yield (maze[y][x], neighbor)

    @staticmethod
    def verify(maze: list[list[Any]], max_x: int, max_y: int) -> bool:
        """Verifies if there are still dead ends that need to be opened."""
        for y in range(max_y):
            for x in range(max_x):
                ft_count = 0
                ft_count += 1 if x + 1 < max_x and maze[y][x + 1].fix else 0
                ft_count += 1 if x - 1 >= 0 and maze[y][x - 1].fix else 0
                ft_count += 1 if y + 1 < max_y and maze[y + 1][x].fix else 0
                ft_count += 1 if y - 1 > 0 and maze[y - 1][x].fix else 0
                if (
                    maze[y][x].wall.bit_count() == 3 and not
                    maze[y][x].fix and ft_count < 3
                ):
                    return True

        return False


class MazeGenerator:
    """
    Manages the complete lifecycle of the maze (creation, solving, and saving).

    Args:
        height (int): Maze height in number of cells.
        width (int): Maze width in number of cells.
        entry (tuple[int, int]): Entry coordinates (x, y).
        exit_maze (tuple[int, int]): Exit coordinates (x, y).
        seed (int): Seed for pseudo-random number generator initialization.
        perfect (bool): Defines whether the maze should be perfect (True) or playable (False).
        output_file (str): Path to the generated output file.

    Attributes:
        maze (list[list[Node]]): Grid containing the generated nodes.
        path (list[Any]): List of nodes forming the solution path.
        path_str (str): Textual representation of the path using 'N', 'E', 'S', 'W'.
    """

    def __init__(
        self, height: int, width: int, entry: tuple[int, int],
        exit_maze: tuple[int, int], seed: int, perfect: bool, output_file: str
    ) -> None:
        self.height = height
        self.width = width
        self.entry = entry
        self.exit_maze = exit_maze
        self.seed = seed
        self.perfect = perfect
        self.output_file = output_file
        self.maze: list[list[Node]] = []
        self.path: list[Any] = []
        self.path_str = ""

    def build(self) -> None:
        """Generate the maze ignoring yield in funcitons."""
        for _ in self.generate_maze():
            pass

    def generate_maze(self) -> Generator[tuple, None, None]:
        """Executes grid construction, logo application, Kruskal's algorithm, and BFS."""
        print(self.seed)
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
        if self.perfect:
            gen = Kruskal.kruskal_perfect(self.maze, self.height, self.width)
            while True:
                try:
                    valor = next(gen)
                    yield valor
                except StopIteration:
                    break
        else:
            # gen_perf = Kruskal.kruskal_perfect(self.maze, self.height, self.width)
            gen_imperf = Kruskal.kruskal_imperfect(self.maze, self.height, self.width)
            # while True:
            #     try:
            #         valor = next(gen_perf)
            #         print("gen =",valor)
            #         yield valor
            #     except StopIteration:
            #         # yield -1
            #         break
            while True:
                try:
                    value = next(gen_imperf)
                    yield value
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
        """Positions the '42' logo in the center of the maze if dimensions allow."""
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

    def new_seed(self):
        self.seed = random.randint(0, 100000)
        random.seed(self.seed)

    def save_file(self) -> None:
        """Writes the hexadecimal bit matrix, coordinates, and path to the output file."""
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
