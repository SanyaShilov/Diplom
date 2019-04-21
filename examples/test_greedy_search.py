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


graph = GridWithWeights(15, 15)
graph.walls = [(i, 5) for i in range(3, 12)] + [(11, j) for j in range(6, 12)]
start = (0, 13)
goal = (14, 2)

came_from = breadth_first_search_3(graph, start, goal)
draw_grid(graph, width=3, point_to=came_from, start=start, goal=goal)
print()
draw_grid(graph, width=3, path=reconstruct_path(came_from, start=start, goal=goal))
print()

came_from = greedy_search(graph, start, goal)
draw_grid(graph, width=3, point_to=came_from, start=start, goal=goal)
print()
draw_grid(graph, width=3, path=reconstruct_path(came_from, start=start, goal=goal))
print()

came_from, cost_so_far = dijkstra_search(graph, start, goal)
draw_grid(graph, width=3, point_to=came_from, start=start, goal=goal)
print()
draw_grid(graph, width=3, path=reconstruct_path(came_from, start=start, goal=goal))
print()

came_from, cost_so_far = a_star_search(graph, start, goal)
draw_grid(graph, width=3, point_to=came_from, start=start, goal=goal)
print()
draw_grid(graph, width=3, path=reconstruct_path(came_from, start=start, goal=goal))
print()
