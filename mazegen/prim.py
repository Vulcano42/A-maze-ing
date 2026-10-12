"""Maze generation with Prim's algorithm backed by a binary min-heap."""

import random
from typing import Generator, Any
from .maze_utils import break_walls_imperfect, Node


class Prim:
    """Prim's algorithm for generating mazes, with a min-heap of nodes.

    The heap is ordered by ``Node.rank``, which holds the lowest known edge
    weight connecting the node to the growing tree.
    """

    @staticmethod
    def parent(index: int) -> int:
        """Return the heap index of the parent of ``index``."""
        return int((index - 1) / 2)

    @staticmethod
    def left(index: int) -> int:
        """Return the heap index of the left child of ``index``."""
        return int(2 * index + 1)

    @staticmethod
    def right(index: int) -> int:
        """Return the heap index of the right child of ``index``."""
        return int(2 * index + 2)

    @staticmethod
    def min_heapify(heap: list[Node], index: int) -> None:
        """Restore the min-heap property for the subtree rooted at ``index``.

        Assumes both child subtrees already satisfy the property. Sinks the
        node down, swapping with its smallest child while needed.

        Args:
            heap: Heap stored as a list of nodes.
            index: Index of the subtree root to fix.
        """
        left = Prim.left(index)
        right = Prim.right(index)
        minimun = index
        if (
            left <= len(heap) - 1 and heap[left].rank < heap[index].rank
        ):
            minimun = left
        if right <= len(heap) - 1 and heap[right].rank < heap[minimun].rank:
            minimun = right
        if minimun != index:
            heap[index], heap[minimun] = heap[minimun], heap[index]
            Prim.min_heapify(heap, minimun)

    @staticmethod
    def extract_min_heap(heap: list[Node]) -> Node:
        """Remove and return the node with the smallest rank.

        Args:
            heap: Non-empty heap stored as a list of nodes.

        Returns:
            The node at the root of the heap.
        """
        heap[0], heap[len(heap) - 1] = heap[len(heap) - 1], heap[0]
        minimun = heap.pop()
        Prim.min_heapify(heap, 0)
        return minimun

    @staticmethod
    def decrease_key(heap: list[Node], node: Node, key: int) -> None:
        """Lower the rank of a node and move it up the heap.

        Does nothing if ``key`` is greater than the current rank.

        Args:
            heap: Heap stored as a list of nodes.
            node: Node whose rank will be lowered; it must be in the heap.
            key: New rank value.
        """
        if key > node.rank:
            return
        node.rank = key
        i = 0
        while heap[i] != node:
            i += 1
        while i > 0 and heap[Prim.parent(i)].rank > heap[i].rank:
            heap[Prim.parent(i)], heap[i] = heap[i], heap[Prim.parent(i)]
            i = Prim.parent(i)

    @staticmethod
    def insert_heap(heap: list[Node], node: Node) -> None:
        """Insert a node into the heap and rebuild the heap property.

        Args:
            heap: Heap stored as a list of nodes.
            node: Node to insert.
        """
        heap.append(node)
        i = int((len(heap) - 1) / 2)
        while i >= 0:
            Prim.min_heapify(heap, i)
            i -= 1

    @staticmethod
    def create_edge(maze: list[list[Node]], height: int, width: int) -> Any:
        """Build the weighted edge list between neighboring cells.

        Edges touching a '42' logo cell are skipped. Each edge receives a
        random weight between 1 and 10000.

        Args:
            maze: 2D matrix containing the maze nodes.
            height: Maze height in cells.
            width: Maze width in cells.

        Returns:
            A list of ``(node_a, node_b, weight)`` tuples.
        """
        adjacency_list: Any = []
        for i in range(height):
            for j in range(width - 1):
                if not maze[i][j].fix and not maze[i][j + 1].fix:
                    adjacency_list.append(
                        (maze[i][j], maze[i][j + 1], random.randint(1, 10000))
                    )
        for i in range(width):
            for j in range(height - 1):
                if not maze[j][i].fix and not maze[j + 1][i].fix:
                    adjacency_list.append(
                        (maze[j][i], maze[j + 1][i], random.randint(1, 10000))
                    )
        return adjacency_list

    @staticmethod
    def prim(
        maze: list[list[Node]], height: int, width: int
    ) -> Generator[tuple[Node, Node], None, None]:
        """Generate a perfect maze using Prim's algorithm.

        Builds a randomly weighted graph of the grid, starts from a random
        node and repeatedly extracts the cheapest node from the heap,
        removing the wall between it and its tree parent.

        Args:
            maze: 2D matrix containing the maze nodes.
            height: Maze height in cells.
            width: Maze width in cells.

        Yields:
            The pair ``(node, parent)`` just connected, for step-by-step
            rendering.
        """
        adjacency_list: list[tuple[Node, Node, int]] = Prim.create_edge(
            maze, height, width
        )
        heap: list[Node] = []
        graph: dict[Node, list[tuple[Node, int]]] = {
            node: [] for line in maze for node in line
        }

        for u, v, weight in adjacency_list:
            graph[u].append((v, weight))
            graph[v].append((u, weight))

        for line in maze:
            for node in line:
                node.rank = 10001
                node.parent = None

        init_node = random.choice(adjacency_list)[0]
        init_node.rank = 0
        for line in maze:
            for node in line:
                Prim.insert_heap(heap, node)

        while heap:
            minimun = Prim.extract_min_heap(heap)
            if minimun.parent is not None:
                if minimun.cords[0] > minimun.parent.cords[0]:
                    minimun.wall -= 2**0
                    minimun.parent.wall -= 2**2
                if minimun.cords[0] < minimun.parent.cords[0]:
                    minimun.wall -= 2**2
                    minimun.parent.wall -= 2**0
                if minimun.cords[1] > minimun.parent.cords[1]:
                    minimun.wall -= 2**3
                    minimun.parent.wall -= 2**1
                if minimun.cords[1] < minimun.parent.cords[1]:
                    minimun.wall -= 2**1
                    minimun.parent.wall -= 2**3
                yield (minimun, minimun.parent)

            for neighbor, weight in graph[minimun]:
                if neighbor in heap and weight < neighbor.rank:
                    neighbor.parent = minimun
                    Prim.decrease_key(heap, neighbor, weight)

    @staticmethod
    def prim_imperfect(
        maze: list[list[Node]], height: int, widht: int
    ) -> Generator[tuple[Node, Node] | tuple[Node], None, None]:
        """Generate an imperfect maze (with loops) using Prim's algorithm.

        Builds a perfect maze first, then removes extra walls from dead
        ends to create loops.

        Args:
            maze: 2D matrix containing the maze nodes.
            height: Maze height in cells.
            widht: Maze width in cells.

        Yields:
            The pair of nodes whose shared wall was just removed.
        """
        yield from Prim.prim(maze, height, widht)
        max_y = len(maze)
        max_x = len(maze[0])
        yield from break_walls_imperfect(maze, max_x, max_y)
