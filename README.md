# Introduction

A PyGame Zero implementation of Conway's Game of Live. For more information visit [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) at Wikipedia.

# Requirements

This game has been built using pyenv and virtual environments for isolating the dependencies required for executing it. Check the local `.python-version` file, if not using pyenv to ensure your local environment is compatible with the project's set up.

# How to run this project

## Local execution

Run the following command standing in the project's directory:

```
pgzrun main.py
```

# Roadmap

- [x] Deactivate activated cells during initial set up
- [x] Block making further changes when the game is running
- [x] Add a button to advance one step only
- [x] Add a pause button
- [ ] Add a feature to save and load the initial state
- [x] Add a reset button
- [ ] Add templates
- [ ] Add a graph to show the evolution of number of alive cells vs generation number
- [ ] Save each generation and allow to move back and forth
- [ ] Add the possibility of starting new timelines from a given point
- [ ] Once the board reaches stability (no changes in two consecutive generations) stop the game