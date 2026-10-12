"""Maze generation with Kruskal's algorithm and a Union-Find structure."""

import random
from typing import Generator

from .maze_utils import break_walls_imperfect, Node


class Kruskal:
    """Kruskal's algorithm for generating mazes as spanning trees."""

    @staticmethod
    def link(x: Node, y: Node) -> None:
        """Merge two disjoint sets using union by rank.

        Args:
            x: Root node of the first set.
            y: Root node of the second set.
        """
        if x.rank > y.rank:
            y.parent = x
        else:
            x.parent = y
            if x.rank == y.rank:
                y.rank += 1

    @staticmethod
    def find_set(x: Node | None) -> Node | None:
        """Return the root of the set containing a node.

        Applies path compression while walking up the tree.

        Args:
            x: Node whose set root is wanted.

        Returns:
            The root node of the set containing ``x``, or None if ``x`` is
            None.
        """
        if x is None:
            return None
        if x.parent != x:
            x.parent = Kruskal.find_set(x.parent)
        return x.parent

    @staticmethod
    def union(x: Node | None, y: Node | None) -> None:
        """Merge the sets containing two nodes.

        Does nothing if either root cannot be found.

        Args:
            x: First node.
            y: Second node.
        """
        root_x = Kruskal.find_set(x)
        root_y = Kruskal.find_set(y)
        if root_x is None or root_y is None:
            return
        Kruskal.link(root_x, root_y)

    @staticmethod
    def create_edge(
        maze: list[list[Node]], height: int, width: int
    ) -> list[tuple[Node, Node]]:
        """Build and shuffle every edge between neighboring cells.

        Args:
            maze: 2D matrix containing the maze nodes.
            height: Maze height in cells.
            width: Maze width in cells.

        Returns:
            A randomly ordered list of horizontally and vertically adjacent
            node pairs.
        """
        adjacency_list: list[tuple[Node, Node]] = []
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
        maze: list[list[Node]], height: int, width: int
    ) -> Generator[tuple[Node, Node], None, None]:
        """Generate a perfect maze (no loops, no isolated areas).

        Iterates over the shuffled edges and removes the wall between two
        cells whenever they are in different sets and neither belongs to the
        '42' logo.

        Args:
            maze: 2D matrix containing the maze nodes.
            height: Maze height in cells.
            width: Maze width in cells.

        Yields:
            The pair of nodes just connected, for step-by-step rendering.
        """
        n = 0
        adjacency_list = Kruskal.create_edge(maze, height, width)
        for t in adjacency_list:
            if Kruskal.find_set(t[0]) != Kruskal.find_set(t[1]) and not (
                t[0].fix or t[1].fix
            ):
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
                Kruskal.union(t[0], t[1])
                n += 1
                yield t

    @staticmethod
    def kruskal_imperfect(
        maze: list[list[Node]], height: int, width: int
    ) -> Generator[tuple[Node, Node] | tuple[Node], None, None]:
        """Generate an imperfect maze (with loops, for game mode).

        Builds a perfect maze first, then removes extra walls from dead
        ends to create loops.

        Args:
            maze: 2D matrix containing the maze nodes.
            height: Maze height in cells.
            width: Maze width in cells.

        Yields:
            The pair of nodes whose shared wall was just removed.
        """
        yield from Kruskal.kruskal_perfect(maze, height, width)
        max_y = len(maze)
        max_x = len(maze[0])
        yield from break_walls_imperfect(maze, max_x, max_y)
