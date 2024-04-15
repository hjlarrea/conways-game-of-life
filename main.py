"""
Conway's Game of Life in Python using PyGame Zero

Coded as a personal proyect to satisfy curiosity and learn about PyGame Zero Capabilities.

Author: Hernan J. Larrea (hjlarrea@hotmail.com)
Date: March, 2024
"""

import pickle
import datetime
import pgzrun
from pgzero import clock
from pygame import Rect
import pgzero.screen
screen: pgzero.screen.Screen

# Game loops


def draw():
    """PyGame Zero's Game Loop"""
    screen.clear()

    # Render Buttons
    for key in buttons.keys():
        if buttons[key]["active"] is False:
            if buttons[key]["enabled"] is True:
                rect_color = (255, 255, 255)
                text_color = (255, 255, 255)
                method = "rect"
            else:
                rect_color = (100, 100, 100)
                text_color = (100, 100, 100)
                method = "rect"
        else:
            rect_color = (255, 255, 255)
            text_color = (0, 0, 0)
            method = "filled_rect"

        rect_method = getattr(screen.draw, method)

        rect_method(
            Rect(
                (buttons[key]["button"]["x"],
                    buttons[key]["button"]["y"]),
                (buttons[key]["button"]["width"],
                    buttons[key]["button"]["height"])
            ),
            rect_color
        )

        screen.draw.text(
            buttons[key]["text"]["label"],
            (buttons[key]["text"]["x"], buttons[key]
                ["text"]["y"]), color=text_color
        )

    # Render Status Messages
    if board.get_game_mode() == 0:
        screen.draw.text("Status: Paused", midleft=(
            BUTTONLEFTMARGING, HEIGHT - 110))
    elif board.get_game_mode() in (1, 3, 4):
        screen.draw.text("Status: In Progress", midleft=(
            BUTTONLEFTMARGING, HEIGHT - 110))
    elif board.get_game_mode() == 5:
        screen.draw.text("Status: Loading...", midleft=(
            BUTTONLEFTMARGING, HEIGHT - 110))
    screen.draw.text(f"Generation: {board.get_generation()}", midleft=(
        BUTTONLEFTMARGING, HEIGHT - 70))
    screen.draw.text(f"Alive Cells: {board.get_alive_cells()}", midleft=(
        BUTTONLEFTMARGING, HEIGHT - 30))

    # Render Main Board Square
    screen.draw.rect(Rect((MARGINGSPACING, MARGINGSPACING),
                     (BOARDSIZEPX, BOARDSIZEPX)), (255, 255, 255))

    # Draw generation on the screen
    for i in range(0, BOARDSIZE):
        for j in range(0, BOARDSIZE):
            if board.get_cell(row=i, col=j).is_alive():
                screen.draw.filled_rect(Rect(board.get_cell(row=i, col=j).get_x(), board.get_cell(row=i, col=j).get_y(
                ), board.get_cell(row=i, col=j).get_x_width(), board.get_cell(row=i, col=j).get_y_width()), (255, 255, 255))
            else:
                # If game is not in progress (e.g. paused) draw a grid on the screen
                if board.get_game_mode() != 1:
                    screen.draw.line((board.get_cell(row=i, col=j).get_x(), board.get_cell(row=i, col=j).get_y(
                    )+9), (board.get_cell(row=i, col=j).get_x()+9, board.get_cell(row=i, col=j).get_y()+9), (255, 255, 255))
                    screen.draw.line((board.get_cell(row=i, col=j).get_x()+9, board.get_cell(row=i, col=j).get_y(
                    )), (board.get_cell(row=i, col=j).get_x()+9, board.get_cell(row=i, col=j).get_y()+9), (255, 255, 255))

    # Render loading screen
    if board.get_game_mode() == 5:
        screen.draw.filled_rect(
            Rect(WIDTH/2-300, HEIGHT/2-100, 600, 200), (255, 255, 255))
        screen.draw.filled_rect(
            Rect(WIDTH/2-290, HEIGHT/2-90, 580, 180), (0, 0, 0))
        screen.draw.text(f"File name  to load (no .sav extension): {
                         file_name}", midleft=(WIDTH/2-280, HEIGHT/2-20))
        screen.draw.text("Hit enter to load",
                         midleft=(WIDTH/2-280, HEIGHT/2+40))

# Event hooks


