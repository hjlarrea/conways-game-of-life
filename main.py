from random import randint
import pygame,pgzero,pgzrun
import matplotlib.pyplot as plt

# Game loops

def draw():
    screen.clear()

    # Render Buttons
    for button in buttons:
        screen.draw.text(button["text"]["label"],(button["text"]["x"],button["text"]["y"]))
        screen.draw.rect(Rect((button["button"]["x"],button["button"]["y"]),(button["button"]["width"],button["button"]["height"])),(255,255,255))

    # Render Status Messages
    if gameMode == 0:
        screen.draw.text("Status: Paused", midleft=(buttonLeftMargin,HEIGHT - 110))
    elif gameMode == 1 or gameMode == 3:
        screen.draw.text("Status: In Progress", midleft=(buttonLeftMargin,HEIGHT - 110))
    screen.draw.text(f"Generation: {generation}", midleft=(buttonLeftMargin,HEIGHT - 70))
    screen.draw.text(f"Alive Cells: {aliveCells}", midleft=(buttonLeftMargin,HEIGHT - 30))

    # Render Main Board Square
    screen.draw.rect(Rect((margingSpacing,margingSpacing),(boardSizePx,boardSizePx)),(255,255,255))

    # Draw generation on the screen
    for i in range(0,boardSize):
        for j in range(0,boardSize):
            if board[i][j].alive:
                screen.draw.filled_rect(Rect(board[i][j].x,board[i][j].y,board[i][j].xWidth,board[i][j].yWidth),(255,255,255))
            else:
                if gameMode != 1:
                    screen.draw.line((board[i][j].x,board[i][j].y+9),(board[i][j].x+9,board[i][j].y+9),(255,255,255))
                    screen.draw.line((board[i][j].x+9,board[i][j].y),(board[i][j].x+9,board[i][j].y+9),(255,255,255))

# Event hooks

def on_mouse_down(pos):
    global state
    global dragging
    global gameMode

    clicked = clickedButton(pos)
    if clicked == 0:
        gameMode = 1
    elif clicked == 1:
        gameMode = 0
        resetBoard()
    elif clicked == 2:
        gameMode = 0
    elif clicked == 3:
        gameMode = 3
    elif gameMode != 1: # Block making further changes one the game has started
        row,col = returnRowCol(pos)
        if posInBoard(pos):
            dragging = True
            if (board[row][col]).isAlive(): #Activate or deactivate on click depending on previous state
                board[row][col].setDead()
            else:
                board[row][col].setAlive()

def on_mouse_up():
    global dragging
    dragging = False

def on_mouse_move(pos):
    global state
    if gameMode != 1: # Block making further changes one the game has started
        row,col = returnRowCol(pos)
        if posInBoard(pos) and dragging == True:
            board[row][col].setAlive()

# Helper functions

# Returns the cell coordinates of the mouse position for drawing the squares
def posInBoard(pos):
    x,y = pos
    if x > 9 and x <= boardSizePx+9 and y > 9 and y <= boardSizePx+9:
        return True
    else:
        return False

# Determine in which button from the Buttons dictionarity the user clicked
def clickedButton(pos):
    for button in buttons:
        if button["button"]["x"] <= pos[0] <= (button["button"]["x"] + button["button"]["width"]) and button["button"]["y"] <= pos[1] <= (button["button"]["y"] + button["button"]["height"]):
            return button["id"] 
    return -1

# Returns the column and row of a given mouse position in the multi demensional array
def returnRowCol(pos):
    x,y = pos
    row = int(y/chunkSize) - 1
    col = int(x/chunkSize) - 1
    return row,col

# Sets board to next generation based on the previous one
def nextGen():
    global board
    global gameMode
    global generation
    global aliveCells
    if gameMode == 1 or gameMode == 3:
        board2 = [[Cell(x=i*10+10,y=j*10+10,row=i,col=j) for i in range(0,boardSize)] for j in range(0,boardSize)]
        for i in range(0,boardSize):
            for j in range(0,boardSize):
                if board[j][i].aliveNeightbours() < 2:
                    board2[j][i].setDead()
                elif board[j][i].aliveNeightbours() > 3:
                    board2[j][i].setDead()
                elif board[j][i].aliveNeightbours() == 3:
                    board2[j][i].setAlive()
                else:
                    board2[j][i] = board[j][i]
        if gameMode == 3:
            gameMode = 0
        board = board2
        generation += 1
        aliveCells = len([board[i][j] for i in range(0,boardSize) for j in range(0,boardSize) if board[i][j].isAlive()])

def resetBoard():
    global board
    global generation
    global aliveCells
    generation = 0
    aliveCells = 0
    board = [[Cell(x=i*10+10,y=j*10+10,row=i,col=j) for i in range(0,boardSize)] for j in range(0,boardSize)]

def main():
    resetBoard()
    # Schedule 1 generation per sectond
    clock.schedule_interval(nextGen, 1.0) # Schedule board updates
    pgzrun.go()

# Cell class

class Cell():
    xWidth = 9
    yWidth = 9
    alive = False

    def __init__(self,x,y, row, col):
        self.x = x
        self.y = y
        self.row = row
        self.col = col

    def setAlive(self):
        self.alive = True

    def setDead(self):
        self.alive = False

    def isAlive(self):
        return self.alive

    def boardNeightbours(self):
        neighbors = []
        for i in range(self.row - 1, self.row + 2):
            for j in range(self.col - 1, self.col + 2):
                if (i != self.row or j != self.col) and 0 <= i < boardSize and 0 <= j < boardSize:
                    neighbors.append((j, i))
        return neighbors
    
    def aliveNeightbours(self):
        aliveNeightbours = 0
        neightbours = self.boardNeightbours()
        for row,col in neightbours:
            if board[row][col].alive:
                aliveNeightbours+=1
        return aliveNeightbours

# Global Variables
boardSize = 80 # Number of cells (e.g. 80 = 80*80)
chunkSize = 10 # Size of each cell for rendering
margingSpacing = 10
boardSizePx = boardSize * chunkSize
buttonLeftMargin = boardSizePx + 2 * margingSpacing
buttonWidth = 100
buttonHeight = 30
textWidth = 200
WIDTH = boardSizePx + 3 * margingSpacing + textWidth
HEIGHT = boardSizePx + 2 * margingSpacing
gameMode = 0
generation = 0
aliveCells = 0
dragging = False
board = ""
buttons = [ # Screen elements to be rendered
    { 
        # Start Button
        "id": 0,
        "text": {"label": "Start", "x": buttonLeftMargin + 30, "y": 18},
        "button" : {"x": buttonLeftMargin, "y": 10, "width": buttonWidth, "height": buttonHeight}
    },
    {
        # Reset button
        "id": 1,
        "text": {"label": "Reset", "x": buttonLeftMargin + 28, "y": 58},
        "button" : {"x": buttonLeftMargin, "y": 50, "width": buttonWidth, "height": buttonHeight}
    },
    {
        # Pause button
        "id": 2,
        "text": {"label": "Pause", "x": buttonLeftMargin + 28, "y": 98},
        "button" : {"x": buttonLeftMargin, "y": 90, "width": buttonWidth, "height": buttonHeight}
    },
    {
        # Step button
        "id": 3,
        "text": {"label": "Step", "x": buttonLeftMargin + 30, "y": 138},
        "button" : {"x": buttonLeftMargin, "y": 130, "width": buttonWidth, "height": buttonHeight}
    }
]

# Start
main()