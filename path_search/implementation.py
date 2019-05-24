import collections
import math

from fuzzy_logic import *


r_distance = Range(0, 40)

dis_small = gaussian(0, 0.3)
dis_below_middle = gaussian(1, 0.3)
dis_middle = gaussian(2, 0.3)
dis_above_middle = gaussian(3, 0.3)
dis_big = f_or(gaussian(4, 0.3), lambda x: 1 if x >= 4 else 0)


r_degree = Range(0, 180)

deg_small = gaussian(0, 3)
deg_below_middle = gaussian(15, 5)
deg_middle = gaussian(30, 5)
deg_above_middle = gaussian(45, 5)
deg_big = f_or(gaussian(60, 5), lambda x: 1 if x >= 60 else 0)


r_heuristic = Range(0, 1)

heur_small = gaussian(0, 0.1)
heur_below_middle = gaussian(0.25, 0.1)
heur_middle = gaussian(0.5, 0.1)
heur_above_middle = gaussian(0.75, 0.1)
heur_big = gaussian(1, 0.1)


base = FuzzyBase.from_parameters(
    conditions_ranges=[r_distance, r_degree],
    conclusion_range=r_heuristic,
    rules_parameters=[
        {
            'conditions': [dis_big, None],
            'conclusion': heur_small
        },
        {
            'conditions': [None, deg_big],
            'conclusion': heur_small
        },
        {
            'conditions': [dis_above_middle, deg_small],
            'conclusion': heur_below_middle
        },
        {
            'conditions': [dis_above_middle, deg_below_middle],
            'conclusion': heur_small
        },
        {
            'conditions': [dis_middle, deg_small],
            'conclusion': heur_middle
        },
        {
            'conditions': [dis_middle, deg_below_middle],
            'conclusion': heur_below_middle
        },
        {
            'conditions': [dis_middle, deg_middle],
            'conclusion': heur_small
        },
        {
            'conditions': [dis_below_middle, deg_small],
            'conclusion': heur_above_middle
        },
        {
            'conditions': [dis_below_middle, deg_below_middle],
            'conclusion': heur_middle
        },
        {
            'conditions': [dis_below_middle, deg_middle],
            'conclusion': heur_below_middle
        },
        {
            'conditions': [dis_below_middle, deg_above_middle],
            'conclusion': heur_small
        },
        {
            'conditions': [dis_small, deg_small],
            'conclusion': heur_big
        },
        {
            'conditions': [dis_small, deg_below_middle],
            'conclusion': heur_above_middle
        },
        {
            'conditions': [dis_small, deg_middle],
            'conclusion': heur_middle
        },
        {
            'conditions': [dis_small, deg_above_middle],
            'conclusion': heur_below_middle
        },
    ],
)


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, element):
        self.elements.append(element)

    def get(self):
        return self.elements.popleft()

    def __iter__(self):
        return iter(self.elements)


def distance(p1, p2):
    return lv(vector(p1, p2))


def vector(p1, p2):
    return p2[0] - p1[0], p2[1] - p1[1]


def lv(v):
    return (v[0] ** 2 + v[1] ** 2) ** 0.5


def scalar_p(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


def p_plus_v(p, v):
    return p[0] + v[0], p[1] + v[1]


def degree_v(v1, v2):
    lv1 = lv(v1)
    lv2 = lv(v2)
    if lv1 and lv2:
        return math.acos(scalar_p(v1, v2) / lv(v1) / lv(v2)) * 180 / math.pi
    return 0


def degree_p(p1, p2, p3):
    return degree_v(vector(p1, p2), vector(p1, p3))


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
            self.matrix = [[1 for _ in range(width)] for _ in range(height)]
            self.divide_into_obstructions()

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

    def not_passable(self, point):
        return not self.passable(point)

    def neighbors(self, point):
        x, y = point
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0:
            results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def neighbor_blocks(self, point):
        x, y = point
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0:
            results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.not_passable, results)
        return results

    def all_neighbors(self, point):
        x, y = point
        results = [
            (x + dx, y + dy)
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if dx or dy
        ]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node, to_node):
        x1, y1 = from_node
        x2, y2 = to_node
        return (self.matrix[y1][x1] + self.matrix[y2][x2]) / 2 * distance(from_node, to_node)

    def fuzzy_heuristic(self, from_node, to_node):
        fh = 0
        for obstruction in self.obstructions:
            block, sign = obstruction.get_block(from_node, to_node)
            dis = r_distance.closest(distance(from_node, block))
            deg = r_degree.closest(degree_p(from_node, to_node, block))
            fh += base.evaluate([
                FuzzySet(r_distance, singleton(dis)),
                FuzzySet(r_degree, singleton(deg))
            ]) * sign
        return fh * 2

    def get_obstruction(self, point):
        blocks_for_obstruction = []
        front_blocks = [point]
        while front_blocks:
            block = front_blocks.pop()
            blocks_for_obstruction.append(block)
            for x, y in self.neighbor_blocks(block):
                if (x, y) not in blocks_for_obstruction:
                    front_blocks.append((x, y))
        return blocks_for_obstruction

    def divide_into_obstructions(self):
        blocks = []
        obstructions = []
        for j in range(self.height):
            for i in range(self.width):
                if self[i, j] == math.inf:
                    if (i, j) not in blocks:
                        blocks_for_obstruction = self.get_obstruction((i, j))
                        blocks.extend(blocks_for_obstruction)
                        obstructions.append(Obstruction(blocks_for_obstruction))
        self.obstructions = obstructions
        return obstructions

    def __repr__(self):
        return '\n'.join(
            ' '.join(
                str(elem) if elem != math.inf else Grid.BLOCK for elem in line
            )
            for line in self.matrix
        )

    def __getitem__(self, item):
        return self.matrix[item[1]][item[0]]

    def __setitem__(self, item, value):
        self.matrix[item[1]][item[0]] = value


