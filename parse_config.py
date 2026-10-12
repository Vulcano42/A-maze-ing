"""Configuration file parsing and validation for the A-Maze-ing project.

The configuration file is made of ``KEY=VALUE`` lines (blank lines and lines
starting with '#' are ignored). This module reads it into a dictionary of raw
strings, then validates and converts each value with a dedicated ``v_*``
function that fills a dictionary of typed values.

Every validation helper reports problems by printing a message and calling
:func:`print_error`, which terminates the program with exit status 1.
"""

import sys
import random
from typing import Any


def print_error() -> None:
    """Print the expected configuration format and exit.

    Raises:
        SystemExit: Always, with status 1.
    """

    error_msg: str = (
        "Error while reading config.txt"
        "\nPlease open the file and write the values in the format:"
        "\nWIDTH=<int>0>"
        "\nHEIGHT=<int>0>"
        "\nENTRY=<int,int>"
        "\nEXIT=<int,int>"
        "\nOUTPUT_FILE=<*.txt>"
        "\nPERFECT=<bool>"
        "\nSEED=<int> or leave it blank"
    )

    print(error_msg)
    exit(1)


def v_width(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:
    """Validate the 'width' value and store it as an integer.

    Args:
        dict_raw (dict[str, str]): Raw key/value pairs read from the file.
        dict_graph (dict[str, Any]): Validated configuration; receives the
            key "width" (int between 1 and 500).

    Raises:
        SystemExit: If the value is missing, not an integer, or outside the
            range 1 to 500.
    """

    try:
        dict_graph["width"] = int(dict_raw["width"])
        if dict_graph["width"] < 1 or dict_graph["width"] > 500:
            print("'Width' should be between 1 and 500")
            print_error()
    except (ValueError, TypeError, KeyError):
        print("'Width' should be between 1 and 500")
        print_error()


def v_height(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:
    """Validate the 'height' value and store it as an integer.

    Args:
        dict_raw (dict[str, str]): Raw key/value pairs read from the file.
        dict_graph (dict[str, Any]): Validated configuration; receives the
            key "height" (int between 1 and 500).

    Raises:
        SystemExit: If the value is missing, not an integer, or outside the
            range 1 to 500.
    """

    try:
        dict_graph["height"] = int(dict_raw["height"])
        if dict_graph["height"] < 1 or dict_graph["height"] > 500:
            print("'Height' should be between 1 and 500")
            print_error()
    except (ValueError, TypeError, KeyError):
        print("'Height' should be between 1 and 500")
        print_error()


def v_perfect(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:
    """Validate the 'perfect' value and store it as a boolean.

    An empty or missing value defaults to True. Matching is
    case-insensitive.

    Args:
        dict_raw (dict[str, str]): Raw key/value pairs read from the file.
        dict_graph (dict[str, Any]): Validated configuration; receives the
            key "perfect" (bool).

    Raises:
        SystemExit: If the value is neither 'true' nor 'false'.
    """

    raw_perfect: str = dict_raw.get("perfect", "").strip()

    if not raw_perfect:
        dict_graph["perfect"] = True
        return

    if raw_perfect.lower() == "true":
        dict_graph["perfect"] = True
    elif raw_perfect.lower() == "false":
        dict_graph["perfect"] = False
    else:
        print("'Perfect' value should be 'True' or 'False'")
        print_error()


def v_output_file(
    dict_raw: dict[str, str], dict_graph: dict[str, Any]
) -> None:
    """Validate the 'output_file' value and store it as a string.

    Args:
        dict_raw (dict[str, str]): Raw key/value pairs read from the file.
        dict_graph (dict[str, Any]): Validated configuration; receives the
            key "output_file" (str ending in '.txt').

    Raises:
        SystemExit: If the value is missing or does not end in '.txt'.
    """

    try:
        dict_graph["output_file"] = str(dict_raw["output_file"])
    except (ValueError, TypeError, KeyError):
        print("'Output_file' should be a sting terminated with '.txt.'")
        print_error()

    if not dict_graph["output_file"].endswith(".txt"):
        print("'Output_file' should be a sting terminated with '.txt.'")
        print_error()


def v_seed(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:
    """Validate the 'seed' value and seed the random number generator.

    An empty or missing value stores the string "random" and leaves the
    generator unseeded. Otherwise the integer is stored and also passed to
    ``random.seed``.

    Args:
        dict_raw (dict[str, str]): Raw key/value pairs read from the file.
        dict_graph (dict[str, Any]): Validated configuration; receives the
            key "seed" (int or "random").

    Raises:
        SystemExit: If the value is not a valid integer.
    """

    raw_seed: str = dict_raw.get("seed", "").strip()

    if not raw_seed:
        dict_graph["seed"] = "random"
        return

    try:
        seed_value: int = int(raw_seed)
        dict_graph["seed"] = seed_value
        random.seed(seed_value)
    except (ValueError, TypeError):
        print("'Seed' should be a number <int> or leave it empty like 'SEED='")
        print_error()
        return


def v_entry(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:
    """Validate the 'entry' value and store it as a pair of integers.

    Args:
        dict_raw (dict[str, str]): Raw key/value pairs read from the file;
            the value must have the form "x,y".
        dict_graph (dict[str, Any]): Validated configuration; receives the
            key "entry" (tuple[int, int]).

    Raises:
        SystemExit: If the value is missing, does not contain exactly two
            comma-separated parts, or the parts are not integers.
    """

    try:
        raw_entry: str = dict_raw["entry"]
        parts = raw_entry.split(",")
        if len(parts) != 2:
            print("'Entry' should have only 2 integers numbers")
            print_error()
        dict_graph["entry"] = (int(parts[0]), int(parts[1]))
    except (ValueError, TypeError, KeyError):
        print("'Entry' should be in format <int,int> with no spaces")
        print_error()


def v_exit(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:
    """Validate the 'exit' value and store it as a pair of integers.

    Args:
        dict_raw (dict[str, str]): Raw key/value pairs read from the file;
            the value must have the form "x,y".
        dict_graph (dict[str, Any]): Validated configuration; receives the
            key "exit" (tuple[int, int]).

    Raises:
        SystemExit: If the value is missing, does not contain exactly two
            comma-separated parts, or the parts are not integers.
    """

    try:
        raw_exit: str = dict_raw["exit"]
        parts = raw_exit.split(",")
        if len(parts) != 2:
            print("'Exit' should have only 2 integers numbers")
            print_error()
        dict_graph["exit"] = (int(parts[0]), int(parts[1]))
        if (
            dict_graph["exit"] > dict_graph["exit"]
            or dict_graph["exit"] > dict_graph["exit"]
        ):
            print("'Exit' should be equal or less than 'witdth'", end="")
            print("or 'height' and must be positive.")
            print_error()
    except (ValueError, TypeError, KeyError):
        print("'Exit' should be in format <int,int> with no spaces")
        print_error()


def compare_entry_exit(dict_graph: dict[str, Any]) -> None:
    """Check entry and exit against the maze bounds and each other.

    Must be called after width, height, entry and exit have been
    validated.

    Args:
        dict_graph (dict[str, Any]): Validated configuration containing
            "width", "height", "entry" and "exit".

    Raises:
        SystemExit: If the entry or the exit lies outside the maze, or if
            both are in the same cell.
    """

    width: int = dict_graph["width"]
    height: int = dict_graph["height"]

    entry_x, entry_y = dict_graph["entry"]
    exit_x, exit_y = dict_graph["exit"]

    if not (0 <= entry_x < width and 0 <= entry_y < height):
        print("Entry is outside the maze, please choose another number.")
        print_error()

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        print("Exit is outside the maze, please choose another number.")
        print_error()

    if entry_x == exit_x and entry_y == exit_y:
        print("Exit and entry are in the same spot, please change it.")
        print_error()


def v_animation(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:
    """Validate the optional 'animation' value and store it as a boolean.

    An empty or missing value defaults to False. Matching is
    case-insensitive.

    Args:
        dict_raw (dict[str, str]): Raw key/value pairs read from the file.
        dict_graph (dict[str, Any]): Validated configuration; receives the
            key "animation" (bool).

    Raises:
        SystemExit: If the value is neither 'true' nor 'false'.
    """
    raw_animation: str = dict_raw.get("animation", "").strip()

    if not raw_animation:
        dict_graph["animation"] = False
        return

    if raw_animation.lower() == "true":
        dict_graph["animation"] = True
    elif raw_animation.lower() == "false":
        dict_graph["animation"] = False
    else:
        print("'animation' value should be 'True' or 'False'")
        print_error()


def v_algorithm(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:
    """Validate the optional 'algorithm' value and store it in lowercase.

    An empty or missing value defaults to "kruskal". Matching is
    case-insensitive.

    Args:
        dict_raw (dict[str, str]): Raw key/value pairs read from the file.
        dict_graph (dict[str, Any]): Validated configuration; receives the
            key "algorithm" ("bfs", "kruskal" or "prim").

    Raises:
        SystemExit: If the value is not one of the supported algorithms.
    """
    raw_algorithm: str = dict_raw.get("algorithm", "").strip()

    if not raw_algorithm:
        dict_graph["algorithm"] = "kruskal"
        return

    if raw_algorithm.lower() in ["bfs", "kruskal", "prim"]:
        dict_graph["algorithm"] = raw_algorithm.lower()
    else:
        print(
            "The 'algorithm' must be one of the",
            "following: BFS, Kruskal or Prim. ",
        )
        print_error()


def validate_config() -> dict[str, Any]:
    """Read the configuration file given on the command line and validate it.

    The path is taken from ``sys.argv[1]``. Blank lines and lines starting
    with '#' are skipped; every other line is split on the first '=' into a
    lowercase key and a stripped value. Each value is then checked by the
    corresponding ``v_*`` function and the entry/exit positions are
    compared against the maze bounds. Finally, any unexpected key in the
    result is rejected.

    Returns:
        dict[str, Any]: The validated configuration with the keys "width",
        "height", "perfect", "seed", "output_file", "entry", "exit",
        "animation" and "algorithm".

    Raises:
        SystemExit: If the number of command-line arguments is wrong or any
            value is invalid.
        Exception: If a line has nothing after the '=' sign (for example
            'SEED='), since a bare ``Exception`` is raised and is not
            caught by this function.
    """

    if len(sys.argv) != 2:
        print("Wrong format for the program, please use:")
        print("python3 a_maze_ing.py config.txt")
        exit(1)

    config_path = sys.argv[1]
    dict_graph: dict[str, Any] = {}
    dict_raw: dict[str, str] = {}

    try:
        with open(config_path, "r") as f:
            for line in f:
                if line == "\n" or line.strip().startswith("#"):
                    continue
                if line.strip().index("=") + 1 == len(line.strip()):
                    raise Exception
                key, value = line.split("=", 1)
                key = key.strip().lower()
                value = value.strip()
                dict_raw[key] = value
    except (ValueError, TypeError):
        print("Be sure the name of the archive is 'config.txt'")
        print_error()

    v_width(dict_raw, dict_graph)
    v_height(dict_raw, dict_graph)
    v_perfect(dict_raw, dict_graph)
    v_seed(dict_raw, dict_graph)
    v_output_file(dict_raw, dict_graph)
    v_entry(dict_raw, dict_graph)
    v_exit(dict_raw, dict_graph)
    compare_entry_exit(dict_graph)
    v_animation(dict_raw, dict_graph)
    v_algorithm(dict_raw, dict_graph)

    valid_keys: set[str] = {
        "width",
        "height",
        "entry",
        "exit",
        "output_file",
        "perfect",
        "seed",
        "animation",
        "algorithm",
    }

    if len(dict_graph.keys()) <= 4 and len(dict_graph.keys()) > 9:
        print("Be sure to have all values like the example below")
        print_error()

    for key in dict_graph.keys():
        if key not in valid_keys:
            print("Be sure to have all values like the example below")
            print_error()

    return dict_graph
