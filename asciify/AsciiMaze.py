from enum import Enum
from typing import TextIO
import io

from .palette import load_colors


COLOR: dict[str, str] = load_colors()
PADDIN: int = 2
ENABLE_SHADOW = True

class Block(str, Enum):
    def __str__(self):
        return self.value
    ROAD = COLOR["road"] + "  " + COLOR["reset"]
    WALL = COLOR["wall"] + "  " + COLOR["reset"]
    CELL = COLOR["cell"] + "    " + COLOR["reset"]
    BLOK = COLOR["blok"] + "    " + COLOR["reset"]
    PADD = COLOR["bg"] + "  " + COLOR["reset"]
    SHADOW = COLOR["shadow"] + "  " + COLOR["reset"]
    PANEL = COLOR["panel"] + " " + COLOR["reset"]


class AsciiCell:
    def __init__(self, val: int = 15):
        self.n = bool(val & 0b0001)
        self.e = bool(val & 0b0010)
        self.s = bool(val & 0b0100)
        self.w = bool(val & 0b1000)


def _intify(hex_str: str) -> list[list[int]]:
    cells: list[list[int]] = []

    lines = hex_str.splitlines()
    for line in lines:
        cell_row: list[int] = []
        for hex_digit in line.strip():
            cell_row.append(int(hex_digit, 16))
        cells.append(cell_row)
    return cells


def _int_asciify(cells: list[list[int]]) -> list[list[AsciiCell]]:
    """list of int to a list of AsciiCell

    Args:
        cells (list[list[int]]): list of ints to parse into AsciiCell

    Returns:
        list[list[AsciiCell]]: list of AsciiCell
    """
    ascii_cells: list[list[AsciiCell]] = []
    for row in cells:
        ascii_row: list[AsciiCell] = []
        for cell in row:
            ascii_row.append(AsciiCell(cell))
        ascii_cells.append(ascii_row)
    return ascii_cells


class AsciiMaze:
    def __init__(self, maze: list[list[int]]):
        self.maze: list[list[AsciiCell]] = _int_asciify(maze)
        self.width = len(maze[0])
        self.height = len(maze)

    @classmethod
    def from_file(cls, maze: str | TextIO) -> 'AsciiMaze':
        if isinstance(maze, io.IOBase):
            maze = maze.read()
        if isinstance(maze, str):
            maze_int = _intify(maze)
        return cls(maze_int)


    def render(self) -> None:
        """displays the maze in the terminal"""

        def margin_x() -> None:
            """prints the left and right margin of the maze"""
            print(Block.PADD * PADDIN, end="")

        def margin_y() -> None:
            """prints the upper and lower margin of the maze"""
            for _ in range(PADDIN):
                margin_x()
                print(Block.PADD * (self.width * 3 + 1 + 2 * ENABLE_SHADOW), end="")
                margin_x()
                print()

        def shadow_x() -> None:
            """prints the right shadow of the maze"""
            if not ENABLE_SHADOW:
                return
            print(Block.SHADOW, end="")

        def shadow_y() -> None:
            """prints the lower shadow of the maze"""
            if not ENABLE_SHADOW:
                return
            margin_x()
            print(Block.SHADOW * (self.width * 3 + 3), end="")
            margin_x()
            print()

        def buttom_shaddow(size: int) -> None:
            """prints the upper and lower margin of the maze"""
            if not ENABLE_SHADOW:
                return
            for _ in range(size):
                print(Block.SHADOW * (self.width * 3 + PADDIN * 2 + 3), end="")
                print()

        # upper margin
        margin_y()
        shadow_y()

        # upper line
        for _ in range(1):
            margin_x()
            shadow_x()
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
                shadow_x()
                if row[0].w:
                    print(Block.WALL, end="")
                else:
                    print(Block.ROAD, end="")

                for cell in row:
                    if all([cell.n, cell.e, cell.w, cell.s]):
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
                shadow_x()
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

        # bottom shadow
        buttom_shaddow(3)


    @staticmethod
    def render_lists_of_ints(maze: list[list[int]]) -> None:
        """renders a list of list of ints as a maze

        Args:
            cells (list[list[int]]): the maze to render
        """
        width = len(maze[0])
        height = len(maze)

        def margin_x() -> None:
            """prints the left and right margin of the maze"""
            print(Block.PADD * PADDIN, end="")

        def margin_y() -> None:
            """prints the upper and lower margin of the maze"""
            for _ in range(PADDIN):
                margin_x()
                print(Block.PADD * (width * 3 + 1 + 2 * ENABLE_SHADOW), end="")
                margin_x()
                print()

        def shadow_x() -> None:
            """prints the right shadow of the maze"""
            if not ENABLE_SHADOW:
                return
            print(Block.SHADOW, end="")

        def shadow_y() -> None:
            """prints the lower shadow of the maze"""
            if not ENABLE_SHADOW:
                return
            margin_x()
            print(Block.SHADOW * (width * 3 + 3), end="")
            margin_x()
            print()

        def buttom_shaddow(size: int) -> None:
            """prints the upper and lower margin of the maze"""
            if not ENABLE_SHADOW:
                return
            for _ in range(size):
                print(Block.SHADOW * (width * 3 + PADDIN * 2 + 3), end="")
                print()

        # upper margin
        margin_y()
        shadow_y()

        # upper line
        for _ in range(1):
            margin_x()
            shadow_x()
            for cell in maze[0]:
                print(Block.WALL, end="")
                if (cell & 0b0001):
                    print(Block.WALL * 2, end="")
                else:
                    print(Block.ROAD * 2, end="")
            print(Block.WALL, end="")
            shadow_x()
            margin_x()
            print()


        # print lines
        for row in maze:

            # middlline
            for _ in range(2):
                margin_x()
                shadow_x()
                if row[0] & 0b1000:
                    print(Block.WALL, end="")
                else:
                    print(Block.ROAD, end="")

                for cell in row:
                    if all([cell & 0b0001, cell & 0b0010,
                            cell & 0b0100, cell & 0b1000]):
                        print(Block.BLOK, end="")
                    else:
                        print(Block.CELL, end="")
                    if cell & 0b0010:
                        print(Block.WALL, end="")
                    else:
                        print(Block.ROAD, end="")
                shadow_x()
                margin_x()
                print()


            # bottom line
            for _ in range(1):
                margin_x()
                shadow_x()
                print(Block.WALL, end="")
                for cell in row:
                    if cell & 0b0100:
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

        # bottom shadow
        buttom_shaddow(3)

