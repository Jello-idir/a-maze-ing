from mazegen import WindowManager, MazeMenu, MazeFrame
from mazegen import MazeConfig
from dataclasses import dataclass

@dataclass
class cfg_clr:
    cell_color: int
    wall_color: int
    menu_color: int
    grid_bg_color: int
    grid_lines_color: int

@dataclass
class cfg_size:
    padding: int
    cell_size: int
    wall_size: int

@dataclass
class cfg_all:
    config: MazeConfig
    colors: cfg_clr
    sizes: cfg_size


def load_maze_from_file() -> list[tuple[int, int, int]]:
    # in the file each cell is hex just 0-f representing the 4-bit wall bitmask, and cells are not separated by spaces, but by newlines. So we read the file line by line, and for each line we read each character and convert it to an int, and store it in a list of tuples (x, y, val) where x and y are the coordinates of the cell and val is the wall bitmask.
    maze_file = open("maze.txt", "r")
    cells = []
    y = 0
    for line in maze_file:
        line = line.strip()
        for x, ch in enumerate(line):
            val = int(ch, 16)  # convert hex char to int
            cells.append((x, y, val))
        y += 1
    return cells


if __name__ == "__main__":
    cfg_file = open("config.txt", "r")
    config = MazeConfig.from_file(cfg_file)

    colors = cfg_clr(
        cell_color=(0x2F2F2F << 8) | 0xFF,
        wall_color=(0xFFFFFF << 8) | 0xFF,
        menu_color=(0x105CB3 << 8) | 0xFF,
        grid_bg_color=(0x000000 << 8) | 0xFF,
        grid_lines_color=(0x141414 << 8) | 0xFF,
    )

    sizes = cfg_size(
        cell_size=32,
        wall_size=3,
        padding=10,
    )

    cfg = cfg_all(config, colors, sizes)

    test_maze = WindowManager(cfg)

    test_maze.frame.fill_frame(colors.grid_bg_color)

    init_cells = [(x, y, 0b1111) for y in range(config.height) for x in range(config.width)]

    file_test_cells = load_maze_from_file()
    test_maze.frame.draw_cells(cfg, file_test_cells)

    test_maze.render()
