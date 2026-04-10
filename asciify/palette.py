import tomllib
from pathlib import Path
from typing import TextIO


def load_colors(fl: TextIO | None = None) -> dict[str, str]:
    if not fl:
        colors_path = Path(__file__).parent / "palettes/light.toml"
        with open(colors_path, "rb") as f:
            _data = tomllib.load(f)
    else:
        _data = tomllib.load(fl)

    def to_ansi(hex_color: str) -> str:
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"\033[48;2;{r};{g};{b}m"

    COLOR = {name: to_ansi(color) for name, color in _data["maze_colors"].items()}
    COLOR["reset"] = "\033[0m"

    return COLOR
