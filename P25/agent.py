from pygame.math import Vector2
import math
from canvas import transform_point, transform_points
import numpy as np
import random

radius = 0.5
def sign(x): return 1 if x >= 0 else -1
def intersection(d, startRay, circlecenter):

	r = radius*2
	f = startRay - circlecenter
	a = np.dot( d,d ) ;
	b = 2*np.dot( f,d ) ;
	c = np.dot( f,f ) - r*r ;
	#print d,f,a,b,c

	discriminant = b*b-4*a*c
	#print discriminant
	if discriminant < 0:
	  return 10000
	else:

	  discriminant = np.sqrt(discriminant)

	  #print a
	  t1 = (-b - discriminant)/(2*a)
	  t2 = (-b + discriminant)/(2*a)
	  #print t1,t2

	  if(t2 >= 0 and t1 < 0):
	  	#print "collision"
	  	return 0.0001
	  if( t1 >= 0):
	  	#print "collid in: ", t1
	  	return t1
	  return 10000



#Classes
###############################################
class Agent(object):

	v_max = 0

	"""docstring for Agent"""
	def __init__(self, startX,startY,goalX,goalY):
		self.pos = Vector2(startX,startY)
		self.form_pos = Vector2(goalX,goalY)
		self.velocity = 0
		self.pointList = [[startX,startY]]


class Virtual_Structure(object):
	"""docstring for Virtual_Structure"""

	def __init__(self, leader, heading, form_pos):
		self.leader = leader
		self.heading = heading
		self.ref_pos = []
		leader_ref_pos = Vector2(form_pos[0][0],form_pos[0][1])
		for pos in form_pos:
			vector = Vector2(pos[0],pos[1])
			self.ref_pos.append(vector - leader_ref_pos)

	def getWorldCoord(self,index):
		return self.leader.pos+self.ref_pos[index].rotate(180/math.pi*(self.heading-math.pi/2))

	def getAllWorldCoords(self):
		coords = []
		for i in range(len(self.ref_pos)):
			coords.append(self.getWorldCoord(i))
		return coords

		

###############################################