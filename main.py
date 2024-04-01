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
    if board.gameMode == 0:
        screen.draw.text("Status: Paused", midleft=(buttonLeftMargin,HEIGHT - 110))
    elif board.gameMode == 1 or board.gameMode == 3:
        screen.draw.text("Status: In Progress", midleft=(buttonLeftMargin,HEIGHT - 110))
    screen.draw.text(f"Generation: {board.generation}", midleft=(buttonLeftMargin,HEIGHT - 70))
    screen.draw.text(f"Alive Cells: {board.aliveCells}", midleft=(buttonLeftMargin,HEIGHT - 30))

    # Render Main Board Square
    screen.draw.rect(Rect((margingSpacing,margingSpacing),(boardSizePx,boardSizePx)),(255,255,255))

    # Draw generation on the screen
    for i in range(0,boardSize):
        for j in range(0,boardSize):
            if board.state[i][j].alive:
                screen.draw.filled_rect(Rect(board.state[i][j].x,board.state[i][j].y,board.state[i][j].xWidth,board.state[i][j].yWidth),(255,255,255))
            else:
                if board.gameMode != 1:
                    screen.draw.line((board.state[i][j].x,board.state[i][j].y+9),(board.state[i][j].x+9,board.state[i][j].y+9),(255,255,255))
                    screen.draw.line((board.state[i][j].x+9,board.state[i][j].y),(board.state[i][j].x+9,board.state[i][j].y+9),(255,255,255))

# Event hooks

def on_mouse_down(pos):
    global board
    global dragging

    clicked = clickedButton(pos)
    if clicked == 0:
        board.gameMode = 1
    elif clicked == 1:
        board.gameMode = 0
        board.resetBoard()
    elif clicked == 2:
        gameMode = 0
    elif clicked == 3:
        board.gameMode = 3
    elif board.gameMode != 1: # Block making further changes one the game has started
        row,col = returnRowCol(pos)
        if posInBoard(pos):
            dragging = True
            if (board.state[row][col]).isAlive(): #Activate or deactivate on click depending on previous state
                board.state[row][col].setDead()
            else:
                board.state[row][col].setAlive()

def on_mouse_up():
    global dragging
    dragging = False

def on_mouse_move(pos):
    global board
    if board.gameMode != 1: # Block making further changes one the game has started
        row,col = returnRowCol(pos)
        if posInBoard(pos) and dragging == True:
            board.state[row][col].setAlive()

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

# Main function
def main():
    board.resetBoard()
    clock.schedule_interval(board.nextGen, 1.0) # Schedule board updates
    pgzrun.go()

# Board class
    
class Board():

    generation = 0
    aliveCells = 0
    gameMode = 0

    def __init__(self):
        self.state =  [[Cell(x=i*10+10,y=j*10+10,row=i,col=j) for i in range(0,boardSize)] for j in range(0,boardSize)]

    def getCell(self,row,col):
        return self.state[row][col].isAlive
    
    def setCellDead(self,row,col):
        self.state[row][col].setDead()
    
    def setCellAlive(self,row,col):
        self.state[row][col].setAlive()

    def aliveNeightbours(self,row,col):
        aliveNeightbours = 0
        neightbours = self.state[row][col].boardNeightbours()
        for row,col in neightbours:
            if self.state[row][col].alive:
                aliveNeightbours+=1
        return aliveNeightbours

    def resetBoard(self):
        self.state = [[Cell(x=i*10+10,y=j*10+10,row=i,col=j) for i in range(0,boardSize)] for j in range(0,boardSize)]
        self.generation = 0
        self.aliveCells = 0
        
    def nextGen(self):
        if board.gameMode == 1 or board.gameMode == 3:
            state2 = [[Cell(x=i*10+10,y=j*10+10,row=i,col=j) for i in range(0,boardSize)] for j in range(0,boardSize)]
            for i in range(0,boardSize):
                for j in range(0,boardSize):
                    if self.aliveNeightbours(row=j,col=i) < 2:
                        state2[j][i].setDead()
                    elif self.aliveNeightbours(row=j,col=i) > 3:
                        state2[j][i].setDead()
                    elif self.aliveNeightbours(row=j,col=i) == 3:
                        state2[j][i].setAlive()
                    else:
                        state2[j][i] = self.state[j][i]
            if self.gameMode == 3:
                self.gameMode = 0
            self.state = state2
            self.generation += 1
            self.aliveCells = len([self.state[i][j] for i in range(0,boardSize) for j in range(0,boardSize) if self.state[i][j].isAlive()])

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

# Variables: Configuration
boardSize = 80 # Number of cells (e.g. 80 = 80*80)
chunkSize = 10 # Size of each cell for rendering
margingSpacing = 10 # Marging space between board and other elements
boardSizePx = boardSize * chunkSize # Board size in pixels
buttonLeftMargin = boardSizePx + 2 * margingSpacing # Where buttons shoudl be placed in the x axis in relation to the board
buttonWidth = 100 # Button size
buttonHeight = 30 # Button sie
textWidth = 200 # Labels width (e.g. Number of alive cells or status)
WIDTH = boardSizePx + 3 * margingSpacing + textWidth # Window width
HEIGHT = boardSizePx + 2 * margingSpacing # Windows height
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

# Variables: Flow Control
dragging = False

# Start
board = Board()
main()