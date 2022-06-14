from collections import deque
import queue
import numpy as np
from math import *
from utils import *

def manhattan(x,y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])

class Search:
    def __init__(self, maze):
        self.maze = maze
        self.path = []
        self.draw_list = deque()

    def create_maze(self):
        self.maze_map = np.zeros((self.height, self.width))
        self.maze_map[self.end[1],self.end[0]] = 2
        for obj in self.maze.obstace:
            self.maze_map[obj[1],obj[0]] = 1
    
    def move(self, move, i,j):
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1    
        
        return i, j

    def valid(self, moves):
        i,j = self.maze.src_pos
        for move in moves:
            i,j = self.move(move,i,j)
            if not(0 < i < self.width -1 and 0 < j < self.height - 1):
                return False
            elif (self.maze_map[j][i] == 1):
                return False
            # self.tmp[j][i] = 1
        return True

    def findEnd(self, moves):
        j,i = self.maze_map.src_pos
        for move in moves:
            i,j = self.move(move,i,j)

        if self.maze_map[j][i] == 2:
            print("Found: " + moves)
            # self.path = moves
            for move in moves:
               i,j = self.move(move,i,j)
               self.path.append((i,j,'olive')) 
            return True

        return False

    def find(self):
        pass


class BFS(Search):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find(self):
        visited = set()
        i,j = self.maze.src_pos
        nums = queue.Queue()
        nums.put(("", i, j))
        add = ""
        
        while not self.findEnd(add):
            add, i, j = nums.get()
            # print(add)
            # self.draw(i,j, draw)
            self.draw_list.append((i,j))
            for move in ["L","R","U","D"]:
                put = add + move
                i_new, j_new = self.move(move, i, j)
                if self.valid(put) and (i_new,j_new) not in visited:
                    visited.add((i_new,j_new))
                    nums.put((put, i_new, j_new))
                    # print(nums.qsize())

class IterDFS(Search):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find(self, draw, maxLen=10000):
        stack = []
        i,j = self.start
        stack.append(("",i,j))
        add = ""
        visited = set()
        while not self.findEnd(add) and len(stack) !=0:
            # print(stack)
            add, i, j = stack.pop()
            self.draw(i,j, draw)
            # if add in visited:
            #     continue
            # visited.add(add)
            for move in ["L","R","U","D"]:
                put = add + move
                i_new, j_new = self.move(move, i, j)
                if self.valid(put) and len(put) < maxLen and (i_new,j_new) not in visited:
                    visited.add((i_new, j_new))
                    stack.append((put, i_new, j_new))
                        # print(nums.qsize())
        return self.findEnd(add)

    def iterFind(self, draw, maxLen):
        depth = 0
        while depth < maxLen:
            res = self.find(draw,depth)
            print(res)
            if res:
                break
            depth += 1
            # print(depth)


# Ho cac thuat toan InformSearch lưu luôn vị trí của các ô đã duyệt vì space complexity 
# của các thuật toán này không lớn như của UnInformSearch -> Ít tốn RAM hơn -> lưu được
class InformSearch(Search):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def findEnd(self, moves, i,j):
        # print(moves)

        if self.maze[j][i] == 2:
            print("Found: " + moves)
            self.path = moves
            return True

        return False
    
class UCS(InformSearch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find(self,draw):
        visited = set()
        self.g_cost = np.ones((self.height, self.width)) * float(inf)
        nums = queue.PriorityQueue()
        i,j = self.start
        self.g_cost[j,i] = 0.0
        nums.put((0.0,"",i,j))
        add = ""
        while not self.findEnd(add, i,j) and not nums.empty():
            g_cost, add, i,j = nums.get()
            self.draw(i,j, draw)
            for move in ["L","R","U","D"]:
                put = add + move
                i_new, j_new = self.move(move, i, j)
                g_cost_new = self.g_cost[j,i] + 1
                if self.valid(put) and (i_new,j_new) not in visited:
                    if g_cost_new < self.g_cost[j_new,i_new]:
                        visited.add((i_new,j_new))
                        self.g_cost[j_new,i_new] = g_cost_new
                        nums.put((g_cost_new, put, i_new,j_new))

class BestFS(InformSearch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def find(self, draw):
        visited = set()
        nums = queue.PriorityQueue()
        i,j = self.start
        nums.put((0.0,"",i,j))
        add = ""
        while not self.findEnd(add, i,j) and not nums.empty():
            cost, add, i,j = nums.get()
            self.draw(i,j, draw)
            for move in ["L","R","U","D"]:
                put = add + move
                i_new, j_new = self.move(move, i, j)
                if self.valid(put) and (i_new,j_new) not in visited:
                    visited.add((i_new,j_new))
                    cost = manhattan((i_new,j_new), self.end)
                    nums.put((cost,put,i_new,j_new))

class AStar(InformSearch):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def find(self,draw):
        visited = set()
        self.f_cost = np.ones((self.height, self.width)) * float(inf)
        self.g_cost = np.ones((self.height, self.width)) * float(inf)
        nums = queue.PriorityQueue()
        i,j = self.start
        self.g_cost[j,i] = 0.0
        self.f_cost[j,i] = manhattan((i,j),self.end)
        nums.put((0.0,self.f_cost[j,i],"",i,j))
        add = ""
        while not self.findEnd(add, i,j) and not nums.empty():
            f_cost, h_cost, add, i,j = nums.get()
            self.draw(i,j, draw)
            for move in ["L","R","U","D"]:
                put = add + move
                i_new, j_new = self.move(move, i, j)
                g_cost_new = self.g_cost[j,i] + 1
                h_cost_new = manhattan((i_new,j_new), self.end)
                f_cost_new = g_cost_new + h_cost_new 
                if self.valid(put) and (i_new,j_new) not in visited:
                    if f_cost_new < self.f_cost[j_new,i_new]:
                        visited.add((i_new,j_new))
                        self.f_cost[j_new,i_new] = f_cost_new
                        self.g_cost[j_new,i_new] = g_cost_new
                        nums.put((f_cost_new,h_cost_new, put, i_new,j_new))