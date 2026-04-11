a-maze-ing/
├── .git/
├── .gitignore
├── README.md
├── pyproject.toml
├── setup.py
├── MANIFEST.in
│
├── mazegen/
│   ├── __init__.py
│   ├── maze_generator.py   # Core MazeGenerator class
│   ├── maze_validator.py   # Validation logic
│   └── utils.py            # Utility functions
│
├── MLX/
│   ├── __init__.py
│   ├── libmlx.py
│   ├── libmlx42.dylib
│   └── libmlx42.so
│
├── display/
│   ├── __init__.py
│   ├── renderer.py         # MLX42 rendering
│   └── visualizer.py       # Maze visualization logic
│
├── a_maze_ing.py           # Main entry point
├── config.txt              # Example config
└── docs/
    └── USAGE.md            # Documentation for mazegen module
