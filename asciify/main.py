from asciify import Maze
from pathlib import Path

def test():
    maze_path = Path(__file__).parent / "maze_example.txt"
    with open(maze_path, "r") as fl:
        maze = Maze(fl)
    print("\n" * 120)
    maze.render()
    print("\n" * 5)


if __name__ == "__main__":
    test()
