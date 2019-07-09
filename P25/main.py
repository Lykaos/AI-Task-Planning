import sys
import deserializer
from canvas import dist,transform_points,transform_point,get_map_variables,get_size_polygon,red,\
green,blue, white,black
#import dijkstra
import random
import pygame
import math
import numpy as np
from agent import Agent, Virtual_Structure

from pygame.math import Vector2
screen_size = 700
numVel = 16. #Number of sampled velocities

#Load data
v_max, a_max,starts, form_pos, b_polygon = deserializer.load_data()
t,theta,x,y = deserializer.load_traj()
obstacles = []
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
	agents.append(Agent(starts[i][0],starts[i][1],form_pos[i+1][0],form_pos[i+1][1]))
	agents[i].velocity = Vector2(0,0)#(agents[i].goal-agents[i].pos).normalize()*v_max

leader = Agent(x[0],y[0],form_pos[0][0],form_pos[0][1])

#colors for the agents
colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(len(agents))]

agents=agents[::]

##Virtual Structure
VS = Virtual_Structure(leader, theta[0], form_pos)


##


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

for it in range(len(t)):

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
	for obs in range(0, len(obstacles)):
		pygame.draw.polygon(screen, red, obstacles_transformed[obs], 3)

	#Leader
	pygame.draw.circle(screen, black, transform_point(leader.pos, screen_data), int(factor/2), 0)
	#pygame.draw.line(screen,red,transform_point(Vector2(x[it],y[it]), screen_data),\
	#		transform_point(Vector2(x[it],y[it])+ Vector2(math.cos(theta[it]),math.sin(theta[it])), screen_data))
	leader.pos = Vector2(x[it],y[it])
	VS.heading = theta[it]
	leader.pointList.append([leader.pos[0],leader.pos[1]])
	pygame.draw.lines(screen, black, False, transform_points(list(leader.pointList),screen_data), 1)			


	#Virtual structure
	form_world_coords = VS.getAllWorldCoords()
	for coords in form_world_coords:
		pygame.draw.circle(screen, red, transform_point(coords, screen_data), int(factor/4), 0)
	VS.heading = theta[i]

	#Agents
	for i in range(0, len(agents)):

		agents[i].velocity = agents[i].velocity + (form_world_coords[i+1]-agents[i].pos).normalize()*a_max*dt/ \
		(form_world_coords[i+1].distance_to(agents[i].pos)+1)*10
		if agents[i].velocity.length() > v_max:
			agents[i].velocity = agents[i].velocity.normalize()*v_max

		

		pygame.draw.circle(screen, colors[i], transform_point(agents[i].pos, screen_data), int(factor/2), 0)
		#pygame.draw.circle(screen, red, transform_point(agents[i].form_pos, screen_data), int(factor/4), 0)
		
		#pygame.draw.line(screen,blue,transform_point(agents[i].pos, screen_data),\
		#	transform_point(agents[i].getVO(agents[(i+1)%len(agents)])[0]+agents[i].pos, screen_data))
		#pygame.draw.line(screen,red,transform_point(agents[i].pos, screen_data),\
		#	transform_point(agents[i].getVO(agents[(i+1)%len(agents)])[1]+agents[i].pos, screen_data))
		
		
		#Draw velocity
		#pygame.draw.line(screen,red,transform_point(agents[i].pos, screen_data),\
		#	transform_point(agents[i].pos+agents[i].velocity, screen_data))
	

		#print agents[i].tc(agents[i].velocity,agents[(i+1)%len(agents)])
		if agents[i].pos.distance_to(agents[i].form_pos)>v_max*dt:
			agents[i].pos += agents[i].velocity*dt
			agents[i].pointList.append([agents[i].pos[0],agents[i].pos[1]])

		#Draw path
		#print agents[i].pointList[0]
		pygame.draw.lines(screen, colors[i], False, transform_points(list(agents[i].pointList),screen_data), 1)			
	#print dist(*agents[0].getVO(agents[1]))

	pygame.display.update()



while True:
	#X button
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()