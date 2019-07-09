import sys
import deserializer
from canvas import dist,transform_points,transform_point,get_map_variables,get_size_polygon,red,\
green,blue, white,black
#import dijkstra
import random
import pygame
import math
import numpy as np
from agent import Agent

from pygame.math import Vector2
screen_size = 700
numVel = 16. #Number of sampled velocities

#Load data
v_max,obstacles, starts, goals, b_polygon = deserializer.load_data()
Agent.v_max = v_max
agents= []
clock = pygame.time.Clock()
factor, offset_x, offset_y = get_map_variables(b_polygon)
screen_data = (factor, offset_x, offset_y)


#Candidate velocities
cVels = [Vector2(0,0) for phi in np.linspace(0,2*math.pi,numVel)]
for i in range(len(cVels)):
	cVels[i].from_polar((v_max,360/len(cVels)*i))
#cVels.append(Vector2(0,0))
#print cVel

#Initialize agents
for i in range(len(starts)):
	agents.append(Agent(starts[i][0],starts[i][1],goals[i][0],goals[i][1]))
	agents[i].velocity = (agents[i].goal-agents[i].pos).normalize()*v_max

#colors for the agents
colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(len(agents))]

agents=agents[::]


##Transform to screen coordinates
b_polygon_transformed = transform_points(b_polygon, screen_data)
obstacles_transformed = []
for i in range(0, len(obstacles)):
	obstacles_transformed.append(transform_points(obstacles[i], screen_data))

pygame.init()
screen = pygame.display.set_mode((screen_size, screen_size))

##########Testing Area##############

#agents[0].getVO(agents[1])
#print agents[0].sampleVels(10)

####################################

while(1):

	#fps = 10
	dt = clock.tick_busy_loop(10)/1000.0

	#X button
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	#Clear screen
	screen.fill(white)

	#Draw the obstacles, starting and ending points, and points of interest.
	pygame.draw.polygon(screen, blue, b_polygon_transformed, 3)
	for i in range(0, len(obstacles)):
		pygame.draw.polygon(screen, red, obstacles_transformed[i], 3)


	#Agents
	for i in range(0, len(agents)):

		agents[i].velocity = agents[i].bestVelocity(cVels, agents)

		
		#Draw agent
		pygame.draw.circle(screen, colors[i], transform_point(agents[i].pos, screen_data), int(factor/2), 0)
		pygame.draw.circle(screen, red, transform_point(agents[i].goal, screen_data), int(factor/4), 0)
		
		#pygame.draw.line(screen,blue,transform_point(agents[i].pos, screen_data),\
		#	transform_point(agents[i].getVO(agents[(i+1)%len(agents)])[0]+agents[i].pos, screen_data))
		#pygame.draw.line(screen,red,transform_point(agents[i].pos, screen_data),\
		#	transform_point(agents[i].getVO(agents[(i+1)%len(agents)])[1]+agents[i].pos, screen_data))
		
		#Draw velocity
		#pygame.draw.line(screen,red,transform_point(agents[i].pos, screen_data),\
		#	transform_point(agents[i].pos+agents[i].velocity, screen_data))

		#print agents[i].tc(agents[i].velocity,agents[(i+1)%len(agents)])
		if agents[i].pos.distance_to(agents[i].goal)>v_max*dt:
			agents[i].pos += agents[i].velocity*dt
			agents[i].pointList.append([agents[i].pos[0],agents[i].pos[1]])
			#print agents[i].pointList

		#Draw path
		#print agents[i].pointList[0]
		pygame.draw.lines(screen, colors[i], False, transform_points(list(agents[i].pointList),screen_data), 1)		
	#print dist(*agents[0].getVO(agents[1]))

	pygame.display.update()



