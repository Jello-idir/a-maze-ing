# ============================================================================
# Codam Coding College, Amsterdam 2018-2025, All Rights Reserved.
# See README in the root project for more information.
# ============================================================================

import signal
import logging
import random
from MLX.libmlx import *

# ============================================================================

WIDTH = 1024
HEIGHT = 480

# ============================================================================

def hexcolor(color: int, alpha: int):
    """add alpha to the the color"""
    return (color << 8) | (alpha & 0xFF)

def fill(image, color):
    for i in range(image.contents.width):
        for y in range(image.contents.height):
            mlx.mlx_put_pixel(image, i, y, color)

@mlx_loop_hook_func
def ft_hook(param):
    mlx_ptr = ctypes.cast(param, ctypes.POINTER(mlx_t))
    if mlx.mlx_is_key_down(mlx_ptr, MLX_KEY_ESCAPE):
        mlx.mlx_close_window(mlx_ptr)
    if mlx.mlx_is_key_down(mlx_ptr, MLX_KEY_UP):
        image.contents.instances[0].y -= 5
    if mlx.mlx_is_key_down(mlx_ptr, MLX_KEY_DOWN):
        image.contents.instances[0].y += 5
    if mlx.mlx_is_key_down(mlx_ptr, MLX_KEY_LEFT):
        image.contents.instances[0].x -= 5
    if mlx.mlx_is_key_down(mlx_ptr, MLX_KEY_RIGHT):
        image.contents.instances[0].x += 5

def main():
    # Better to encapsulate in a class, but keeping it simple for the example
    global image
    global mlx_ptr

    # Initialize MLX
    mlx_ptr = mlx.mlx_init(WIDTH, HEIGHT, b"a-maze-ing", True)
    if not mlx_ptr:
        logging.critical(f"Error: {mlx.mlx_strerror(mlx.mlx_get_errno()).decode()}")
        exit(1)

    # Create a new image
    image = mlx.mlx_new_image(mlx_ptr, WIDTH, HEIGHT)
    if not image:
        mlx.mlx_close_window(mlx_ptr)
        logging.critical(f"Error: {mlx.mlx_strerror(mlx.mlx_get_errno()).decode()}")
        exit(1)

    # Display the image in the window
    if mlx.mlx_image_to_window(mlx_ptr, image, 0, 0) == -1:
        mlx.mlx_delete_image(mlx_ptr, image)
        mlx.mlx_close_window(mlx_ptr)
        exit(1)

    fill(image, hexcolor(0x000000, 0xFF))
    mlx.mlx_loop_hook(mlx_ptr, ft_hook, ctypes.cast(mlx_ptr, c_void_p))

    mlx.mlx_loop(mlx_ptr)
    mlx.mlx_terminate(mlx_ptr)


def signal_handler(sig, frame):
    mlx.mlx_terminate(mlx_ptr)

# ============================================================================

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
