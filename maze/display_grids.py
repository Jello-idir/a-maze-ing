from typing import IO
from maze import Cell
from common.enums import GColor

def display_maze(cell: Cell) -> None:
    curr_row = cell
    while (curr_row):
        curr_cell = curr_row
        while (curr_cell):
            all_neighbors = [curr_cell.top, curr_cell.right, curr_cell.bottom, curr_cell.left]
            output = [" ↑ ", " → ", " ↓ ", " ← "]
            neighbor = curr_cell.neighbor
            if curr_cell.is_origin:
                print(f"{GColor.RED.value} * {GColor.DEFAULT.value}", end="")
            else:
                for cmp_neigh, out in zip(all_neighbors, output):
                    if cmp_neigh and neighbor:
                        if neighbor == cmp_neigh:
                            print(out, end="")
            curr_cell = curr_cell.right
        print("\n")
        curr_row = curr_row.bottom

def write_maze(cell: Cell, output_file: IO) -> None:
    curr_row: Cell = cell
    while (curr_row):
        curr_cell: Cell = curr_row
        while (curr_cell):
            if curr_cell.neighbor and curr_cell.neighbor == curr_cell.right:
                print("→", end="", file=output_file)
            elif curr_cell.neighbor and curr_cell.neighbor == curr_cell.left:
                print("←", end="", file=output_file)
            elif curr_cell.neighbor and curr_cell.neighbor == curr_cell.top:
                print("↑", end="", file=output_file)
            elif curr_cell.neighbor and curr_cell.neighbor == curr_cell.bottom:
                print("↓", end="", file=output_file)
            curr_cell = curr_cell.right
        print(file=output_file)
        curr_row = curr_row.bottom
