from .MazeConfig import MazeConfig
from MLX.libmlx import *
from typing import Any
import ctypes


# def fill_image(img_ptr, color: int) -> None:
#     img = img_ptr.contents
#     pixels = img.pixels
#     r = (color >> 24) & 0xFF
#     g = (color >> 16) & 0xFF
#     b = (color >> 8 ) & 0xFF
#     a = (color      ) & 0xFF
#     for y in range(img.height):
#         for x in range(img.width):
#             idx = (y * img.width + x) * 4
#             pixels[idx]     = r
#             pixels[idx + 1] = g
#             pixels[idx + 2] = b
#             pixels[idx + 3] = a

class MazeMenu:
    def __init__(self, mlx_ptr, cfg, abs_width, abs_height) -> None:
        self.cfg = cfg
        self.width = abs_width
        self.height = abs_height
        self.img = mlx.mlx_new_image(mlx_ptr, abs_width, abs_height)

    def decorate(self) -> None:
        # filling the manu with the menu color
        img = self.img.contents
        pixels = img.pixels
        menu_color = self.cfg.colors.menu
        for y in range(img.height):
            for x in range(img.width):
                idx = (y * img.width + x) * 4
                pixels[idx]     = (menu_color >> 24) & 0xFF
                pixels[idx + 1] = (menu_color >> 16) & 0xFF
                pixels[idx + 2] = (menu_color >> 8 ) & 0xFF
                pixels[idx + 3] = (menu_color      ) & 0xFF

        # drawing the border
        border_color = self.cfg.colors.wall
        # border_color = 0xff0000ff

        thick = self.cfg.sizes.wall

        # drawing horizental lines
        for side in (0, img.height - thick):
            for t in range(thick):
                for x in range(img.width):
                    idx = ((t + side) * img.width + x) * 4
                    pixels[idx]     = (border_color >> 24) & 0xFF
                    pixels[idx + 1] = (border_color >> 16) & 0xFF
                    pixels[idx + 2] = (border_color >> 8 ) & 0xFF
                    pixels[idx + 3] = (border_color      ) & 0xFF
        # drawing vertical lines
        for side in (0,):
            for y in range(img.height):
                for t in range(thick):
                    idx = (y * img.width) * 4
                    pixels[idx]     = (border_color >> 24) & 0xFF
                    pixels[idx + 1] = (border_color >> 16) & 0xFF
                    pixels[idx + 2] = (border_color >> 8 ) & 0xFF
                    pixels[idx + 3] = (border_color      ) & 0xFF
                return

class MazeFrame:
    def __init__(self, mlx_ptr, cfg, width, height) -> None:
        self.cfg = cfg
        self.img = mlx.mlx_new_image(
            mlx_ptr,
            width  * self.cfg.sizes.cell + self.cfg.sizes.wall,
            height * self.cfg.sizes.cell + self.cfg.sizes.wall
        )

    def gridify(self) -> None:
        img = self.img.contents
        pixels = img.pixels
        cell = self.cfg.sizes.cell
        thick = self.cfg.sizes.wall
        grid_color = self.cfg.colors.grid
        bg_grid_color = self.cfg.colors.bg_grid

        for y in range(img.height):
            for x in range(img.width):
                idx = (y * img.width + x) * 4
                if (x % cell) < thick or (y % cell) < thick:
                    pixels[idx]     = (grid_color >> 24) & 0xFF
                    pixels[idx + 1] = (grid_color >> 16) & 0xFF
                    pixels[idx + 2] = (grid_color >> 8 ) & 0xFF
                    pixels[idx + 3] = (grid_color      ) & 0xFF
                else:
                    pixels[idx]     = (bg_grid_color >> 24) & 0xFF
                    pixels[idx + 1] = (bg_grid_color >> 16) & 0xFF
                    pixels[idx + 2] = (bg_grid_color >> 8 ) & 0xFF
                    pixels[idx + 3] = (bg_grid_color      ) & 0xFF

    def draw_cells(self, cells: list[tuple[int, int, int]]) -> None:
        img = self.img.contents
        pixels = img.pixels
        cell = self.cfg.sizes.cell
        thick = self.cfg.sizes.wall

        def put(px, py, color):
            if 0 <= px < img.width and 0 <= py < img.height:
                idx = (py * img.width + px) * 4
                pixels[idx]     = (color >> 24) & 0xFF
                pixels[idx + 1] = (color >> 16) & 0xFF
                pixels[idx + 2] = (color >> 8 ) & 0xFF
                pixels[idx + 3] = (color      ) & 0xFF

        for x, y, val in cells:
            ox = x * cell
            oy = y * cell
            color = self.cfg.colors.cell
            wall_color = self.cfg.colors.wall

            if (val & 0b1111) == 0b1111:
                color = self.cfg.colors.block

            for j in range(thick, cell):
                for i in range(thick, cell):
                    put(ox + i, oy + j, color)

            if val & 0b0001:
                for j in range(thick):
                    for i in range(cell + thick):
                        put(ox + i, oy + j, wall_color)

            if val & 0b0010:
                for j in range(cell + thick):
                    for i in range(thick):
                        put(ox + cell + i, oy + j, wall_color)

            if val & 0b0100:
                for j in range(thick):
                    for i in range(cell + thick):
                        put(ox + i, oy + cell + j, wall_color)

            if val & 0b1000:
                for j in range(cell + thick):
                    for i in range(thick):
                        put(ox + i, oy + j, wall_color)



class MlxWindow:
    def __init__(self, cfg) -> None:
        frame_size = (
            cfg.config.width  * cfg.sizes.cell + cfg.sizes.wall,
            cfg.config.height * cfg.sizes.cell + cfg.sizes.wall
        )
        menu_size = (
            200,
            max(frame_size[1], 400)
        )

        self.mlx_ptr = mlx.mlx_init(
            frame_size[0] + menu_size[0],
            max(menu_size[1], 400),
            b"A-Maze-Ing", False
        )
        self.frame = MazeFrame(
            self.mlx_ptr,
            cfg,
            cfg.config.width,
            cfg.config.height
        )
        self.menu = MazeMenu(
            self.mlx_ptr,
            cfg,
            menu_size[0],
            menu_size[1]
        )

    def render(self, func) -> None:
        mlx.mlx_image_to_window(self.mlx_ptr, self.frame.img, 0, 0)
        mlx.mlx_image_to_window(self.mlx_ptr, self.menu.img, self.frame.img.contents.width, 0)


        f = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(func)

        mlx.mlx_loop_hook(self.mlx_ptr, f, None)
        mlx.mlx_loop(self.mlx_ptr)
        mlx.mlx_terminate(self.mlx_ptr)
