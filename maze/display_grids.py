from maze import Cell

def display_maze(cell: Cell) -> None:
    curr_row = cell
    while (curr_row):
        curr_cell = curr_row
        while (curr_cell):
            if curr_cell.neighbor and curr_cell.neighbor == curr_cell.right:
                print(" → ", end="")
            elif curr_cell.neighbor and curr_cell.neighbor == curr_cell.left:
                print(" ← ", end="")
            elif curr_cell.neighbor and curr_cell.neighbor == curr_cell.top:
                print(" ↑ ", end="")
            elif curr_cell.neighbor and curr_cell.neighbor == curr_cell.bottom:
                print(" ↓ ", end="")
            else:
                print("\033[31m * \033[37m")
            curr_cell = curr_cell.right
        print("\n")
        curr_row = curr_row.bottom

def write_maze(cell, output_file) -> None:
    curr_row = cell
    while (curr_row):
        curr_cell = curr_row
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
