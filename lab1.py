from turtle import Screen, Turtle, shape
from utils import *
from math import *
from search import *

class Draw:
    def __init__(self, shape, center, src_pos, dst_pos, method):
        self.shape = shape
        self.center = center
        self.src_pos = src_pos
        self.dst_pos = dst_pos
        self.obstace = []
        self._maze_size()
        self.method = method(self.maze_width,self.maze_height,src_pos,dst_pos, center)

    def _maze_size(self):
        self.maze_width, self.maze_height = map(int,shape.split(' ')) 
        self.maze_width +=2
        self.maze_height +=2
    
    def normalize(self, x,y):
        if isinstance(x,list):
            x,y = x 
        x = (x - self.center[0]) * TILE_SIZE
        y = (self.center[1] - y) * TILE_SIZE
        return x,y

    def setup_maze(self, wall_draw, bg_draw):
        ''' Conversion from the list to the map in turtle. '''

        for y in range(self.maze_height):
            for x in range(self.maze_width):
                screen_x, screen_y = self.normalize(x,y)
                if x == 0 or x == self.maze_width-1 or y == 0 or y == self.maze_height-1:
                    wall_draw.goto(screen_x, screen_y)
                    wall_draw.stamp()

                else:
                    bg_draw.goto(screen_x, screen_y)
                    bg_draw.stamp()

    def _draw(self, pos, draw):
        draw.goto(pos[0],pos[1])
        draw.pendown()
        draw.stamp()  

    def setup_position(self, src_draw, dst_draw):
        screen_x_src,screen_y_src = self.normalize(self.src_pos, None) 
        screen_x_dst, screen_y_dst = self.normalize(self.dst_pos, None)
        self._draw((screen_x_src,screen_y_src),src_draw)
        self._draw((screen_x_dst,screen_y_dst),dst_draw)

    def point_line(self, x1,x2):

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

    def drawPolygon(self, arr, draw):
        ind = 0
        while True:
            if ind == len(arr) -2:
                points = self.point_line(arr[ind:ind+2], arr[:2])
            else:
                points = self.point_line(arr[ind:ind+2],arr[ind+2:ind+4])
           
            for i, pos in enumerate(points):
                if i in [0,1]:
                    draw.color('black', 'orange')
                else:
                    draw.color('black', 'yellow')
                x,y = self.normalize(pos,None)
                draw.goto(x,y)
                draw.pendown()
                draw.stamp()
                draw.penup()
                self.obstace.append(pos)
            
            ind = ind + 2
            if ind >= len(arr) -1:
                break

    def drawPath(self, moves, draw):
        i,j = self.src_pos
        for move in moves[:-1]: 
            if move == "L":
                i -= 1

            elif move == "R":
                i += 1

            elif move == "U":
                j -= 1

            elif move == "D":
                j += 1

            draw.color('black','olive')

            screen_x,screen_y = self.normalize(i, j) 
            self._draw((screen_x,screen_y),draw) 
        print("Cost of Path is:", len(moves))

    def search(self, draw):
        self.method.create_maze(self.obstace)
        self.method.find(draw)
        self.drawPath(self.method.path, draw)
    
    def iterSearch(self, draw, maxLen):
        self.method.create_maze(self.obstace)
        self.method.iterFind(draw,maxLen)
        self.drawPath(self.method.path, draw)

if __name__ == "__main__":
  
    shape, src_pos, des_pos, obstace = read_input('input.txt')
    maze_width,maze_height = map(int,shape.split(' '))

    screen = Screen()
    screen.setup((maze_width + 4)*TILE_SIZE, (maze_height + 4)*TILE_SIZE)
    screen.title("MAZE")
    
    wall_draw = PenWall()
    bg_draw = PenInWall()
    src_draw = Source()
    dst_draw = Dst()
    pen_poly = PenPoly()

    draw = Draw(shape, (maze_width/2,maze_height/2),src_pos, des_pos, BFS)

    draw.setup_maze(wall_draw, bg_draw)
    draw.setup_position(src_draw, dst_draw)
    for obj in obstace:
        obj_list = list(map(int,obj.split(' ')))
        draw.drawPolygon(obj_list, pen_poly)
    # draw.iterSearch(PenPath(), 40)
    draw.search(PenPath())
    screen.mainloop()

    # print(point_line([4,4],[5,9]))