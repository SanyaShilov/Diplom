from implementation import *


draw_grid(g)
print()


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


came_from = breadth_first_search_2(g, (8, 7))
draw_grid(g, width=2, point_to=came_from, start=(8, 7))
print()


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


parents = breadth_first_search_3(g, (8, 7), (17, 2))
draw_grid(g, width=2, point_to=parents, start=(8, 7), goal=(17, 2))
print()


from implementation import *
came_from, cost_so_far = dijkstra_search(g2, (1, 4), (7, 8))
draw_grid(g2, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
print()
draw_grid(g2, width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))
print()
draw_grid(g2, width=3, path=reconstruct_path(came_from, start=(1, 4), goal=(7, 8)))
print()
