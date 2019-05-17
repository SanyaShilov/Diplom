from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

from path_search.implementation import *


GREEN = QColor(Qt.green)
BLUE = QColor(Qt.blue)
CYAN = QColor(Qt.cyan)


class Window(QWidget):
    def __init__(self, algorith, grid, start, goal, delay=100):
        super().__init__()

        self.grid = grid
        self.start = start
        self.goal = goal
        self.gen = algorith(grid, start, goal)
        self.visited = set()
        self.current = start

        self.cellsize = min(800 // self.grid.width,
                            800 // self.grid.height)
        self.cellsize3 = self.cellsize // 3
        self.cellsize4 = self.cellsize // 4
        self.setFixedSize(self.cellsize * self.grid.width,
                          self.cellsize * self.grid.height)
        self.cellsize6 = self.cellsize // 6
        self.cellsize23 = self.cellsize3 * 2
        self.cellsize34 = self.cellsize4 * 3
        self.qp = QPainter()
        self.timer = self.startTimer(delay)

    def paint_cell(self, i, j):
        self.qp.drawRect(i * self.cellsize, j * self.cellsize,
                         self.cellsize, self.cellsize)

    def paint_grid(self):
        self.qp.setPen(Qt.black)
        for i in range(self.grid.height):
            self.qp.drawLine(
                0,
                i * self.cellsize,
                self.width(),
                i * self.cellsize)
        for i in range(self.grid.width):
            self.qp.drawLine(
                i * self.cellsize,
                0,
                i * self.cellsize,
                self.height())
        self.qp.setBrush(Qt.black)
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid[x, y] is math.inf:
                    self.paint_cell(x, y)

        for x, y in self.visited:
            cost = self.grid.cost(None, (x, y))
            self.qp.setBrush(GREEN.darker(100 + (cost - 1) * 20))
            self.paint_cell(x, y)
        self.qp.setBrush(Qt.yellow)
        self.paint_cell(*self.start)
        self.qp.setBrush(Qt.red)
        self.paint_cell(*self.goal)
        self.qp.setBrush(Qt.blue)
        self.paint_cell(*self.current)

    def paintEvent(self, event):
        self.qp.begin(self)
        self.paint_grid()
        self.qp.end()

    def timerEvent(self, event):
        try:
            self.current, self.visited = next(self.gen)
            self.repaint()
        except StopIteration:
            self.repaint()
            self.killTimer(self.timer)
