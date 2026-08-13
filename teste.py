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
    def kruskal_perfect(maze: list[list[Node]], height: int, width: int) -> list[tuple[Node, Node]]:
        # maze = [[Node(j, i) for i in range(self.width)] for j in range(self.height)]
        adjacency_list = []
        mst = []
        for i in range(height):
            for j in range(width - 1):
                adjacency_list.append((maze[i][j], maze[i][j + 1]))
        for i in range(width):
            for j in range(height - 1):
                adjacency_list.append((maze[i][j], maze[i][j + 1]))
        random.shuffle(adjacency_list)
        for t in adjacency_list:
            if Kruskal.find_set(t[0]) != Kruskal.find_set(t[1]):
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

    def kruskal_imperfect():
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




# def parse_config(file: str) -> dict(int, int, tuplent, int):


def validate_config() -> dict[str, int | bool | str | tuple[int, int]]:
    error_msg: str = (
        "Error while reading config.text"
        "\nPlease open the file and write the values in the format:"
        "\nWIDTH=<int>"
        "\nHEIGHT=<int>"
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
                dict_raw[key] = value
    except Exception:
        print(error_msg)
        sys.exit(1)
    try:
        dict_graph["width"] = int(dict_raw["width"])
        dict_graph["height"] = int(dict_raw["height"])
        dict_graph["perfect"] = bool(dict_raw["perfect"])
        dict_graph["seed"] = int(dict_raw["seed"])
        if not dict_raw["output_file"].endswith(".txt\n"):
            dict_graph["output_file"] = dict_raw["output_file"]
            print(error_msg)
            sys.exit(1)
        entry = dict_raw["entry"].split(",")
        exit_maze = dict_raw["exit"].split(",")
        if len(entry) != 2 or len(exit_maze) != 2:
            print(error_msg)
            sys.exit(1)
        dict_graph["entry"] = (int(entry[0]), int(entry[1]))
        dict_graph["exit"] = (int(exit_maze[0]), int(entry[1]))
        for key in dict_graph.keys():
            if not (key == "widht" or "height" or "entry" or "exit"
                    or "output_file" or "perfect" or "seed"):
                print(error_msg)
                sys.exit(1)

        if len(dict_graph.keys()) != 7:
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
    maze.imprimir()
    # maze = MazeGenerator()
    #
    # height = 7
    # width = 9
