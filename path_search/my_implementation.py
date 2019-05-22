from path_search.implementation import *


GROUPS = {
    (1, 1): [[(1, 1), (1, 0), (0, 1), (1, -1), (-1, 1)], [(0, -1), (-1, 0)]],
    (1, -1): [[(1, -1), (1, 0), (0, -1), (1, 1), (-1, -1)], [(0, 1), (-1, 0)]],
    (-1, 1): [[(-1, 1), (-1, 0), (0, 1), (1, 1), (-1, -1)], [(1, 0), (0, -1)]],
    (-1, -1): [[(-1, -1), (-1, 0), (0, -1), (1, -1), (-1, 1)], [(1, 0), (0, 1)]],

    (1, 0): [[(1, 0), (1, 1), (1, -1)], [(0, 1), (0, -1), (-1, 1), (-1, -1)]],
    (0, 1): [[(0, 1), (1, 1), (-1, 1)], [(1, 0), (-1, 0), (-1, -1), (1, -1)]],
    (-1, 0): [[(-1, 0), (-1, 1), (-1, -1)], [(0, 1), (0, -1), (1, 1), (1, -1)]],
    (0, -1): [[(0, -1), (1, -1), (-1, -1)], [(1, 0), (-1, 0), (-1, 1), (1, 1)]],

    None: [[(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]],
}


def divide_into_groups(points, prev, current):
    v = vector(prev, current) if prev else None
    for group in GROUPS[v]:
        gps = [p_plus_v(current, gv) for gv in group]
        yield [p for p in gps if p in points]


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
    prev, current = None, start
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
                prev, current = current, next_point
                break
            if next_point not in visited:
                points.append(next_point)
        else:
            if points:
                groups = divide_into_groups(points, prev, current)
                for group in groups:
                    if group:
                        group.sort(
                            key=lambda point:
                            graph.cost(current, point)
                            + distance(goal, point)
                            + graph.fuzzy_heuristic(current, point)
                        )
                        prev, current = current, group[0]
                        break
            else:
                prev, current = current, find_new_path(graph, current, visited)
                while current in visited:
                    yield (
                        current,
                        visited
                    )
                    prev, current = current, find_new_path(graph, current, visited)
