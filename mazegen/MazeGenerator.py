from collections.abc import Callable
from asciify import AsciiMaze
import random
import time


def flush_after(method: Callable) -> Callable:
    def wrapper(self, *args, **kwargs) -> None:
        method(self, *args, *kwargs)
        self.flush()
    return wrapper


unvisited = []

class MazeGenerator:
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int],
                 seed: int | None = None, perfect: bool = True,
                 output_file: str = "maze.txt",
                 already_valid: bool = False) -> None:
        self.w: int = width
        self.h: int = height
        self.maze: list[list[int]] = []
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.path: str = ""
        self.output_file: str = output_file
        self.perfect: bool = perfect
        self.seed = seed
        self.asciimaze: AsciiMaze | None = None
        if seed is None:
            self.seed = int(time.time())
        random.seed(self.seed)
        if not already_valid:
            self._validate_params()

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
            already_valid=True
        )

    def _validate_params(self) -> None:
        if self.w < 9 or self.h < 7:
            raise ValueError("Width and height must be at least 9 and 7 respectively")
        if not (0 <= self.entry[0] < self.w and 0 <= self.entry[1] < self.h):
            raise ValueError("Entry coordinates out of bounds")
        if not (0 <= self.exit[0] < self.w and 0 < self.exit[1] <= self.h):
            raise ValueError("Exit coordinates out of bounds")
        if self.entry == self.exit:
            raise ValueError("Entry and exit cannot be the same point")

    def intialize(self) -> None:
        """generates the maze by initializing it, adding the 42 pattern, marking the entry and exit,
        """
        # initializes empty maze
        self.maze = [[15 for _ in range(self.w)] for _ in range(self.h)]
        # closes borders
        for i in range(self.w):
            self.maze[0][i] |= 0b0001
            self.maze[self.h - 1][i] |= 0b0100
        for i in range(self.h):
            self.maze[i][0] |= 0b1000
            self.maze[i][self.w - 1] |= 0b0010
        # marks start and end
        self.mark_entry(self.entry)
        self.mark_connected(self.entry)
        self.mark_exit(self.exit)

    def connect_ascii(self, ascii: AsciiMaze) -> None:
        """connects the maze generator to an AsciiMaze instance for visualization during generation and solving
        """
        self.asciimaze = ascii

    def flush(self, mode: int | None = None) -> None:
        if isinstance(self.asciimaze, AsciiMaze):
            self.asciimaze.flush_ints(self.maze)


    def random_unvisited_point(self) -> tuple[int, int]:
        while True:
            p = (random.randint(0, self.w - 1), random.randint(0, self.h - 1))
            if not self.maze[p[1]][p[0]] & 0b10000:
                return p

    def generate(self) -> None:
        unvisited: set[tuple[int, int]] = set((x, y) for x in range(self.w)
                                              for y in range(self.h)
                                              if not self.maze[y][x] >> 4 & 0b1)
        rpoint: tuple[int, int] = random.choice(list(unvisited))

        while True:
            if not unvisited:
                break
            while rpoint not in unvisited:
                rpoint = random.choice(list(unvisited))
            new_connected = self._wilson_path(rpoint)
            for point in new_connected:
                self.mark_connected(point)
            unvisited -= set(new_connected)
            self.carve_path(new_connected)



    def _wilson_path(self, start: tuple[int, int]) -> list[tuple[int, int]]:
        path: list[tuple[int, int]] = [start]
        self.mark_visited(start)
        p = start
        def random_neighbor(p: tuple[int, int]) -> tuple[int, int]:
            neighbors = []
            if p[1] > 0 and self.maze[p[1] - 1][p[0]] >> 4 != 0b1111:
                neighbors.append((p[0], p[1] - 1))
            if p[0] < self.w - 1 and self.maze[p[1]][p[0] + 1] >> 4 != 0b1111:
                neighbors.append((p[0] + 1, p[1]))
            if p[1] < self.h - 1 and self.maze[p[1] + 1][p[0]] >> 4 != 0b1111:
                neighbors.append((p[0], p[1] + 1))
            if p[0] > 0 and self.maze[p[1]][p[0] - 1] >> 4 != 0b1111:
                neighbors.append((p[0] - 1, p[1]))
            res = random.choice(neighbors)
            return res

        while True:
            p: tuple[int, int] = random_neighbor(p)
            if p in path:
                loop_start = path.index(p)
                to_remove = path[loop_start + 1:]
                path = path[:loop_start + 1]
                for cell in to_remove:
                    self.mark_not_visited(cell)

            elif self.maze[p[1]][p[0]] >> 5 & 1:
                path.append(p)
                return path

            else:
                path.append(p)
                self.mark_visited(p)

    def carve_path(self, path: list[tuple[int, int]]) -> None:
        for i in range(len(path) - 1):
            p1, p2 = path[i], path[i + 1]
            if p1[0] == p2[0]:
                if p1[1] < p2[1]:
                    self._change_wall(p1, "S", "open")
                else:
                    self._change_wall(p1, "N", "open")
            else:
                if p1[0] < p2[0]:
                    self._change_wall(p1, "E", "open")
                else:
                    self._change_wall(p1, "W", "open")


    def _add_42_pattern(self) -> None:
        """closes the walls in a pattern that resembles the 42 logo in the center of the maze
        """
        logo_42: list[tuple[int, int]] = [
            (0, 0), (0, 1), (0, 2), (1, 2),
            (2, 2), (2, 3), (2, 4), (2, 1),
            (2, 0), (4, 0), (5, 0), (6, 0),
            (6, 1), (6, 2), (5, 2), (4, 2),
            (4, 3), (4, 4), (5, 4), (6, 4)
            ]
        self._close_points(logo_42,
                           (round(self.w / 2) - 3,
                            round(self.h / 2) - 2))
        for point in logo_42:
            p_offset: tuple[int, int] = (
                point[0] + round(self.w / 2) - 3,
                point[1] + round(self.h / 2) - 2
                )
            self.maze[p_offset[1]][p_offset[0]] |= 0b11110000


    def _close(self, x: int, y: int, binary: int):
        self.maze[y][x] |= binary

    def _open(self, x: int, y: int, binary: int):
        self.maze[y][x] &= ~binary

    def _change_wall(self, point: tuple[int, int], directions: str, flag: str) -> None:
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
            self._change_wall((x + offset[0], y + offset[1]), "NESW", "close")


    def mark_visited(self, point: tuple[int, int]) -> None:
        self.maze[point[1]][point[0]] |= 0b10000

    def mark_not_visited(self, point: tuple[int, int]) -> None:
        self.maze[point[1]][point[0]] &= ~0b10000

    def mark_connected(self, point: tuple[int, int]) -> None:
        self.maze[point[1]][point[0]] |= 0b100000

    def mark_not_connected(self, point: tuple[int, int]) -> None:
        self.maze[point[1]][point[0]] &= ~0b100000

    def mark_entry(self, point: tuple[int, int]) -> None:
        self.maze[point[1]][point[0]] |= 0b10000000

    def mark_exit(self, point: tuple[int, int]) -> None:
        self.maze[point[1]][point[0]] |= 0b01000000

    def mark_path(self, point: tuple[int, int]) -> None:
        self.maze[point[1]][point[0]] |= 0b11110000

    def mark_not_path(self, point: tuple[int, int]) -> None:
        self.maze[point[1]][point[0]] &= ~0b11110000

    def is_visited(self, point: tuple[int, int]) -> bool:
        return bool(self.maze[point[1]][point[0]] & 0b10000)

    def is_connected(self, point: tuple[int, int]) -> bool:
        return bool(self.maze[point[1]][point[0]] & 0b100000)

    def _solve_maze(self) -> str:
        ...


    def write_to_file(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for row in self.maze:
                line = ''.join(f"{cell & 0b1111:X}" for cell in row)
                f.write(line + '\n')



