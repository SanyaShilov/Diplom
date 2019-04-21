import collections
import queue


class SimpleGraph:
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, point):
        return self.edges[point]


example_graph = SimpleGraph()
example_graph.edges = {
    'A': ['B'],
    'B': ['A', 'C', 'D'],
    'C': ['A'],
    'D': ['E', 'A'],
    'E': ['B']
}


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


# utility functions for dealing with square grids
def from_point_width(point, width):
    return point % width, point // width


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
    if point in graph.walls:
        r = "#"
    return r


def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style), end="")
        print()


# data from main article
DIAGRAM1_WALLS = [
    from_point_width(point, width=30) for point in [
        21, 22, 51, 52, 81, 82, 93, 94, 111, 112, 123, 124, 133, 134, 141,
        142, 153, 154, 163, 164, 171, 172, 173, 174, 175, 183, 184, 193,
        194, 201, 202, 203, 204, 205, 213, 214, 223, 224, 243, 244, 253,
        254, 273, 274, 283, 284, 303, 304, 313, 314, 333, 334, 343, 344,
        373, 374, 403, 404, 433, 434]
]


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
    
    def in_bounds(self, point):
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, point):
        return point not in self.walls
    
    def neighbors(self, point):
        (x, y) = point
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0:
            results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}
    
    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


diagram4 = GridWithWeights(10, 10)
diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
diagram4.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6), 
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6), 
                                       (5, 7), (5, 8), (6, 2), (6, 3), 
                                       (6, 4), (6, 5), (6, 6), (6, 7), 
                                       (7, 3), (7, 4), (7, 5)]}


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
