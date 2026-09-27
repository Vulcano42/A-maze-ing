import random
from typing import Generator

from .maze_utils import break_walls_imperfect, Node


class Prim:
    @staticmethod
    def parent(index: int) -> int:
        return int((index - 1) / 2) # como temos o indice começa com 0 então é necessário este - 1 para corrigir problemas com indices pares pois senão este parent(2) dá errado == 1????

    @staticmethod
    def left(index: int) -> int:
        return int(2*index + 1)

    @staticmethod
    def right(index: int) -> int:
        return int(2*index + 2)

    @staticmethod
    def min_heapify(heap: list, index: int) -> None:
        left = Prim.left(index)
        right = Prim.right(index)
        min = index
        if left <= len(heap) - 1 and heap[left].rank < heap[index].rank: # tem que mudar heap[l].key ou algo parecido
            min = left
        if right <= len(heap) - 1 and heap[right].rank < heap[min].rank:
            min = right
        if min != index:
            heap[index], heap[min] = heap[min], heap[index]
            Prim.min_heapify(heap, min)

    @staticmethod
    def extract_min_heap(heap: list[Node]) -> Node:
        # if not heap:
        #     return
        heap[0], heap[len(heap) - 1] = heap[len(heap) - 1], heap[0]
        min = heap.pop()
        Prim.min_heapify(heap, 0)
        return min

    @staticmethod
    def decrease_key(heap, node, key) -> None:
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
    def insert_heap(heap, node) -> None:
        heap.append(node)
        i = int((len(heap) - 1) / 2)
        while i >= 0:
            Prim.min_heapify(heap, i)
            i -= 1

    @staticmethod
    def create_edge(
        maze: list[list[Node]],
        height: int, width: int
    ) -> list[tuple[Node, Node, int]]:
        adjacency_list: list = []
        for i in range(height):
            for j in range(width - 1):
                if not maze[i][j].fix and not maze[i][j + 1].fix:
                    adjacency_list.append((maze[i][j], maze[i][j + 1], random.randint(1, 10000)))
        for i in range(width):
            for j in range(height - 1):
                if not maze[j][i].fix and not maze[j + 1][i].fix:
                    adjacency_list.append((maze[j][i], maze[j + 1][i], random.randint(1, 10000)))
        return adjacency_list

    @staticmethod
    def prim(maze, height, width) -> Generator[tuple[Node, Node], None, None]:
        adjacency_list: list[tuple[Node, Node, int]] = Prim.create_edge(maze, height, width)
        heap: list[Node] = []
        graph: dict[Node, list[tuple[Node, int]]] = {node: [] for line in maze for node in line}

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
            min = Prim.extract_min_heap(heap)
            if min.parent is not None:
                if min.cords[0] > min.parent.cords[0]:
                    min.wall -= 2**0
                    min.parent.wall -= 2**2
                if min.cords[0] < min.parent.cords[0]:
                    min.wall -= 2**2
                    min.parent.wall -= 2**0
                if min.cords[1] > min.parent.cords[1]:
                    min.wall -= 2**3
                    min.parent.wall -= 2**1
                if min.cords[1] < min.parent.cords[1]:
                    min.wall -= 2**1
                    min.parent.wall -= 2**3
                yield (min, min.parent)

            for neighbor, weight in graph[min]:
                if neighbor in heap and weight < neighbor.rank:
                    neighbor.parent = min
                    Prim.decrease_key(heap, neighbor, weight)

    @staticmethod
    def prim_imperfect(maze, height, widht):
        yield from Prim.prim(maze, height, widht)
        max_y = len(maze)
        max_x = len(maze[0])
        yield from break_walls_imperfect(maze, max_x, max_y)
