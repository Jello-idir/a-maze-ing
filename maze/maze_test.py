from maze import MazeGenerator
from asciify import Maze
from maze import  display_grids

if __name__ == "__main__":
    maze = MazeGenerator()
    origin = maze.initialize_grid(10, 10)
    start_origin = maze.initial_maze(origin)
    maze.origin_shift(start_origin, 3)
    # maze.generate_output_file(origin, "output_maze.txt")

    display_grids.display_maze(origin)
    with open("maze_visualization.txt", 'w') as file:
        display_grids.write_maze(origin, file)

    with open("output_maze.txt", 'r') as f:
        m = Maze(f)
        m.display_maze()
