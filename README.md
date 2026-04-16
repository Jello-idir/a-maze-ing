*This project has been created as part of the 42 curriculum by aait-idi, yoabied.*

# Description
The goal of this project is to create a maze generator and solver. The program will generate a maze based on a given configuration file and then solve it using a chosen algorithm. The maze will be displayed in the terminal, and the solution will be highlighted.

# Instructions
To install the project requiremenets, run the following command in the terminal:
```
make install
```

To run the program, use the following command:
```
make run
```

To clean the project, use the following command:
```
make clean
```

To lint the code, use the following command:
```
make lint
```

# Resources
- [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- AI was used to assist in the development of this projects's repetetive and tedious tasks, as well as to optimize the code for better performance. AI tools were also utilized for code review and debugging purposes.


# Additionals

## Config file structure
The configuration file is a simple text file that contains the following parameters:
```
WIDTH=20 -> the width of the maze
HEIGHT=10 -> the height of the maze
ENTRY=1,1 -> the coordinates of the maze entry point (x,y)
EXIT=18,8 -> the coordinates of the maze exit point (x,y)
OUTPUT_FILE=maze.txt -> the name of the file where the generated maze will be saved
PERFECT=True -> whether the maze should be perfect (no loops) or not
SEED=12345 (optional) -> the seed for the random number generator, which can be used to generate the same maze multiple times for testing purposes
```

## Maze generation algorithm
The maze generation algorithm used in this project is Wilson's algorithm. This algorithm is based on the concept of random walks and is known for producing perfect mazes (mazes without loops).

## Why Wilson's algorithm
Wilson's algorithm was chosen for this project because it is efficient and produces high-quality mazes. It is also relatively easy to implement and understand, making it a suitable choice for this project.

## Reusable code
The code for the maze generation and solving algorithms can be reused in other projects that require similar functionality. The code is modular and can be easily integrated into other applications.

## Team and project management
- Team members: aait-idi (Maze Generation, Path finding, ...), yoabied (parsing, config validation and program stracture)
- Anticipated planning: The project was planned to be completed in 2 weeks, with each week dedicated to a specific phase of the project (planning, implementation, testing, and documentation). The planning changes as we progressed through the project.
- What worked well: The team was able to effectively communicate and collaborate throughout the project, which helped to ensure that tasks were completed on time and to a high standard.
- What could be improved: The team could have spent more time refining the project and mazegeneration implimentation, as well as testing the code more thoroughly to identify and fix any bugs or issues.
- Tools used: The team used Git for version control, and a code editor Visual Studio Code for writing and editing the code. We also utilized AI tools for code review and debugging purposes.

