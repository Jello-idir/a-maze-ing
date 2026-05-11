from .MazeConfig import MazeConfig
from MLX.libmlx import *
from typing import Any
import ctypes

def fill_image(img_ptr, color: int) -> None:
    img = img_ptr.contents
    pixels = img.pixels
    r = (color >> 24) & 0xFF
    g = (color >> 16) & 0xFF
    b = (color >> 8 ) & 0xFF
    a = (color      ) & 0xFF
    for y in range(img.height):
        for x in range(img.width):
            idx = (y * img.width + x) * 4
            pixels[idx]     = r
            pixels[idx + 1] = g
            pixels[idx + 2] = b
            pixels[idx + 3] = a

class MazeMenu:
    def __init__(self, mlx_ptr, abs_width, abs_height) -> None:
        self.width = abs_width
        self.height = abs_height
        self.img = mlx.mlx_new_image(mlx_ptr, abs_width, abs_height)

    def fill_menu(self, color: int) -> None:
        fill_image(self.img, color)

class MazeFrame:
    def __init__(self, mlx_ptr, cfg, width, height) -> None:
        self.width = width
        self.height = height
        self.colors = cfg.colors
        self.sizes = cfg.sizes
        self.img = mlx.mlx_new_image(
            mlx_ptr,
            width  * self.sizes.cell_size + self.sizes.wall_size,
            height * self.sizes.cell_size + self.sizes.wall_size
        )

    def fill_frame(self, color: int) -> None:
        fill_image(self.img, color)

    def draw_cells(self, cfg, cells: list[tuple[int, int, int]]) -> None:
        img = self.img.contents
        pixels = img.pixels
        cell = self.sizes.cell_size
        thick = self.sizes.wall_size

        def put(px, py, color):
            if 0 <= px < img.width and 0 <= py < img.height:
                idx = (py * img.width + px) * 4
                pixels[idx]     = (color >> 24) & 0xFF
                pixels[idx + 1] = (color >> 16) & 0xFF
                pixels[idx + 2] = (color >> 8 ) & 0xFF
                pixels[idx + 3] = (color      ) & 0xFF

                # --- walls (bitmask: West=8, South=4, East=2, North=1) ---
        for x, y, val in cells:
            ox = x * cell  # pixel origin of this cell
            oy = y * cell
            color = self.colors.cell_color

            if val == 0b1111:
                color = self.colors.block_color

            # --- fill cell interior ---
            for j in range(thick, cell):
                for i in range(thick, cell):
                    put(ox + i, oy + j, color)

            # --- walls (bitmask: West=8, South=4, East=2, North=1) ---

            # North wall (top edge): horizontal bar
            if val & 0b0001:
                for j in range(thick):
                    for i in range(cell + thick):
                        put(ox + i, oy + j, self.colors.wall_color)

            # East wall (right edge): vertical bar
            if val & 0b0010:
                for j in range(cell + thick):
                    for i in range(thick):
                        put(ox + cell + i, oy + j, self.colors.wall_color)

            # South wall (bottom edge): horizontal bar
            if val & 0b0100:
                for j in range(thick):
                    for i in range(cell + thick):
                        put(ox + i, oy + cell + j, self.colors.wall_color)

            # West wall (left edge): vertical bar
            if val & 0b1000:
                for j in range(cell + thick):
                    for i in range(thick):
                        put(ox + i, oy + j, self.colors.wall_color)


class WindowManager:
    def __init__(self, cfg) -> None:
        self.mlx_ptr = mlx.mlx_init(
            cfg.config.width  * cfg.sizes.cell_size + cfg.sizes.wall_size,
            cfg.config.height * cfg.sizes.cell_size + cfg.sizes.wall_size,
            b"A-Maze-Ing", False
        )
        self.frame = MazeFrame(
            self.mlx_ptr,
            cfg,
            cfg.config.width,
            cfg.config.height
        )

    def render(self) -> None:
        mlx.mlx_image_to_window(self.mlx_ptr, self.frame.img, 0, 0)
        mlx.mlx_loop(self.mlx_ptr)
