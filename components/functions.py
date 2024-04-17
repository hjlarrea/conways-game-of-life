"""
This file contains the auxiliary functions to be used by the main project.

Author: Hernan J. Larrea (hjlarrea@hotmail.com)
Date: March, 2024
"""

# Helper functions

# Returns the cell coordinates of the mouse position for drawing the squares


def pos_in_board(pos, board_size_px):
    """Returns a boolean that is True when the position being clicked is within the borders
    of the board."""
    x, y = pos
    if x > 9 and x <= board_size_px+9 and y > 9 and y <= board_size_px+9:
        return True
    return False

# Determine in which button from the Buttons dictionarity the user clicked


def clicked_button(pos, buttons):
    """Returns the button id based on the positional coordinates of the mouse when 
    clicked. For references on the buttons check the buttons variable."""
    for key in buttons.keys():
        if buttons[key]["button"]["x"] <= pos[0] <= (buttons[key]["button"]["x"] + buttons[key]["button"]["width"]) and buttons[key]["button"]["y"] <= pos[1] <= (buttons[key]["button"]["y"] + buttons[key]["button"]["height"]):
            return buttons[key]["id"]
    return -1

# Returns the column and row of a given mouse position in the multi demensional array


def return_row_col(pos, chunk_size):
    """Returns a tuple with row,col coordinates based on the positional coordinates 
    of the mouse when clicked"""
    x, y = pos
    row = int(y/chunk_size) - 1
    col = int(x/chunk_size) - 1
    return row, col
