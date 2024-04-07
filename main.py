import pgzrun
from pgzero import clock
from pygame import Rect
# import matplotlib.pyplot as plt

# Game loops


def draw():
    screen.clear()

    # Render Buttons
    for key in buttons.keys():
        if buttons[key]["active"] == False:
            screen.draw.text(
                buttons[key]["text"]["label"],
                (buttons[key]["text"]["x"], buttons[key]["text"]["y"])
            )
            screen.draw.rect(
                Rect(
                    (buttons[key]["button"]["x"], buttons[key]["button"]["y"]),
                    (buttons[key]["button"]["width"],
                     buttons[key]["button"]["height"])
                ),
                (255, 255, 255)
            )
        else:
            # Paint the active speed button
            screen.draw.filled_rect(
                Rect(
                    (buttons[key]["button"]["x"], buttons[key]["button"]["y"]),
                    (buttons[key]["button"]["width"],
                     buttons[key]["button"]["height"])
                ),
                (255, 255, 255)
            )
            screen.draw.text(buttons[key]["text"]["label"], (buttons[key]
                             ["text"]["x"], buttons[key]["text"]["y"]), color=(0, 0, 0))

    # Render Status Messages
    if board.get_game_mode() == 0:
        screen.draw.text("Status: Paused", midleft=(
            BUTTONLEFTMARGING, HEIGHT - 110))
    elif board.get_game_mode() == 1 or board.get_game_mode() == 3:
        screen.draw.text("Status: In Progress", midleft=(
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

# Event hooks


def on_mouse_down(pos):
    global DRAGGING

    clicked = clickedButton(pos)
    if clicked == 0:  # Start button
        board.set_game_mode(1)
    elif clicked == 1:  # Reset button
        board.set_game_mode(0)
        board.reset_board()
        """Resets the board, same a closing the game and opening it again."""
    elif clicked == 2:  # Pause button
        board.set_game_mode(0)
    elif clicked == 3:  # Step button
        board.set_game_mode(3)
    elif clicked == 4:  # X1 speed button
        clock.unschedule(board.calculate_next_generation)
        # Schedule board updates
        clock.schedule_interval(board.calculate_next_generation, 1.0)
        buttons["x1"]["active"] = True
        buttons["x2"]["active"] = False
        buttons["x4"]["active"] = False
    elif clicked == 5:  # X2 speed button
        clock.unschedule(board.calculate_next_generation)
        # Schedule board updates
        clock.schedule_interval(board.calculate_next_generation, 0.5)
        buttons["x1"]["active"] = False
        buttons["x2"]["active"] = True
        buttons["x4"]["active"] = False
    elif clicked == 6:  # X4 speed button
        clock.unschedule(board.calculate_next_generation)
        # Schedule board updates
        clock.schedule_interval(board.calculate_next_generation, 0.25)
        buttons["x1"]["active"] = False
        buttons["x2"]["active"] = False
        buttons["x4"]["active"] = True
    elif board.get_game_mode() != 1:  # Block making further changes one the game has started
        row, col = returnRowCol(pos)
        if posInBoard(pos):
            DRAGGING = True
            # Activate or deactivate on click depending on previous state
            if board.get_cell(row=row, col=col).is_alive():
                board.get_cell(row=row, col=col).set_dead()
            else:
                board.get_cell(row=row, col=col).set_alive()


def on_mouse_up():
    global DRAGGING
    DRAGGING = False


def on_mouse_move(pos):
    global board
    if board.get_game_mode() != 1:  # Block making further changes one the game has started
        row, col = returnRowCol(pos)
        if posInBoard(pos) and DRAGGING == True:
            board.get_cell(row=row, col=col).set_alive()

# Helper functions

# Returns the cell coordinates of the mouse position for drawing the squares


def posInBoard(pos):
    x, y = pos
    if x > 9 and x <= BOARDSIZEPX+9 and y > 9 and y <= BOARDSIZEPX+9:
        return True
    else:
        return False

# Determine in which button from the Buttons dictionarity the user clicked


def clickedButton(pos):
    for key in buttons.keys():
        if buttons[key]["button"]["x"] <= pos[0] <= (buttons[key]["button"]["x"] + buttons[key]["button"]["width"]) and buttons[key]["button"]["y"] <= pos[1] <= (buttons[key]["button"]["y"] + buttons[key]["button"]["height"]):
            return buttons[key]["id"]
    return -1

# Returns the column and row of a given mouse position in the multi demensional array


def returnRowCol(pos):
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
    _alive_cells = 0
    _game_mode = 0

    def __init__(self):
        self.state = [[Cell(x=j*10+10, y=i*10+10)
                       for j in range(0, BOARDSIZE)] for i in range(0, BOARDSIZE)]

    def get_cell(self, row, col):
        """Gets a given cell specified by the coordinates row,col."""
        return self.state[row][col]

    def get_generation(self):
        """Returns the generation number."""
        return self._generation

    def get_alive_cells(self):
        """Returns the number of alive cells. The number of alive cells is valculated over the calculate_next_generation method execution."""
        return self._alive_cells

    def get_game_mode(self):
        """Returns the game mode (see set_game_mode docstring for reference on game modes)."""
        return self._game_mode

    def set_game_mode(self, mode):
        """Sets the game mode to one of these:
        0 - Game is not in progress and editing the board is allowed.
        1 - Game is in progress, editing the board is not allowed.
        2 - Not in use
        3 - Game is in step mode, advances one step forward and then reverts to game mode 0.
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
        self.state = [[Cell(x=j*10+10, y=i*10+10)
                       for j in range(0, BOARDSIZE)] for i in range(0, BOARDSIZE)]
        self._generation = 0
        self._alive_cells = 0
        self._game_mode = 0

    def calculate_next_generation(self):
        """Calculates the next generation based on the current one by updating the 'state' 2 dimensional array."""
        if self._game_mode == 1 or self._game_mode == 3:
            state2 = [[Cell(x=j*10+10, y=i*10+10) for j in range(0, BOARDSIZE)]
                      for i in range(0, BOARDSIZE)]
            for i in range(0, BOARDSIZE):
                for j in range(0, BOARDSIZE):
                    if self.alive_neightbours(row=i, col=j) < 2:
                        state2[i][j].set_dead()
                    elif self.alive_neightbours(row=i, col=j) > 3:
                        state2[i][j].set_dead()
                    elif self.alive_neightbours(row=i, col=j) == 3:
                        state2[i][j].set_alive()
                    else:
                        state2[i][j] = self.get_cell(row=i, col=j)
            if self.get_game_mode() == 3:  # Step forward and revert back to state 0
                self.set_game_mode(0)
            self.state = state2
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
        "active": False
    },
    "reset": {
        # Reset button
        "id": 1,
        "text": {"label": "Reset", "x": BUTTONLEFTMARGING + 28, "y": 58},
        "button": {"x": BUTTONLEFTMARGING, "y": 50, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False
    },
    "pause": {
        # Pause button
        "id": 2,
        "text": {"label": "Pause", "x": BUTTONLEFTMARGING + 28, "y": 98},
        "button": {"x": BUTTONLEFTMARGING, "y": 90, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False
    },
    "step": {
        # Step button
        "id": 3,
        "text": {"label": "Step", "x": BUTTONLEFTMARGING + 30, "y": 138},
        "button": {"x": BUTTONLEFTMARGING, "y": 130, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False
    },
    "x1": {
        # X1 speed button
        "id": 4,
        "text": {"label": "X1", "x": BUTTONLEFTMARGING + 40, "y": 178},
        "button": {"x": BUTTONLEFTMARGING, "y": 170, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": True
    },
    "x2": {
        # X2 speed button
        "id": 5,
        "text": {"label": "X2", "x": BUTTONLEFTMARGING + 40, "y": 218},
        "button": {"x": BUTTONLEFTMARGING, "y": 210, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False
    },
    "x4": {
        # X4 speed button
        "id": 6,
        "text": {"label": "X4", "x": BUTTONLEFTMARGING + 40, "y": 258},
        "button": {"x": BUTTONLEFTMARGING, "y": 250, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False
    }
}

# Variables: Flow Control
DRAGGING = False

# Start
board = Board()
main()
