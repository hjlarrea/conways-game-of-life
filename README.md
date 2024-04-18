# Introduction

A PyGame Zero implementation of Conway's Game of Live. For more information visit [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) at Wikipedia.

![animation](./docs/img/animation.gif)

# Requirements

This game has been built using pyenv and virtual environments for isolating the dependencies required for executing it. Check the local `.python-version` file, if not using pyenv to ensure your local environment is compatible with the project's set up.

# How to run this project

## Local execution

Run the following command standing in the project's directory:

```
pgzrun main.py
```

## Running tests

At the root of the repository run:

```
pytest -v
```

# Documentation

- [Instructions](./docs/Instructions.md)

# Roadmap

- [x] Deactivate activated cells during initial set up
- [x] Block making further changes when the game is running
- [x] Add a button to advance one step only
- [x] Add a pause button
- [x] Add Speed buttons
- [x] Add a reset button
- [x] Make the board infinite or a continium across borders
- [x] Save each generation and allow to move back and forth
- [x] Add a feature to save and load the initial state
- [x] Once the board reaches stability (no changes in two consecutive generations) stop the game
- [ ] Add templates
