from maze import Cell
from random import choice

class MazeGenerator():
    def __init__(self) -> None:
        pass

    def initialize_grid(self, width: int, height: int) -> Cell:
        origin: Cell = None

        top_row = None
        first = True
        id = 100
        while (height):
            curr_row = Cell(id)
            if first:
                origin = curr_row
                first = False

            row_width = width - 1
            curr_cell = curr_row
            while (row_width):
                new_cell = Cell(id)

                curr_cell.right = new_cell
                new_cell.left = curr_cell
                curr_cell.top = top_row

                if top_row:
                    top_row.bottom = curr_cell

                top_row = top_row.right if top_row else None

                curr_cell = curr_cell.right
                row_width -= 1
                id += 1
            curr_cell.top = top_row
            if top_row:
                    top_row.bottom = curr_cell
            top_row = curr_row
            height -= 1

        return origin


    def initial_maze(self, cell: Cell) -> Cell:
        curr_row: Cell = cell

        while (curr_row):
            curr_cell: Cell = curr_row

            while curr_cell:
                curr_cell.neighbor = curr_cell.right
                if not curr_cell.neighbor:
                    curr_cell.neighbor = curr_cell.bottom
                if not curr_cell.bottom and not curr_cell.right:
                    origin = curr_cell
                curr_cell.update_walls()
                curr_cell = curr_cell.right
            curr_row = curr_row.bottom
        return origin

    ## main algo for generation
    def origin_shift(self, origin: Cell, seed: float):

        while seed > 0:
            all_choice = [origin.top, origin.right, origin.bottom, origin.left]
            origin.neighbor = choice(all_choice)
            while not origin.neighbor:
                origin.neighbor = choice(all_choice)
            while origin.neighbor.neighbor and origin.neighbor == origin.neighbor.neighbor:
                origin.neighbor = choice(all_choice)

            origin = origin.neighbor
            origin.update_walls()
            seed -= 0.001

    def generate_output_file(self, cell: Cell, filename: str) -> None:
        curr_row = cell
        with open(filename, 'w') as output_f:
            while (curr_row):
                curr_cell = curr_row
                while (curr_cell):
                    print("0123456789ABCDEF"[curr_cell.hex], end="", file=output_f)
                    curr_cell = curr_cell.right
                print(file=output_f)
                curr_row = curr_row.bottom
