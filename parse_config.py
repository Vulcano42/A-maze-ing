import sys
import random
from typing import Any


def print_error() -> None:

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

    try:
        dict_graph["width"] = int(dict_raw["width"])
        if dict_graph["width"] < 1 or dict_graph["width"] > 500:
            print("'Width' should be between 1 and 500")
            print_error()
    except Exception:
        print("'Width' should be between 1 and 500")
        print_error()


def v_height(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:

    try:
        dict_graph["height"] = int(dict_raw["height"])
        if dict_graph["height"] < 1 or dict_graph["height"] > 500:
            print("'Height' should be between 1 and 500")
            print_error()
    except Exception:
        print("'Height' should be between 1 and 500")
        print_error()


def v_perfect(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:

    try:
        raw_perfect: str = dict_raw["perfect"].strip()
        if raw_perfect.lower() == "true":
            dict_graph["perfect"] = True
        elif raw_perfect.lower() == "false":
            dict_graph["perfect"] = False
        else:
            print("'Perfect' value should be 'True' or 'False'")
            print_error()

    except Exception:
        print("'Perfect' value should be 'True' or 'False'")
        print_error()


def v_output_file(
    dict_raw: dict[str, str], dict_graph: dict[str, Any]
) -> None:

    try:
        dict_graph["output_file"] = str(dict_raw["output_file"])
    except Exception:
        print("'Output_file' should be a sting terminated with '.txt.'")
        print_error()

    if not dict_graph["output_file"].endswith(".txt"):
        print("'Output_file' should be a sting terminated with '.txt.'")
        print_error()


def v_seed(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:

    raw_seed: str = dict_raw.get("seed", "").strip()

    if not raw_seed:
        dict_graph["seed"] = "random"
        return

    try:
        seed_value: int = int(raw_seed)
        dict_graph["seed"] = seed_value
        random.seed(seed_value)
    except Exception:
        print("'Seed' should be a number <int> or leave it empty like 'SEED='")
        print_error()
        return


def v_entry(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:

    try:
        raw_entry: str = dict_raw["entry"]
        parts = raw_entry.split(",")
        if len(parts) != 2:
            print("'Entry' should have only 2 integers numbers")
            print_error()
        dict_graph["entry"] = (int(parts[0]), int(parts[1]))
    except Exception:
        print("'Entry' should be in format <int,int> with no spaces")
        print_error()


def v_exit(dict_raw: dict[str, str], dict_graph: dict[str, Any]) -> None:

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
    except Exception:
        print("'Exit' should be in format <int,int> with no spaces")
        print_error()


def compare_entry_exit(dict_graph: dict[str, Any]) -> None:

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

def validate_config() -> dict[str, Any]:

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
    except Exception:
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

    valid_keys: set[str] = {
        "width", "height", "entry", "exit", "output_file", "perfect",
        "seed", "animation"
        }

    if len(dict_graph.keys()) < 6 and len(dict_graph.keys()) > 8:
        print("Be sure to have all values like the example below")
        print_error()

    for key in dict_graph.keys():
        if key not in valid_keys:
            print("Be sure to have all values like the example below")
            print_error()

    return dict_graph
