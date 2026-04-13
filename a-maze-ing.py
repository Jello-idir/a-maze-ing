import sys
import time
from mazegen import MazeGenerator
from parsing import MazeConfig
from asciify import AsciiMaze
import termios
import tty

def get_config() -> MazeConfig:
    argc = len(sys.argv)
    if argc != 2:
        raise ValueError("Usage: python a-maze-ing.py <config_file>")
    try:
        with open(sys.argv[1]) as f:
            return MazeConfig.from_file(f)
    except FileNotFoundError:
        raise ValueError(f"Config file '{sys.argv[1]}' not found.")

def display_info(config: MazeConfig, color: str = "\033[30m") -> None:
    for key, value in config.get_config().items():
        print(f"{color}\033[1m {key.upper()} {value} \033[0m   ", end="", flush=True)
    print()



def read_key() -> str:
    """reads a single character from the user input without blocking
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    except Exception as e:
        print(f"\033[31mError reading input:\033[0m {e}")
        ch = ""
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch.lower()


def start(maze: MazeGenerator, mazeconfig: MazeConfig, mazeascii: AsciiMaze) -> None:
    while True:
        print("\n" * 50)
        display_info(mazeconfig, mazeascii.color["blok"])
        print()
        mazeascii.render_ints(maze.maze)
        key = read_key()
        if len(key) > 1:
            splitted = key.split(" ")
            action = splitted[0]
            x = int(splitted[1])
            y = int(splitted[2])
            maze._change_wall((x, y), "NESW", action)
        elif key == "q":
            break
        elif key == "c":
            ascii.next_color()
        elif key == "s":
            print("cant solve yet, working on it ...")
            time.sleep(1)
        elif key == "1":
            maze._change_wall((1, 1), "NSEW", "close")
        elif key == "1":
            maze._change_wall((1, 1), "NSEW", "close")


def main() -> None:
    mazeconfig = get_config()

    global maze
    maze = MazeGenerator.from_object(mazeconfig)
    maze.intialize()
    ascii = AsciiMaze(maze.maze)
    maze._add_42_pattern()
    maze.connect_ascii(ascii)
    maze.generate()
    ascii.render()
    #start(maze, mazeconfig, ascii)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        #print("seed:", maze.seed)
        pass
    except Exception as e:
        print(f"\033[31mError:\033[0m {e}")
