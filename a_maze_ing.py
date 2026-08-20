#!/usr/bin/env python3
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    a_maze_ing.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: eguedes- <eguedes-@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/08/17 13:22:08 by eguedes-          #+#    #+#              #
#    Updated: 2026/08/17 13:22:08 by eguedes-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random
import sys
from typing import Any
from parse_config import validate_config


# mst == minimum spanning tree


class Node:
    def __init__(self, x: int, y: int) -> None:
        self.parent = self
        self.rank = 0
        self.distance = -1
        self.visited = "white"
        self.wall = 15
        self.cords = (x, y)
        self.fix = False


class Bfs():
    @staticmethod
    def short_path(
        maze: list[list[Any]],
        entry: tuple[int, int],
        exit_maze: tuple[int, int]
    ) -> list[Any]:

        start_node: set[Node] = maze[entry[0]][entry[1]]
        visited: set[set[Node]] = {start_node}

        queue: list = [(start_node, [start_node])]
        max_y: int = len(maze)
        max_x: int = len(maze[0])

        while queue:
            current, path = queue.pop(0)

            if current.cords == exit:
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


class Kruskal():
    @staticmethod
    def link(x: Node, y: Node) -> None:
        if x.rank > y.rank:
            y.parent = x
        else:
            x.parent = y
            if x.rank == y.rank:
                y.rank += 1

    @staticmethod
    def find_set(x: Node) -> Node:
        if x.parent != x:
            x.parent = Kruskal.find_set(x.parent)
        return x.parent

    @staticmethod
    def union(x: Node, y: Node) -> None:
        Kruskal.link(Kruskal.find_set(x), Kruskal.find_set(y))

    @staticmethod
    def create_edge(
        maze: list[list[Node]],
        height: int, width: int
    ) -> list[tuple[Node, Node]]:
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
    ) -> list[tuple[Node, Node]]:
        adjacency_list = Kruskal.create_edge(maze, height, width)
        mst = []
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
                mst.append((t[0], t[1]))
                Kruskal.union(t[0], t[1])
        return mst

    @staticmethod
    def kruskal_imperfect(
        maze: list[list[Node]],
        height: int, width: int
    ) -> None:
        Kruskal.kruskal_perfect(maze, height, width)
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

    @staticmethod
    def verify(maze: list[list[Any]], max_x: int, max_y: int) -> bool:
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
    def __init__(
        self,
    ) -> None:
        self.dict_graph: dict[str, Any] = {}
        self.dict_graph = validate_config()
        self.height = self.dict_graph["height"]
        self.width = self.dict_graph["width"]
        self.entry = self.dict_graph["entry"]
        self.exit_maze = self.dict_graph["exit"]
        self.seed = self.dict_graph["seed"]
        self.perfect = bool(self.dict_graph["perfect"])
        self.output_file = self.dict_graph["output_file"]
        self.maze: list[list[Node]] = []
        self.path = ""

    def genereate_maze(self) -> None:
        self.dict_graph = validate_config()
        self.maze = [
            [Node(j, i) for i in range(self.dict_graph["width"])]
            for j in range(self.dict_graph["height"])
        ]
        self.logo()
        if self.perfect:
            Kruskal.kruskal_perfect(self.maze, self.height, self.width)
        else:
            Kruskal.kruskal_imperfect(self.maze, self.height, self.width)
        path = Bfs.short_path(self.maze, self.entry, self.exit_maze)
        path_str = ""
        for i in range(len(path) - 1):
            if path[i].cords[0] > path[i + 1].cords[0]:
                path_str += "N"
            if path[i].cords[0] < path[i + 1].cords[0]:
                path_str += "S"
            if path[i].cords[1] > path[i + 1].cords[1]:
                path_str += "W"
            if path[i].cords[1] < path[i + 1].cords[1]:
                path_str += "E"
        self.path = path_str

        # print(f"{self.entry[0]},{self.entry[1]}\n{self.exit_maze[0]},{self.exit_maze[1]}")
        # print(path_str)

    def logo(self) -> None:

        mid_h = int(self.dict_graph["height"] / 2)
        mid_w = int(self.dict_graph["width"] / 2)

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

        if self.maze[self.entry[0] - 1][self.entry[1] - 1].fix:
            print("Maze entry is the same as 42 logo")
            exit(1)

        if self.maze[self.exit_maze[0] - 1][self.exit_maze[1] - 1].fix:
            print("Maze exit is the same as 42 logo")
            exit(1)

    def save_file(self) -> None:

        try:
            with open(self.output_file, "w") as file:
                for row in range(self.height):
                    for node in range(self.width):
                        file.write(f"{self.maze[row][node].wall:x}")
                    file.write("\n")
                file.write("\n")
                file.write(f"{self.entry[0]},{self.entry[1]}\n")
                file.write(f"{self.exit_maze[0]},{self.exit_maze[1]}\n")
                file.write(self.path)
            print(f"Maze succesfully save in: {self.output_file}")

        except OSError:
            print("Error while tring to save output file.")


if __name__ == "__main__":
    maze = MazeGenerator()
    maze.genereate_maze()
    maze.save_file()
    # print(f"{maze.dict_graph}")
