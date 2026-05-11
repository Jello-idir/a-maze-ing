from .MazeConfig import MazeConfig
from MLX.libmlx import *
from typing import Any
import ctypes


class MazeMenu:
    def __init__(self, mlx_ptr, width, height) -> None:
        self.width = width
        self.height = height
        self.img = mlx.mlx_new_image(mlx_ptr, width, height)
        self.options = ["Generate New Maze (R)", "Change Color (C)", "Solve Maze (S)",
                        "Toggle Path Display (H)", "Free Move (M)", "Write to File (W)", "Quit (Q)"]

    def fill_menu(self, color: int) -> None:
        img = self.img.contents
        pixels = img.pixels
        r = (color >> 24 ) & 0xFF
        g = (color >> 16 ) & 0xFF
        b = (color >> 8  ) & 0xFF
        a = (color       ) & 0xFF

        for y in range(img.height):
            for x in range(img.width):
                idx = (y * img.width + x) * 4
                pixels[idx]     = r
                pixels[idx + 1] = g
                pixels[idx + 2] = b
                pixels[idx + 3] = a


class MazeFrame:
    def __init__(self, mlx_ptr, width: int, height: int, cell_size: int) -> None:
        self.img = mlx.mlx_new_image(mlx_ptr, width, height)
        self.cell_size = cell_size
        if not self.img:
            raise ValueError("Failed to create frame")

    def gridify(self, color: int) -> None:
        img = self.img.contents
        pixels = img.pixels
        r = (color >> 24 ) & 0xFF
        g = (color >> 16 ) & 0xFF
        b = (color >> 8  ) & 0xFF
        a = (color       ) & 0xFF

        # draw vertical lines
        for x in range(0, img.width, self.cell_size):
            for y in range(img.height):
                idx = (y * img.width + x) * 4
                pixels[idx]     = r
                pixels[idx + 1] = g
                pixels[idx + 2] = b
                pixels[idx + 3] = a

        # draw horizontal lines
        for y in range(0, img.height, self.cell_size):
            for x in range(img.width):
                idx = (y * img.width + x) * 4
                pixels[idx]     = r
                pixels[idx + 1] = g
                pixels[idx + 2] = b
                pixels[idx + 3] = a

class WindowManager:
    def __init__(self, MazeConfig: MazeConfig) -> None:
        self.mwidth = 200
        self.fwidth = MazeConfig.width * 32
        self.fheight = MazeConfig.height * 32
        self.mlx = mlx.mlx_init(self.fwidth + self.mwidth,
                                self.fheight, b"a-maze-ing", True)
        if not self.mlx:
            raise ValueError("Failed to initialize MLX")

        self.frame = MazeFrame(self.mlx, self.fwidth, self.fheight, 32)
        self.menu = MazeMenu(self.mlx, self.mwidth, self.fheight)


    def render(self) -> None:
        mlx.mlx_image_to_window(self.mlx, self.frame.img, 0, 0)
        mlx.mlx_image_to_window(self.mlx, self.menu.img, self.fwidth, 0)
        mlx.mlx_loop(self.mlx)

# def put_pixel(img_ptr, x: int, y: int, r: int, g: int, b: int, a: int):
#     img = img_ptr.contents          # dereference the pointer -> mlx_image_t
#     idx = (y * img.width + x) * 4  # RGBA = 4 bytes per pixel
#     img.pixels[idx + 0] = r
#     img.pixels[idx + 1] = g
#     img.pixels[idx + 2] = b
#     img.pixels[idx + 3] = a
