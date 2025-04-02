# Maze Game Solver
<div align = "right">
 <em> Originally written in March 2023 without multithreading, but was not pushed to Github </em>
</div>

## Overview
This project created with Python's Pygame library is a maze game where a player can navigate through a maze, and a solver powered by a genetic algorithm attempts to find the optimal path to the goal. The solver uses a population of "bots" that evolve over generations to improve their ability to navigate the maze.

## Demo
<div align="center"> <img src="Maze_Game_GIF_2.gif" width="800"/> </div>

## How to Run
1. Install the required dependencies:
   ```
   pip install pygame
   ```
2. Run the game:
   ```
   python Actual_Game.py
   ```

## Key Concepts
1. **`Maze Generation`**:
**Kruskall's algorithm** is used to generate the maze. First, a grid of walls is created, and then walls are removed to create passages. **Disjoint Set Union** helps implement this algorithm.

2. **`Maze Solver`**:
**Genetic algorithm** is used to evolve a population of bots that attempt to navigate the maze. Each bot has a "brain" that determines its movement. The algorithm includes:
   - **Selection**: The best-performing bots are selected to pass on their genes.
   - **Crossover**: Selected bots combine their brains to create offspring.
   - **Mutation**: Random changes are introduced to the offspring's brains to maintain genetic diversity.

3. **`Multithreading`**:
The solver takes some time in updating the population of bots. To ensure smooth gameplay, the bot population is updated in a separate thread. This allows the player to navigate the maze while the solver is working in the background.

## Code Structure

### 1. **Core Components**
- **`Maze`**: Handles maze generation, rendering, and collision detection.
- **`Bot`**: Each bot has a position, velocity, and a "brain" that determines its movement.
- **`Brain`**: Stores the movement directions for a bot and handles mutation and cloning.
- **`Population`**: Manages the group of bots, handles natural selection, and updates their states.

### 2. **Constants**
You can tweak various parameters in `Constants.py` to modify the game's behavior:
- **Maze Properties**: Block size, wall thickness, etc.
- **Bot Properties**: Population size, mutation rate, velocity, etc.
- **Display Settings**: Window size, colors, FPS, etc.

### 3. **Game Logic**
- **`Actual_Game.py`**: The main entry point for the game. It initializes the maze, player, and solver, and handles the game loop.
- **Player Movement**: The player can move using arrow keys, with collision checks to prevent passing through walls.
- **Visualizer**: The game uses `pygame` for rendering the player, maze and the bots.

## Acknowledgments
The project was inspired by [this video on genetic algorithm](https://www.youtube.com/watch?v=mUs6qY9Xurs)
