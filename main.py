import os
import sys
import tomllib
from MLX.libmlx import mlx
from mazegen import MazeGenerator, MlxWindow, MazeConfig, ColorConfig, SizeConfig, Config


color_pallets = ["blue.toml", "green.toml", "orange.toml"]

def load_color(pallet_path: str) -> ColorConfig:
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


show_path = False


def start(param) -> None:
    global show_path
    if (window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 256)
        or mlx.mlx_is_key_down(window.mlx_ptr, 81) ):   # ESC or Q
        mlx.mlx_close_window(window.mlx_ptr)

    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 82):   # R
        generator.initialize()
        generator.wilson_algo()
        generator.a_star()
        window.frame.draw_cells(generator.get_maze(), show_path=show_path)

    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 72):   # H
        show_path = not show_path
        window.frame.draw_cells(generator.get_maze(), show_path=show_path)

    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 67):   # C
        window.use_color(load_color("green.toml"))
        window.frame.draw_cells(generator.get_maze(), show_path=show_path)

def init_config() -> Config:
    cfg_file = open("config.txt", "r")
    config = MazeConfig.from_file(cfg_file)
    colors = load_color("blue.toml")
    sizes = SizeConfig(
        cell=32,
        wall=3,
        padd=10,
    )
    return Config(config, colors, sizes)


if __name__ == "__main__":
    global window
    global generator

    try:
        cfg = init_config()
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        exit(1)

    try:
        generator = MazeGenerator.from_object(cfg.config)
    except Exception as e:
        print(f"Error initializing maze generator: {e}", file=sys.stderr)
        exit(1)

    try:
        window = MlxWindow(cfg)
    except Exception as e:
        print(f"Error initializing window: {e}", file=sys.stderr)
        exit(1)

    try:
        generator.initialize()
        generator.wilson_algo()
        generator.a_star()
        window.start(generator.get_maze(), start)
    except Exception as e:
        print(f"Error starting window: {e}", file=sys.stderr)
        exit(1)
