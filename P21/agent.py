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
		self.goal = Vector2(goalX,goalY)
		self.velocity = 0
		self.pointList = [[startX,startY]]

	#Not currently used
	def getVO(self,agentB):
		#print 2*radius/(self.pos.distance_to(agentB.pos))
		#print self.pos.distance_to(agentB.pos)
		res = agentB.pos - self.pos
		gamma = math.atan(res[1]/res[0])
		#print agentB.pos - self.pos
		#print agentB.pos - self.pos
		alpha = gamma - math.asin(2*radius/(self.pos.distance_to(agentB.pos)))+(0.5+0.5*sign(res[1]))*math.pi
		#print alpha

		rightVector = Vector2(0,0)
		rightVector.from_polar((4,alpha*180/math.pi))
		leftVector = rightVector.reflect((agentB.pos-self.pos).rotate(-90))
		#print leftVector.angle_to(agentB.pos-self.pos)
		#if leftVector.angle_to(agentB.pos-self.pos)>180:
			#leftVector,rightVector = rightVector,leftVector

		return leftVector, rightVector

	def tc(self, cVel, agentB):
		#leftVector,rightVector = self.getVO(agentB)
		#cVel = cVel -agentB.velocity #Makes calculations easier
		cVel = 2*cVel - self.velocity - agentB.velocity
		if cVel == [0,0]:
			return 100000
		t = intersection(cVel, self.pos, agentB.pos)

		return t

	def tcAll(self, cVel, agents):
		t = 1000
		for agent in agents:
			tc = self.tc(cVel,agent)
			if tc < t:
				t = tc
		return t

	def penalty(self, cVel, agents):
		
		

		#print 1/self.tcAll(cVel,agents), ((self.goal-self.pos).normalize()*Agent.v_max).distance_to(cVel)
		return 1/self.tcAll(cVel,agents)+ ((self.goal-self.pos).normalize()*Agent.v_max).distance_to(cVel)

	def bestVelocity(self, candidateVels, agents):
		candidateVels = self.sampleVels()
		agents = [agent for agent in agents if agent is not self and self.pos.distance_to(agent.pos)<4]
		#print len(agents)

		#print candidateVels[0]
		bestVel = self.velocity#((self.goal-self.pos).normalize()*Agent.v_max)
		bestPenalty = self.penalty(bestVel,agents)#10000#self.penalty(bestVel, agents)
		for candidateVel in candidateVels:
			penalty = self.penalty(candidateVel,agents)
			if penalty <= bestPenalty:
				bestPenalty = penalty
				bestVel = candidateVel
		#print bestPenalty
		return bestVel

	def sampleVels(self,n=20):
		candidateVels = [0]*n
		for i in range(n):
			t = 2*math.pi*random.random()
			u = random.random()*Agent.v_max+random.random()*Agent.v_max
			r = (Agent.v_max*2-u if u >Agent.v_max else u)
			vel = Vector2(r*math.cos(t), r*math.sin(t))
			candidateVels[i] = vel
		return candidateVels

	#Broken
	def sampleAccVels(self,n=40):
		candidateVels = [self.velocity]*n
		max_speed_add = 1.3*0.01
		for i in range(n):
			vel = Vector2(10,10)
			while vel.length()>max_speed_add or (self.velocity+vel).length() > Agent.v_max:
				t = 2*math.pi*random.random()
				u = random.random()*max_speed_add+random.random()*max_speed_add
				r = max_speed_add#(max_speed_add*2-u if u >max_speed_add else u)
				vel = Vector2(r*math.cos(t), r*math.sin(t))
			#print self.velocity+vel
			candidateVels[i] += vel
		#print candidateVels[0]
		return candidateVels


###############################################