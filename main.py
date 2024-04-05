from random import randint
import pygame,pgzero,pgzrun
import matplotlib.pyplot as plt

# Game loops

def draw():
    screen.clear()

    # Render Buttons
    for key in buttons.keys():
        if buttons[key]["active"] == False:
            screen.draw.text(buttons[key]["text"]["label"],(buttons[key]["text"]["x"],buttons[key]["text"]["y"]))
            screen.draw.rect(Rect((buttons[key]["button"]["x"],buttons[key]["button"]["y"]),(buttons[key]["button"]["width"],buttons[key]["button"]["height"])),(255,255,255))
        else:
            # Paint the active speed button
            screen.draw.filled_rect(Rect((buttons[key]["button"]["x"],buttons[key]["button"]["y"]),(buttons[key]["button"]["width"],buttons[key]["button"]["height"])),(255,255,255))
            screen.draw.text(buttons[key]["text"]["label"],(buttons[key]["text"]["x"],buttons[key]["text"]["y"]),color=(0,0,0))

    # Render Status Messages
    if board.getGameMode() == 0:
        screen.draw.text("Status: Paused", midleft=(buttonLeftMargin,HEIGHT - 110))
    elif board.getGameMode() == 1 or board.getGameMode() == 3:
        screen.draw.text("Status: In Progress", midleft=(buttonLeftMargin,HEIGHT - 110))
    screen.draw.text(f"Generation: {board.getGeneration()}", midleft=(buttonLeftMargin,HEIGHT - 70))
    screen.draw.text(f"Alive Cells: {board.getAliveCells()}", midleft=(buttonLeftMargin,HEIGHT - 30))

    # Render Main Board Square
    screen.draw.rect(Rect((margingSpacing,margingSpacing),(boardSizePx,boardSizePx)),(255,255,255))

    # Draw generation on the screen
    for i in range(0,boardSize):
        for j in range(0,boardSize):
            if board.getCell(row=i,col=j).isAlive():
                screen.draw.filled_rect(Rect(board.getCell(row=i,col=j).getX(),board.getCell(row=i,col=j).getY(),board.getCell(row=i,col=j).getXWidth(),board.getCell(row=i,col=j).getYWidth()),(255,255,255))
            else:
                if board.gameMode != 1: # If game is not in progress (e.g. paused) draw a grid on the screen
                    screen.draw.line((board.getCell(row=i,col=j).getX(),board.getCell(row=i,col=j).getY()+9),(board.getCell(row=i,col=j).getX()+9,board.getCell(row=i,col=j).getY()+9),(255,255,255))
                    screen.draw.line((board.getCell(row=i,col=j).getX()+9,board.getCell(row=i,col=j).getY()),(board.getCell(row=i,col=j).getX()+9,board.getCell(row=i,col=j).getY()+9),(255,255,255))

# Event hooks

def on_mouse_down(pos):
    global board
    global dragging

    clicked = clickedButton(pos)
    if clicked == 0: # Start button
        board.gameMode = 1
    elif clicked == 1: # Reset button
        board.gameMode = 0
        board.resetBoard()
    elif clicked == 2: # Pause button
        board.gameMode = 0
    elif clicked == 3: # Step button
        board.gameMode = 3
    elif clicked == 4: # X1 speed button
        clock.unschedule(board.nextGen)
        clock.schedule_interval(board.nextGen, 1.0) # Schedule board updates
        buttons["x1"]["active"] = True
        buttons["x2"]["active"] = False
        buttons["x4"]["active"] = False
    elif clicked == 5: # X2 speed button
        clock.unschedule(board.nextGen)
        clock.schedule_interval(board.nextGen, 0.5) # Schedule board updates
        buttons["x1"]["active"] = False
        buttons["x2"]["active"] = True
        buttons["x4"]["active"] = False
    elif clicked == 6: # X4 speed button
        clock.unschedule(board.nextGen)
        clock.schedule_interval(board.nextGen, 0.25) # Schedule board updates
        buttons["x1"]["active"] = False
        buttons["x2"]["active"] = False
        buttons["x4"]["active"] = True
    elif board.gameMode != 1: # Block making further changes one the game has started
        row,col = returnRowCol(pos)
        if posInBoard(pos):
            dragging = True
            if board.getCell(row=row,col=col).isAlive(): #Activate or deactivate on click depending on previous state
                board.getCell(row=row,col=col).setDead()
            else:
                board.getCell(row=row,col=col).setAlive()

def on_mouse_up():
    global dragging
    dragging = False

def on_mouse_move(pos):
    global board
    if board.gameMode != 1: # Block making further changes one the game has started
        row,col = returnRowCol(pos)
        if posInBoard(pos) and dragging == True:
            board.getCell(row=row,col=col).setAlive()

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
    for key in buttons.keys():
        if buttons[key]["button"]["x"] <= pos[0] <= (buttons[key]["button"]["x"] + buttons[key]["button"]["width"]) and buttons[key]["button"]["y"] <= pos[1] <= (buttons[key]["button"]["y"] + buttons[key]["button"]["height"]):
            return buttons[key]["id"] 
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

