
import random
import pygame
import sys
import math

NUM_NODES = 10
NUM_EDGES = 100
MAX_COST = 10
MIN_COST = 3
PATH_LEN = NUM_NODES
CHILDREN_IN_GENERATION = 50

S_WIDTH = 1240
S_HEIGHT = 800
S_CENTER = (S_WIDTH//2,S_HEIGHT//2)
NODE_RAD = 15
NODE_WIDTH = 4

# Make an array of triples such that each element of the array represents an edge of the map:
# (nodestart,nodeend,cost)
# While this says node start and end, the edges of the graph are not directed.
# This function makes the number of edges defined on top.
def makeMap():
	arr = []
	for _ in range(NUM_EDGES):
		nodestart = random.randint(0,NUM_NODES-1)
		legitpath = False
		while(not legitpath):
			nodeend = random.randint(0,NUM_NODES-1)
			if(not nodestart == nodeend):
				if(len(arr)==0):
					legitpath=True
					break
				failOnce = False
				for path in arr:
					current = (nodestart,nodeend,path[2])
					if(((nodestart,nodeend,path[2]) == path) or ((nodeend,nodestart,path[2]) == path)):
						failOnce = True
				legitpath = not failOnce
		cost = random.randint(MIN_COST,MAX_COST)
		arr.append((nodestart,nodeend,cost))
	return arr

# Same as makeMap() above, but makes a complete map for all nodes, and random costs.
def makeFullMap():
	arr = []
	for i in range(NUM_NODES):
		for j in range(i+1,NUM_NODES):
			arr.append((i,j,random.randint(1,MAX_COST)))
	print(str(arr))
	return arr

# For drawing the nodes in pygame. 
# This lays out each node evenly spaced in a circle.
def getNodeCoords():
	p = []
	angle =0
	anglestep = (2*math.pi)/NUM_NODES
	radius = int(min(S_CENTER[0],S_CENTER[1])*.8)
	for _ in range(NUM_NODES):
		xcoord = S_CENTER[0]+int(radius * math.cos(angle))
		ycoord = S_CENTER[1]+int(radius * math.sin(angle))
		angle+=anglestep
		p.append((xcoord,ycoord))
	return p

# Function to draw text.
def getTextObj(text, font):
	textSurface = font.render(text, True, (0,0,0))
	return textSurface, textSurface.get_rect()
# Sister function of above.
def drawText(screen,text,center,font):
	ts,tr = getTextObj(text,font)
	tr.center = center
	screen.blit(ts,tr)

#get the coordinates of the lines such that they dont draw onto the interior of the node.
def getLinePoints(point1,point2):
	anglediff = math.atan2(point2[1]-point1[1],point2[0]-point1[0])
	changelengthx = (NODE_RAD)*(math.cos(anglediff))
	changelengthy = (NODE_RAD)*(math.sin(anglediff))
	newp1 = [point1[0]+changelengthx,point1[1]+changelengthy]
	newp2 = [point2[0]-changelengthx,point2[1]-changelengthy]
	return [newp1,newp2]

# Get the value of the specified path
# Returns cost,val
# Cost of the aggregate cost of the edges traveled
# Val is the number of unique nodes visited
def getPathVal(path):
	totalCost = 0
	uniqueVisited = [0]*NUM_NODES
	for line in path:
		totalCost += line[2]
		uniqueVisited[line[0]]=1
		uniqueVisited[line[1]]=1
	return totalCost, sum(uniqueVisited)

# Returns a random, legitimate path passing through a number of nodes as defined by PATH_LEN.
def getRandomPath(paths):
	mypath = []
	nodesvisited = []
	currentNode = 0
	for _ in range(PATH_LEN):
		legitpath = False
		rpath = None
		while(not legitpath):
			rpath = random.choice(paths)
			if(rpath[0] == currentNode or rpath[1] == currentNode):
				legitpath = True
		nodesvisited.append(currentNode)
		if(rpath[0] == currentNode):
			currentNode = rpath[1]
		else:
			currentNode = rpath[0]
		mypath.append(rpath)
	return mypath

# Returns a path modified (or identical) to the passed map.
# Generates CHILDREN_IN_GENERATION number of child paths and sees which is the best.
# Returns the best one
#
# TODO: Make actual genetic algorithm. Currently it chooses the best out of 50 random, but the generated ones should use genetic algorithms to adapt the given path.
def getAdaptedPath(tried,paths):
	oldCost, oldNodesVisited = getPathVal(tried)
	candidates = []
	for i in range(CHILDREN_IN_GENERATION):
		splicer = random.randint(0,oldCost)
		costCounter = 0
		candidates.append(getRandomPath(paths))
		""" for x in range(len(tried)):
			if(splicer < costCounter): #once we get to our splicing position
				currentNode = 0
				if(x==1): 
					currentNode = tried[x][0] if tried[x][1]==0 else tried[x][1]
				if(x>1):
					currentNode = tried[x][0] if (tried[x][1]==tried[x-1][0] or tried[x][1]==tried[x-1][1]) else tried[x][1] 
				legitpath = False
				rpath = None
				while(not legitpath):
					rpath = random.choice(paths)
					if(rpath[0] == currentNode or rpath[1] == currentNode):
						legitpath = True
				if(rpath[0] == currentNode):
					currentNode = rpath[1]
				else:
					currentNode = rpath[0]
				candidates[i][x] = rpath
			costCounter+=tried[x][2] """
	candidates.append(tried)
	lowestcost = oldCost
	bestpath = len(candidates)-1
	for i in range(len(candidates)):
		cost,val = getPathVal(candidates[i])
		lowestcost = min(cost,lowestcost)
		if(lowestcost == cost):
			bestpath = i
	for i in range(len(candidates)):
		if(i==bestpath):
			print('best -> ', end='')
		c,v = getPathVal(candidates[i])
		print(str(i) + "'s cost:" + str(c))
		
	return candidates[bestpath]

# Get a path, either random or adapted, depending on if one has been tried yet.
def getPath(tried,paths):
	
	if(tried == None):
		return getRandomPath(paths)
	else:
		return getAdaptedPath(tried,paths)

#Pygame is used to demonstrate the path.
def main():
	paths = makeFullMap()
	pygame.init()
	pygame.font.init()
	myfont = pygame.font.SysFont('Ariel', 12)
	screen = pygame.display.set_mode((S_WIDTH,S_HEIGHT))

	screen.fill((220,220,220))

	nodespoints = getNodeCoords()	
	print(str(nodespoints))
	
	"""  """
	p = None

	while(True):
		screen.fill((220,220,220))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() 
				sys.exit()
			if(event.type == pygame.KEYDOWN): #Setup so that spacebar updates the path. If its not updating, you probably found the best path. (local minima)
				if(event.key == pygame.K_SPACE):
					p = getPath(p,paths)

		#drawing functions...
		for i in range(len(nodespoints)):
			pygame.draw.circle(screen,(40,40,40),nodespoints[i],NODE_RAD,NODE_WIDTH)
			drawText(screen,str(i),nodespoints[i],myfont)
		for path in paths:
			pygame.draw.lines(screen,(20,150,20),False,getLinePoints(nodespoints[path[0]],nodespoints[path[1]]),path[2])
		if(not p==None):
			c = 0
			cstep = 200//PATH_LEN
			pygame.draw.circle(screen,(250,20,50),nodespoints[0],NODE_RAD,NODE_WIDTH)
			for path in p:
				pygame.draw.lines(screen,(min(250 - c,255),20,min(50 + c,255)),False,getLinePoints(nodespoints[path[0]],nodespoints[path[1]]),path[2])
				c+=cstep

		pygame.display.update()




main()