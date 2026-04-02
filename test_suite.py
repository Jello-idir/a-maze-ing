from maze import MazeGenerator
from asciify import Maze
from maze import  display_grids
from config_parser import ConfigParser


if __name__ == "__main__":

    with open('config.txt', 'r') as f:
        config = ConfigParser.parse(f)
        print(config)
    maze = MazeGenerator()
    origin = maze.initialize_grid(config["WIDTH"], config["HEIGHT"])
    start_origin = maze.initial_maze(origin)
    maze.origin_shift(start_origin, 3)
    maze.generate_output_file(origin, "output_maze.txt")

    display_grids.display_maze(origin)
    with open("maze_visualization.txt", 'w') as file:
        display_grids.write_maze(origin, file)

    with open("output_maze.txt", 'r') as f:
        m = Maze(f)
        m.display_maze()
