import tomllib
from typing import TextIO, Generator
import os


def load_colors(theme: str) -> dict[str, str]:
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "palettes", f"{theme}.toml")
    with open(path, "rb") as f:
        _data = tomllib.load(f)

    def to_ansi(hex_color: str) -> str:
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"\033[48;2;{r};{g};{b}m"

    colors = {k: to_ansi(v) for k, v in _data["maze_colors"].items()}
    colors["reset"] = "\033[0m"
    return colors

COLOR: dict[str, str] = load_colors("orange")
PADDIN: int = 2

def _color_generator() -> Generator[dict[str, str], None, None]:
    colors = [load_colors(theme) for theme in ["orange", "green", "red", "blue"]]
    while True:
        for color in colors:
            yield color


class AsciiMaze:
    def __init__(self, maze: list[list[int]]):
        self.maze: list[list[int]] =  maze
        self.width = len(maze[0])
        self.height = len(maze)
        self.color_gen = _color_generator()
        self.color = load_colors("blue")

    def render(self) -> None:
        """renders the generated maze to the terminal
        """
        self.render_ints(self.maze)

    def next_color(self) -> None:
        """switches to the next color scheme
        """
        self.color = next(self.color_gen)

    @classmethod
    def from_file(cls, maze: TextIO) -> 'AsciiMaze':
        """creates an AsciiMaze from a file containing hex digits

        Args:
            maze (TextIO): a file containing hex digits representing the maze

        Returns:
            AsciiMaze: the generated maze
        """
        return cls(cls._intify(maze.read()))

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

    def flush_ints(self, maze: list[list[int]]) -> None:
        print(f"\033[{self.height * 3 + 1 + 11}F", end="")
        self.render_ints(maze)

    def render_ints(self, maze: list[list[int]]) -> None:
        """renders a list of list of ints as a maze

        Args:
            cells (list[list[int]]): the maze to render
        """

        ROAD = self.color["road"] + "  "
        WALL = self.color["wall"] + "  "
        CELL = self.color["cell"] + "    "
        BLOK = self.color["blok"] + "    "
        PADD = self.color["blok"] + "  "
        SHADOW = self.color["shadow"] + "  "
        VISITED = self.color["visited"] + "    "
        CONNECTED = self.color["connected"] + "    "
        ENTRY = self.color["entry"] + "    "
        EXIT = self.color["exit"] + "    "
        PATH = self.color["path"] + "    "

        def margin_x() -> None:
            """prints the left and right margin of the maze"""
            print(PADD * PADDIN * 2, end="")

        def margin_y() -> None:
            """prints the upper and lower margin of the maze"""
            for _ in range(PADDIN):
                margin_x()
                print(PADD * (self.width * 3 + 1 + 2), end="")
                margin_x()
                print(self.color["reset"])

        def shadow_x() -> None:
            """prints the right shadow of the maze"""
            print(SHADOW, end="")

        def shadow_y() -> None:
            """prints the lower shadow of the maze"""
            margin_x()
            print(SHADOW * (self.width * 3 + 3), end="")
            margin_x()
            print(self.color["reset"])

        def buttom_shaddow(size: int) -> None:
            """prints the upper and lower margin of the maze"""
            for _ in range(size):
                print(SHADOW * (self.width * 3 + PADDIN * 4 + 3), end="")
                print(self.color["reset"])

        # upper margin
        margin_y()
        shadow_y()
        shadow_y()

        # upper line
        for _ in range(1):
            margin_x()
            shadow_x()
            for cell in maze[0]:
                print(WALL, end="")
                if (cell & 0b0001):
                    print(WALL * 2, end="")
                else:
                    print(ROAD * 2, end="")
            print(WALL, end="")
            shadow_x()
            margin_x()
            print(self.color["reset"])

        # print lines
        for row in maze:

            # middlline
            for _ in range(2):
                margin_x()
                shadow_x()
                if row[0] & 0b1000:
                    print(WALL, end="")
                else:
                    print(ROAD, end="")

                for cell in row:
                    if ((cell >> 4) == 0b1111):
                        print(BLOK, end="")
                    elif (cell >> 6) == 0b11:
                        print(PATH, end="")
                    elif cell & 0b10000000:
                        print(ENTRY, end="")
                    elif cell & 0b1000000:
                        print(EXIT, end="")
                    elif cell & 0b100000:
                        print(CONNECTED, end="")
                    elif (cell & 0b10000):
                        print(VISITED, end="")
                    else:
                        print(CELL, end="")
                    if cell & 0b0010:
                        print(WALL, end="")
                    else:
                        print(ROAD, end="")
                shadow_x()
                margin_x()
                print(self.color["reset"])

            # bottom line
            for _ in range(1):
                margin_x()
                shadow_x()
                print(WALL, end="")
                for cell in row:
                    if cell & 0b0100:
                        print(WALL * 2, end="")
                    else:
                        print(ROAD * 2, end="")
                    print(WALL, end="")
                shadow_x()
                margin_x()
                print(self.color["reset"])

        # lower margin
        margin_y()
        margin_y()

        # bottom shadow
        buttom_shaddow(3)

    def render_binary(self, maze: list[list[int]]) -> None:
        """renders a list of list of ints as a maze

        Args:
            cells (list[list[int]]): the maze to render
        """

        ROAD = self.color["road"] + "  "
        WALL = self.color["wall"] + "  "
        CELL = self.color["cell"]
        BLOK = self.color["blok"]
        PADD = self.color["blok"] + "  "
        SHADOW = self.color["shadow"] + "  "
        VISITED = self.color["visited"]
        CONNECTED = self.color["connected"]
        ENTRY = self.color["entry"]
        EXIT = self.color["exit"]
        PATH = self.color["path"]

        def margin_x() -> None:
            """prints the left and right margin of the maze"""
            print(PADD * PADDIN * 2, end="")

        def margin_y() -> None:
            """prints the upper and lower margin of the maze"""
            for _ in range(PADDIN):
                margin_x()
                print(PADD * (self.width * 3 + 1 + 2), end="")
                margin_x()
                print(self.color["reset"])

        def shadow_x() -> None:
            """prints the right shadow of the maze"""
            print(SHADOW, end="")

        def shadow_y() -> None:
            """prints the lower shadow of the maze"""
            margin_x()
            print(SHADOW * (self.width * 3 + 3), end="")
            margin_x()
            print(self.color["reset"])

        def buttom_shaddow(size: int) -> None:
            """prints the upper and lower margin of the maze"""
            for _ in range(size):
                print(SHADOW * (self.width * 3 + PADDIN * 4 + 3), end="")
                print(self.color["reset"])

        # upper margin
        margin_y()
        shadow_y()
        shadow_y()

        # upper line
        for _ in range(1):
            margin_x()
            shadow_x()
            for cell in maze[0]:
                print(WALL, end="")
                if (cell & 0b0001):
                    print(WALL * 2, end="")
                else:
                    print(ROAD * 2, end="")
            print(WALL, end="")
            shadow_x()
            margin_x()
            print(self.color["reset"])

        # print lines
        for row in maze:

            # middlline
            for _ in range(2):
                margin_x()
                shadow_x()
                if row[0] & 0b1000:
                    print(WALL, end="")
                else:
                    print(ROAD, end="")

                for cell in row:
                    if ((cell >> 4) == 0b1111):
                        print(f"{BLOK}{cell>>4:04b}", end="")
                    elif (cell >> 6) == 0b11:
                        print(f"{PATH}{cell>>4:04b}", end="")
                    elif cell & 0b10000000:
                        print(f"{ENTRY}{cell>>4:04b}", end="")
                    elif cell & 0b1000000:
                        print(f"{EXIT}{cell>>4:04b}", end="")
                    elif cell & 0b100000:
                        print(f"{CONNECTED}{cell>>4:04b}", end="")
                    elif (cell & 0b10000):
                        print(f"{VISITED}{cell>>4:04b}", end="")
                    else:
                        print(f"{CELL}{cell:04b}", end="")
                    if cell & 0b0010:
                        print(WALL, end="")
                    else:
                        print(ROAD, end="")
                shadow_x()
                margin_x()
                print(self.color["reset"])

            # bottom line
            for _ in range(1):
                margin_x()
                shadow_x()
                print(WALL, end="")
                for cell in row:
                    if cell & 0b0100:
                        print(WALL * 2, end="")
                    else:
                        print(ROAD * 2, end="")
                    print(WALL, end="")
                shadow_x()
                margin_x()
                print(self.color["reset"])

        # lower margin
        margin_y()
        margin_y()

        # bottom shadow
        buttom_shaddow(3)
