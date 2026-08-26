#!/usr/bin/env python3

from typing import Any
from src import MazeGenerator
from render_maze import Render
from parse_config import validate_config


def main() -> None:
    """Entry point of the script that validates configuration and starts rendering."""
    config: dict[str, Any] = validate_config()
    maze = MazeGenerator(config["height"], config["width"], config["entry"],
                         config["exit"], config["seed"],
                         config["perfect"], config["output_file"])
    maze.genereate_maze()
    maze.save_file()
    render = Render(maze)
    render.start()


if __name__ == "__main__":
    main()
