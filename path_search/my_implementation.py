from path_search.implementation import *


def next_in_new_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    return path[-1]


def find_new_path(graph, start, visited):
    frontier = Queue()
    frontier.put(start)
    came_from = {start: None}

    while not frontier.empty():
        current = frontier.get()

        if current not in visited:
            return next_in_new_path(came_from, start, current)

        for next in graph.all_neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current


def my_search_generator(graph, start, goal):
    current = start
    visited = {start}

    while True:
        yield (
            current,
            visited
        )

        if current == goal:
            break

        visited.add(current)

        points = []
        for next_point in graph.all_neighbors(current):
            if next_point == goal:
                current = next_point
                break
            if next_point not in visited:
                points.append(next_point)
        else:
            if points:
                points.sort(key=lambda point: graph.cost(current, point) + heuristic(goal, point))
                current = points[0]
            else:
                current = find_new_path(graph, current, visited)
                while current in visited:
                    yield (
                        current,
                        visited
                    )
                    current = find_new_path(graph, current, visited)
