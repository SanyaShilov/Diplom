from path_search.implementation import *


draw_grid(grid1)
print()


parents = breadth_first_search(grid1, (8, 7), (17, 2))
draw_grid(grid1, width=2, point_to=parents, start=(8, 7), goal=(17, 2))
print()


came_from, cost_so_far = dijkstra_search(grid2, (1, 4), (7, 8))
draw_grid(grid2, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
print()
draw_grid(grid2, width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))
print()
draw_grid(grid2, width=3, path=reconstruct_path(came_from, start=(1, 4), goal=(7, 8)))
print()

obstructions = grid1.divide_into_obstructions()
for obs in obstructions:
    print(obs.center)
