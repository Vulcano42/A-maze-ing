#!/usr/bin/env python3

from os import truncate
from typing import Any
from mazegen import MazeGenerator
from render_maze import Render
from parse_config import validate_config
import time


def main() -> None:
    """Entry point of the script that validates configuration and starts rendering."""
    config: dict[str, Any] = validate_config()
    maze = MazeGenerator(config["height"], config["width"], config["entry"],
                         config["exit"], config["seed"],
                         config["perfect"], config["output_file"])
    render = Render(maze)
    gen = maze.generate_maze()
    render.start()
    while True:
        value = next(gen)
        print(value)
        if value == -1:
            break
        render.render_maze(render.params_r)
        # render.loop()
        print("main")
    maze.save_file()


if __name__ == "__main__":
    main()
