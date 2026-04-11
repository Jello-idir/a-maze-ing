import sys
import time
from mazegen import MazeGenerator
from parsing import MazeConfig
from asciify import AsciiMaze

def get_config() -> MazeConfig:
    argc = len(sys.argv)
    if argc != 2:
        raise ValueError("Usage: python a-maze-ing.py <config_file>")
    try:
        with open(sys.argv[1]) as f:
            return MazeConfig.from_file(f)
    except FileNotFoundError:
        raise ValueError(f"Config file '{sys.argv[1]}' not found.")


def draw_face(maze: MazeGenerator):
    maze.generate()
    maze._cwall((11, 5), "NESW", "close")
    maze._cwall((12, 5), "NESW", "close")

    maze._cwall((19, 5), "NESW", "close")
    maze._cwall((20, 5), "NESW", "close")

    maze._cwall((14, 7), "NESW", "close")
    maze._cwall((15, 7), "NESW", "close")
    maze._cwall((16, 7), "NESW", "close")
    maze._cwall((17, 7), "NESW", "close")


def main() -> None:
    mazeconfig = get_config()

    for key, value in mazeconfig.get_config().items():
        print(f"{key.upper():12} {value}")

    maze = MazeGenerator.from_object(mazeconfig)
    maze.generate()

    draw_face(maze)
    ascii = AsciiMaze(maze.maze)
    ascii.render_lists_of_ints(maze.maze)


    maze.write_to_file("output.txt")



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\033[31mError:\033[0m {e}")
