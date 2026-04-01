from helper import Cell


def initialize_grid(width: int, height: int) -> Cell:
    origin: Cell = None

    top_row = None
    first = True
    while (height):
        curr_row = Cell()
        if first:
            origin = curr_row
            first = False

        row_width = width - 1
        curr_cell = curr_row
        while (row_width):
            new_cell = Cell()

            curr_cell.right = new_cell
            new_cell.left = curr_cell
            curr_cell.top = top_row

            if top_row:
                top_row.bottom = curr_cell

            top_row = top_row.right if top_row else None

            curr_cell = curr_cell.right
            row_width -= 1
        curr_cell.top = top_row
        if top_row:
                top_row.bottom = curr_cell
        top_row = curr_row
        height -= 1

    return origin

from random import choice
def origin_shift(origin: Cell, seed: float):

    while seed > 0:
        all_choice = [origin.top, origin.right, origin.bottom, origin.left]
        print(seed)
        origin.neighbor = choice(all_choice)
        while not origin.neighbor:
            origin.neighbor = choice(all_choice)
        while origin.neighbor.neighbor and origin.neighbor == origin.neighbor.neighbor:
            origin.neighbor = choice(all_choice)


        if origin.neighbor == origin.right or origin.neighbor == origin.left:
            origin.north = True
            origin.south = True
            if origin.neighbor == origin.right:
                origin.east = False
            else:
                origin.west = False

        elif origin.neighbor == origin.top or origin.neighbor == origin.bottom:
            origin.east = True
            origin.west = True
            if origin.neighbor == origin.top:
                origin.north = False
            else:
                origin.south = False
        



        origin.is_origin = False
        origin = origin.neighbor
        origin.is_origin = True
        seed -= 0.01

    pass


def initial_maze(cell) -> Cell:
    # - - - - - - |
    # - - - - - - |
    # - - - - - - |
    # - - - - - - |
    # - - - - - - +
    # + be the origin all nodes if moving forward it go to origin
    curr_row: Cell = cell
    while (curr_row):
        curr_cell: Cell = curr_row
        while curr_cell:
            curr_cell.neighbor = curr_cell.right
            if not curr_cell.neighbor:
                curr_cell.neighbor = curr_cell.bottom
            if not curr_cell.bottom and not curr_cell.right:
                origin = curr_cell
            curr_cell = curr_cell.right
        curr_row = curr_row.bottom
    return origin


def display_grid(cell: Cell) -> None:
    curr_row = cell
    # print("\n" * 50)
    while (curr_row):
        curr_cell = curr_row
        while (curr_cell):
            if curr_cell.is_origin:
                print(" 0 ", end="")
            elif curr_cell.neighbor and curr_cell.neighbor == curr_cell.right:
                print(" → ", end="")
            elif curr_cell.neighbor and curr_cell.neighbor == curr_cell.left:
                print(" ← ", end="")
            elif curr_cell.neighbor and curr_cell.neighbor == curr_cell.top:
                print(" ↑ ", end="")
            elif curr_cell.neighbor and curr_cell.neighbor == curr_cell.bottom:
                print(" ↓ ", end="")
            else:
                print("\033[31m * \033[37m")

            # print(f" {curr_cell.value} ", end="")
            curr_cell = curr_cell.right
        print("\n")
        curr_row = curr_row.bottom





if __name__ == "__main__":
    # fd = sys.stdin.fileno()
    # old = termios.tcgetattr(fd)
    cell = initialize_grid(10, 10)
    origin = initial_maze(cell)
    origin_shift(origin, 3)
    display_grid(cell)

    # try:
    # 	# move_in_grid(cell)
    # except Exception:
    # 	print("\033[31m Error\033[0m")



# import termios
# import tty
# import sys

# def get_key() -> str:

# 	try:
# 		tty.setraw(fd)
# 		key = sys.stdin.read(1)
# 	finally:
# 		termios.tcsetattr(fd, termios.TCSADRAIN, old)
# 	return key

# def move_in_grid(cell: Cell):

# 	origin = cell
# 	while(True):
# 		cell.value = "X"
# 		display_grid(origin)
# 		cell.value = "."
# 		key = get_key()
# 		if key == 'w':
# 			print("up")
# 			cell = cell.top
# 		elif key == 'd':
# 			print("right")
# 			cell = cell.right
# 		elif key == 's':
# 			print("down")
# 			cell = cell.bottom
# 		elif key == 'a':
# 			print("left")
# 			cell = cell.left
# 		else:
# 			break

# class dir(Enum):
# 	N = 0
# 	E = 1
# 	S = 2
# 	W = 3


# self.hex: int = 1
# 0000
# 0010

# def open_east:
# 	if self.hex >> dir.E & 1 == 1:
# 		self.hex = self.hex - 2

# def close_east:
# 	if self.hex >> dir.W & 1 == 0:
# 		self.hex = self.hex
