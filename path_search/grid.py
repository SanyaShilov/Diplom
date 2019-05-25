import copy
import math

from path_search.fuzzy import *
from path_search.geometry import *
from path_search.obstruction import Obstruction


class Grid:
    BLOCK = math.inf

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[1 for _ in range(width)] for _ in range(height)]
        self.copy_matrix = copy.deepcopy(self.matrix)
        self.obstructions = self.get_obstructions()
        self.movable_obstructions = []

    def in_bounds(self, point):
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, point):
        x, y = point
        return self.matrix[y][x] != Grid.BLOCK

    def not_passable(self, point):
        return not self.passable(point)

    def neighbors(self, point):
        x, y = point
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def neighbor_blocks(self, point):
        x, y = point
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
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
            fh += base.evaluate([dis, deg]) * sign
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

    def move_obstructions(self):
        self.matrix = copy.deepcopy(self.copy_matrix)
        for obstruction in self.movable_obstructions:
            obstruction.move()
            for block in obstruction.blocks:
                if block[0] >= 0 and block[1] >= 0:
                    try:
                        self[block] = Grid.BLOCK
                    except IndexError:
                        pass

    def divide_into_obstructions(self):
        self.obstructions = self.get_obstructions()

    def get_obstructions(self):
        blocks = []
        obstructions = []
        for j in range(self.height):
            for i in range(self.width):
                if self[i, j] == Grid.BLOCK:
                    if (i, j) not in blocks:
                        blocks_for_obstruction = self.get_obstruction((i, j))
                        blocks.extend(blocks_for_obstruction)
                        obstructions.append(Obstruction(blocks_for_obstruction))
        return obstructions

    def restart(self):
        for obstruction in self.movable_obstructions:
            obstruction.blocks = obstruction.start_blocks
        self.matrix = copy.deepcopy(self.copy_matrix)

    def __getitem__(self, item):
        return self.matrix[item[1]][item[0]]

    def __setitem__(self, item, value):
        self.matrix[item[1]][item[0]] = value
