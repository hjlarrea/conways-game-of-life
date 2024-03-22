from random import randint
import pygame,pgzero,pgzrun

WIDTH = 800
HEIGHT = 630

def draw():
    screen.draw.rect(Rect((10,10),(609,609)),(200,200,200))
    for item in state:
        screen.draw.filled_rect(Rect(item),(200,200,200))
        


def update():
    pass

def on_mouse_down(pos):
    global state
    global dragging
    coordinates = returnCoordinates(pos)
    (x,y),(wx,wy) = coordinates
    if x > 9 and x <= 610 and y > 9 and y <= 610:
        dragging = True
        state.append(coordinates)

def on_mouse_up():
    global dragging
    dragging = False

def on_mouse_move(pos):
    global state
    coordinates = returnCoordinates(pos)
    (x,y),(wx,wy) = coordinates
    if x > 9 and x <= 610 and y > 9 and y <= 610 and dragging == True:
        state.append(coordinates)

def returnCoordinates(pos):
    chunkSize = 10
    x,y = pos
    absX = int(x/chunkSize)*10
    absY = int(y/chunkSize)*10
    return ((absX,absY),(9,9))

def main():
    pgzrun.go()

dragging = False
state = []
main()