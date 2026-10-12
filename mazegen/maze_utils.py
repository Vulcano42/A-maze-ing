"""Shared helpers for the maze generators: the Node class and wall breaking."""

import random
from typing import Generator


class Node:
    """A single cell of the maze grid.

    Attributes:
        parent: Parent in the Union-Find forest (Kruskal) or in the spanning
            tree (Prim). A node starts as its own parent.
        rank: Union-Find rank (Kruskal) or the priority key in the heap
            (Prim).
        wall: Bitmask of the closed walls: 1 = North, 2 = East, 4 = South,
            8 = West. A set bit means the wall is present.
        cords: Position in the grid as (row, column).
        fix: True if the cell belongs to the fixed '42' logo.
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialize a cell with all four walls closed.

        Args:
            x: Row index of the cell (stored as ``cords[0]``).
            y: Column index of the cell (stored as ``cords[1]``).
        """
        self.parent: Node | None = self
        self.rank = 0
        self.wall = 15
        self.cords = (x, y)
        self.fix = False


def verify(maze: list[list[Node]], max_x: int, max_y: int) -> bool:
    """Check whether any dead end can still be opened.

    A dead end is a non-logo cell with exactly three closed walls that is
    not mostly surrounded by logo cells.

    Args:
        maze: 2D matrix containing the maze nodes.
        max_x: Maze width in cells.
        max_y: Maze height in cells.

    Returns:
        True if at least one openable dead end remains, False otherwise.
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
    """Open walls of dead ends to turn a perfect maze into an imperfect one.

    Repeatedly scans the grid and, for each dead end, removes one wall
    shared with a randomly chosen non-logo neighbor, until ``verify``
    reports no more dead ends.

    Args:
        maze: 2D matrix containing the maze nodes.
        max_x: Maze width in cells.
        max_y: Maze height in cells.

    Yields:
        The pair of adjacent nodes whose shared wall was just removed.
    """
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
