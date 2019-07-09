import deserializer
import canvas
import P2aux as aux


# --- PROBLEM 2 --- #
v_max, points, obstacles, starts, goals, b_polygon = deserializer.load_data_P2()
edges = aux.getEdges(obstacles)
coord = aux.getCoordinates(points, starts, obstacles, goals)

graph = aux.create_vgraph(coord, edges)
subpaths = aux.create_matrix_subpaths(graph, edges)
path = aux.greedy_path(points, goals, graph, coord, edges, v_max, subpaths)
best_path = aux.tabu_search(path, points, graph, coord, edges, v_max, goals, subpaths)

canvas.draw_map(b_polygon, obstacles, starts, goals, points, coord, best_path, len(points), graph, subpaths)
"""

# --- PROBLEM 3 --- #
v_max, points, obstacles, starts, goals, b_polygon, s_range = deserializer.load_data_P3()
edges = aux.getEdges(obstacles)
clusters = aux.getClusters(points, edges, s_range)
coord = aux.getCoordinates(clusters, starts, obstacles, goals)

graph = aux.create_vgraph(coord, edges)
subpaths = aux.create_matrix_subpaths(graph, edges)
path = aux.greedy_path(clusters, goals, graph, coord, edges, v_max, subpaths)
best_path = aux.tabu_search(path, clusters, graph, coord, edges, v_max, goals, subpaths)

canvas.draw_map(b_polygon, obstacles, starts, goals, clusters, coord, best_path, len(clusters), graph, subpaths)
"""