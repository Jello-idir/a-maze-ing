from mazegen import MlxWindow, MazeConfig, ColorConfig, SizeConfig, Config
from MLX.libmlx import mlx
import tomllib
import os


def load_maze_from_file(file) -> list[tuple[int, int, int]]:
    maze_file = open(str(file), "r")
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


def hooker_test(param) -> None:
    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 256):  # ESC
        mlx.mlx_close_window(window.mlx_ptr)
    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 82):   # R
        window.frame.draw_cells(load_maze_from_file(2))
    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 83):   # S
        window.frame.gridify()
    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 84):   # T
        ...
    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 85):   # U
        ...
    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 86):   # V
        ...
    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 87):   # W
        ...
    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 88):   # X
        ...


if __name__ == "__main__":
    global window

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
    file_maze = load_maze_from_file(1)


    # init
    # -------------------------
    window = MlxWindow(cfg)
    window.render(file_maze, hooker_test)
