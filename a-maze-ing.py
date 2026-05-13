import sys
import termios
import tty


try:
    from pydantic import ValidationError
    from mazegen import MazeGenerator, AsciiMaze, MazeConfig
except ImportError as e:
    print(f"\033[31mMissing dependency:\033[0m {e}")
    print("Run: make install")
    sys.exit(1)


def get_config() -> MazeConfig:
    argc = len(sys.argv)
    if argc != 2:
        raise ValueError("Usage: python a-maze-ing.py <config_file>")
    try:
        with open(sys.argv[1]) as f:
            return MazeConfig.from_file(f)
    except FileNotFoundError:
        raise ValueError(f"Config file '{sys.argv[1]}' not found.")
    except PermissionError:
        raise ValueError(f"Permission denied for config file '{sys.argv[1]}'.")
    except OSError as e:
        raise ValueError(f"Error opening config file '{sys.argv[1]}': {e}")


def display_info(config: MazeConfig, color: str = "\033[31m") -> None:
    for key, value in config.get_config().items():
        if key == "seed" and value is None:
            value = "Random"
        print(f"{color} {key} {value} \033[0m   ", end="")
    print("\n")


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


def display_menu(colors: dict[str, str]) -> None:
    beff = "\033[1m"
    teff = "\033[3m"

    bclr = colors["block"] + "\033[38;2;255;255;255m"
    rst = colors["reset"]

    print()
    print(
        f"{bclr}{beff} R {rst}|{bclr}{teff} Re-generate {rst}  "
        f"{bclr}{beff} C {rst}|{bclr}{teff} Change Color {rst}  "
        f"{bclr}{beff} S {rst}|{bclr}{teff} Solve {rst}  "
        f"{bclr}{beff} A {rst}|{bclr}{teff} Animate Solution {rst}  "
        f"{bclr}{beff} Q {rst}|{bclr}{teff} Quit {rst}  "
        f"{bclr}{beff} M {rst}|{bclr}{teff} Move {rst}  "
        f"{bclr}{beff} H {rst}|{bclr}{teff} Show/Hide Path {rst}  "
        f"{bclr}{beff} W {rst}|{bclr}{teff} Write to File {rst}"
        )


def start(mzgen: MazeGenerator, mzcnf: MazeConfig, mzasci: AsciiMaze) -> None:
    while True:
        sys.stdout.write("\033[H\033[J")
        mzasci.render(mzgen.maze)
        display_menu(mzasci.clr)
        key = read_key().lower()
        if key == "q":
            break
        elif key == "r":
            mzgen.intialize()
            mzgen.wilson_algo()
            mzasci = AsciiMaze(mzgen.maze)
            mzgen.connect_ascii(mzasci)
        elif key == "c":
            mzasci.next_color()
        elif key == "s":
            mzgen.a*(False)
            mzasci.showpath = True
        elif key == "a":
            mzasci.delete_path()
            mzasci.showpath = True
            mzgen.a*(True)
        elif key == "h":
            mzasci.toggle_path()
        elif key == "m":
            mzasci.showpath = True
            mzasci.delete_path()
            mzgen.free_move()
        elif key == "w":
            try:
                mzgen.write_to_file(mzcnf.output_file)
                print(f"\033[32mMaze written to {mzcnf.output_file}\033[0m")
            except Exception as e:
                print(f"\033[31mError writing to file:\033[0m {e}")


def start_maze_interaction() -> None:
    """the main function of the program,
    it initializes the maze generator,
    the ascii maze and starts the interactive menu
    """
    mzcnf = get_config()

    mzgen = MazeGenerator.from_object(mzcnf)
    mzgen.intialize()

    mzasci = AsciiMaze(mzgen.maze)
    mzgen.connect_ascii(mzasci)

    mzgen.wilson_algo()
    mzgen.a*(False)

    start(mzgen, mzcnf, mzasci)


if __name__ == "__main__":
    try:
        start_maze_interaction()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\033[31mError:\033[0m {e}")
        sys.exit(1)
