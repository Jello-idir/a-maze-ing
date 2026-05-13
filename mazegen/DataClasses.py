from dataclasses import dataclass
from .MazeConfig import MazeConfig


@dataclass
class ColorConfig:
    cell: int
    wall: int
    block: int
    visited: int
    path: int
    menu: int
    grid: int
    bg_grid: int
    entry: int
    exit: int


@dataclass
class SizeConfig:
    padd: int
    cell: int
    wall: int


@dataclass
class Config:
    config: MazeConfig
    colors: ColorConfig
    sizes: SizeConfig
