from turtle import Screen, Turtle, shape
from math import *
TILE_SIZE = 24
CURSOR_SIZE = 20


def read_input(input_file):
    with open(input_file,'r') as f:
        data = f.read().splitlines()
    
    shape = data[0]
    pos = list(map(int,data[1].split(' ')))
    src_pos = pos[:2] 
    des_pos = pos[2:]
    obstace = data[3:]

    return shape, src_pos, des_pos, obstace

def sign(x):
    return int(copysign(1,x))

class Pen(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('square')
        self.shapesize(TILE_SIZE / CURSOR_SIZE)
        self.color('black', 'grey')
        self.penup()
        self.speed('fastest')

class PenWall(Pen):
    def __init__(self):
        super().__init__()
        # self.color('black', 'grey')

class PenInWall(Pen):
    def __init__(self):
        super().__init__()
        self.color('black', 'white')

class SourceDraw(Pen):
    def __init__(self):
        super().__init__()
        self.color('black', 'blue')
        
class DstDraw(Pen):
    def __init__(self):
        super().__init__()
        self.color('black', 'red')

class PenPoly(Pen):
    def __init__(self):
        super().__init__()
        self.color('black', 'yellow')

class PenPath(Pen):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color('black', 'white')
        self.shapesize(TILE_SIZE / (2*CURSOR_SIZE))