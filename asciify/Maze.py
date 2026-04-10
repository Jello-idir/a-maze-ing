from enum import Enum
from typing import TextIO
from .palette import load_colors
import io


COLOR: dict[str, str] = load_colors()
PADDIN: int = 2


class Block(str, Enum):
    def __str__(self):
        return self.value
    ROAD = COLOR["road"] + "  " + COLOR["reset"]
    WALL = COLOR["wall"] + "  " + COLOR["reset"]
    CELL = COLOR["cell"] + "    " + COLOR["reset"]
    BLOK = COLOR["blok"] + "    " + COLOR["reset"]
    PADD = COLOR["bg"] + "  " + COLOR["reset"]
    SHADOW = COLOR["shadow"] + "  " + COLOR["reset"]


class AsciiCell:
    def __init__(self, hex_value: str):
        self.value = int(hex_value, 16)
        self.n, self.e, self.s, self.w = self.hex_to_bool(self.value)

    def binary_repr(self) -> str:
        return f"{self.w}{self.s}{self.e}{self.n}"

    @staticmethod
    def hex_to_bool(hex: int) -> list[bool]:
        return [
            bool((hex >> 0) & 1),
            bool((hex >> 1) & 1),
            bool((hex >> 2) & 1),
            bool((hex >> 3) & 1),
        ]


def cellify(cells_str: str) -> list[list[AsciiCell]]:
    cells: list[list[AsciiCell]] = []

    lines = cells_str.splitlines()
    for line in lines:
        cell_row: list[AsciiCell] = []
        for hex_digit in line.strip():
            cell_row.append(AsciiCell(hex_digit))
        cells.append(cell_row)
    return cells


class Maze:
    def __init__(self, maze: str | TextIO):
        if isinstance(maze, io.IOBase):
            maze = maze.read()
        if isinstance(maze, str):
            self.maze = cellify(maze)
            self.width = len(self.maze[0])
            self.height = len(self.maze)

    def render(self) -> None:
        """displays the maze in the terminal"""

        def margin_x() -> None:
            """prints the left and right margin of the maze"""
            print(Block.PADD * PADDIN, end="")

        def margin_y() -> None:
            """prints the upper and lower margin of the maze"""
            for _ in range(PADDIN):
                margin_x()
                print(Block.PADD * (self.width * 3 + 2), end="")
                margin_x()
                print()

        def shadow_x() -> None:
            """prints the right shadow of the maze"""
            print(Block.SHADOW, end="")

        def shadow_y() -> None:
            """prints the lower shadow of the maze"""
            margin_x()
            print(Block.SHADOW * (self.width * 3 + 2), end="")
            margin_x()
            print()

        # upper margin
        margin_y()

        # upper line
        for _ in range(1):
            margin_x()
            for cell in self.maze[0]:
                print(Block.WALL, end="")
                if (cell.n):
                    print(Block.WALL * 2, end="")
                else:
                    print(Block.ROAD * 2, end="")
            print(Block.WALL, end="")
            shadow_x()
            margin_x()
            print()


        # print lines
        for row in self.maze:

            # middlline
            for _ in range(2):
                margin_x()
                if row[0].w:
                    print(Block.WALL, end="")
                else:
                    print(Block.ROAD, end="")

                for cell in row:
                    if cell.value == 15:
                        print(Block.BLOK, end="")
                    else:
                        print(Block.CELL, end="")
                    if cell.e:
                        print(Block.WALL, end="")
                    else:
                        print(Block.ROAD, end="")
                shadow_x()
                margin_x()
                print()


            # bottom line
            for _ in range(1):
                margin_x()
                print(Block.WALL, end="")
                for cell in row:
                    if cell.s:
                        print(Block.WALL * 2, end="")
                    else:
                        print(Block.ROAD * 2, end="")
                    print(Block.WALL, end="")
                shadow_x()
                margin_x()
                print()

        # lower margin
        shadow_y()
        margin_y()

