from path_search_examples.test_my_graphics import *
from path_search.my_implementation import *


if __name__ == '__main__':
    qapp = QApplication([])
    w = MainWindow(my_search_generator)
    w.show()
    qapp.exec_()
