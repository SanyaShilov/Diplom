from pprint import pprint
from implementation import *


def breadth_first_search_1(graph, start):
    # печать того, что мы нашли
    frontier = Queue()
    frontier.put(start)
    visited = {start: True}

    while not frontier.empty():
        current = frontier.get()
        print("Visiting %r" % current)
        for next in graph.neighbors(current):
            if next not in visited:
                frontier.put(next)
                visited[next] = True


breadth_first_search_1(example_graph, 'A')
print()


from implementation import *
g = SquareGrid(30, 15)
g.walls = DIAGRAM1_WALLS # список long, [(21, 0), (21, 2), ...]
draw_grid(g)
print()

from implementation import *


def breadth_first_search_2(graph, start):
    # возвращает "came_from"
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        current = frontier.get()
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return came_from


g = SquareGrid(30, 15)
g.walls = DIAGRAM1_WALLS

came_from = breadth_first_search_2(g, (8, 7))
draw_grid(g, width=2, point_to=came_from, start=(8, 7))
print()

from implementation import *


def breadth_first_search_3(graph, start, goal):
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return came_from


g = SquareGrid(30, 15)
g.walls = DIAGRAM1_WALLS

parents = breadth_first_search_3(g, (8, 7), (17, 2))
draw_grid(g, width=2, point_to=parents, start=(8, 7), goal=(17, 2))
print()


from implementation import *
came_from, cost_so_far = dijkstra_search(diagram4, (1, 4), (7, 8))
draw_grid(diagram4, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
print()
draw_grid(diagram4, width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))
print()
draw_grid(diagram4, width=3, path=reconstruct_path(came_from, start=(1, 4), goal=(7, 8)))
print()
