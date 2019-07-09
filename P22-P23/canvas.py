# Map rendering
import sys
import pygame
import random
import math
import dijkstra

screen_size = 700

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

colors = []

# Transforms a list of points into an adapted list of points for the canvas
def transform_points(points, factor, offset_x, offset_y):
	for i in range(0, len(points)):
		points[i] = [(points[i][0] + offset_x)*factor, (points[i][1]*-1 + offset_y)*factor]
	return points

# Transforms a single point into an adapted single point for the canvas
def transform_point(point, factor, offset_x, offset_y):
	point = [int((point[0] + offset_x)*factor), int((point[1]*-1 + offset_y)*factor)]
	return point

# Returns the most right, left, up and down point of a polygon
def get_size_polygon(points):
	min_x = float("inf")
	min_y = float("inf")
	max_x = -float("inf")
	max_y = -float("inf")
	for i in range(0, len(points)):
		x = points[i][0]
		y = points[i][1]
		if (x < min_x): min_x = x
		if (x > max_x): max_x = x
		if (y < min_y): min_y = y
		if (y > max_y): max_y = y

	return max_x, min_x, max_y, min_y

# Sets the scaling factor: 1 unit in the json file will become the pygame screen size divided by 
# the max(horizontal, vertical) length of the bounding polygon units
def get_map_variables(b_polygon):
	max_x, min_x, max_y, min_y = get_size_polygon(b_polygon)
	if (min_x < 0 or min_y < 0):
		offset_x = -min_x + 5
		offset_y = max_y + 5
	factor = screen_size / max(max_x - min_x + 10, max_y - min_y + 10)
	return factor, offset_x, offset_y

def dist(p1, p2):
	return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))

def center_segment(p1, p2):
	return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]

def draw_path(coord, path, screen, factor, offset_x, offset_y, n_points, goals, graph, subpaths):
	last_pos = path[0]
	current_agent = path[0]
	for i in range(1, len(path)):
		color = colors[current_agent - n_points]
		if (path[i] < n_points):
			draw_dijkstra(coord, graph, last_pos, path[i], color, screen, factor, offset_x, offset_y, subpaths)
		else:
			goal = len(coord) - len(goals) + current_agent - n_points
			draw_dijkstra(coord, graph, last_pos, goal, color, screen, factor, offset_x, offset_y, subpaths)
			current_agent = path[i]
		last_pos = path[i]
	goal = len(coord) - len(goals) + current_agent - n_points
	draw_dijkstra(coord, graph, last_pos, goal, color, screen, factor, offset_x, offset_y, subpaths)

def draw_dijkstra(coord, graph, start, goal, color, screen, factor, offset_x, offset_y, subpaths):
	path = subpaths[start][goal]
	start = coord[start]
	for j in range(0, len(path)):
		pygame.draw.line(screen, color, transform_point(start, factor, offset_x, offset_y), transform_point(coord[path[j]], factor, offset_x, offset_y), 1)
		start = coord[path[j]]	

# Draws the full map
def draw_map(b_polygon, obstacles, starts, goals, points, coord, path, n_points, graph, subpaths):
	pygame.init()
	screen = pygame.display.set_mode((screen_size, screen_size))
	screen.fill(white)
	factor, offset_x, offset_y = get_map_variables(b_polygon)

	# Draw the obstacles, starting and ending points, and points of interest.
	pygame.draw.polygon(screen, blue, transform_points(b_polygon, factor, offset_x, offset_y), 3)
	for i in range(0, len(obstacles)):
		pygame.draw.polygon(screen, red, transform_points(obstacles[i], factor, offset_x, offset_y), 3)
	for i in range(0, len(starts)):
		color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		pygame.draw.circle(screen, color, transform_point(starts[i], factor, offset_x, offset_y), int(factor/2), 0)
		pygame.draw.circle(screen, color, transform_point(goals[i], factor, offset_x, offset_y), int(factor/2), 0)
		colors.append(color)
	for i in range(0, len(points)):
		pygame.draw.circle(screen, black, transform_point(points[i], factor, offset_x, offset_y), int(factor/4), 1)

	draw_path(coord, path, screen, factor, offset_x, offset_y, n_points, goals, graph, subpaths)

	pygame.display.update()

	while(1):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()


