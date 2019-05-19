from PyQt5.QtWidgets import QWidget, QApplication, QDockWidget, QMainWindow, QPushButton, QLabel, QSpinBox
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

from path_search.implementation import *
from path_search.my_implementation import my_search_generator

import math


GREEN = QColor(Qt.green)
BLUE = QColor(Qt.blue)
CYAN = QColor(Qt.cyan)


class Panel(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window
        window.panel = self

        self.set_start_btn = QPushButton('Начальная точка', self)
        self.set_start_btn.setGeometry(50, 50, 200, 50)
        self.set_start_btn.clicked.connect(self.window.set_start_f)

        self.set_goal_btn = QPushButton('Конечная точка', self)
        self.set_goal_btn.setGeometry(50, 150, 200, 50)
        self.set_goal_btn.clicked.connect(self.window.set_goal_f)

        self.set_blocks_btn = QPushButton('Препятствия', self)
        self.set_blocks_btn.setGeometry(50, 250, 200, 50)
        self.set_blocks_btn.clicked.connect(self.window.set_blocks_f)

        self.remove_blocks_btn = QPushButton('Убрать препятствия', self)
        self.remove_blocks_btn.setGeometry(50, 350, 200, 50)
        self.remove_blocks_btn.clicked.connect(self.window.remove_blocks_f)

        self.start_btn = QPushButton('Пуск', self)
        self.start_btn.setGeometry(50, 500, 200, 50)
        self.start_btn.clicked.connect(self.window.start_f)

        self.timer_lbl = QLabel('Скорость анимации', self)
        self.timer_lbl.setGeometry(50, 610, 200, 20)

        self.timer_spin = QSpinBox(self)
        self.timer_spin.setRange(30, 300)
        self.timer_spin.setValue(100)
        self.timer_spin.setSingleStep(10)
        self.timer_spin.setSuffix('%')
        self.timer_spin.setGeometry(190, 600, 60, 50)

        self.restart_btn = QPushButton('Вернуться', self)
        self.restart_btn.setGeometry(50, 700, 200, 50)
        self.restart_btn.clicked.connect(self.window.restart_f)

        self.clean_btn = QPushButton('Очистить', self)
        self.clean_btn.setGeometry(50, 800, 200, 50)
        self.clean_btn.clicked.connect(self.window.clean_f)


class MainWindow(QMainWindow):
    def __init__(self, algorith):
        super().__init__()

        self.window = Window(self, algorith)
        self.setCentralWidget(self.window)

        self.dock = QDockWidget()
        self.dock.setWidget(Panel(self.window))
        self.dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock.setFixedWidth(300)

        self.setFixedSize(1201, 901)
        self.move(400, 100)


class Window(QWidget):
    def __init__(self, parent, algorith):
        super().__init__(parent)

        self.grid = Grid(width=30, height=30)
        self.start = (4, 4)
        self.goal = (25, 25)
        self.visited = set()
        self.save_visited = set()
        self.current = None
        self.save_current = None
        self.gen = None
        self.delay = 300
        self.going = False
        self.timer = None
        self.mode = None
        self.pressed = False
        self.panel = None

        self.cellsize = min(900 // self.grid.width,
                            900 // self.grid.height)
        self.cellsize3 = self.cellsize // 3
        self.cellsize4 = self.cellsize // 4
        self.setFixedSize(self.cellsize * self.grid.width + 1,
                          self.cellsize * self.grid.height + 1)
        self.cellsize6 = self.cellsize // 6
        self.cellsize23 = self.cellsize3 * 2
        self.cellsize34 = self.cellsize4 * 3
        self.qp = QPainter()

    def paint_cell(self, i, j):
        self.qp.drawRect(i * self.cellsize, j * self.cellsize,
                         self.cellsize, self.cellsize)

    def paint_grid(self):
        self.qp.setPen(Qt.black)
        for i in range(self.grid.height + 1):
            self.qp.drawLine(
                0,
                i * self.cellsize,
                self.width(),
                i * self.cellsize)
        for i in range(self.grid.width + 1):
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
        if self.start:
            self.paint_cell(*self.start)
        self.qp.setBrush(Qt.red)
        if self.goal:
            self.paint_cell(*self.goal)
        self.qp.setBrush(Qt.blue)
        if self.current:
            self.paint_cell(*self.current)

    def paintEvent(self, event):
        self.qp.begin(self)
        self.paint_grid()
        self.qp.end()

    def timerEvent(self, event):
        try:
            self.current, self.visited = next(self.gen)
        except StopIteration:
            self.killTimer(self.timer)
            self.timer = None
        self.repaint()

    def mousePressEvent(self, event):
        if self.going:
            return
        i, j = self.pressed_cell(event)
        if self.mode == 'set_start':
            self.start = i, j
        if self.mode == 'set_goal':
            self.goal = i, j
        if self.mode == 'set_blocks' or self.mode == 'remove_blocks':
            self.pressed = True
        self.repaint()

    def mouseReleaseEvent(self, event):
        self.pressed = False

    def mouseMoveEvent(self, event):
        if self.pressed:
            i, j = self.pressed_cell(event)
            if self.mode == 'set_blocks':
                self.grid[i, j] = math.inf
            if self.mode == 'remove_blocks':
                self.grid[i, j] = 1
            self.repaint()

    def pressed_cell(self, event):
        pos = event.pos()
        return pos.x() // self.cellsize, pos.y() // self.cellsize

    def set_start_f(self):
        self.mode = 'set_start'

    def set_goal_f(self):
        self.mode = 'set_goal'

    def set_blocks_f(self):
        self.mode = 'set_blocks'

    def remove_blocks_f(self):
        self.mode = 'remove_blocks'

    def start_f(self):
        if not self.going and self.start and self.goal:
            self.going = True
            self.save_current = self.current
            self.save_visited = self.visited
            self.gen = my_search_generator(self.grid, self.start, self.goal)
            self.timer = self.startTimer(300 * 100 / self.panel.timer_spin.value())

    def restart_f(self):
        if self.going:
            if self.timer:
                self.killTimer(self.timer)
            self.going = False
            self.current = self.save_current
            self.visited = self.save_visited
            self.repaint()

    def clean_f(self):
        if self.timer:
            self.killTimer(self.timer)
        self.going = False
        self.grid = Grid(width=30, height=30)
        self.current = None
        self.visited = set()
        self.start = None
        self.goal = None
        self.repaint()
