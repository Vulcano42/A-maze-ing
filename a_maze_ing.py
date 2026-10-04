#!/usr/bin/env python3

from typing import Any
from mazegen import MazeGenerator
from render_maze import Render
from parse_config import validate_config


def main() -> None:
    """Entry point of the script that validates configuration and
    starts rendering."""
    config: dict[str, Any] = validate_config()
    print(config)
    maze = MazeGenerator(config["height"], config["width"], config["entry"],
                         config["exit"], config["output_file"], config["seed"],
                         config["perfect"], config["algorithm"])
    render = Render(maze, config["animation"])
    render.start()
    render.init_animation()


if __name__ == "__main__":
    main()
