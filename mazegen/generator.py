from collections.abc import Callable

class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool = True, seed: int = 42,
                 output_file: str = "maze.txt", already_valid: bool = False) -> None:
        self.w: int = width
        self.h: int = height
        self.maze: list[list[int]] = []
        self.inn: tuple[int, int] = entry
        self.out: tuple[int, int] = exit
        self.path: str = ""
        self.output_file: str = output_file
        self.perfect: bool = perfect
        self.seed = seed
        if not already_valid:
            self._validate_params()


    def generate(self) -> None:
        self.maze = [[0 for _ in range(self.w)] for _ in range(self.h)]
        self._close_borders()
        #self._add_42_pattern()


    def _close_borders(self) -> None:
        for i in range(self.w):
            self.maze[0][i] |= 0b0001
            self.maze[self.h - 1][i] |= 0b0100
        for i in range(self.h):
            self.maze[i][0] |= 0b1000
            self.maze[i][self.w - 1] |= 0b0010


    def _close(self, x: int, y: int, binary: int):
        self.maze[y][x] |= binary

    def _open(self, x: int, y: int, binary: int):
        self.maze[y][x] &= ~binary


    def _cwall(self, point: tuple[int, int], directions: str, flag: str) -> None:
        x, y = point
        """closes or opens the walls of a cell in the specified directions
        Args:
            point (tuple[int, int]): the coordinates of the cell
            directions (str): a string containing the directions to modify (N, E, S, W)
            flag (str): "close" to close the walls, "open" to open the walls
        """
        action: Callable = self._close if flag == "close" else self._open
        if 'N' in directions:
            action(x, y, 0b0001)
            if y > 0:
                action(x, y - 1, 0b0100)
        if 'E' in directions:
            action(x, y, 0b0010)
            if x < self.w - 1:
                action(x + 1, y, 0b1000)
        if 'S' in directions:
            action(x, y, 0b0100)
            if y < self.h - 1:
                action(x, y + 1, 0b0001)
        if 'W' in directions:
            action(x, y, 0b1000)
            if x > 0:
                action(x - 1, y, 0b0010)


    def _close_points(self, points: list[tuple[int, int]], offset: tuple[int, int]):
        for x, y in points:
            self._cwall((x + offset[0], y + offset[1]), "NESW", self._close)


    def _carve_passages(self, x: int, y: int, visited: list[list[bool]]) -> None:
        ...


    def _add_42_pattern(self) -> None:
        self._close_points(
            [
                (1, 1), (2, 2), (3, 3)
            ],
            (0, 0)
        )


    def _open_entry_exit(self) -> None:
        ...


    def _solve_maze(self) -> str:
        ...


    def write_to_file(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for row in self.maze:
                line = ''.join(f"{cell:X}" for cell in row)
                f.write(line + '\n')


    def get_cell_walls(self, x: int, y: int) -> dict[str, bool]:
        """provides a dictionary indicating the presence of walls in each direction for a given cell

        Args:
            x (int): the x-coordinate of the cell
            y (int): the y-coordinate of the cell

        Returns:
            dict[str, bool]: a dictionary with keys 'N', 'E', 'S', 'W',
            indicating the presence of walls in each direction
        """
        cell_value = self.maze[y][x]
        return {
            'N': bool(cell_value & 1),
            'E': bool(cell_value & 2),
            'S': bool(cell_value & 4),
            'W': bool(cell_value & 8)
        }


    def _validate_params(self) -> None:
        if self.w <= 0 or self.h <= 0:
            raise ValueError("Width and height must be positive integers")
        if not (0 <= self.inn[0] <= self.w and 0 <= self.inn[1] <= self.h):
            raise ValueError("Entry coordinates out of bounds")
        if not (0 <= self.out[0] <= self.w and 0 <= self.out[1] <= self.h):
            raise ValueError("Exit coordinates out of bounds")
        if self.inn == self.out:
            raise ValueError("Entry and exit cannot be the same point")
    @classmethod
    def from_object(cls, config) -> 'MazeGenerator':
        return cls(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit=config.exit,
            perfect=config.perfect,
            seed=config.seed,
            output_file=config.output_file,
            already_valid=False
        )
