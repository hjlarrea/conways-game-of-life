"""
Conway's Game of Life in Python using PyGame Zero

Coded as a personal proyect to satisfy curiosity and learn about PyGame Zero Capabilities.

Author: Hernan J. Larrea (hjlarrea@hotmail.com)
Date: March, 2024
"""

import pgzrun
from pgzero import clock
from pygame import Rect
import pgzero.screen
screen: pgzero.screen.Screen
from components.classes import Board
from components.functions import clicked_button, pos_in_board, return_row_col

# Game loops


def draw():
    """PyGame Zero's Game Loop"""
    screen.clear()

    # Render Buttons
    for key in buttons.keys():
        if buttons[key]["active"] is False:
            method = "rect"
            if buttons[key]["enabled"] is True:
                rect_color = (255, 255, 255)
                text_color = (255, 255, 255)
            else:
                rect_color = (100, 100, 100)
                text_color = (100, 100, 100)
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
    elif board.get_game_mode() == 6:
        screen.draw.text("Status: Stable", midleft=(
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
                if board.get_game_mode() == 0:
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

    clicked = clicked_button(pos, buttons)
    if clicked == 0:  # Start button
        board.set_game_mode(1)
        buttons["save"]["enabled"] = False
        buttons["load"]["enabled"] = False
        buttons["randomize"]["enabled"] = False
    elif clicked == 1:  # Reset button
        board.set_game_mode(0)
        buttons["save"]["enabled"] = True
        buttons["load"]["enabled"] = True
        buttons["randomize"]["enabled"] = True
        board.reset_board()
    elif clicked == 2:  # Pause button
        board.set_game_mode(0)
        buttons["save"]["enabled"] = True
        buttons["load"]["enabled"] = True
    elif clicked == 3:  # Step button
        board.set_game_mode(3)
        buttons["save"]["enabled"] = True
        buttons["load"]["enabled"] = True
        buttons["randomize"]["enabled"] = False
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
    elif clicked == 10:
        board.randomize()
    elif board.get_game_mode() == 0:  # Only allow making changes when the game is not in progress
        row, col = return_row_col(pos, CHUNKSIZE)
        if pos_in_board(pos, BOARDSIZEPX):
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
        row, col = return_row_col(pos, CHUNKSIZE)
        if pos_in_board(pos, BOARDSIZEPX) and DRAGGING:
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
            file_name += chr(key)

# Main function


def main():
    """Main function, executs the entire game."""
    board.reset_board()
    clock.schedule_interval(board.calculate_next_generation,
                            1.0)  # Schedule board updates
    pgzrun.go()


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
        "text": {"label": "Play", "x": BUTTONLEFTMARGING + 30, "y": 18},
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
        "text": {"label": "FW", "x": BUTTONLEFTMARGING + 35, "y": 138},
        "button": {"x": BUTTONLEFTMARGING, "y": 130, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    },
    "back": {
        # Step back button
        "id": 4,
        "text": {"label": "RW", "x": BUTTONLEFTMARGING + 35, "y": 178},
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
    },
    "randomize": {
        "id": 10,
        "text": {"label": "Randomize", "x": BUTTONLEFTMARGING + 5, "y": 418},
        "button": {"x": BUTTONLEFTMARGING, "y": 410, "width": BUTTONWIDTH, "height": BUTTONHEIGHT},
        "active": False,
        "enabled": True
    }
}

# Variables: Flow Control
DRAGGING = False
file_name = ""

# Start
board = Board(BOARDSIZE)
main()
