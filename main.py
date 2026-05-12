from mazegen import MlxWindow, MazeMenu, MazeFrame, MazeConfig, ColorConfig, SizeConfig, Config
import tomllib
import os


def load_maze_from_file() -> list[tuple[int, int, int]]:
    maze_file = open("maze.txt", "r")
    cells = []
    y = 0
    for line in maze_file:
        line = line.strip()
        for x, ch in enumerate(line):
            val = int(ch, 16)
            cells.append((x, y, val))
        y += 1
    return cells


def load_colors_from_file(pallet_path: str) -> ColorConfig:
    """ loads the colors from a toml file and returns a ColorConfig object

    Args:
        pallet_path (str): the path to the toml file containing the colors

    Returns:
        ColorConfig: a ColorConfig object containing the colors
    """

    # the path is relative, so we need to get the absolute path
    pallates_dir = os.path.join(os.path.dirname(__file__), "mazegen/palettes")
    pallet_path = os.path.join(pallates_dir, pallet_path)
    with open(pallet_path, "rb") as f:
        raw = tomllib.load(f)

    # adding the opacity byte
    for key, val in raw["maze_colors"].items():
        raw["maze_colors"][key] = val << 8 | 0xff

    return ColorConfig(**raw["maze_colors"])



if __name__ == "__main__":

    # config
    # -------------------------
    cfg_file = open("config.txt", "r")
    config = MazeConfig.from_file(cfg_file)

    colors = load_colors_from_file("default.toml")

    sizes = SizeConfig(
        cell=32,
        wall=3,
        padd=10,
    )

    cfg = Config(config, colors, sizes)


    # test file
    # -------------------------
    file_maze = load_maze_from_file()


    # init
    # -------------------------
    window = MlxWindow(cfg)
    window.frame.gridify()
    window.menu.decorate()

    window.frame.draw_cells(file_maze)


    window.render()