class Obstruction:
    def __init__(self, blocks):
        self.blocks = blocks
        self.all_blocks = [
            (i, j)
            for i in range(
                min(blocks, key=lambda block: block[0])[0],
                max(blocks, key=lambda block: block[0])[0] + 1,
            )
            for j in range(
                min(blocks, key=lambda block: block[1])[1],
                max(blocks, key=lambda block: block[1])[1] + 1,
            )
        ]
        self.left = min(blocks, key=lambda block: block[0])[0]
        self.right = max(blocks, key=lambda block: block[0])[0]
        self.top = min(blocks, key=lambda block: block[1])[1]
        self.bottom = max(blocks, key=lambda block: block[1])[1]
        self.left_blocks = [(self.left, j) for j in range(self.top, self.bottom + 1)]
        self.right_blocks = [(self.right, j) for j in range(self.top, self.bottom + 1)]
        self.top_blocks = [(i, self.top) for i in range(self.left, self.right + 1)]
        self.bottom_blocks = [(i, self.bottom) for i in range(self.left, self.right + 1)]

    def get_block(self, from_node, to_node):
        sign = 1
        if from_node[0] < self.left:
            if from_node[1] < self.top:
                blocks = self.left_blocks + self.top_blocks
            elif from_node[1] > self.bottom:
                blocks = self.left_blocks + self.bottom_blocks
            else:
                blocks = self.left_blocks
        elif from_node[0] > self.right:
            if from_node[1] < self.top:
                blocks = self.right_blocks + self.top_blocks
            elif from_node[1] > self.bottom:
                blocks = self.right_blocks + self.bottom_blocks
            else:
                blocks = self.right_blocks
        else:
            if from_node[1] < self.top:
                blocks = self.top_blocks
            elif from_node[1] > self.bottom:
                blocks = self.bottom_blocks
            else:
                blocks = self.left_blocks + self.right_blocks + self.top_blocks + self.bottom_blocks
                sign = -1
        block = min(blocks, key=lambda block: (degree_p(from_node, to_node, block), distance(from_node, block)))
        return block, sign


GROUPS = {
    (1, 1): [[(1, 1), (1, 0), (0, 1), (1, -1), (-1, 1)], [(0, -1), (-1, 0)]],
    (1, -1): [[(1, -1), (1, 0), (0, -1), (1, 1), (-1, -1)], [(0, 1), (-1, 0)]],
    (-1, 1): [[(-1, 1), (-1, 0), (0, 1), (1, 1), (-1, -1)], [(1, 0), (0, -1)]],
    (-1, -1): [[(-1, -1), (-1, 0), (0, -1), (1, -1), (-1, 1)], [(1, 0), (0, 1)]],

    (1, 0): [[(1, 0), (1, 1), (1, -1)], [(0, 1), (0, -1), (-1, 1), (-1, -1)]],
    (0, 1): [[(0, 1), (1, 1), (-1, 1)], [(1, 0), (-1, 0), (-1, -1), (1, -1)]],
    (-1, 0): [[(-1, 0), (-1, 1), (-1, -1)], [(0, 1), (0, -1), (1, 1), (1, -1)]],
    (0, -1): [[(0, -1), (1, -1), (-1, -1)], [(1, 0), (-1, 0), (-1, 1), (1, 1)]],

    None: [[(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]],
}


def divide_into_groups(points, prev, current):
    v = vector(prev, current) if prev else None
    for group in GROUPS[v]:
        gps = [p_plus_v(current, gv) for gv in group]
        yield [p for p in gps if p in points]


def next_in_new_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    return path[-1]


def find_new_path(graph, start, visited):
    frontier = Queue()
    frontier.put(start)
    came_from = {start: None}

    while not frontier.empty():
        current = frontier.get()

        if current not in visited:
            return next_in_new_path(came_from, start, current)

        for next in graph.all_neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current


def my_search_generator(graph, start, goal):
    prev, current = None, start
    visited = {start}

    while True:
        yield (
            current,
            visited
        )

        if current == goal:
            break

        visited.add(current)

        points = []
        for next_point in graph.all_neighbors(current):
            if next_point == goal:
                prev, current = current, next_point
                break
            if next_point not in visited:
                points.append(next_point)
        else:
            if points:
                groups = divide_into_groups(points, prev, current)
                for group in groups:
                    if group:
                        group.sort(
                            key=lambda point:
                            graph.cost(current, point)
                            + distance(goal, point)
                            + graph.fuzzy_heuristic(current, point)
                        )
                        prev, current = current, group[0]
                        break
            else:
                prev, current = current, find_new_path(graph, current, visited)
                while current in visited:
                    yield (
                        current,
                        visited
                    )
                    prev, current = current, find_new_path(graph, current, visited)
