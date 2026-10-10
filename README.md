# Asteroid

An Asteroids-style arcade game built with pygame. You can play it yourself, or watch a population of small neural networks learn to dodge asteroids on their own.

This was my first project with neural networks, so the AI part is a learning exercise rather than a polished model.

## Features

- **Player mode**: classic keyboard-controlled ship that can rotate, move and shoot.
- **AI mode**: 100 neural networks play at the same time. Each generation, the best one is kept and the others are mutated copies of it.
- **Adjustable simulation speed** from the settings menu.
- **Save and import** a trained network from the pause menu and reload it later.

## Requirements

- Python 3.11 or newer
- [pygame](https://www.pygame.org/) and [shapely](https://shapely.readthedocs.io/) (installed automatically)

## Installation

```bash
git clone https://github.com/Materwan/asteroid.git
cd asteroid

python -m venv .venv
.venv/Scripts/pip install -e .
```

## Running the game

Run the game from the project root, because the sprites are loaded with relative paths from the `New Asteroid/` folder:

```bash
.venv/Scripts/asteroid.exe
```

## Controls

| Action              | Key            |
|---------------------|----------------|
| Rotate and move     | Arrow keys     |
| Shoot               | Space          |
| Pause / resume      | Escape         |

In the main menu, choose **Play** to start, **Settings** to change the options, or **Quit** to exit.

## Settings

- **Mode**: `AI` (neural networks play) or `Player` (you play).
- **Speed**: simulation speed multiplier. The default is `1`.
- **Import**: path to a saved network file, such as `save.txt`, to continue training from it.

In AI mode, press Escape during a game and choose **Save** to write the current best network to `save.txt`.

## How the AI works

- **Inputs**: the play area is split into a 10×10 grid. Each cell is `1` if an asteroid is inside it, and `0` otherwise.
- **Outputs**: five neurons decide whether to move left, right, up, down, or shoot.
- **Learning**: at the end of each round, the network that survived longest is kept. The other networks are replaced by mutated copies of it. Mutations can add or remove neurons and connections, and change weights.
- **Network structure**: the networks start with a single hidden layer and can grow new layers over time.

## Project structure

```
src/asteroid/
├── main.py              # Game loop and the player / AI modes
├── menu.py              # Main, settings, pause and game-over menus
├── playerScript.py      # Player ship
├── asteroidScript.py    # Asteroids
├── bulletScript.py      # Bullets
├── AAI.py               # Neural network used in AI mode
├── Neural_network.py    # Older neural network implementation
├── SaveScript.py        # Saving and loading networks
└── UIScript.py          # Buttons, input boxes and counters
```

## Ideas for improvement

- Train without rendering, to speed up learning
- Track and display the average score per generation
- Add more inputs, such as the ship's position or the direction of nearby asteroids
- Use real training algorithms, and numpy for arrays
