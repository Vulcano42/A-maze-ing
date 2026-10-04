import random
from typing import Generator

from .maze_utils import break_walls_imperfect, Node



class BfsGenerator:
    """Generates perfect mazes utilizing Randomized Breadth-First Search (Prim's variant)."""

    @staticmethod
    def bfs_perfect(
        maze: list[list[Node]],
        start_y: int,
        start_x: int,
        height: int,
        width: int
    ) -> Generator[tuple[Node, Node]]:
        """
        Executes the maze generation step-by-step.

        Args:
            maze (List[List[Node]]): 2D matrix containing the maze nodes.
            start_y (int): Starting y-coordinate.
            start_x (int): Starting x-coordinate.
            max_y (int): Maze height boundary.
            width (int): Maze width boundary.

        Yields:
            Tuple[Node, Node]: The current pair of nodes having a wall removed.
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
        max_x: int
    ) -> None:
        """
        Finds valid unvisited neighbors and adds them to the expansion frontier,
        respecting fixed boundaries like logos.
        """
        y, x = node.cords

        if y > 0 and maze[y - 1][x] not in visited and not maze[y - 1][x].fix:
            frontier.append((node, maze[y - 1][x]))

        if y < max_y - 1 and maze[y + 1][x] not in visited and not maze[y + 1][x].fix:
            frontier.append((node, maze[y + 1][x]))

        if x > 0 and maze[y][x - 1] not in visited and not maze[y][x - 1].fix:
            frontier.append((node, maze[y][x - 1]))

        if x < max_x - 1 and maze[y][x + 1] not in visited and not maze[y][x + 1].fix:
            frontier.append((node, maze[y][x + 1]))

    @staticmethod
    def _break_wall(n1: Node, n2: Node) -> None:
        """
        Removes the shared wall between two adjacent nodes using arithmetic operations.
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
        width: int
    ) -> Generator[tuple[Node, Node]]:
        yield from BfsGenerator.bfs_perfect(
                    maze, start_y, start_x,
                    height, width
            )
        max_y = len(maze)
        max_x = len(maze[0])
        yield from break_walls_imperfect(maze, max_x, max_y)


class Bfs:
    """Implements the Breadth-First Search algorithm."""

    @staticmethod
    def short_path(
        maze: list[list[Node]],
        entry: tuple[int, int],
        exit_maze: tuple[int, int]
    ) -> list[Node]:
        """
        Calculates the shortest path between the maze entry and exit.

        Args:
            maze (list[list[Node]]): 2D matrix containing the maze nodes.
            entry (tuple[int, int]): Entry coordinates (x, y).
            exit_maze (tuple[int, int]): Exit coordinates (x, y).

        Returns:
            list: A list of ordered nodes making up the shortest path from
             entry to exit. Returns an empty list if no path is found.
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
