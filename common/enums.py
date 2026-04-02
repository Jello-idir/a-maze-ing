# module for enums
from enum import Enum


class GColor(Enum):
    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"
    DEFAULT = "\033[39m"

    BLACK_BG   = "\033[40m"
    RED_BG     = "\033[41m"
    GREEN_BG   = "\033[42m"
    YELLOW_BG  = "\033[43m"
    BLUE_BG    = "\033[44m"
    MAGENTA_BG = "\033[45m"
    CYAN_BG    = "\033[46m"
    WHITE_BG   = "\033[47m"
    DEFAULT_BG = "\033[49m"


class Color(Enum):
    OPEN = "\033[48;2;30;35;50m"
    WALL = "\033[48;2;255;255;255m"
    CELL = "\033[48;2;30;50;80m"
    RESET = "\033[0m"
    BLOCK = "\033[48;2;0;100;200m"


class Block(Enum):
    OPEN = f"{Color.OPEN.value}  {Color.RESET.value}"
    WALL = f"{Color.WALL.value}  {Color.RESET.value}"
    CELL = f"{Color.CELL.value}    {Color.RESET.value}"
    BLOCK = f"{Color.BLOCK.value}    {Color.RESET.value}"


class Dir(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


class Action(Enum):
    OPEN = 0
    CLOSE = 1
