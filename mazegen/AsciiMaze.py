import tomllib
from typing import TextIO, Generator
import os
import sys


def load_colors(theme: str) -> dict[str, str]:
    """ loads a color scheme from the palettes folder, the color scheme is a

    Args:
        theme (str): the name of the color scheme to load,
        it should correspond to a .toml file

    Returns:
        dict[str, str]: a dictionary mapping color names
        to ANSI escape codes for background color
    """
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "palettes", f"{theme}.toml")
    with open(path, "rb") as f:
        _data = tomllib.load(f)

    def to_ansi(hex_color: str) -> str:
        """ converts a hex color code to an ANSI
        escape code for background color

        Args:
            hex_color (str): a hex color code in the format "#RRGGBB"

        Returns:
            str: an ANSI escape code for background color
            in the format "\033[48;2;R;G;Bm"
        """
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"\033[48;2;{r};{g};{b}m"

    colors = {k: to_ansi(v) for k, v in _data["maze_colors"].items()}
    colors["reset"] = "\033[0m"
    return colors


def _color_generator() -> Generator[dict[str, str], None, None]:
    """ a generator that yields a color scheme from the palettes folder,

    Yields:
        Generator[dict[str, str], None, None]: a generator that yields a
        color scheme from the palettes folder
    """
    colors = [load_colors(theme) for theme in
              ["orange", "green", "red",
               "purple", "brown", "blue"]]
    while True:
        for color in colors:
            yield color


class AsciiMaze:
    def __init__(self, maze: list[list[int]]):
        """ a class representing an ASCII maze,
        it can render the maze to the console

        Args:
            maze (list[list[int]]): a 2D list of integers
            representing the maze, where each integer is a hex digit
        """
        self.maze: list[list[int]] = maze
        self.w = len(maze[0])
        self.h = len(maze)
        self.clr_gen = _color_generator()
        self.clr = load_colors("blue")
        self.showpath = False

    @classmethod
    def from_file(cls, maze: TextIO) -> 'AsciiMaze':
        """creates an AsciiMaze from a file

        Args:
            maze (TextIO): a file containing hex digits representing the maze

        Raises:
            ValueError: if the file is closed

        Returns:
            AsciiMaze: the generated maze
        """
        if maze.closed:
            raise ValueError("File must be open to read")
        return cls(cls._intify(maze.read()))

    def delete_path(self) -> None:
        """deletes the path from the maze, this is used to animate the solution
        """
        for r in range(self.h):
            for c in range(self.w):
                if (self.maze[r][c] >> 4) == 0b1100:
                    self.maze[r][c] &= 0b111111

    @classmethod
    def from_str(cls, maze: str) -> 'AsciiMaze':
        """creates an AsciiMaze from a string of hex digits

        Args:
            maze (str): a string of hex digits representing the maze

        Returns:
            AsciiMaze: the generated maze
        """
        return cls(cls._intify(maze))

    @staticmethod
    def _intify(hex_str: str) -> list[list[int]]:
        """converts a string of hex digits into a list of list of ints

        Args:
            hex_str (str): a string of hex digits representing the maze

        Returns:
            list[list[int]]: a list of list of ints representing the maze
        """
        cells: list[list[int]] = []

        lines = hex_str.splitlines()
        for line in lines:
            cell_row: list[int] = []
            for hex_digit in line.strip():
                cell_row.append(int(hex_digit, 16))
            cells.append(cell_row)
        return cells

    def next_color(self) -> None:
        """switches to the next color scheme
        """
        self.clr = next(self.clr_gen)

    def toggle_path(self) -> None:
        """toggles the visibility of the path in the maze
        """
        self.showpath = not self.showpath

    def flush(self, maze: list[list[int]] | None) -> None:
        """flushes the console and re-renders the maze,
        this is used to update the maze in place without scrolling

        Args:
            maze (list[list[int]] | None): the maze to render,
            if None, the maze stored in the object will be rendered

        Raises:
            ValueError: if no maze is provided
            and no maze is stored in the object
        """
        if maze is None and self.maze is None:
            raise ValueError("No maze to flush")
        print(f"\033[{self.h * 3 + 1 + 11}F", end="")
        self.render(maze)

    def render(self, maze: list[list[int]] | None = None) -> None:
        """renders the maze to the console

        Args:
            maze (list[list[int]] | None, optional): the maze to render,
            Defaults to None.

        Raises:
            ValueError: if no maze is provided
            and no maze is stored in the object
        """
        if maze is None:
            if self.maze is None:
                raise ValueError("No maze to render")
            maze = self.maze

        write = sys.stdout.write
        buff = []

        ROAD = self.clr["road"] + "  "
        WALL = self.clr["wall"] + "  "
        CELL = self.clr["cell"] + "    "
        BLOCK = self.clr["block"] + "  "
        SHADOW = self.clr["shadow"] + "  "
        VISITED = self.clr["visited"] + "    "
        CONNECTED = self.clr["connected"] + "    "
        ENTRY = self.clr["entry"] + "    "
        EXIT = self.clr["exit"] + "    "
        PATH = self.clr["path"] + "    " if self.showpath else CELL
        R = self.clr["reset"]
        M = BLOCK * 4

        UPSHADOW = M + SHADOW * (self.w * 3 + 3) + M

        buff.append(f"{M + BLOCK * (self.w * 3 + 3) + M + R + "\n"}" * 2)
        buff.append(f"{UPSHADOW + R + "\n"}" * 2)

        line = M + SHADOW
        for point in maze[0]:
            line += WALL
            if (point & 0b0001):
                line += WALL * 2
            else:
                line += ROAD * 2
        line += WALL + SHADOW + M + R + "\n"
        buff.append(line)

        for row in maze:
            for _ in range(2):
                line = M + SHADOW
                if row[0] & 0b1000:
                    line += WALL
                else:
                    line += ROAD

                for point in row:
                    if ((point >> 4) == 0b1111):
                        line += BLOCK * 2
                    elif (point >> 6) == 0b11:
                        line += PATH
                    elif point & 0b10000000:
                        line += ENTRY
                    elif point & 0b1000000:
                        line += EXIT
                    elif point & 0b100000:
                        line += CONNECTED
                    elif (point & 0b10000):
                        line += VISITED
                    else:
                        line += CELL
                    if point & 0b0010:
                        line += WALL
                    else:
                        line += ROAD

                line += SHADOW + M + R + "\n"
                buff.append(line)

            line = M + SHADOW + WALL
            for point in row:
                if point & 0b0100:
                    line += WALL * 2
                else:
                    line += ROAD * 2
                line += WALL
            line += SHADOW + M + R + "\n"
            buff.append(line)

        buff.append(f"{M + BLOCK * (self.w * 3 + 3) + M + R + "\n"}" * 4)
        buff.append(f"{SHADOW * (self.w * 3 + 11) + R + "\n"}" * 2)

        write(''.join(buff))
