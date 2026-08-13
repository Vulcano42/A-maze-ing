#!/usr/bin/env python3

# from abc import ABC, abstractmethod
import random
import sys

# height == números de linhas
# widht == número de colunas
# mst == minimum spanning tree


class Node:
    def __init__(self, x, y) -> None:
        self.parent = self
        self.rank = 0
        self.distance = 0
        self.color = "white"
        self.wall = 15
        self.cords = (x, y)
        self.fix = False




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
    def create_edge(maze: list[list[Node]], height: int, width: int) -> list[tuple[Node, Node]]:
        adjacency_list = []
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
    def kruskal_perfect(maze: list[list[Node]], height: int, width: int) -> list[tuple[Node, Node]]:
        # maze = [[Node(j, i) for i in range(self.width)] for j in range(self.height)]
        adjacency_list = Kruskal.create_edge(maze, height, width)
        mst = []
        for t in adjacency_list:
            if (Kruskal.find_set(t[0]) != Kruskal.find_set(t[1])
                and not (t[0].fix or t[1].fix)):
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

    # def kruskal_imperfect():
        # Em teoria é criamos uma mst, e depois tendo a mst iteramos ela para buscar celulas celulas
        # com 3 paredes e selecionar uma parede de forma aleatorio e eliminar ela, mas existem limitações
        # como não podemos criar 3x3 area aberta e não pode retirar os cantos do labirinto


class MazeGenerator:
    def __init__(self, config: dict) -> None:
        for key, value in config.items():
            setattr(self, key, value)
        self.maze: list[list[Node]] = []

    # def imprimir(self):
    #     print(self.output_file)
    def genereate_maze(self):
        self.maze = [[Node(j, i) for i in range(self.width)] for j in range(self.height)]
        self.maze[9][1].wall = 0
        self.logo()
        # mst = Kruskal.kruskal_perfect(self.maze, self.height, self.width)
        # print(maze)
        # for i in range(self.height):
        #     for j in range(self.width):
        #         print(self.maze[i][j].wall, end=" ")
        #     print()
        # # print(mst)
        #
        # print("--------------")
        for i in range(self.height):
            for j in range(self.width):
                print(f"{self.maze[i][j].wall:x}", end=" ")
            print()

    def logo(self) -> None:
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

        self.maze[mid_h][mid_w - 1].wall = 0
        self.maze[mid_h][mid_w - 2].wall = 0
        self.maze[mid_h][mid_w - 3].wall = 0
        self.maze[mid_h - 1][mid_w - 3].wall = 0
        self.maze[mid_h - 2][mid_w - 3].wall = 0
        self.maze[mid_h + 1][mid_w - 1].wall = 0
        self.maze[mid_h + 2][mid_w - 1].wall = 0
        self.maze[mid_h][mid_w + 1].wall = 0
        self.maze[mid_h][mid_w + 2].wall = 0
        self.maze[mid_h][mid_w + 3].wall = 0
        self.maze[mid_h - 1][mid_w + 3].wall = 0
        self.maze[mid_h - 2][mid_w + 3].wall = 0
        self.maze[mid_h - 2][mid_w + 2].wall = 0
        self.maze[mid_h - 2][mid_w + 1].wall = 0
        self.maze[mid_h + 1][mid_w + 1].wall = 0
        self.maze[mid_h + 2][mid_w + 1].wall = 0
        self.maze[mid_h + 2][mid_w + 2].wall = 0
        self.maze[mid_h + 2][mid_w + 3].wall = 0




# def parse_config(file: str) -> dict(int, int, tuplent, int):


def validate_config() -> dict[str, int | bool | str | tuple[int, int]]:
    error_msg: str = (
        "Error while reading config.text"
        "\nPlease open the file and write the values in the format:"
        "\nWIDTH=<int>0>"
        "\nHEIGHT=<int>0>"
        "\nENTRY=<int,int>"
        "\nEXIT=<int,int>"
        "\nOUTPUT_FILE=<*.txt>"
        "\nPERFECT=<bool>"
        "\nSEED=<int>"
    )
    dict_raw: dict[str, str] = {}
    dict_graph: dict[str, int | bool | str | tuple[int, int]] = {}
    try:
        with open("config.txt", "r") as f:
            for line in f:
                if line == "\n":
                    continue
                key, value = line.split("=", 1)
                key = key.lower()
                value = value.strip()
                dict_raw[key] = value
    except Exception:
        print(error_msg)
        sys.exit(1)
    try:
        dict_graph["width"] = int(dict_raw["width"])
        dict_graph["height"] = int(dict_raw["height"])
        dict_graph["perfect"] = bool(dict_raw["perfect"])
        dict_graph["seed"] = int(dict_raw["seed"])
        dict_graph["output_file"] = dict_raw["output_file"]
        if not dict_raw["output_file"].endswith(".txt"):
            print(error_msg)
            sys.exit(1)
        entry = dict_raw["entry"].split(",")
        exit_maze = dict_raw["exit"].split(",")
        if len(entry) != 2 or len(exit_maze) != 2:
            print(error_msg)
            sys.exit(1)
        dict_graph["entry"] = (int(entry[0]), int(entry[1]))
        dict_graph["exit"] = (int(exit_maze[0]), int(entry[1]))
        if not (
            int(entry[0]) <= dict_graph["height"]
            and int(entry[1]) <= dict_graph["width"]
            and int(exit_maze[0]) <= dict_graph["height"]
            and int(exit_maze[1]) <= dict_graph["width"]
            and int(entry[0]) >= 0
            and int(entry[1]) >= 0
            and int(exit_maze[0])
            and int(exit_maze[1]) >= 0
        ):
            print(error_msg)
            sys.exit(1)
        for key in dict_graph.keys():
            if not (key == "widht" or "height" or "entry" or "exit"
                    or "output_file" or "perfect" or "seed"):
                print(error_msg)
                sys.exit(1)

        if len(dict_graph.keys()) != 7:
            print(dict_graph)
            print("mais de 7")
            print(error_msg)
            sys.exit(1)
    except Exception:
        print(error_msg)
        sys.exit(1)
    return (dict_graph)


if __name__ == "__main__":
    config = validate_config()
    maze = MazeGenerator(config)
    maze.genereate_maze()
    # maze = MazeGenerator()
    #
    # height = 7
    # width = 9
