from path_search_examples.test_graphics import *


if __name__ == '__main__':
    grid = Grid.from_filename('/home/sanyash/myrepos/Diplom/matrix2.txt')
    start = (1, 4)
    goal = (7, 8)
    qapp = QApplication([])
    w = Window(a_star_search_generator, grid, start, goal)
    w.show()
    qapp.exec_()
