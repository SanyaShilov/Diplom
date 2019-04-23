from path_search.implementation import *


def breadth_first_search_3(graph, start, goal):
    frontier = Queue()
    frontier.put(start)
    came_from = {start: None}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return came_from


graph = Grid.from_filename('/home/sanyash/myrepos/Diplom/matrix4.txt')
start = (0, 14)
goal = (19, 0)

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
