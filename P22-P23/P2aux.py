# Functions for P2
import numpy
import dijkstra
import random
import canvas

def getEdges(obstacles):
	edges = []
	for i in range(0, len(obstacles)):
		for j in range(0, len(obstacles[i])):
			try:
				edges.append([obstacles[i][j], obstacles[i][j+1]])
			except:
				edges.append([obstacles[i][0], obstacles[i][j]])
				continue
		if (len(obstacles[i]) > 3): # To avoid going through opposite vertices
			edges.append([obstacles[i][0], obstacles[i][2]])
	return edges

def getCoordinates(points, starts, obstacles, goals):
	coord = [] # [Points, Starts, Obstacles, Goals]
	for i in range(0, len(points)):
		coord.append(points[i])
	for i in range(0, len(starts)):
		coord.append(starts[i])
	for i in range(0, len(obstacles)):
		for j in range(0, len(obstacles[i])):
			coord.append(obstacles[i][j])
	for i in range(0, len(goals)):
		coord.append(goals[i])
	return coord

def create_matrix_subpaths(graph, edges):
	matrix = []
	for i in range(0, len(graph.vertices)):
		matrix.append([])
		for j in range(0, len(graph.vertices)):
			if (i != j):
				matrix[i].append(dijkstra.shortest_path(graph, i, j))
			else:
				matrix[i].append(0)
	return matrix

# Taken from https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def feasible_segment(p1, p2, edges):
	for j in range(0, len(edges)):
		if (intersect(p1, p2, edges[j][0], edges[j][1])):
			return False
	return True

def find_nearest_point(point, point_list):
	min_dist = float("inf")
	nearest_point = 0
	for i in range(0, len(point_list)):
		if (point_list[i] == -1):
			continue
		dist = canvas.dist(point, point_list[i])
		if (dist < min_dist and dist != 0 and feasible_segment(point, point_list[i])):
			min_dist = dist
			nearest_point = i
	return nearest_point

def getClusters(points, edges, s_range):
	clusters = points

	for i in range(0, len(clusters)):
		for j in range(0, len(clusters)):
			try:
				if (canvas.dist(clusters[i], clusters[j]) < s_range and i != j and feasible_segment(clusters[i], clusters[j], edges)):
					del clusters[j]
			except:
				break
	return clusters

# Calculates the time a certain path needs for being completed at max velocity
def calculate_path(path, points, graph, coord, edges, v_max, goals, subpaths):

	total_distance = 0
	time = 0
	worst_time = 0
	current_agent = path[0]

	for i in range(1, len(path)):
		if (path[i] < len(points)): # The current agent goes to another point
			node_path = subpaths[path[i-1]][path[i]]
			for j in range(1, len(node_path)):
				dist = canvas.dist(coord[node_path[j]], coord[node_path[j-1]])
				total_distance += dist
				time += dist / v_max
		else: # Another agent starts its path
			node_path = subpaths[path[i-1]][len(coord) - len(goals) + current_agent - len(points)]
			for j in range(1, len(node_path)):
				dist = canvas.dist(coord[node_path[j]], coord[node_path[j-1]])
				total_distance += dist
				time += dist / v_max
			current_agent = path[i]
			if (time > worst_time):
				worst_time = time
			time = 0
	if (time > worst_time):
		worst_time = time

	return total_distance, worst_time

def create_vgraph(coord, edges):
	graph = dijkstra.Graph()
	for i in range(0, len(coord)):
		graph.add_vertex(i)
		for j in range(0, len(coord)):
			if (i != j):
				if feasible_segment(coord[i], coord[j], edges):
					graph.add_edge(i, j, canvas.dist(coord[i], coord[j]))
	return graph

def greedy_path(points, goals, graph, coord, edges, v_max, subpaths):
	positions = []
	individual_paths = []
	remaining_points = [i for i in range(len(points))]
	current_i = 0
	for i in range(0, len(goals)):
		positions.append(len(points) + i)
		individual_paths.append([len(points) + i])

	while(len(remaining_points) > 0):
		min_dist = float("inf")
		selected_pos = [-1, -1, [-1]] # [Agent, new position, [path]]
		for i in range(0, len(positions)):
			for j in range(0, len(remaining_points)):
				dist, time = calculate_path([positions[i], remaining_points[j]], points, graph, coord, edges, v_max, goals, subpaths)
				if (dist < min_dist):
					min_dist = dist
					selected_pos = [positions[i], j, remaining_points[j]]
					current_i = i
		individual_paths[current_i] += [selected_pos[2]]
		positions[current_i] = remaining_points[selected_pos[1]]
		del remaining_points[selected_pos[1]]
	greedy_path = [item for sublist in individual_paths for item in sublist]
	return greedy_path

def tabu_search(path, points, graph, coord, edges, v_max, goals, subpaths):

	best_dist, best_time = calculate_path(path, points, graph, coord, edges, v_max, goals, subpaths)
	N = 100000
	for i in range(0, N):
		if (i % 10000 == 0):
			print("Iterations: ", i, " / 100000")
		id1 = random.randint(1, len(path) - 1)
		id2 = random.randint(1, len(path) - 1)
		path[id1], path[id2] = path[id2], path[id1]
		dist, time = calculate_path(path, points, graph, coord, edges, v_max, goals, subpaths)
		if (time < best_time):
			best_time = time
		else:
			path[id1], path[id2] = path[id2], path[id1]
	return path