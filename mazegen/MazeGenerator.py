import termios
import sys
import random
import time
import tty
from collections.abc import Callable
from .AsciiMaze import AsciiMaze
from .MazeConfig import MazeConfig
from heapq import heappush, heappop


class MazeGenerator:
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int],
                 seed: int | None = None, perfect: bool = True,
                 output_file: str = "maze.txt",
                 already_valid: bool = False) -> None:
        """ initializes the MazeGenerator with the given parameters,

        Args:
            width (int): the width of the maze to generate
            height (int): the height of the maze to generate
            entry (tuple[int, int]): the coordinates of the entry point (x,y)
            exit (tuple[int, int]): the coordinates of the exit point (x,y)
            seed (int | None, optional): the seed for
            the random number generator,
            if None, it will be set to the current time.
            Defaults to None.
            perfect (bool, optional): whether to generate
            a perfect maze (no loops),
            or a non-perfect maze (with loops). Defaults to True.
            output_file (str, optional): the file to write the maze
            to when finished. Defaults to "maze.txt".
            already_valid (bool, optional): whether
            the parameters have already been validated,
            this is used when creating a MazeGenerator
            from a MazeConfig object,
            to avoid validating the parameters twice. Defaults to False.
        """
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
        self.solution: str = ""
        if seed is None:
            self.seed = int(time.time())
        random.seed(self.seed)
        if not already_valid:
            self._validate_params()

    @classmethod
    def from_object(cls, config: MazeConfig) -> 'MazeGenerator':
        """ creates a MazeGenerator from a configuration object,
        which should have the same attributes as the constructor parameters

        Args:
            config ('MazeConfig'): a configuration object with attributes:
            width, height, entry, exit, perfect, seed, output_file

        Returns:
            MazeGenerator: the generated maze
        """
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
        """ validates the parameters for maze generation,
        ensuring that the width and height are sufficient,

        Raises:
            ValueError: if the width or height are too small,
            or if the entry or exit points are out of bounds,
            or if the entry and exit points are the same
        """
        if self.w < 9 or self.h < 7:
            raise ValueError("Width and height must be at least 9 and 7")
        if not (0 <= self.entry[0] < self.w and 0 <= self.entry[1] < self.h):
            raise ValueError("Entry coordinates out of bounds")
        if not (0 <= self.exit[0] < self.w and 0 < self.exit[1] <= self.h):
            raise ValueError("Exit coordinates out of bounds")
        if self.entry == self.exit:
            raise ValueError("Entry and exit cannot be the same point")

    def write_to_file(self, filename: str) -> None:
        """ writes the generated maze to a file in the specified format,

        Args:
            filename (str): the name of the file to write the maze to
        """
        with open(filename, 'w') as f:
            for row in self.maze:
                line = ''.join(f"{cell & 0b1111:X}" for cell in row)
                f.write(line + '\n')
            f.write("\n")
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")
            f.write(self.solution + '\n')

    def intialize(self) -> None:
        """generates the maze by initializing it,
        adding the 42 pattern, marking the entry and exit,
        """
        self.maze = [[15 for _ in range(self.w)] for _ in range(self.h)]
        for i in range(self.w):
            self.maze[0][i] |= 0b0001
            self.maze[self.h - 1][i] |= 0b0100
        for i in range(self.h):
            self.maze[i][0] |= 0b1000
            self.maze[i][self.w - 1] |= 0b0010

        self.maze[self.entry[1]][self.entry[0]] |= 0b10000000
        self.maze[self.entry[1]][self.entry[0]] |= 0b100000
        self.maze[self.exit[1]][self.exit[0]] |= 0b01000000
        self._add_42_pattern()

    def connect_ascii(self, ascii: AsciiMaze) -> None:
        """connects the maze generator to an AsciiMaze instance
        for visualization during generation and solving
        """
        if not isinstance(ascii, AsciiMaze):
            raise ValueError("Expected an instance of AsciiMaze")
        self.asciimaze = ascii

    def wilson_algo(self) -> None:
        """ generates the maze using Wilson's algorithm,
        which is a randomized algorithm
        """
        def wilson_path(start: tuple[int, int]) -> list[tuple[int, int]]:
            """ performs a random walk from the start point
            until it reaches a cell that is already part of the maze,

            Args:
                start (tuple[int, int]): the starting point of the random walk

            Returns:
                list[tuple[int, int]]: the path taken by the random walk,
                which will be carved into the maze
            """
            path: list[tuple[int, int]] = [start]
            self.maze[start[1]][start[0]] |= 0b10000
            p = start

            def random_neighbor(p: tuple[int, int]) -> tuple[int, int]:
                neighbors = []
                if (p[1] > 0
                        and self.maze[p[1] - 1][p[0]] >> 4 != 0b1111):
                    neighbors.append((p[0], p[1] - 1))
                if (p[0] < self.w - 1
                        and self.maze[p[1]][p[0] + 1] >> 4 != 0b1111):
                    neighbors.append((p[0] + 1, p[1]))
                if (p[1] < self.h - 1
                        and self.maze[p[1] + 1][p[0]] >> 4 != 0b1111):
                    neighbors.append((p[0], p[1] + 1))
                if (p[0] > 0
                        and self.maze[p[1]][p[0] - 1] >> 4 != 0b1111):
                    neighbors.append((p[0] - 1, p[1]))
                res = random.choice(neighbors)
                if res[0] == p[0]:
                    res = random.choice(neighbors)
                return res

            while True:
                p = random_neighbor(p)
                if p in path:
                    loop_start = path.index(p)
                    to_remove = path[loop_start + 1:]
                    path = path[:loop_start + 1]
                    for cell in to_remove:
                        self.maze[cell[1]][cell[0]] &= ~0b10000

                elif self.maze[p[1]][p[0]] >> 5 & 1:
                    path.append(p)
                    return path

                else:
                    path.append(p)
                    self.maze[p[1]][p[0]] |= 0b10000

        def carve_path(path: list[tuple[int, int]]) -> None:
            """ carves the path taken by the random walk
            into the maze by opening the walls

            Args:
                path (list[tuple[int, int]]): the path to carve into the maze
            """
            def get_neighbors(p: tuple[int, int]) -> list[tuple[int, int]]:
                """ returns the neighboring cells of a given cell
                that are not completely closed off,

                Args:
                    p (tuple[int, int]): the cell to get the neighbors of

                Returns:
                    list[tuple[int, int]]: the neighboring cells that
                    are not completely closed off
                """
                neighbors = []
                if p[1] > 0 and self.maze[p[1] - 1][p[0]] >> 4 != 0:
                    neighbors.append((p[0], p[1] - 1))
                if p[0] < self.w - 1 and self.maze[p[1]][p[0] + 1] >> 4 != 0:
                    neighbors.append((p[0] + 1, p[1]))
                if p[1] < self.h - 1 and self.maze[p[1] + 1][p[0]] >> 4 != 0:
                    neighbors.append((p[0], p[1] + 1))
                if p[0] > 0 and self.maze[p[1]][p[0] - 1] >> 4 != 0:
                    neighbors.append((p[0] - 1, p[1]))
                return neighbors

            def is_safe_to_break(p: tuple[int, int]) -> bool:
                """ checks if it's safe to break a wall at
                the given cell without creating a loop,

                Args:
                    p (tuple[int, int]): the cell to check

                Returns:
                    bool: True if safe to break a wall at the given cell,
                    False otherwise
                """
                neighbors = get_neighbors(p)
                if len(neighbors) != 4:
                    return False
                for n in neighbors:
                    if self.maze[n[1]][n[0]] >> 4 == 0b1111:
                        return False
                return True

            for i in range(len(path) - 1):
                p1, p2 = path[i], path[i + 1]
                self.maze[p1[1]][p1[0]] &= ~0b10000
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
            if (is_safe_to_break(p1)
                    and random.random() < 0.5
                    and not self.perfect):
                to_break = "NESW"
                self._change_wall(p1, random.choice(to_break), "open")

        unvisited = set((x, y) for x in range(self.w)
                        for y in range(self.h)
                        if not self.maze[y][x] >> 4 & 0b1)
        rpoint: tuple[int, int] = random.choice(list(unvisited))
        while True:
            if not unvisited:
                break
            while rpoint not in unvisited:
                rpoint = random.choice(list(unvisited))
            new_connected = wilson_path(rpoint)
            for point in new_connected:
                self.maze[point[1]][point[0]] |= 0b100000
            unvisited -= set(new_connected)
            carve_path(new_connected)

        for y in range(self.h):
            for x in range(self.w):
                self.maze[y][x] &= ~0b100000

        self.maze[self.entry[1]][self.entry[0]] |= 0b10000000
        self.maze[self.exit[1]][self.exit[0]] |= 0b01000000

        for y in range(self.h):
            for x in range(self.w):
                if self.maze[y][x] & 0b1111 == 0b1111:
                    self.maze[y][x] = 0b11111111

    def _add_42_pattern(self) -> None:
        """closes the walls in a pattern that resembles
        the 42 logo in the center of the maze
        """
        l42: list[tuple[int, int]] = [
            (0, 0), (0, 1), (0, 2), (1, 2),
            (2, 2), (2, 3), (2, 4), (2, 1),
            (2, 0), (4, 0), (5, 0), (6, 0),
            (6, 1), (6, 2), (5, 2), (4, 2),
            (4, 3), (4, 4), (5, 4), (6, 4)]

        for p in l42:
            p_offset: tuple[int, int] = (
                p[0] + round(self.w / 2) - 3,
                p[1] + round(self.h / 2) - 3
                )
            if p_offset in (self.entry, self.exit):
                raise ValueError("42 pattern overlaps entry or exit")
            self._change_wall(p_offset, "NESW", "close")
            self.maze[p_offset[1]][p_offset[0]] |= 0b11110000

    def _close(self, x: int, y: int, binary: int) -> None:
        """ closes the wall at the given coordinates
        by setting the corresponding bit in the maze grid

        Args:
            x (int): the x-coordinate of the cell to close the wall for
            y (int): the y-coordinate of the cell to close the wall for
            binary (int): the binary representation of the wall
            to close (1 for north, 2 for east, 4 for south, 8 for west)
        """
        self.maze[y][x] |= binary

    def _open(self, x: int, y: int, binary: int) -> None:
        """ opens the wall at the given coordinates

        Args:
            x (int): the x-coordinate of the cell to open the wall for
            y (int): the y-coordinate of the cell to open the wall for
            binary (int): the binary representation of the wall to open
        """
        self.maze[y][x] &= ~binary

    def _change_wall(self, p: tuple[int, int],
                     to_change: str, flag: str) -> None:
        """closes or opens the walls of a cell in the specified directions
        Args:
            point (tuple[int, int]): the coordinates of the cell
            to_change (str): a string containing the walls to modify
            flag (str): "close" to close the walls, "open" to open the walls
        """
        action: Callable[
            [int, int, int],
            None] = self._close if flag == "close" else self._open
        if 'N' in to_change:
            action(p[0], p[1], 0b0001)
            if p[1] > 0:
                action(p[0], p[1] - 1, 0b0100)
        if 'E' in to_change:
            action(p[0], p[1], 0b0010)
            if p[0] < self.w - 1:
                action(p[0] + 1, p[1], 0b1000)
        if 'S' in to_change:
            action(p[0], p[1], 0b0100)
            if p[1] < self.h - 1:
                action(p[0], p[1] + 1, 0b0001)
        if 'W' in to_change:
            action(p[0], p[1], 0b1000)
            if p[0] > 0:
                action(p[0] - 1, p[1], 0b0010)

    def render(self) -> None:
        """ renders the maze using the connected
        AsciiMaze instance, if available,
        """
        if self.asciimaze:
            self.asciimaze.render()

    def free_move(self) -> None:
        """gives the ability to move in the maze using WASD,
        it marks your position as path (|= 11000000) using termios
        """
        def display_menu(color: str) -> None:
            """ displays the menu for the free move mode,
            showing the controls and their descriptions

            Args:
                color (str): the color to use for the menu display
            """
            beff = "\033[1m"
            teff = "\033[3m"

            bclr = color + "\033[38;2;255;255;255m"
            rst = "\033[0m"

            print()
            print(
                f"{bclr}{beff} W {rst}|{bclr}{teff} Move Up {rst}  "
                f"{bclr}{beff} A {rst}|{bclr}{teff} Move Left {rst}  "
                f"{bclr}{beff} S {rst}|{bclr}{teff} Move Down {rst}  "
                f"{bclr}{beff} D {rst}|{bclr}{teff} Move Right {rst}  "
                )

        def read_key() -> str:
            """reads a single character from the user input without blocking
            """
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            except Exception as e:
                print(f"\033[31mError reading input:\033[0m {e}")
                ch = ""
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch.lower()

        pos = self.entry
        new_pos = pos
        color = self.asciimaze.clr["block"] if self.asciimaze else "\033[44m"
        while True:
            self.maze[new_pos[1]][new_pos[0]] |= 0b11000000
            sys.stdout.write("\033[H\033[J")
            self.render()
            display_menu(color)
            pos = new_pos
            if pos == self.exit:
                break
            key = read_key()
            if key in ('q', '\x03', 'm'):
                self.maze[pos[1]][pos[0]] &= ~0b11000000
                self.maze[self.entry[1]][self.entry[0]] |= 0b10000000
                self.maze[self.exit[1]][self.exit[0]] |= 0b01000000
                break
            elif key == 'w':
                if not self.maze[pos[1]][pos[0]] & 0b0001:
                    new_pos = (pos[0], pos[1] - 1)
            elif key == 'a':
                if not self.maze[pos[1]][pos[0]] & 0b1000:
                    new_pos = (pos[0] - 1, pos[1])
            elif key == 's':
                if not self.maze[pos[1]][pos[0]] & 0b0100:
                    new_pos = (pos[0], pos[1] + 1)
            elif key == 'd':
                if not self.maze[pos[1]][pos[0]] & 0b0010:
                    new_pos = (pos[0] + 1, pos[1])
            if pos == self.entry:
                self.maze[pos[1]][pos[0]] &= ~0b01000000
            elif pos == self.exit:
                self.maze[pos[1]][pos[0]] &= ~0b1000000
            else:
                self.maze[pos[1]][pos[0]] &= ~0b11000000

    def solve_maze(self, with_animation: bool) -> list[tuple[int, int]] | None:
        """ solves the maze using the A* algorithm,
        which is a pathfinding algorithm

        Args:
            with_animation (bool): whether to animate the solving
            process by rendering the maze at each step,

        Returns:
            list[tuple[int, int]] | None: the path from the entry
            to the exit as a list of coordinates,
        """
        start = self.entry
        end = self.exit

        def points_to_path(points: list[tuple[int, int]]) -> str:
            """ converts a list of coordinates
            representing a path through the maze

            Args:
                points (list[tuple[int, int]]): a list of
                coordinates representing a path through the maze

            Returns:
                str: a string representation of the path,
                where each character represents
            """
            path = ""
            for i in range(len(points) - 1):
                p1, p2 = points[i], points[i + 1]
                if p1[0] == p2[0]:
                    if p1[1] < p2[1]:
                        path += "S"
                    else:
                        path += "N"
                else:
                    if p1[0] < p2[0]:
                        path += "E"
                    else:
                        path += "W"
            return path

        def how_far(p: tuple[int, int]) -> int:
            """ calculates the Manhattan distance from
            the given point to the exit point,

            Args:
                p (tuple[int, int]): the point to calculate the distance from

            Returns:
                int: the Manhattan distance from
                the given point to the exit point
            """
            return abs(p[0] - end[0]) + abs(p[1] - end[1])

        def get_neighbors(p: tuple[int, int]) -> list[tuple[int, int]]:
            """ returns the neighboring cells of a given cell
            that are not blocked by walls,

            Args:
                p (tuple[int, int]): the cell to get the neighbors of

            Returns:
                list[tuple[int, int]]: the neighboring
                cells that are not blocked by walls
            """
            neighbors = []
            if not self.maze[p[1]][p[0]] & 0b0001 and p[1] > 0:
                neighbors.append((p[0], p[1] - 1))
            if not self.maze[p[1]][p[0]] & 0b0010 and p[0] < self.w - 1:
                neighbors.append((p[0] + 1, p[1]))
            if not self.maze[p[1]][p[0]] & 0b0100 and p[1] < self.h - 1:
                neighbors.append((p[0], p[1] + 1))
            if not self.maze[p[1]][p[0]] & 0b1000 and p[0] > 0:
                neighbors.append((p[0] - 1, p[1]))
            return neighbors

        heap = [(how_far(start), 0, start, [start])]
        visited: set[tuple[int, int]] = set()

        while heap:
            if with_animation:
                sys.stdout.write("\033[H\033[J")
                self.render()
            _, cost, point, path = heappop(heap)
            if point == end:
                for p in path:
                    self.maze[p[1]][p[0]] |= 0b11000000
                    if with_animation:
                        sys.stdout.write("\033[H\033[J")
                        self.render()
                        time.sleep(0.04)
                self.maze[start[1]][start[0]] &= ~0b01000000
                self.maze[end[1]][end[0]] &= ~0b10000000
                for p in visited:
                    self.maze[p[1]][p[0]] &= ~0b10000
                self.solution = points_to_path(path)
                return path
            if point in visited:
                continue
            visited.add(point)
            self.maze[point[1]][point[0]] |= 0b10000
            for neighbor in get_neighbors(point):
                if neighbor not in visited:
                    new_cost = cost + 1
                    heappush(heap, (
                        new_cost + how_far(neighbor),
                        new_cost,
                        neighbor,
                        path + [neighbor]
                    ))
            if with_animation:
                time.sleep(0.04)

        return None
