import random
from typing import Generator


class Node:
    """
    Represents an individual cell within the maze grid.

    Attributes:
        parent (Node): Reference to the cell itself (used in the
         Union-Find algorithm).
        rank (int): Hierarchical level of the tree (used for Union-Find
         optimization).
        wall (int): Bitmask encoding the state of the 4 walls (N, E, S, W).
        cords (tuple[int, int]): Coordinates (x, y) of the cell in the matrix.
        fix (bool): Indicates whether the cell is part of the fixed '42' logo.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a node (cell) with walls closed in all directions.

        Args:
            x (int): The x-coordinate (column) of the node.
            y (int): The y-coordinate (row) of the node.
        """
        self.parent: Node | None = self
        self.rank = 0
        self.wall = 15
        self.cords = (x, y)
        self.fix = False


def verify(maze: list[list[Node]], max_x: int, max_y: int) -> bool:
    """
    Verifies if there are still dead ends that need to be
        opened in an imperfect maze.

    Args:
        maze (list[list[Node]]): 2D matrix containing the maze nodes.
        max_x (int): Maximum width index of the maze.
        max_y (int): Maximum height index of the maze.

    Returns:
        bool: True if dead ends remain, False otherwise.
    """
    for y in range(max_y):
        for x in range(max_x):
            ft_count = 0
            ft_count += 1 if x + 1 < max_x and maze[y][x + 1].fix else 0
            ft_count += 1 if x - 1 >= 0 and maze[y][x - 1].fix else 0
            ft_count += 1 if y + 1 < max_y and maze[y + 1][x].fix else 0
            ft_count += 1 if y - 1 > 0 and maze[y - 1][x].fix else 0
            if (
                maze[y][x].wall.bit_count() == 3
                and not maze[y][x].fix
                and ft_count < 3
            ):
                return True

    return False


def break_walls_imperfect(
    maze: list[list[Node]], max_x: int, max_y: int
) -> Generator[tuple[Node, Node] | tuple[Node], None, None]:
    while verify(maze, max_x, max_y):
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
