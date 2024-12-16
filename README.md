# Jueguito: Puzzle Solver Game

## Overview
**Jueguito** is a Python-based game where players attempt to fit puzzle pieces onto a grid board. The game includes functionality to solve the puzzle automatically using a backtracking algorithm.

## Features
- Interactive board where players can drag and drop pieces.
- Automatic solving functionality with optimized backtracking.
- Pieces with multiple rotations to increase complexity.
- Visual feedback using Pygame.

## Requirements
- Python 3.8+
- Pygame library

### Installation
1. Clone this repository or download the project files.
2. Install the required Python packages:
   ```bash
   pip install pygame
   ```

## How to Play
1. Run the game using:
   ```bash
   python main.py
   ```
2. The game window will open, showing the board and the puzzle pieces.
3. Drag and drop pieces onto the board:
   - Click and drag pieces to position them.
   - Use keyboard controls to rotate the active piece:
     - `W` or `UP ARROW`: Rotate upwards
     - `A` or `LEFT ARROW`: Rotate left
     - `S` or `DOWN ARROW`: Rotate downwards
     - `D` or `RIGHT ARROW`: Rotate right
4. Use the buttons on the left:
   - **New**: Reset the game with a fresh board and pieces.
   - **Solve**: Automatically solve the puzzle using the backtracking algorithm.

## Game Elements
### Pieces
- Each piece has a unique tag (e.g., `A`, `B`, `C`) and can be rotated into multiple orientations.
- Precomputed rotations are cached for efficient solving.

### Board
- The board is an 11x5 grid where players or the solver must fit all the pieces without overlapping.

## Key Functionalities
### Backtracking Solver
The game includes a backtracking algorithm to solve the puzzle:
1. Precomputes valid positions for each piece.
2. Attempts to fit pieces recursively.
3. Backtracks when a piece cannot be placed.

### Optimization Features
- **Precomputed Valid Positions**: All valid placements for each piece are cached before solving.
- **Sorting**: Pieces are sorted by size and complexity to minimize recursive depth.

## Code Structure
### `main.py`
- Handles game initialization and user interactions.
- Includes event listeners for dragging pieces, rotating them, and button actions.

### `Game.py`
- Defines the `Board`, `Piece`, and `Button` classes.
- Implements core logic for piece placement, rotation, and the solver algorithm.

## Extending the Game
### Adding New Pieces
1. Define a new piece in the `declarePieces` function in `main.py`.
2. Specify its initial position, size, and parts (blocks).
3. Call the `generateRotations` method to generate all possible orientations.

### Modifying the Board
1. Change the board dimensions in the `Board` initialization in `main.py`:
   ```python
   board = Board(X, Y, ...)
   ```
2. Adjust piece definitions accordingly.

## Known Limitations
- The solver may be slow for very large boards or complex configurations due to the recursive nature of backtracking.


## Future Enhancements
- Add difficulty levels with varying board sizes and piece complexities.
- Implement a timer and scoring system.
- Support for saving and loading game states.

## Credits
- Developed using [Pygame](https://www.pygame.org/).

## License
This project is licensed under the MIT License. See the LICENSE file for details.

