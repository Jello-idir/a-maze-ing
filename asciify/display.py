from enum import Enum
from typing import TextIO
import io


class Color(Enum):
    OPEN = "\033[48;2;30;35;50m"
    WALL = "\033[48;2;255;255;255m"
    CELL = "\033[48;2;30;50;80m"
    RESET = "\033[0m"
    BLOCK = "\033[48;2;0;100;200m"


class Block(Enum):
    OPEN = f"{Color.OPEN.value}  {Color.RESET.value}"
    WALL = f"{Color.WALL.value}  {Color.RESET.value}"
    CELL = f"{Color.CELL.value}    {Color.RESET.value}"
    BLOCK = f"{Color.BLOCK.value}    {Color.RESET.value}"


class AsciiCell:
    def __init__(self, hex_value: str):
        self.hex_value = hex_value
        self.value = int(hex_value, 16)
        self.north, self.east, self.south, self.west = [
            (self.value >> 0) & 1,
            (self.value >> 1) & 1,
            (self.value >> 2) & 1,
            (self.value >> 3) & 1,
        ]
        self.is_last: bool = False

    def binary_repr(self) -> str:
        return f"{self.west}{self.south}{self.east}{self.north}"

    @staticmethod
    def hex_to_bool(hex: int) -> list[bool]:
        pass


def parse_cells(cells_str: str) -> list[list[AsciiCell]]:
    cells: list[list[AsciiCell]] = []

    lines = cells_str.splitlines()
    for line in lines:
        cell_row: list[AsciiCell] = []
        for hex_digit in line.strip():
            cell_row.append(AsciiCell(hex_digit))
        cells.append(cell_row)
        cell_row[-1].is_last = True
    return cells


class Maze:
    def __init__(self, maze: str | TextIO):
        if isinstance(maze, io.IOBase):
            maze = maze.read()

        self.maze = parse_cells(maze)
        self.width = len(self.maze[0])
        self.height = len(self.maze)

    def display_maze(self) -> None:

        # upper line
        for cell in self.maze[0]:
            print(Block.WALL.value, end="")
            if (cell.north):
                print(Block.WALL.value * 2, end="")
            else:
                print(Block.OPEN.value * 2, end="")
        print(Block.WALL.value)

        # print lines
        for row in self.maze:

            # middlline
            for _ in range(2):
                if row[0].west:
                    print(Block.WALL.value, end="")
                else:
                    print(Block.OPEN.value, end="")

                for cell in row:
                    if cell.hex_value == "F":
                        print(Block.BLOCK.value, end="")
                    else:
                        print(Block.CELL.value, end="")
                    if cell.east:
                        print(Block.WALL.value, end="")
                    else:
                        print(Block.OPEN.value, end="")
                print()

            # bottom line
            print(Block.WALL.value, end="")
            for cell in row:
                if cell.south:
                    print(Block.WALL.value * 2, end="")
                else:
                    print(Block.OPEN.value * 2, end="")
                print(Block.WALL.value, end="")
            print()


def test():
    with open("maze_example.txt", "r") as fl:
        maze = Maze(fl)
    print("\n" * 120)
    maze.display_maze()
    print("\n" * 5)


if __name__ == "__main__":
    test()
