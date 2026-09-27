import random
from typing import Generator

from .maze_utils import break_walls_imperfect, Node


class Kruskal:
    """Implements Kruskal's algorithm for minimum spanning tree generation."""

    @staticmethod
    def link(x: Node, y: Node) -> None:
        """
        Unites two disjoint sets based on their ranks.

        Args:
            x (Node): The root node of the first set.
            y (Node): The root node of the second set.
        """
        if x.rank > y.rank:
            y.parent = x
        else:
            x.parent = y
            if x.rank == y.rank:
                y.rank += 1

    @staticmethod
    def find_set(x: Node) -> Node:
        """
        Finds the root of the set to which the node belongs, applying path
         compression.

        Args:
            x (Node): The node to find the root for.

        Returns:
            Node: The root node of the set containing x.
        """
        if x.parent != x:
            x.parent = Kruskal.find_set(x.parent)
        return x.parent

    @staticmethod
    def union(x: Node, y: Node) -> None:
        """
        Performs the union of the sets containing the two specified nodes.

        Args:
            x (Node): The first node.
            y (Node): The second node.
        """
        Kruskal.link(Kruskal.find_set(x), Kruskal.find_set(y))

    @staticmethod
    def create_edge(
        maze: list[list[Node]],
        height: int, width: int
    ) -> list[tuple[Node, Node]]:
        """
        Generates and shuffles all possible edges between neighboring cells.

        Args:
            maze (list[list[Node]]): 2D matrix containing the maze nodes.
            height (int): Maze height in number of cells.
            width (int): Maze width in number of cells.

        Returns:
            list[tuple[Node, Node]]: A randomized list of adjacent node pairs.
        """
        adjacency_list: list = []
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
        """
        Generates a perfect maze (no loops and no isolated areas) using
         Kruskal's algorithm.

        Args:
            maze (list[list[Node]]): 2D matrix containing the maze nodes.
            height (int): Maze height in number of cells.
            width (int): Maze width in number of cells.

        Yields:
            tuple[Node, Node]: The current pair of nodes being connected,
             useful for step-by-step rendering.
        """
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
                Kruskal.union(t[0], t[1])
                n += 1
                yield t

    @staticmethod
    def kruskal_imperfect(
        maze: list[list[Node]],
        height: int, width: int
    ) -> Generator[tuple[Node, Node], None, None]:
        """
        Generates an imperfect maze (with loops for game/Pac-Man mode).

        First creates a perfect maze, then randomly breaks additional walls to
            create loops.

        Args:
            maze (list[list[Node]]): 2D matrix containing the maze nodes.
            height (int): Maze height in number of cells.
            width (int): Maze width in number of cells.

        Yields:
            tuple[Node, Node]: The current pair of nodes having a wall removed.
        """
        yield from Kruskal.kruskal_perfect(maze, height, width)
        max_y = len(maze)
        max_x = len(maze[0])
        yield from break_walls_imperfect(maze, max_x, max_y)
