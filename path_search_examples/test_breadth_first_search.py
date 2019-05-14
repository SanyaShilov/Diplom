from path_search_examples.test_graphics import *


if __name__ == '__main__':
    grid = Grid.from_filename('/home/sanyash/myrepos/Diplom/matrix1.txt')
    start = (8, 7)
    goal = (17, 2)
    qapp = QApplication([])
    w = Window(breadth_first_search_generator, grid, start, goal, delay=25)
    w.show()
    qapp.exec_()
