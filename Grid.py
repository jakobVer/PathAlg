import numpy as np
# y value is always first element, x value is always second element -> Matrix Logic

np.random.seed(1) # fixed barriers for exploring how do different algorithms perform on the same task
class Spot():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        # For A* Search
        self.g = float('inf')
        self.f = float('inf')

        self.h = None

        # For Dijkstra's algorithm
        self.dist = float('inf')

        self.isBarrier = False
        self.isStart = False
        self.isFinish = False
        self.edges = self.neighbors()
        self.parent = None
        self.weight = None

    def make_Barrier(self, percentage):
        if percentage == 0:
            pass
        else:
            ran_num = np.random.randint(0,int(100/percentage))
            if ran_num or self.isStart or self.isFinish:
                pass
            else:
                self.isBarrier = True
    def make_Weight(self, max_weight):
        if self.isBarrier:
            pass
        elif self.isStart:
            self.weight = 0
        else:
            ran_num = np.random.randint(1, max_weight + 1)
            self.weight = ran_num

    def neighbors(self):
        edges = []
        if self.x - 1 >= 0:
            edges.append([self.y, self.x - 1])
        if self.x + 1 < self.size:
            edges.append([ self.y, self.x + 1])
        if self.y - 1 >= 0:
            edges.append([self.y - 1, self.x, ])
        if self.y + 1 < self.size:
            edges.append([self.y + 1, self.x, ])
        return edges

    def heuristic(self, finish):
        # Manhattan distance: |x1-x2| + |y1-y2|
        dist = abs(self.x - finish[1]) + abs(self.y - finish[0])
        return dist

class Grid(Spot):
    def __init__(self, size, start, finish, barrier_per, weights=False, max_weight=None):
        self.size = size
        self.start_x = start[1]
        self.start_y = start[0]
        self.finish_x = finish[1]
        self.finish_y = finish[0]
        self.weights = weights
        self.max_weight = max_weight
        self.barrier_per = barrier_per

        self.grid = self.makeGrid()
        self.setStart()
        self.setFinish()
        self.setBarrier()

        if self.weights:
            self.setWeights()

    def makeGrid(self):
        Q = []
        for i in range(self.size):
            q = []
            for j in range(self.size):
                q.append(Spot(j, i, self.size))
            Q.append(q)
        return Q

    def setStart(self):
        self.grid[self.start_y][self.start_x].isStart = True

    def setFinish(self):
        self.grid[self.finish_y][self.finish_x].isFinish = True

    def setBarrier(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j].make_Barrier(self.barrier_per)

    def getSpot(self, vec):
        return self.grid[vec[0]][vec[1]]

    def setWeights(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j].make_Weight(self.max_weight)