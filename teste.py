#!/usr/bin/env python3

import random
import sys

class Node:
    def __init__(self) -> None:
        self.parent = self
        self.rank = 0
        self.distance = 0
        self.color = "white"
        self.wall = 15


class MazeGenerator:
    def __init__(self, config: dict) -> None:
        for key, value in config.items():
            setattr(self, key, value)
        self.maze = genereate_maze()

    def imprimir(self):
        print(self.output_file)

    def krustal(raw_maze):
        for (u, v) in ramdom.shuffle(raw_maze)


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
