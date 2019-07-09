# Map rendering
import sys
import pygame
import random
import math


screen_size = 700

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

#Screen functions
#########################################
def dist(p1, p2):
	return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))

# Transforms a list of points into an adapted list of points for the canvas
def transform_points(points, screen_data):
	factor, offset_x, offset_y = screen_data[0],screen_data[1],screen_data[2]
	for i in range(0, len(points)):
		points[i] = [(points[i][0] + offset_x)*factor, (points[i][1]*-1 + offset_y)*factor]
	return points

# Transforms a single point into an adapted single point for the canvas
def transform_point(point, screen_data):
	factor, offset_x, offset_y = screen_data[0],screen_data[1],screen_data[2]
	point = [int((point[0] + offset_x)*factor), int((point[1]*-1 + offset_y)*factor)]
	return point

# Sets the scaling factor: 1 unit in the json file will become the pygame screen size divided by 
# the max(horizontal, vertical) length of the bounding polygon units
def get_map_variables(b_polygon):
	max_x, min_x, max_y, min_y = get_size_polygon(b_polygon)
	if (min_x < 0 or min_y < 0):
		offset_x = -min_x + 5
		offset_y = max_y + 5
	factor = screen_size / max(max_x - min_x + 10, max_y - min_y + 10)
	return factor, offset_x, offset_y

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