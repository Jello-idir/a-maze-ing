from maze import Cell
import random

class MazeGenerator():

    def __init__(self) -> None:
        self.origin: Cell = None
        self.tmp_origin: Cell = None

    def initialize_grid(self, width: int, height: int) -> None:
        top_row = None
        first = True
        while (height):
            curr_row = Cell()
            if first:
                self.origin = curr_row
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

    def initial_maze(self):
        curr_row: Cell = self.origin

        while (curr_row):
            curr_cell: Cell = curr_row

            while curr_cell:
                curr_cell.neighbor = curr_cell.right
                if not curr_cell.neighbor:
                    curr_cell.neighbor = curr_cell.bottom
                if not curr_cell.bottom and not curr_cell.right:
                    self.tmp_origin = curr_cell
                curr_cell.is_origin = False
                curr_cell = curr_cell.right
                if curr_cell:
                    curr_cell.is_origin = True
            curr_row = curr_row.bottom

    ## main algo for generation
    def update_all_walls(self):
        curr_row: Cell = self.origin

        while (curr_row):
            curr_cell: Cell = curr_row

            while curr_cell:
                curr_cell.update_walls()
                curr_cell = curr_cell.right
            curr_row = curr_row.bottom

    def origin_shift(self, seed: float):
        origin = self.tmp_origin
        while seed > 0:
            random.seed(seed)
            all_choice = [origin.top, origin.right, origin.bottom, origin.left]
            origin.neighbor = random.choice(all_choice)
            while not origin.neighbor:
                origin.neighbor = random.choice(all_choice)
            while origin.neighbor.neighbor and origin.neighbor == origin.neighbor.neighbor:
                origin.neighbor = random.choice(all_choice)

            origin.is_origin = False
            self.update_all_walls()

            origin = origin.neighbor
            origin.is_origin = True
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
