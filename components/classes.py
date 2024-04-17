"""
This file contains the classes to be used by the main project.

Author: Hernan J. Larrea (hjlarrea@hotmail.com)
Date: March, 2024
"""

import pickle
import datetime
from random import randint

# Classes

# Board class


class Board():
    """Board class represents the core of the game of life. It implements a two dimensional array to store cells and provides
    a number of methods to manage the game state or return associated data to a given generation."""
    _generation = 0
    _max_generation = 0
    _alive_cells = 0
    _game_mode = 0

    def __init__(self, board_size):
        self.board_size = board_size
        self.state = [[[Cell(x=j*10+10, y=i*10+10)
                       for j in range(0, self.board_size)] for i in range(0, self.board_size)]]

    def get_cell(self, row, col):
        """Gets a given cell specified by the coordinates row,col."""
        return self.state[self._generation][row][col]

    def get_generation(self):
        """Returns the generation number."""
        return self._generation

    def get_alive_cells(self):
        """Returns the number of alive cells. The number of alive cells is valculated over the calculate_next_generation method execution."""
        return self._alive_cells

    def get_game_mode(self):
        """Returns the game mode (see set_game_mode docstring for reference on game modes)."""
        return self._game_mode

    def get_current_generation(self):
        """Returns the active generation. Active, meaning the one that will be rendered on the screen."""
        return self._generation

    def decrease_active_generation(self):
        """Reduces the active generation by 1 so a previous generation can be rendered on the screen."""
        if self._generation > 0:
            self._generation -= 1
            self._game_mode = 3

    def set_game_mode(self, mode):
        """Sets the game mode to one of these:
        0 - Game is not in progress and editing the board is allowed.
        1 - Game is in progress, editing the board is not allowed.
        2 - Not in use
        3 - Game is in step mode, advances one step forward and then reverts to game mode 0.
        4 - Game is in step mode, moves one step backward and then reverts to game mode 0.
        5 - Load Screen
        6 - Stable board
        """
        self._game_mode = mode

    def alive_neightbours(self, row, col):
        """Returns the number of alive neightbours for a given cell references by row,col coordinates in the board."""
        alive_neightbours = 0
        neightbours = self.cell_neightbours(row=row, col=col)
        for row, col in neightbours:
            if self.get_cell(row=row, col=col).is_alive():
                alive_neightbours += 1
        return alive_neightbours

    def reset_board(self):
        """Resets the board, same a closing the game and opening it again."""
        self.state = [[[Cell(x=j*10+10, y=i*10+10)
                       for j in range(0, self.board_size)] for i in range(0, self.board_size)]]
        self._generation = 0
        self._max_generation = 0
        self._alive_cells = 0
        self._game_mode = 0

    def calculate_next_generation(self):
        """Calculates the next generation based on the current one by updating the 'state' 2 dimensional array."""
        if self.get_generation() > 1 and (self.state[-1] == self.state[-2]) and self.get_game_mode(): # Check if the board is stable in two generations in a row
            self.set_game_mode(6)
        elif self._game_mode in (1, 3):
            if self.get_game_mode() == 3:  # Step forward and revert back to state 0
                self.set_game_mode(0)
            if self._generation < self._max_generation: # If rendering a previous state move forward to the next generation without calculating it
                self._generation += 1
            elif self._generation == self._max_generation:
                new_state = [[Cell(x=j*10+10, y=i*10+10) for j in range(0, self.board_size)]
                             for i in range(0, self.board_size)]
                for i in range(0, self.board_size):
                    for j in range(0, self.board_size):
                        if self.alive_neightbours(row=i, col=j) < 2:
                            new_state[i][j].set_dead()
                        elif self.alive_neightbours(row=i, col=j) > 3:
                            new_state[i][j].set_dead()
                        elif self.alive_neightbours(row=i, col=j) == 3:
                            new_state[i][j].set_alive()
                        else:
                            new_state[i][j] = self.get_cell(row=i, col=j)
                self.state.append(new_state)
                self._max_generation += 1
                self._generation += 1
            self._alive_cells = len([self.get_cell(row=i, col=j) for i in range(
                0, self.board_size) for j in range(0, self.board_size) if self.get_cell(row=i, col=j).is_alive()])

    def cell_neightbours(self, row, col):
        """Returns a list of cells (in the form of tuples of x,y coordinateds) that are arround the cell specified through 
        the row (y) and col (x) parameters."""
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_x = (row + i) % self.board_size
                neighbor_y = (col + j) % self.board_size
                neighbors.append((neighbor_x, neighbor_y))
        return neighbors

    def save_to_file(self):
        """Saves the board array into a binary file using pickle."""
        date = datetime.datetime.now()
        file_path = f"{
            date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}.sav"
        data_to_save = [[[1 if (self.state[k][i][j]).is_alive() else 0 for j in range(
            0, self.board_size)] for i in range(0, self.board_size)] for k in range(0, self._max_generation + 1)]
        with open(file_path, 'wb') as file:
            pickle.dump(data_to_save, file)

    def load_from_file(self, file_name):
        """Load the board array from a binary file using pickle."""
        try:
            # Load binary save file
            with open(file_name+".sav", 'rb') as file:
                data_to_load = pickle.load(file)
            # Initialize state variables
            self._max_generation = len(data_to_load) - 1
            self._generation = 0
            # Initialize the state to match the data to be loaded in size
            self.state = [[[Cell(x=j*10+10, y=i*10+10)
                            for j in range(len(data_to_load[k][i]))] for i in range(len(data_to_load[k]))] for k in range(len(data_to_load))]
            # Match the state to the data loaded
            for k in range(self._max_generation + 1):
                for i in range(self.board_size):
                    for j in range(self.board_size):
                        if data_to_load[k][i][j] == 1:
                            self.state[k][i][j].set_alive()
            # Initialize state variables
            self._alive_cells = len([self.get_cell(row=i, col=j) for i in range(
                0, self.board_size) for j in range(0, self.board_size) if self.get_cell(row=i, col=j).is_alive()])
        except FileNotFoundError:
            print(f"File {file_name} not found.")

    def randomize(self):
        """Create a random state for the board."""
        hit = False
        top = 20
        for i in range(self.board_size):
            for j in range(self.board_size):
                if hit is True:
                    if randint(0,top) == 1:
                        self.get_cell(row=i, col=j).set_alive()
                else:
                    if randint(0, top) == 1:
                        self.get_cell(row=i, col=j).set_alive()
                        hit = True
                        top = top - 1
                    else:
                        self.get_cell(row=i, col=j).set_dead()
                        hit = False
                        top = 20

# Cell class


class Cell():
    """Cell class, used to instantiate every cell in the board. When the board it is initialized a 2 dimensional array is 
    created, each position of the array is populated with a Cell type object."""

    _xWidth = 9
    _yWidth = 9
    _alive = False

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_x(self):
        """Returns the X coordinate from the board, used for drawing."""
        return self._x

    def get_y(self):
        """Returns the Y coordinate from the board, used for drawing."""
        return self._y

    def get_x_width(self):
        """Returns the height of the cell, used for drawing."""
        return self._xWidth

    def get_y_width(self):
        """Returns the width of the cell, used for drawing."""
        return self._yWidth

    def set_alive(self):
        """Sets the cell to alive state."""
        self._alive = True

    def set_dead(self):
        """Sets the cell to dead state."""
        self._alive = False

    def is_alive(self):
        """Returns a boolean indicating whether the cell is alive or dead."""
        return self._alive
    
    def __eq__(self, other):
        return isinstance(other, Cell) and self.is_alive() == other.is_alive()
