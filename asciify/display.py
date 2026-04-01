#Each cell in the maze is written as a single hexadecimal digit,
# where the digit encodes the state of that cell's four walls as a 4-bit value.

# bit 0 = 1 → North wall closed
# bit 1 = 1 → East wall closed
# bit 2 = 0 → South wall open
# bit 3 = 0 → West wall open

from enum import Enum


class Block(Enum):
    OPEN = " "
    WALL = "█"
    CELL = "  "


class Color(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"


class Cell:
    def __init__(self, hex_value: str):
        self.hex_value = hex_value
        self.value = int(hex_value, 16)
        self.north = (self.value >> 0) & 1
        self.east = (self.value >> 1) & 1
        self.south = (self.value >> 2) & 1
        self.west = (self.value >> 3) & 1
        self.is_last = False

    def binary_repr(self) -> str:
        return f"{self.west}{self.south}{self.east}{self.north}"

    def closed_walls(self) -> list[str]:
        walls = []
        if self.north:
            walls.append("N")
        if self.east:
            walls.append("E")
        if self.south:
            walls.append("S")
        if self.west:
            walls.append("W")
        return walls

    
    def open_walls(self) -> list[str]:
        walls = []
        if not self.north:
            walls.append("N")
        if not self.east:
            walls.append("E")
        if not self.south:
            walls.append("S")
        if not self.west:
            walls.append("W")
        return walls


class Row:
    def __init__(self, cells: list[Cell]):
        self.cells = cells

    def print_row(self):
        # first print the north and south walls
        print(Block.WALL.value, end="")
        for cell in self.cells:
            print(Block.CELL.value, end="")
            if cell.east or cell.is_last:
                print(Block.WALL.value, end="")
            else:
                print(Block.OPEN.value, end="")
        print()

        # second print the south walls
        print(Block.WALL.value, end="")
        for cell in self.cells:
            print(Block.CELL.value, end="")
            if cell.east or cell.is_last: 
                print(Block.WALL.value, end="")
            else:
                print(Block.OPEN.value, end="")
        print()

        # third print the south walls
        print(Block.WALL.value, end="")
        for cell in self.cells:
            if cell.south:
                print(Block.WALL.value * 3, end="")
            elif cell.is_last:
                print(Block.OPEN.value * 2, end="")
                print(Block.WALL.value, end="")
            else:
                print(Block.OPEN.value * 2, end="")
                print(Block.WALL.value, end="")
        print()



    
    

def parse_instructions(instructions: str) -> list[list[Cell]]:
    cells: list[list[Cell]] = []

    lines = instructions.strip().splitlines()

    for line in lines:
        cell_row: list[Cell] = []
        for hex_digit in line.strip():
            cell_row.append(Cell(hex_digit))
        cells.append(cell_row)
        cell_row[-1].is_last = True
    return cells
            

def print_upper_wall(width: int):
    for _ in range(width):
        print(Block.WALL.value * 3, end="")
    print(Block.WALL.value)

# def ascii_cells(fd, instructions) -> None:


def print_maze(instructions: str) -> None:

    print()
    width = len(instructions.splitlines()[0])
    height = len(instructions.splitlines())
    cells = parse_instructions(instructions)
    print_upper_wall(width)
    rows = [Row(cell_row) for cell_row in cells]
    for row in rows:
        row.print_row()

    print()

def test():
    with open("maze_example.txt", "r") as f:
        instructions = f.read()

    print_maze(instructions)



if __name__ == "__main__":
    test()