from path_search.geometry import *


class Obstruction:
    def __init__(self, blocks, dx=0, dy=0):
        self.blocks = blocks
        self.start_blocks = blocks
        self.dx = dx
        self.dy = dy
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

    def move(self):
        self.blocks = [(block[0] + self.dx, block[1] + self.dy) for block in self.blocks]
