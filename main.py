from random import randint
import pygame,pgzero,pgzrun
import matplotlib.pyplot as plt

# Constants

WIDTH = 800
HEIGHT = 630
chunkSize = 10
boardSize = 61
boardSizePx = boardSize * 10

# Game loops

def draw():
    screen.clear()
    
    buttons = [
        { 
            # Start Button
            "text": {"label": "Start", "x": 660, "y": 18},
            "button" : {"x": 630, "y": 10, "width": 100, "height": 30}
        },
        {
            # Reset button
            "text": {"label": "Reset", "x": 658, "y": 58},
            "button" : {"x": 630, "y": 50, "width": 100, "height": 30}
        },
        {
            # Pause button
            "text": {"label": "Pause", "x": 658, "y": 98},
            "button" : {"x": 630, "y": 90, "width": 100, "height": 30}
        },
        {
            # Step button
            "text": {"label": "Step", "x": 660, "y": 138},
            "button" : {"x": 630, "y": 130, "width": 100, "height": 30}
        }
    ]

    # Render Buttons
    for button in buttons:
        screen.draw.text(button["text"]["label"],(button["text"]["x"],button["text"]["y"]))
        screen.draw.rect(Rect((button["button"]["x"],button["button"]["y"]),(button["button"]["width"],button["button"]["height"])),(255,255,255))

    # Render Status Message
    if gameMode == 0:
        screen.draw.text("Status: Paused", midleft=(630,550))
    elif gameMode == 1 or gameMode == 3:
        screen.draw.text("Status: In Progress", midleft=(630,550))
    screen.draw.text(f"Generation: {generation}", midleft=(630,580))
    screen.draw.text(f"Alive Cells: {aliveCells}", midleft=(630,610))

    # Render Main Board Square
    screen.draw.rect(Rect((10,10),(609,609)),(200,200,200))

    # Draw generation on the screen
    for i in range(0,61):
        for j in range(0,61):
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
    if 630 <= pos[0] <= 730 and 10 <= pos[1] <= 40: # Start button coordinates
        gameMode = 1
    elif 630 <= pos[0] <= 730 and 50 <= pos[1] <= 80: # Reset button coordinates
        gameMode = 0
        resetBoard()
    elif 630 <= pos[0] <= 730 and 90 <= pos[1] <= 120: # Pause button coordinates
        gameMode = 0
    elif 630 <= pos[0] <= 730 and 130 <= pos[1] <= 160: # Step button coordinates
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
    if x > 9 and x <= 619 and y > 9 and y <= 619:
        return True
    else:
        return False

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
        board2 = [[Cell(x=i*10+10,y=j*10+10,row=i,col=j) for i in range(0,61)] for j in range(0,61)]
        for i in range(0,61):
            for j in range(0,61):
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
        aliveCells = len([board[i][j] for i in range(0,61) for j in range(0,61) if board[i][j].isAlive()])

def resetBoard():
    global board
    global generation
    global aliveCells
    generation = 0
    aliveCells = 0
    board = [[Cell(x=i*10+10,y=j*10+10,row=i,col=j) for i in range(0,61)] for j in range(0,61)]

def main():
    resetBoard()
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
                if (i != self.row or j != self.col) and 0 <= i < 61 and 0 <= j < 61:
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
gameMode = 0
generation = 0
aliveCells = 0
dragging = False
board = ""

# Schedule 1 generation per sectond
clock.schedule_interval(nextGen, 1.0) # Schedule board updates

# Start
main()