def on_mouse_down(pos):
    """PyGame Zero Event Handler for mouse down."""
    global DRAGGING

    clicked = clicked_button(pos)
    if clicked == 0:  # Start button
        board.set_game_mode(1)
        buttons["save"]["enabled"] = False
        buttons["load"]["enabled"] = False
    elif clicked == 1:  # Reset button
        board.set_game_mode(0)
        buttons["save"]["enabled"] = True
        buttons["load"]["enabled"] = True
        board.reset_board()
    elif clicked == 2:  # Pause button
        board.set_game_mode(0)
        buttons["save"]["enabled"] = True
        buttons["load"]["enabled"] = True
    elif clicked == 3:  # Step button
        board.set_game_mode(3)
        buttons["save"]["enabled"] = True
        buttons["load"]["enabled"] = True
    elif clicked == 4:  # RW button
        board.set_game_mode(4)
        board.decrease_active_generation()
        board.set_game_mode(0)
        buttons["save"]["enabled"] = True
        buttons["load"]["enabled"] = True
    elif clicked == 5:  # X1 speed button
        clock.unschedule(board.calculate_next_generation)
        # Schedule board updates
        clock.schedule_interval(board.calculate_next_generation, 1.0)
        buttons["x1"]["active"] = True
        buttons["x2"]["active"] = False
        buttons["x4"]["active"] = False
    elif clicked == 6:  # X2 speed button
        clock.unschedule(board.calculate_next_generation)
        # Schedule board updates
        clock.schedule_interval(board.calculate_next_generation, 0.5)
        buttons["x1"]["active"] = False
        buttons["x2"]["active"] = True
        buttons["x4"]["active"] = False
    elif clicked == 7:  # X4 speed button
        clock.unschedule(board.calculate_next_generation)
        # Schedule board updates
        clock.schedule_interval(board.calculate_next_generation, 0.25)
        buttons["x1"]["active"] = False
        buttons["x2"]["active"] = False
        buttons["x4"]["active"] = True
    elif clicked == 8 and buttons["save"]["enabled"]:
        board.save_to_file()
    elif clicked == 9 and buttons["load"]["enabled"]:
        board.set_game_mode(5)
    elif board.get_game_mode() not in (1, 5):  # Block making further changes one the game has started
        row, col = return_row_col(pos)
        if pos_in_board(pos):
            DRAGGING = True
            # Activate or deactivate on click depending on previous state
            if board.get_cell(row=row, col=col).is_alive():
                board.get_cell(row=row, col=col).set_dead()
            else:
                board.get_cell(row=row, col=col).set_alive()


def on_mouse_up():
    """PyGame Zero Event Handler for mouse up."""
    global DRAGGING
    DRAGGING = False


def on_mouse_move(pos):
    """PyGame Zero Event Handler for mouse movement."""
    if board.get_game_mode() not in (1, 5):  # Block making further changes one the game has started
        row, col = return_row_col(pos)
        if pos_in_board(pos) and DRAGGING:
            board.get_cell(row=row, col=col).set_alive()


def on_key_down(key):
    """PyGame Zero Event Handler for Keyboard"""
    global file_name
    if board.get_game_mode() == 5:
        if key == 8:
            file_name = file_name[0:-1]
        elif key == 13:
            board.load_from_file(file_name)
            board.set_game_mode(0)
        elif (key >= 48 and key <= 57) or (key >= 97 and key <= 122) or key == 45:
            pressedKey = chr(key)
            file_name += pressedKey

# Helper functions

# Returns the cell coordinates of the mouse position for drawing the squares


def pos_in_board(pos):
    """Returns a boolean that is True when the position being clicked is within the borders
    of the board."""
    x, y = pos
    if x > 9 and x <= BOARDSIZEPX+9 and y > 9 and y <= BOARDSIZEPX+9:
        return True
    return False

# Determine in which button from the Buttons dictionarity the user clicked


def clicked_button(pos):
    """Returns the button id based on the positional coordinates of the mouse when 
    clicked. For references on the buttons check the buttons variable."""
    for key in buttons.keys():
        if buttons[key]["button"]["x"] <= pos[0] <= (buttons[key]["button"]["x"] + buttons[key]["button"]["width"]) and buttons[key]["button"]["y"] <= pos[1] <= (buttons[key]["button"]["y"] + buttons[key]["button"]["height"]):
            return buttons[key]["id"]
    return -1

