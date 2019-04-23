import collections
import queue
import math


class Queue:
    """Обертка над collections.deque для поддержания единого интерфейса с PriorityQueue"""
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()


class PriorityQueue:
    def __init__(self):
        self.elements = queue.PriorityQueue()

    def empty(self):
        return self.elements.empty()

    def put(self, item, priority):
        return self.elements.put((priority, item))

    def get(self):
        """Нас не интересует приоритет элемента после извлечения из очереди"""
        return self.elements.get()[1]


def draw_tile(graph, point, style):
    r = "."
    if 'number' in style and point in style['number']:
        r = "%d" % style['number'][point]
    if 'point_to' in style and style['point_to'].get(point, None) is not None:
        (x1, y1) = point
        (x2, y2) = style['point_to'][point]
        if x2 == x1 + 1:
            r = "<"
        if x2 == x1 - 1:
            r = ">"
        if y2 == y1 + 1:
            r = "^"
        if y2 == y1 - 1:
            r = "v"
    if 'start' in style and point == style['start']:
        r = "A"
    if 'goal' in style and point == style['goal']:
        r = "Z"
    if 'path' in style and point in style['path']:
        r = "@"
    if graph[point] == math.inf:
        r = "#"
    return r


def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style), end="")
        print()


class Grid:
    EMPTY = '.'
    BLOCK = '#'

    def __init__(self, width=None, height=None, matrix=None):
        if matrix:
            self.width = len(matrix[0])
            self.height = len(matrix)
            self.matrix = [
                [
                    1 if symbol == Grid.EMPTY else math.inf if symbol == Grid.BLOCK else int(symbol)
                    for symbol in line
                ]
                for line in matrix
            ]
        else:
            if not width or not height:
                raise RuntimeError('Can\'t construct grid')
            self.width = width
            self.height = height
            self.matrix = [1 * width for _ in range(height)]

    @classmethod
    def from_filename(cls, filename):
        with open(filename) as f:
            matrix = [line.split() for line in f.readlines()]
            return cls(matrix=matrix)

    def in_bounds(self, point):
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, point):
        x, y = point
        return self.matrix[y][x] != math.inf

    def neighbors(self, point):
        x, y = point
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0:
            results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node, to_node):
        x, y = to_node
        return self.matrix[y][x]

    def __repr__(self):
        return '\n'.join(
            ' '.join(
                str(elem) if elem != math.inf else Grid.BLOCK for elem in line
            )
            for line in self.matrix
        )

    def __getitem__(self, item):
        return self.matrix[item[1]][item[0]]


def greedy_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_point in graph.neighbors(current):
            if next_point not in came_from:
                priority = heuristic2(goal, next_point)
                frontier.put(next_point, priority)
                came_from[next_point] = current

    return came_from


def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next_point in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_point)
            if next_point not in cost_so_far or new_cost < cost_so_far[next_point]:
                cost_so_far[next_point] = new_cost
                priority = new_cost
                frontier.put(next_point, priority)
                came_from[next_point] = current
    
    return came_from, cost_so_far


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def heuristic2(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next_point in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_point)
            if next_point not in cost_so_far or new_cost < cost_so_far[next_point]:
                cost_so_far[next_point] = new_cost
                priority = new_cost + heuristic2(goal, next_point)
                frontier.put(next_point, priority)
                came_from[next_point] = current
    
    return came_from, cost_so_far


g = Grid.from_filename('/home/sanyash/myrepos/Diplom/matrix.txt')
g2 = Grid.from_filename('/home/sanyash/myrepos/Diplom/matrix2.txt')
