from mazegen import WindowManager, MazeMenu, MazeFrame
from mazegen import MazeConfig


# open config file and create a MazeConfig object
file = open("config.txt")
config = MazeConfig.from_file(file)


test_maze = WindowManager(config)
test_maze.frame.gridify((0x476174 << 8) | 0xFF)
test_maze.menu.fill_menu((0x787BA1 << 8) | 0xFF)
test_maze.render()