# Returns the column and row of a given mouse position in the multi demensional array


def return_row_col(pos):
    """Returns a tuple with row,col coordinates based on the positional coordinates 
    of the mouse when clicked"""
    x, y = pos
    row = int(y/CHUNKSIZE) - 1
    col = int(x/CHUNKSIZE) - 1
    return row, col

# Main function


def main():
    """Main function, executs the entire game."""
    board.reset_board()
    clock.schedule_interval(board.calculate_next_generation,
                            1.0)  # Schedule board updates
    pgzrun.go()

# Classes

# Board class


class Board():
    """Board class represents the core of the game of life. It implements a two dimensional array to store cells and provides
    a number of methods to manage the game state or return associated data to a given generation."""
    _generation = 0
    _max_generation = 0
    _alive_cells = 0
    _game_mode = 0

    def __init__(self):
        self.state = [[[Cell(x=j*10+10, y=i*10+10)
                       for j in range(0, BOARDSIZE)] for i in range(0, BOARDSIZE)]]

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
        """
        self._game_mode = mode

    def alive_neightbours(self, row, col):
        """Returns the number of alive neightbours for a given cell references by row,col coordinates in the board."""
        alive_neightbours = 0
        neightbours = self.cell_neightbours(row=row, col=col)
        for row, col in neightbours:
            if self.get_cell(row=row, col=col).alive:
                alive_neightbours += 1
        return alive_neightbours

    def reset_board(self):
        """Resets the board, same a closing the game and opening it again."""
        self.state = [[[Cell(x=j*10+10, y=i*10+10)
                       for j in range(0, BOARDSIZE)] for i in range(0, BOARDSIZE)]]
        self._generation = 0
        self._max_generation = 0
        self._alive_cells = 0
        self._game_mode = 0

    def calculate_next_generation(self):
        """Calculates the next generation based on the current one by updating the 'state' 2 dimensional array."""
        if self._game_mode in (1, 3):
            if self.get_game_mode() == 3:  # Step forward and revert back to state 0
                self.set_game_mode(0)
            if self._generation < self._max_generation:
                self._generation += 1
            elif self._generation == self._max_generation:
                new_state = [[Cell(x=j*10+10, y=i*10+10) for j in range(0, BOARDSIZE)]
                             for i in range(0, BOARDSIZE)]
                for i in range(0, BOARDSIZE):
                    for j in range(0, BOARDSIZE):
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
                0, BOARDSIZE) for j in range(0, BOARDSIZE) if self.get_cell(row=i, col=j).is_alive()])

    def cell_neightbours(self, row, col):
        """Returns a list of cells (in the form of tuples of x,y coordinateds) that are arround the cell specified through 
        the row (y) and col (x) parameters."""
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_x = (row + i) % BOARDSIZE
                neighbor_y = (col + j) % BOARDSIZE
                neighbors.append((neighbor_x, neighbor_y))
        return neighbors

    def save_to_file(self):
        """Saves the board array into a binary file using pickle."""
        date = datetime.datetime.now()
        file_path = f"{
            date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}.sav"
        data_to_save = [[[1 if (self.state[k][i][j]).is_alive() else 0 for j in range(
            0, BOARDSIZE)] for i in range(0, BOARDSIZE)] for k in range(0, self._max_generation + 1)]
        with open(file_path, 'wb') as file:
            pickle.dump(data_to_save, file)

    def load_from_file(self, file_name):
        """Load the board array from a binary file using pickle."""
        try:
            with open(file_name+".sav", 'rb') as file:
                data_to_load = pickle.load(file)

            self._max_generation = len(data_to_load) - 1
            self._generation = self._max_generation

            self.state = [[[Cell(x=j*10+10, y=i*10+10)
                            for j in range(len(data_to_load[k][i]))] for i in range(len(data_to_load[k]))] for k in range(len(data_to_load))]

            for k in range(self._max_generation + 1):
                for i in range(BOARDSIZE):
                    for j in range(BOARDSIZE):
                        if data_to_load[k][i][j] == 1:
                            self.state[k][i][j].set_alive()

            self._alive_cells = len([self.get_cell(row=i, col=j) for i in range(
                0, BOARDSIZE) for j in range(0, BOARDSIZE) if self.get_cell(row=i, col=j).is_alive()])
        except (FileNotFoundError):
            print(f"File {file_name} not found.")

# Cell class


class Cell():
    """Cell class, used to instantiate every cell in the board. When the board it is initialized a 2 dimensional array is 
    created, each position of the array is populated with a Cell type object."""

    xWidth = 9
    yWidth = 9
    alive = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        """Returns the X coordinate from the board, used for drawing."""
        return self.x

    def get_y(self):
        """Returns the Y coordinate from the board, used for drawing."""
        return self.y

    def get_x_width(self):
        """Returns the height of the cell, used for drawing."""
        return self.xWidth

    def get_y_width(self):
        """Returns the width of the cell, used for drawing."""
        return self.yWidth

    def set_alive(self):
        """Sets the cell to alive state."""
        self.alive = True

    def set_dead(self):
        """Sets the cell to dead state."""
        self.alive = False

    def is_alive(self):
        """Returns a boolean indicating whether the cell is alive or dead."""
        return self.alive


# Variables: Configuration
BOARDSIZE = 80  # Number of cells (e.g. 80 = 80*80)
CHUNKSIZE = 10  # Size of each cell for rendering
MARGINGSPACING = 10  # Marging space between board and other elements
BOARDSIZEPX = BOARDSIZE * CHUNKSIZE  # Board size in pixels
# Where buttons shoudl be placed in the x axis in relation to the board
BUTTONLEFTMARGING = BOARDSIZEPX + 2 * MARGINGSPACING
BUTTONWIDTH = 100  # Button size
BUTTONHEIGHT = 30  # Button sie
TEXTWIDTH = 200  # Labels width (e.g. Number of alive cells or status)
WIDTH = BOARDSIZEPX + 3 * MARGINGSPACING + TEXTWIDTH  # Window width
HEIGHT = BOARDSIZEPX + 2 * MARGINGSPACING  # Windows height
buttons = {  # Screen elements to be rendered
    "start": {
        # Start Button
        "id": 0,
        "text": {"label": "Start", "x": BUTTONLEFTMARGING + 30, "y": 18},
        "button": {"x": BUTTONLEFTMARGING, "y": 10, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    },
    "reset": {
        # Reset button
        "id": 1,
        "text": {"label": "Reset", "x": BUTTONLEFTMARGING + 28, "y": 58},
        "button": {"x": BUTTONLEFTMARGING, "y": 50, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    },
    "pause": {
        # Pause button
        "id": 2,
        "text": {"label": "Pause", "x": BUTTONLEFTMARGING + 28, "y": 98},
        "button": {"x": BUTTONLEFTMARGING, "y": 90, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    },
    "step": {
        # Step forward button
        "id": 3,
        "text": {"label": "FW", "x": BUTTONLEFTMARGING + 40, "y": 138},
        "button": {"x": BUTTONLEFTMARGING, "y": 130, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    },
    "back": {
        # Step back button
        "id": 4,
        "text": {"label": "RW", "x": BUTTONLEFTMARGING + 40, "y": 178},
        "button": {"x": BUTTONLEFTMARGING, "y": 170, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    },
    "x1": {
        # X1 speed button
        "id": 5,
        "text": {"label": "X1", "x": BUTTONLEFTMARGING + 40, "y": 218},
        "button": {"x": BUTTONLEFTMARGING, "y": 210, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": True,
        "enabled": True
    },
    "x2": {
        # X2 speed button
        "id": 6,
        "text": {"label": "X2", "x": BUTTONLEFTMARGING + 40, "y": 258},
        "button": {"x": BUTTONLEFTMARGING, "y": 250, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    },
    "x4": {
        # X4 speed button
        "id": 7,
        "text": {"label": "X4", "x": BUTTONLEFTMARGING + 40, "y": 298},
        "button": {"x": BUTTONLEFTMARGING, "y": 290, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    },
    "save": {
        # Save statebutton
        "id": 8,
        "text": {"label": "Save", "x": BUTTONLEFTMARGING + 30, "y": 338},
        "button": {"x": BUTTONLEFTMARGING, "y": 330, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    },
    "load": {
        # Load state button
        "id": 9,
        "text": {"label": "Load", "x": BUTTONLEFTMARGING + 30, "y": 378},
        "button": {"x": BUTTONLEFTMARGING, "y": 370, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    }
}

# Variables: Flow Control
DRAGGING = False
file_name = ""

# Start
board = Board()
main()
