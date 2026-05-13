import os
import sys
import tomllib
from MLX.libmlx import mlx
from mazegen import (
    MazeGenerator, MlxWindow,
    MazeConfig, ColorConfig,
    SizeConfig, Config
    )


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


def color_generator():
    """ returns a generator that each time it is called,
    it returns a color pallet from the color_pallets list in a loop

    Returns:
        generator: a generator that each time it is called,
        it returns a color pallet from the color_pallets list in a loop
    """
    color_pallets = ["blue.toml", "green.toml", "orange.toml"]
    while True:
        for pallet in color_pallets:
            yield load_color(pallet)


show_path = False
clr_gen = color_generator()


def start(param) -> None:
    global show_path

    if (window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 256)
            or mlx.mlx_is_key_down(window.mlx_ptr, 81)):
        mlx.mlx_close_window(window.mlx_ptr)

    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 82):
        generator.init()
        generator.generation_algo()
        generator.a_star()
        window.frame.draw_cells(generator.get_maze(), show_path=show_path)

    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 72):
        show_path = not show_path
        window.frame.draw_cells(generator.get_maze(), show_path=show_path)

    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 67):
        window.use_color(next(clr_gen))
        window.frame.draw_cells(generator.get_maze(), show_path=show_path)
        window.menu.decorate()

    if window.mlx_ptr and mlx.mlx_is_key_down(window.mlx_ptr, 87):
        try:
            generator.write_to_file(window.cfg.config.output_file)
        except Exception as e:
            print(f"\033[31mError writing to file:\033[0m {e}")


def init_config() -> Config:
    cfg_file = open("config.txt", "r")
    config = MazeConfig.from_file(cfg_file)
    colors = next(clr_gen)
    sizes = SizeConfig(
        cell=32,
        wall=4,
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
        generator.init()
        generator.generation_algo()
        generator.a_star()
        print("Quit: ESC or Q",
              "Regenerate: R",
              "Show/Hide Path: H",
              "Change Color: C",
              "Write to File: W",
              sep="\n")
        window.start(generator.get_maze(), start)
    except Exception as e:
        print(f"Error starting window: {e}", file=sys.stderr)
        exit(1)
