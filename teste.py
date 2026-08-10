#!/usr/bin/env python3

# import random
import sys


class MazeGenerator:
    def __init__(self, config: dict) -> None:
        for key, value in config.items():
            setattr(self, key, value)

    def imprimir(self):
        print(self.output_file)

# def parse_config(file: str) -> dict(int, int, tuplent, int):


def validate_config() -> dict:
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
    dict_graph = {}
    try:
        with open("config.txt", "r") as f:
            for line in f:
                if line == "\n":
                    continue
                key, value = line.split("=", 1)
                key = key.lower()
                dict_graph[key] = value
    except Exception:
        print(error_msg)
        sys.exit(1)
    try:
        dict_graph["width"] = int(dict_graph["width"])
        dict_graph["height"] = int(dict_graph["height"])
        dict_graph["perfect"] = bool(dict_graph["perfect"])
        dict_graph["seed"] = int(dict_graph["seed"])
        if not dict_graph["output_file"].endswith(".txt\n"):
            print(error_msg)
            sys.exit(1)
        entry = dict_graph["entry"].split(",")
        exit_maze = dict_graph["exit"].split(",")
        if len(entry) != 2 or len(exit_maze) != 2:
            print(error_msg)
            sys.exit(1)
        entry[0], entry[1] = int(entry[0]), int(entry[1])
        exit_maze[0], exit_maze[1] = int(exit_maze[0]), int(exit_maze[1])
        dict_graph["entry"] = (entry[0], entry[1])
        dict_graph["exit"] = (exit_maze[0], exit_maze[1])
        exit_maze[0], exit_maze[1] = int(exit_maze[0]), int(exit_maze[1])
        for key in dict_graph.keys():
            if not(key == "widht" or "height" or "entry" or "exit"
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
    return(dict_graph)


if __name__ == "__main__":
    config = validate_config()
    maze = MazeGenerator(config)
    maze.imprimir()
    # maze = MazeGenerator()
    #
    # height = 7
    # width = 9