# Classes

# Board class  
class Board():
    generation = 0
    aliveCells = 0
    gameMode = 0

    def __init__(self):
        self.state =  [[Cell(x=j*10+10,y=i*10+10) for j in range(0,boardSize)] for i in range(0,boardSize)]

    def getCell(self,row,col):
        return self.state[row][col]
    
    def getGeneration(self):
        return self.generation
    
    def getAliveCells(self):
        return self.aliveCells
    
    def getGameMode(self):
        return self.gameMode
    
    def setGameMode(self,mode):
        self.gameMode = mode

    def aliveNeightbours(self,row,col):
        aliveNeightbours = 0
        neightbours = self.cellNeightbours(row=row,col=col)
        for row,col in neightbours:
            if self.getCell(row=row,col=col).alive:
                aliveNeightbours+=1
        return aliveNeightbours

    def resetBoard(self):
        self.state = [[Cell(x=j*10+10,y=i*10+10) for j in range(0,boardSize)] for i in range(0,boardSize)]
        self.generation = 0
        self.aliveCells = 0
        self.gameMode = 0
        
    def nextGen(self):
        if board.gameMode == 1 or board.gameMode == 3:
            state2 = [[Cell(x=j*10+10,y=i*10+10) for j in range(0,boardSize)] for i in range(0,boardSize)]
            for i in range(0,boardSize):
                for j in range(0,boardSize):
                    if self.aliveNeightbours(row=i,col=j) < 2:
                        state2[i][j].setDead()
                    elif self.aliveNeightbours(row=i,col=j) > 3:
                        state2[i][j].setDead()
                    elif self.aliveNeightbours(row=i,col=j) == 3:
                        state2[i][j].setAlive()
                    else:
                        state2[i][j] = self.getCell(row=i,col=j)
            if self.getGameMode() == 3: # Step forward and revert back to state 0
                self.setGameMode(0)
            self.state = state2
            self.generation += 1
            self.aliveCells = len([self.getCell(row=i,col=j) for i in range(0,boardSize) for j in range(0,boardSize) if self.getCell(row=i,col=j).isAlive()])
    
    def cellNeightbours(self,row,col):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_x = (row + i) % boardSize
                neighbor_y = (col + j) % boardSize
                neighbors.append((neighbor_x,neighbor_y))
        return neighbors


# Cell class
class Cell():
    xWidth = 9
    yWidth = 9
    alive = False

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getXWidth(self):
        return self.xWidth
    
    def getYWidth(self):
        return self.yWidth

    def setAlive(self):
        self.alive = True

    def setDead(self):
        self.alive = False

    def isAlive(self):
        return self.alive

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
buttons = { # Screen elements to be rendered
    "start": { 
        # Start Button
        "id": 0,
        "text": {"label": "Start", "x": buttonLeftMargin + 30, "y": 18},
        "button" : {"x": buttonLeftMargin, "y": 10, "width": buttonWidth, "height": buttonHeight},
        "active": False
    },
    "reset": {
        # Reset button
        "id": 1,
        "text": {"label": "Reset", "x": buttonLeftMargin + 28, "y": 58},
        "button" : {"x": buttonLeftMargin, "y": 50, "width": buttonWidth, "height": buttonHeight},
        "active": False
    },
    "pause": {
        # Pause button
        "id": 2,
        "text": {"label": "Pause", "x": buttonLeftMargin + 28, "y": 98},
        "button" : {"x": buttonLeftMargin, "y": 90, "width": buttonWidth, "height": buttonHeight},
        "active": False
    },
    "step":{
        # Step button
        "id": 3,
        "text": {"label": "Step", "x": buttonLeftMargin + 30, "y": 138},
        "button" : {"x": buttonLeftMargin, "y": 130, "width": buttonWidth, "height": buttonHeight},
        "active": False
    },
    "x1":{
        # X1 speed button
        "id": 4,
        "text": {"label": "X1", "x": buttonLeftMargin + 40, "y": 178},
        "button" : {"x": buttonLeftMargin, "y": 170, "width": buttonWidth, "height": buttonHeight},
        "active": True
    },
    "x2": {
        # X2 speed button
        "id": 5,
        "text": {"label": "X2", "x": buttonLeftMargin + 40, "y": 218},
        "button" : {"x": buttonLeftMargin, "y": 210, "width": buttonWidth, "height": buttonHeight},
        "active": False
    },
    "x4": {
        # X4 speed button
        "id": 6,
        "text": {"label": "X4", "x": buttonLeftMargin + 40, "y": 258},
        "button" : {"x": buttonLeftMargin, "y": 250, "width": buttonWidth, "height": buttonHeight},
        "active": False
    }
}

# Variables: Flow Control
dragging = False

# Start
board = Board()
main()