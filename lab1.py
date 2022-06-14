from turtle import Screen, Turtle, shape
from utils import *
from math import *
from search import *
from collections import deque

class NormalizeCenter:
    def __call__(self, x,y, center):
        if isinstance(x,list):
            x,y = x 
        x = (x - center[0]) * TILE_SIZE
        y = (center[1] - y) * TILE_SIZE
        return x,y

class Maze:
    def __init__(self, shape, center):
        self.shape = shape
        self.center = center
        self.obstace = []
        self.draw_list = deque()
        self._maze_size()
    
    def _maze_size(self):
        self.maze_width, self.maze_height = map(int,shape.split(' ')) 
        self.maze_width +=2
        self.maze_height +=2
    
    def setup_maze(self, normalize):
        ''' Conversion from the list to the map in turtle. '''

        for y in range(self.maze_height):
            for x in range(self.maze_width):
                screen_x, screen_y = normalize(x,y, self.center)
                if x == 0 or x == self.maze_width-1 or y == 0 or y == self.maze_height-1:
                    self.draw_list.append((screen_x,screen_y,"grey"))
                else:
                    self.draw_list.append((screen_x,screen_y,"white"))

class Position:
    def __init__(self, pos = (0,0)):
        self.pos = pos
        self.draw_list = deque()
        self.draw_list.append((*self.pos,'blue'))
    def asign_to_object(self, object):
        pass

class Source(Position):
    def __init__(self,*args, **kwargs):
        super(Source,self).__init__(*args, **kwargs)
    
    def asign_to_object(self, object):
        object.src_pos = self.pos
    def setup(self, normalize):
        self.draw_list.append((*self.pos,'blue'))

    

class Target(Position):
    def __init__(self,*args, **kwargs):
        super(Target,self).__init__(*args, **kwargs)
        self.draw_list.append((*self.pos,'red'))

    def asign_to_object(self, object):
        object.dst_pos = self.pos

class Polygon:
    def __init__(self, maze):
        self.maze = maze
        self.draw_list = deque()

    def point_line(self, x1, x2):

        dis_x = x1[0] - x2[0]
        dis_y = x1[1] - x2[1]
        
        start_x = x2[0]
        start_y = x2[1]
        end_x = x1[0]
        end_y = x1[1]

        points = [x1,x2]

        if abs(dis_x) > abs(dis_y):
            step_x = 1* sign(dis_x)
            step_y = dis_y/abs(dis_x)
            start = start_x
            end = end_x
            step = 1*sign(dis_x)
            
        elif abs(dis_x) < abs(dis_y):
            step_y = 1* sign(dis_y)
            step_x = dis_x/abs(dis_y)
            start = start_y
            end = end_y
            step = 1*sign(dis_y)
        else:
            start = start_x
            end = end_x
            step_x = 1* sign(dis_x)
            step_y = 1* sign(dis_y)
            step = 1*sign(dis_x)
        # print(start)
        # print(end)
        while True:
            start_x  += step_x
            start_y  += step_y
            start += step
            # print(start)
            if start == end:
                break
            points.append([floor(start_x), floor(start_y)])

        return points 

    def setup_polygon(self, arr, normalize):
        ind = 0
        while True:
            if ind == len(arr) -2:
                points = self.point_line(arr[ind:ind+2], arr[:2])
            else:
                points = self.point_line(arr[ind:ind+2],arr[ind+2:ind+4])
           
            for i, pos in enumerate(points):
                x,y = normalize(*pos,self.maze.center)
                if i in [0,1]:
                    self.draw_list.append((x,y,'orange'))
                else:
                    self.draw_list.append((x,y,'yellow'))
                
                self.maze.obstace.append(pos)
            
            ind = ind + 2
            if ind >= len(arr) -1:
                break


class Draw():

    def draw(self, pen, draw_oject):
        while len(draw_oject.draw_list) != 0:
            x,y , color = draw_oject.draw_list.popleft()
            pen.color('black',color)
            pen.goto(x,y)
            pen.pendown()
            pen.stamp()
            pen.penup()

class DrawPath():
    def draw(self, pen, draw_oject, path, normalize):
        for x,y, color in draw_oject.path:
            pen.color('black',color)
            pen.goto(x,y)
            pen.pendown()
            pen.stamp()
            # pen.penup()

if __name__ == "__main__":
  
    shape, src_pos, des_pos, obstace = read_input('input.txt')
    maze_width,maze_height = map(int,shape.split(' '))

    screen = Screen()
    screen.setup((maze_width + 4)*TILE_SIZE, (maze_height + 4)*TILE_SIZE)
    screen.title("MAZE")
    
    wall_draw = PenWall()
    bg_draw = PenInWall()
    src_draw = SourceDraw()
    dst_draw = DstDraw()
    pen_poly = PenPoly()

    # draw = Draw(shape, (maze_width/2,maze_height/2),src_pos, des_pos, BFS)

    # draw.setup_maze(wall_draw, bg_draw)
    # draw.setup_position(src_draw, dst_draw)
    # for obj in obstace:
    #     obj_list = list(map(int,obj.split(' ')))
    #     draw.drawPolygon(obj_list, pen_poly)
    # # draw.iterSearch(PenPath(), 40)
    # draw.search(PenPath())

    normalize = NormalizeCenter()
    maze = Maze(shape, (maze_width/2,maze_height/2))
    maze.setup_maze(normalize)
    draw = Draw()
    draw_path = DrawPath()
    draw.draw(wall_draw, maze)
    polygon = Polygon(maze)
    for obj in obstace:
        obj_list = list(map(int,obj.split(' ')))
        polygon.setup_polygon(obj_list, normalize)
    
    draw.draw(pen_poly,polygon)
    source = Source(src_pos)
    source.asign_to_object(maze)
    target = Target(des_pos)
    target.asign_to_object(maze)
    draw.draw(src_draw, source)
    draw.draw(src_draw, target)

    search = BFS(maze)
    search.find()
    draw.draw(PenPath(), search)

    # draw.join()

    screen.mainloop()

    # print(point_line([4,4],[5,9]))