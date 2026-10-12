"""Randomized frontier maze generation and BFS shortest-path solving."""

import random
from typing import Generator, Any
from .maze_utils import break_walls_imperfect, Node


class BfsGenerator:
    """Generate mazes with a randomized frontier expansion (Prim's variant).

    Despite the name, cells are taken from the frontier at random, not in
    queue order.
    """

    @staticmethod
    def bfs_perfect(
        maze: list[list[Node]],
        start_y: int,
        start_x: int,
        height: int,
        width: int,
    ) -> Generator[tuple[Node, Node], None, None]:
        """Generate a perfect maze one wall removal at a time.

        Starts from the center cell of the grid and repeatedly picks a
        random edge from the frontier, connecting it if the target cell is
        still unvisited.

        Args:
            maze: 2D matrix containing the maze nodes.
            start_y: Starting row. Currently unused; the center is used.
            start_x: Starting column. Currently unused; the center is used.
            height: Maze height in cells.
            width: Maze width in cells.

        Yields:
            The pair ``(current, neighbor)`` whose shared wall was removed.
        """
        start_node = maze[int(height / 2)][int(width / 2)]
        visited: set[Node] = {start_node}
        frontier: list[tuple[Node, Node]] = []
        generate_edges: list[tuple[Node, Node]] = []

        BfsGenerator._add_unvisited_neighbors(
            start_node, maze, visited, frontier, height, width
        )

        while frontier:

            current, neighbor = frontier.pop(random.randrange(len(frontier)))

            if neighbor in visited:
                continue

            visited.add(neighbor)
            BfsGenerator._break_wall(current, neighbor)
            yield (current, neighbor)
            generate_edges.append((current, neighbor))
            BfsGenerator._add_unvisited_neighbors(
                neighbor, maze, visited, frontier, height, width
            )

    @staticmethod
    def _add_unvisited_neighbors(
        node: Node,
        maze: list[list[Node]],
        visited: set[Node],
        frontier: list[tuple[Node, Node]],
        max_y: int,
        max_x: int,
    ) -> None:
        """Add the unvisited neighbors of a node to the frontier.

        Neighbors that belong to the fixed '42' logo are ignored.

        Args:
            node: Cell whose neighbors are examined.
            maze: 2D matrix containing the maze nodes.
            visited: Cells already part of the maze.
            frontier: List of ``(from_node, to_node)`` edges, updated in
                place.
            max_y: Maze height in cells.
            max_x: Maze width in cells.
        """
        y, x = node.cords

        if y > 0 and maze[y - 1][x] not in visited and not maze[y - 1][x].fix:
            frontier.append((node, maze[y - 1][x]))

        if (
            y < max_y - 1
            and maze[y + 1][x] not in visited
            and not maze[y + 1][x].fix
        ):
            frontier.append((node, maze[y + 1][x]))

        if x > 0 and maze[y][x - 1] not in visited and not maze[y][x - 1].fix:
            frontier.append((node, maze[y][x - 1]))

        if (
            x < max_x - 1
            and maze[y][x + 1] not in visited
            and not maze[y][x + 1].fix
        ):
            frontier.append((node, maze[y][x + 1]))

    @staticmethod
    def _break_wall(n1: Node, n2: Node) -> None:
        """Remove the wall shared by two adjacent nodes.

        Clears the matching bit in each node's wall bitmask.

        Args:
            n1: First node.
            n2: Node adjacent to ``n1``.
        """
        y1, x1 = n1.cords
        y2, x2 = n2.cords

        if y1 > y2:
            n1.wall -= 2**0
            n2.wall -= 2**2
        elif y1 < y2:
            n1.wall -= 2**2
            n2.wall -= 2**0

        if x1 > x2:
            n1.wall -= 2**3
            n2.wall -= 2**1
        elif x1 < x2:
            n1.wall -= 2**1
            n2.wall -= 2**3

    @staticmethod
    def bfs_imperfect(
        maze: list[list[Node]],
        start_y: int,
        start_x: int,
        height: int,
        width: int,
    ) -> Generator[tuple[Node, Node] | tuple[Node], None, None]:
        """Generate an imperfect maze (with loops).

        Builds a perfect maze first, then removes extra walls from dead
        ends to create loops.

        Args:
            maze: 2D matrix containing the maze nodes.
            start_y: Starting row, forwarded to ``bfs_perfect``.
            start_x: Starting column, forwarded to ``bfs_perfect``.
            height: Maze height in cells.
            width: Maze width in cells.

        Yields:
            The pair of nodes whose shared wall was just removed.
        """
        yield from BfsGenerator.bfs_perfect(
            maze, start_y, start_x, height, width
        )
        max_y = len(maze)
        max_x = len(maze[0])
        yield from break_walls_imperfect(maze, max_x, max_y)


class Bfs:
    """Breadth-First Search solver for finding the shortest maze path."""

    @staticmethod
    def short_path(
        maze: list[list[Node]],
        entry: tuple[int, int],
        exit_maze: tuple[int, int],
    ) -> Any:
        """Find the shortest path between the maze entry and exit.

        Args:
            maze: 2D matrix containing the maze nodes.
            entry: Entry coordinates as (x, y), i.e. (column, row).
            exit_maze: Exit coordinates as (x, y), i.e. (column, row).

        Returns:
            The ordered list of nodes from entry to exit, or an empty list
            if no path exists.
        """
        start_node: Node = maze[entry[1]][entry[0]]
        visited: set[Node] = {start_node}

        queue: list[tuple[Node, list[Node]]] = [(start_node, [start_node])]
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
