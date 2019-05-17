from path_search_examples.test_my_graphics import *
from path_search.my_implementation import *


if __name__ == '__main__':
    grid = Grid.from_filename('/home/sanyash/myrepos/Diplom/matrix6.txt')
    start = (0, 3)
    goal = (11, 3)
    qapp = QApplication([])
    w = Window(my_search_generator, grid, start, goal,delay=300)
    w.show()
    qapp.exec_()
