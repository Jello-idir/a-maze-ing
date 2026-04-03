from maze import MazeGenerator
from asciify import Maze
from maze import  display_grids
from config_parser import ConfigParser

if __name__ == "__main__":

    with open('config.txt', 'r') as f:
        config = ConfigParser.parse(f)

    seed = 3
    if "SEED" in config:
        seed = config["SEED"]
    maze = MazeGenerator(config["WIDTH"], config["HEIGHT"])
    maze.initialize_grid()
    maze.initial_maze()
    maze.origin_shift(seed)
    maze.update_all_walls()
    maze.generate_output_file("output_maze.txt")

    # display_grids.display_maze(maze.origin)
    # with open("maze_visualization.txt", 'w') as file:
    #     display_grids.write_maze(maze.origin, file)

    with open("output_maze.txt", 'r') as f:
        m = Maze(f)
        m.display_maze()

