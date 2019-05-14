from path_search_examples.test_graphics import *


if __name__ == '__main__':
    grid = Grid.from_filename('/home/sanyash/myrepos/Diplom/matrix4.txt')
    start = (2, 9)
    goal = (9, 2)
    qapp = QApplication([])
    w = Window(dijkstra_search_generator, grid, start, goal)
    w.show()
    qapp.exec_()
