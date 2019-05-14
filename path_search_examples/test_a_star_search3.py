from path_search_examples.test_graphics import *


if __name__ == '__main__':
    grid = Grid.from_filename('/home/sanyash/myrepos/Diplom/matrix5.txt')
    start = (2, 9)
    goal = (13, 2)
    qapp = QApplication([])
    w = Window(a_star_search_generator, grid, start, goal)
    w.show()
    qapp.exec_()
