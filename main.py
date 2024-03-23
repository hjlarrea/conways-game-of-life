from random import randint
import pygame,pgzero,pgzrun

# Constants

WIDTH = 800
HEIGHT = 630
chunkSize = 10

# Game loops

def draw():
    screen.clear()
    start.draw()
    screen.draw.rect(Rect((10,10),(609,609)),(200,200,200))
    for i in range(0,61):
        for j in range(0,61):
            if board[i][j].alive:
                screen.draw.filled_rect(Rect(board[i][j].x,board[i][j].y,board[i][j].xWidth,board[i][j].yWidth),(255,255,255))
        
def update():
    pass

# Event hooks

def on_mouse_down(pos):
    global state
    global dragging
    global gameMode
    if start.collidepoint(pos):
        gameMode = 1
    else:
        row,col = returnRowCol(pos)
        if posInBoard(pos):
            dragging = True
            board[row][col].setAlive()

def on_mouse_up():
    global dragging
    dragging = False

def on_mouse_move(pos):
    global state
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

# Place the start button
def placeStartButton():
    start.x = 710
    start.y = 50

def nextGen():
    global board
    if gameMode == 1:
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
        board = board2

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

# Main
def main():
    placeStartButton()
    pgzrun.go()

gameMode = 0
dragging = False
start = Actor("start")
clock.schedule_interval(nextGen, 1.0)
board = [[Cell(x=i*10+10,y=j*10+10,row=i,col=j) for i in range(0,61)] for j in range(0,61)]
main()