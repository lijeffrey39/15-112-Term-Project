import pygame 
from pygame.locals import *
import pygame.gfxdraw
import random
import copy
import sys
import pymunk
import pymunk.pygame_util
import math

#Curves for slopes were created from the Bezier Algorithm (https://en.wikipedia.org/wiki/B%C3%A9zier_curve)
#Rock Image - https://cdn.vectorstock.com/i/thumb-large/65/58/10436558.jpg
#Coin Image - http://www.freepik.com/blog/wp-content/uploads/2016/06/32-done.gif
#Stick Man - http://www.clker.com/cliparts/a/5/c/f/1207432041269822555snow%20boarding%20white.svg.med.png

pygame.font.init()

screen_width = 700
screen_height = 600

flags=FULLSCREEN | DOUBLEBUF
gameDisplay=pygame.display.set_mode((screen_width,screen_height))
space = pymunk.Space()
space.gravity = (0.0, -4500.0)
draw_options = pymunk.pygame_util.DrawOptions(gameDisplay)

clock = pygame.time.Clock()
listp = [[0, 400]]

def generateSlope(tempList):
	x = tempList[0][0]
	y = tempList[0][1]
	for i in range(2):
		addx = random.randrange(300, 3000)
		x += addx
		if (300 <= addx <= 800):
			addy = random.randrange(100, 150)
		elif (800 <= addx <= 2000):
			addy = random.randrange(150, 400)
		elif (2000 <= addx <= 3000):
			addy = random.randrange(400, 500)
		y += addy
		tempList += [[x, y]]
	return tempList

listp = [[0, 400], [1000, 900], [4000, 1600]]

#Colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
background = (127, 173, 162)
top = (66,123,106)
bot = (106,164,142)
cloud = (255, 255, 255)
treecolor = (33, 71, 67)

###############################################################################
#                             Background Stuff
###############################################################################

#Creates list of snow particles
snow_list = []

for i in range(50):
	x = random.randrange(0, screen_width)
	y = random.randrange(0, screen_height)
	snow_list.append([x, y])

def updateSnow(snowList):
	for i in range(len(snow_list)):
		pygame.draw.circle(gameDisplay, WHITE, snow_list[i], 2)

		snow_list[i][1] += 1
		if snow_list[i][1] > screen_height:
			y = random.randrange(-50, -10)
			snow_list[i][1] = y
			x = random.randrange(0, screen_width)
			snow_list[i][0] = x

mountain = []
mountain1 = []
mountain2 = []
start = -580
start1 = -430
start2 = -580
for i in range(10):
	y = 0
	y1 = 0
	if (i % 2 == 0):
		y = 300
		y1 = 260
	else:
		y = 400
		y1 = 360
	mountain += [[start, y]]
	mountain1 += [[start1, y]]
	start += 200
	start1 += 200

for i in range(16):
	y = 0
	y1 = 0
	if (i % 2 == 0):
		y = 350
		y1 = 410
	else:
		y = 400
		y1 = 360
	mountain2 += [[start2, y]]
	start2 += 100

for i in range(len(mountain1)):
	mountain1[i][0] += random.randrange(-20, 20)
	mountain1[i][1] += random.randrange(-10, 10)
	mountain1[i][1] += 10

for i in range(len(mountain2)):
	mountain2[i][0] += random.randrange(-10, 10)
	mountain2[i][1] += random.randrange(-5, 5)
	mountain2[i][1] -= 70

def drawMountain():
	global mountain
	global top
	global bot

	pygame.draw.rect(gameDisplay, bot, (0, 400, screen_width, screen_height))

	for i in range(len(mountain)):
		#pygame.draw.circle(gameDisplay, WHITE, [int(mountain[i][0]), int(mountain[i][1])], 3)

		mountain[i][0] -= 0.8
		if (mountain[3][0] < 0):
			last = mountain[len(mountain) - 1]
			first = mountain[0]
			second = mountain[1]
			dist = mountain[1][0] - mountain[0][0]
			mountain += [[last[0] + dist, first[1]]]
			mountain = mountain[1:]

	check = copy.deepcopy(mountain)

	if (check[0][1] < check[1][1]):
		check = check[1:]
	else:
		check = check[:len(check) - 1]

	for i in range(len(check) - 2):
		if (i % 2 == 0):
			X1 = check[i][0]
			Y1 = check[i][1]
			X2 = check[i + 2][0]
			Y2 = check[i + 2][1]
			midX = check[i + 1][0]
			midY = check[i + 1][1]
			m1 = (Y1 - midY) / (midX - X1)
			m2 = (midY - Y2) / (X2 - midX)

			h1 = Y1 - midY
			h2 = Y2 - midY
			a = bot
			b = top

			rate1 = (float((b[0] - a[0]) / h1),
					 (float(b[1] - a[1]) / h1),
					 (float(b[2] - a[2]) / h1)
					 )

			for i in range(int(Y1 - midY)):
				first = (X1 + int(i / m1), Y1 - i)
				second = (midX, Y1 - i)

				color = (min(max(a[0] + (rate1[0] * i), 0), 255), 
					min(max(a[1] + (rate1[1] * i), 0), 255), 
					min(max(a[2] + (rate1[2] * i), 0),255))
				pygame.draw.line(gameDisplay, color, first, second, 1)

			for i in range(int(Y2 - midY)):
				num = -i
				first = (midX, Y2 - i)
				second = (X2 - int(num / m2), Y2 - i)
				
				color = (min(max(a[0] + (rate1[0] * i), 0), 255), 
					min(max(a[1] + (rate1[1] * i), 0), 255), 
					min(max(a[2] + (rate1[2] * i), 0),255))
				pygame.draw.line(gameDisplay, color, first, second, 1)

	# for i in range(len(mountain) - 1):
	# 	first = (int(mountain[i][0]), int(mountain[i][1]))
	# 	second = (int(mountain[i + 1][0]), int(mountain[i + 1][1]))

	# 	pygame.draw.line(gameDisplay, BLACK, first, second, 3)

def drawSolidMountain():
	global mountain1
	global mountain2

	for i in range(len(mountain2)):
		#pygame.draw.circle(gameDisplay, WHITE, [int(mountain1[i][0]), int(mountain1[i][1])], 3)

		mountain2[i][0] -= 0.2
		if (mountain2[3][0] < 0):
			last = mountain2[len(mountain2) - 1]
			first = mountain2[0]
			second = mountain2[1]
			dist = mountain2[1][0] - mountain2[0][0]
			mountain2 += [[last[0] + dist, first[1]]]
			mountain2 = mountain2[1:]
	tempMountain = copy.deepcopy(mountain2)
	tempMountain.insert(0, [0, screen_height])
	tempMountain.append([screen_width, screen_height])
	pygame.draw.polygon(gameDisplay, bot, tempMountain)

	for i in range(len(mountain1)):
		#pygame.draw.circle(gameDisplay, WHITE, [int(mountain1[i][0]), int(mountain1[i][1])], 3)

		mountain1[i][0] -= 0.4
		if (mountain1[3][0] < 0):
			last = mountain1[len(mountain1) - 1]
			first = mountain1[0]
			second = mountain1[1]
			dist = mountain1[1][0] - mountain1[0][0]
			mountain1 += [[last[0] + dist, first[1]]]
			mountain1 = mountain1[1:]
	tempMountain = copy.deepcopy(mountain1)
	tempMountain.insert(0, [0, screen_height])
	tempMountain.append([screen_width, screen_height])
	pygame.draw.polygon(gameDisplay, (91,152,134), tempMountain)


layer1 = [[-400, screen_height]]
layer2 = [[-400, screen_height]]
layer3 = [[-400, screen_height]]

def createClouds(layer1, rangeY1, rangeY2, cloudSteepness):
	layer1 += [[-400, 400]]
	startX = layer1[1][0]
	startY = layer1[1][1]
	while(startX < screen_width + 400):
		addX1 = random.randrange(20, 70)
		addX2 = random.randrange(30, 130)
		addY = cloudSteepness
		addOrSub = random.randrange(0, 2)
		if (addOrSub == 0):
			addY = addY
		else:
			addY = -addY
		if (startY < rangeY1):
			addY = abs(addY)
		if (startY > rangeY2):
			addY = -abs(addY)
		startX += addX1
		startY += addY
		layer1 += [[startX, startY]]
		startX += addX2
		layer1 += [[startX, startY]]
	layer1 += [[startX, screen_height]]
	return layer1

layer1 = createClouds(layer1, 400, 450, 15)
layer2 = createClouds(layer2, 450, 490, 25)
layer3 = createClouds(layer3, 470, 520, 30)

def shiftClouds(layer):
	for i in range(len(layer)):
		layer[i][0] -= 0.8
		if (layer[0][0] < -402):
			last = layer[len(layer) - 1]
			secondLast = layer[len(layer) - 2]
			first = layer[0]
			second = layer[1]
			third = layer[2]
			dist = layer[2][0] - layer[1][0]
			layer[0][0] = layer[2][0]
			layer[len(layer) - 1][0] = last[0] + dist
			layer.insert(len(layer) - 1, [secondLast[0] + dist, layer[1][1]])
			layer.pop(1)

def drawClouds():
	shiftClouds(layer1)
	shiftClouds(layer2)
	shiftClouds(layer3)

	cloud1 = pygame.Surface((screen_width + 800,screen_height))
	cloud1.set_colorkey((0,0,0))
	cloud1.set_alpha(40)
	pygame.draw.polygon(cloud1, cloud, layer1)

	cloud2 = pygame.Surface((screen_width + 800,screen_height))
	cloud2.set_colorkey((0,0,0))
	cloud2.set_alpha(60)
	pygame.draw.polygon(cloud2, cloud, layer2)

	cloud3 = pygame.Surface((screen_width + 800,screen_height))
	cloud3.set_colorkey((0,0,0))
	cloud3.set_alpha(80)
	pygame.draw.polygon(cloud3, cloud, layer3)

	gameDisplay.blit(cloud1, (0,20))
	gameDisplay.blit(cloud2, (0,20))
	gameDisplay.blit(cloud3, (0,20))

def gradient(x1, x2, y1, y2, color1, color2):
	x1 = 0
	x2 = screen_width
	a, b = color1, color2
	y1 = 0
	y2 = screen_height
	h = y2 - y1
	rate = (float((b[0] - a[0]) / h),
			 (float(b[1] - a[1]) / h),
			 (float(b[2] - a[2]) / h)
			 )
	for line in range(y1,y2):
		 color = (min(max(a[0] + (rate[0] * line), 0), 255),
				  min(max(a[1] + (rate[1] * line), 0), 255),
				  min(max(a[2] + (rate[2] * line), 0),255))
		 pygame.draw.line(gameDisplay, color, (0, line), (screen_width, line), 2)


###############################################################################
#                             Create Slope
###############################################################################

def makeControl(listp):
	L = []
	for i in range(len(listp) - 1):
		first = listp[i]
		second = listp[i + 1]
		distance = second[0] - first[0]
		tempL = [first, (first[0] + distance / 2, first[1]), (second[0] - distance / 2, second[1]), second]
		L += [tempL]
	return L

perm = makeControl(listp)

def multiply(num, vect):
	return [num * vect[0], num * vect[1]]

def summing(a, b, c, d):
	return[a[0] + b[0] + c[0] + d[0], a[1] + b[1] + c[1] + d[1]]

def GetBezierPoint(points, t):
	p1 = multiply(math.pow((1.0 - t), 3), points[0])
	p2 = multiply((3 * math.pow((1.0 - t), 2) * t), points[1])
	p3 = multiply((3 * (1.0 - t) * math.pow((t), 2)), points[2])
	p4 = multiply(math.pow((t), 3), points[3])

	return summing(p1, p2, p3, p4)

def createPoints():
	tempPoints = []
	for points in perm:
		t = 0.0
		while t < 1.02:
			tempPoints.append(GetBezierPoint(points, t))
			t += 0.02
	return tempPoints

def createHills():
	static_lines = []
	static_body = space.static_body

	for i in range(len(allPoints)):
		allPointsFake[i][1] = screen_height - allPointsFake[i][1] + 300

	for i in range(len(allPoints) - 1):
		static_lines += [pymunk.Segment(static_body, (allPointsFake[i][0], allPointsFake[i][1]), 
			(allPointsFake[i + 1][0], allPointsFake[i + 1][1]), 0.5)]

	for line in static_lines:
		line.elasticity = 0
		line.friction = 400000
	space.add(static_lines)

def drawSolidSlope():
	global allPoints
	new = copy.deepcopy(allPoints)

	for i in range(len(allPoints)):
		new[i][1] = screen_height - allPoints[i][1]

	#pygame.draw.aalines(gameDisplay, (222, 249, 255), False, new)
	for i in range(len(allPoints) - 1):
		pygame.gfxdraw.aapolygon(gameDisplay, ((allPoints[i][0], screen_height), 
			(allPoints[i][0], screen_height - allPoints[i][1]), (allPoints[i + 1][0], screen_height - allPoints[i + 1][1]), 
			(allPoints[i + 1][0], screen_height)), (228,234,231))
		pygame.gfxdraw.filled_polygon(gameDisplay, ((allPoints[i][0], screen_height), 
			(allPoints[i][0], screen_height - allPoints[i][1]), (allPoints[i + 1][0], screen_height - allPoints[i + 1][1]), 
			(allPoints[i + 1][0], screen_height)), (228,234,231))

def shiftSlope():
	global allPoints
	global timer
	global rockPoints
	global treePoints
	global coinPoints

	for i in range(len(allPoints)):
		allPoints[i][0] = pastPoints[i][0]
		allPoints[i][1] = pastPoints[i][1]

	shiftx = shape1.body.position[0] - 200
	for i in range(len(allPoints)):
		allPoints[i][0] -= shiftx

	shifty = 515 - shape1.body.position[1] + 70

	for i in range(len(allPoints)):
		allPoints[i][1] += shifty

	for i in range(len(rockPoints)):
		rockPoints[i][0] = pastRockPoint[i][0]
		rockPoints[i][1] = pastRockPoint[i][1]
		rockPoints[i][0] -= shiftx
		rockPoints[i][1] += shifty

	for i in range(len(treePoints)):
		treePoints[i][0] = pastTreePoints[i][0]
		treePoints[i][1] = pastTreePoints[i][1]
		treePoints[i][0] -= shiftx
		treePoints[i][1] += shifty

	for i in range(len(coinPoints)):
		coinPoints[i][0] = coinPointsPast[i][0]
		coinPoints[i][1] = coinPointsPast[i][1]
		coinPoints[i][0] -= shiftx
		coinPoints[i][1] += shifty

def adjustCoords():
	for i in range(len(allPoints)):
		allPoints[i][1] = screen_height - allPoints[i][1]

allPoints = createPoints()
allPointsFake = copy.deepcopy(allPoints) 
adjustCoords()
pastPoints = copy.deepcopy(allPoints)
createHills()

point1 = None
point2 = None

angleSlope = 0
anglePerson = 0
yValue = None

###############################################################################
#                         	Physics of Player
###############################################################################

player_img = pygame.image.load("snowboarder.png")

rock_imgDim = (50, 40)
rock_img = pygame.image.load("rock1.png")
rock_img = pygame.transform.smoothscale(rock_img, rock_imgDim)

centerx = 200
centery = 382

#Checks to make sure ball is only drawn once
drawn = False 

touching = False

def checkTouch(arbiter, space, data):
	global touching
	touching = True

def begin(space, arbiter, *args, **kwargs):
	global touching
	touching_top = True
	return True

ch = space.add_collision_handler(0, 0)
ch.data["surface"] = gameDisplay
ch.post_solve = checkTouch
ch.begin = begin

class Player(pygame.sprite.Sprite):
	global anglePerson
	global touching
	global centerx
	global centery

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.smoothscale(player_img, (50, 46))
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery
		self.anglePerson = 0.3

	def update(self):
		orig_rect = player_img.get_rect()
		rot_image = pygame.transform.rotozoom(player_img, -self.anglePerson * 57.2958, 1)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		self.image = rot_image

allSprites = pygame.sprite.Group()
player = Player()
allSprites.add(player)

timer = 0

currSlope = 0
currSlopeY = 0
currSlopeX = 0

def findAngle():
	global allPointsFake
	global angleSlope
	global anglePerson
	global currSlopeX
	global currSlopeY
	global currSlope

	for i in range(len(allPointsFake) - 1):
		if (allPointsFake[i][0] > shape1.body.position[0]):
			currSlopeY = allPointsFake[i][1]
			currSlopeX = allPointsFake[i][0]
			yValue = shape1.body.position[1] - allPointsFake[i][1]
			point1 = (allPointsFake[i][0], screen_height - allPointsFake[i][1])
			point2 = (allPointsFake[i + 1][0], screen_height - allPointsFake[i + 1][1])
			if ((point2[0] - point1[0]) == 0):
				break
			m = ((point2[1] - point1[1]) / (point2[0] - point1[0]))
			currSlope = m
			if (touching == False):
				angleSlope = math.atan(m)
				break
			angleSlope = math.atan(m)
			anglePerson = angleSlope
			break

flip = False
pastListp = []
newList = listp

def generateRocks():
	global allPoints
	global newList

	pp = copy.deepcopy(allPoints)
	numRocks = random.randrange(2, 4)
	returnRockPoints = [] 
	counter = 0

	for i in range(len(pp)):
		if (pp[i][0] > newList[0][0]):
			counter = i
			break

	if (len(listp) == 3):
		xValue = 0
		iValue = 0
		while (xValue < pp[len(pp) - 1][0] - 800):
			iValue += 1
			xValue = pp[iValue][0]
		for i in range(1):
			index = random.randrange(5 * iValue // 6, iValue)
			returnRockPoints += [pp[index]]
	else:
		xValue = 0
		iValue = counter
		while (xValue < pp[len(pp) - 1][0] - 700):
			iValue += 1
			xValue = pp[iValue][0]
		xValue1 = pp[len(pp) - 1][0]
		iValue1 = len(pp) - 1
		while (xValue1 > pp[counter][0] + 100):
			iValue1 -= 1
			xValue1 = pp[iValue1][0]
		for i in range(numRocks):
			index = random.randrange(iValue1, iValue)
			returnRockPoints += [pp[index]]

	return returnRockPoints

rockPoints = generateRocks()
pastRockPoint = copy.deepcopy(rockPoints)

distance = 0
prevTimer = [True, 0]
prevAngle = 0

coinPoints = []

def generateTreePoints():
	global allPoints
	global newList
	global coinPoints

	allPointsss = copy.deepcopy(allPoints)
	returnTreePoint = [] 
	numTrees = random.randrange(15, 22)
	counter2 = 0

	coinNum = random.randrange(10, 12)
	coinPoints = []

	for i in range(len(allPointsss)):
		if (allPointsss[i][0] > newList[0][0]):
			counter2 = i
			break

	if (len(listp) == 3):
		xValue = 0
		iValue = 0
		while (xValue < allPointsss[len(allPointsss) - 1][0] - 800):
			iValue += 1
			xValue = allPointsss[iValue][0]
		for i in range(numTrees):
			index = random.randrange(0, iValue)
			returnTreePoint += [allPointsss[index]]
		for i in range(coinNum):
			index = random.randrange(0, iValue)
			coinPoints += [allPointsss[index]]
	else:
		xValue = 0
		iValue = counter2
		while (xValue < allPointsss[len(allPointsss) - 1][0] - 700):
			iValue += 1
			xValue = allPointsss[iValue][0]
		xValue1 = allPointsss[len(allPointsss) - 1][0]
		iValue1 = len(allPointsss) - 1
		while (xValue1 > allPointsss[counter2][0] + 100):
			iValue1 -= 1
			xValue1 = allPointsss[iValue1][0]
		for i in range(numTrees):
			index = random.randrange(iValue1, iValue)
			returnTreePoint += [allPointsss[index]]
		for i in range(coinNum):
			index = random.randrange(iValue1, iValue)
			coinPoints += [allPointsss[index]]

	return returnTreePoint

treePoints = generateTreePoints()
pastTreePoints = copy.deepcopy(treePoints)
coinPointsPast = copy.deepcopy(coinPoints)

def drawTree():
	global coinPoints
	global coin
	width = 70
	height = 150
	for i in range(len(treePoints)):
		pygame.gfxdraw.filled_polygon(gameDisplay, [[treePoints[i][0] - width // 2, 
			screen_height - treePoints[i][1] + 10], [treePoints[i][0] + width // 2, 
			screen_height - treePoints[i][1] + 35], [treePoints[i][0], 
			screen_height - treePoints[i][1] - height + 35]], treecolor)

def checkRockCollision():
	global centerx
	global centery
	global rockPoints
	global rock_imgDim
	global splash
	global gameOver

	xDim = rock_imgDim[0]
	yDim = rock_imgDim[1]

	for i in range(len(rockPoints)):
		rockX = rockPoints[i][0]
		rockY = rockPoints[i][1]
		if (rockX - (xDim // 2) < centerx and rockX + (xDim // 2) > centerx):
			if (rockY + (yDim // 2) > screen_height - centery and rockY - (yDim // 2) < screen_height -centery):
				splash = False
				gameOver = True

def checkCoinCollision():
	global coinPoints
	global centerx
	global centery
	global touchedCoin
	global currCoin
	global bonus
	global coinBonusTime
	global coinPointsPast

	coinPointsLen = len(coinPoints)
	for i in range(coinPointsLen - 1):
		coinX = coinPoints[i][0]
		coinY = coinPoints[i][1] 
		if (coinX < centerx < coinX + 25):
			if (coinY < screen_height - centery < coinY + 25):
				if (touchedCoin == False and currCoin != i):
					coinBonusTime = 50
					bonus += 500
					coinPointsLen -= 1
					coinPoints.pop(i)
					coinPointsLen -= 1
					coinPointsPast.pop(i)
				currCoin = i
				touchedCoin = True


###############################################################################
#                         	Score Keeping
###############################################################################
score = 0
bonus = 0
timerBonusPlus = 0
touchedCoin = False
coinBonusTime = 0
currCoin = 0

font = pygame.font.Font("rale/raleway.ttf", 50)
font1 = pygame.font.Font("rale/raleway.ttf", 45)
velocityText = pygame.font.Font("rale/raleway.ttf", 30)
font2 = pygame.font.Font("rale/raleway.ttf", 40)
titleFont = pygame.font.Font("rale/avenir.otf", 70)

backFlipText = velocityText.render("Backflip", 1, BLACK)
frontFlipText = velocityText.render("FrontFlip", 1, BLACK)
backFlipBonus = velocityText.render("+" + str(int(50)) , 1, BLACK)
coinText = velocityText.render("Coin Collected", 1, BLACK)
coinBonus = velocityText.render("+" + str(int(5)) , 1, BLACK)

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

splash = True
helpScreen = False
playing = True
aboutScreen = False
gameOver = False

coin = pygame.image.load("coins.png")
numImages = 6
cImage = 0

def drawCoin():
	global coin
	global numImages
	global cImage
	if(cImage >= numImages - 1):
		cImage = 0
	else:
		cImage += 1
	for i in range(len(coinPoints)):
		gameDisplay.blit(coin, (coinPoints[i][0], screen_height - coinPoints[i][1] - 35), (cImage * 25, 0, 25, 43))


def gameLoop():
	global listp, touching, timer, drawn, shape1, anglePerson, bonus, flip, prevTimer, timerBonusPlus, rockPoints, allPoints
	global rockPoints, pastPoints, treePoints, pastRockPoint, pastTreePoints, snow_list, newList, pastListp, perm, allPointsFake
	global splash, playing, coin, numImages, cImage, coinPointsPast, coinPoints, helpScreen, gameOver, allSprites, touchedCoin
	global coinBonusTime, prevAngle, aboutScreen

	pressedSpace = False
	prevPressedSpace = True
	backFlip = False
	frontFlip = False

	while playing:

		while (splash == True):
			gameDisplay.fill(background)
			gradient(0, screen_width, 0, 400, (204,243,196), (109,170,152))
			drawSolidMountain()
			drawMountain()
			drawTree()

			drawSolidSlope()
			allSprites.update()       
			allSprites.draw(gameDisplay)

			startButton = font1.render("Press Space to Begin", 1, BLACK)
			gameDisplay.blit(startButton, (140, 3 * screen_height // 4))

			startButton = titleFont.render("SNOWBOARD", 1, BLACK)
			gameDisplay.blit(startButton, (115, 130))
			startButton = titleFont.render("ADVENTURES", 1, BLACK)
			gameDisplay.blit(startButton, (115, 200))

			Help = font2.render("Help", 1, BLACK)
			gameDisplay.blit(Help, (20, 20))

			About = font2.render("About", 1, BLACK)
			gameDisplay.blit(About, (562, 20))

			mouse = pygame.mouse.get_pos()
			click = pygame.mouse.get_pressed()

			if (10 < mouse[0] < 115 and 10 < mouse[1] < 65):
				pygame.draw.rect(gameDisplay, bot, (10,10,105,55), 1)
				Help = font2.render("Help", 1, bot)
				gameDisplay.blit(Help, (20, 20))
				if (click[0] == 1):
					helpScreen = True
					splash = False
					gameLoop()
			else:
				pygame.draw.rect(gameDisplay, BLACK,(10,10,105,55), 1)

			if (555 < mouse[0] < 680 and 10 < mouse[1] < 65):
				pygame.draw.rect(gameDisplay, bot,(555,10,125,55), 1)
				About = font2.render("About", 1, bot)
				gameDisplay.blit(About, (562, 20))
				if (click[0] == 1):
					aboutScreen = True
					splash = False
					gameLoop()
			else:
				pygame.draw.rect(gameDisplay, BLACK,(555,10,125,55), 1)

			# pygame.draw.rect(gameDisplay, BLACK,(10,10,105,55), 1)
			# pygame.draw.rect(gameDisplay, BLACK,(555,10,125,55), 1)


			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						splash = False
						gameLoop()

		while (helpScreen == True):
			gameDisplay.fill(background)
			gradient(0, screen_width, 0, 400, (204,243,196), (109,170,152))

			startButton = font1.render("Press Space to go Home", 1, BLACK)
			gameDisplay.blit(startButton, (100, 4 * screen_height // 5))

			startButton = velocityText.render("- Press space to jump", 1, BLACK)
			gameDisplay.blit(startButton, (100, 1 * screen_height // 5 + 20))
			startButton = velocityText.render("- Press the left and right arrow in the air", 1, BLACK)
			gameDisplay.blit(startButton, (100, 3 * screen_height // 10 - 15 + 20))
			startButton = velocityText.render("  to perform tricks", 1, BLACK)
			gameDisplay.blit(startButton, (100, 3 * screen_height // 10 + 20 + 20))
			startButton = velocityText.render("- Collect coins for points", 1, BLACK)
			gameDisplay.blit(startButton, (100, 2 * screen_height // 5 + 5 + 20))

			startButton = titleFont.render("HELP", 1, BLACK)
			gameDisplay.blit(startButton, (260, 30))

			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						splash = True
						helpScreen = False
						gameLoop()


		while (aboutScreen == True):
			gameDisplay.fill(background)
			gradient(0, screen_width, 0, 400, (204,243,196), (109,170,152))

			startButton = font1.render("Press Space to go Home", 1, BLACK)
			gameDisplay.blit(startButton, (100, 4 * screen_height // 5))

			startButton = velocityText.render("Created by Jeffrey Li for the 15-112 Term Project", 1, BLACK)
			gameDisplay.blit(startButton, (26, 3 * screen_height // 10 - 15 + 20))

			startButton = titleFont.render("ABOUT", 1, BLACK)
			gameDisplay.blit(startButton, (230, 30))

			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						splash = True
						aboutScreen = False
						gameLoop()


		while (gameOver == True):
			gameDisplay.fill(background)
			gradient(0, screen_width, 0, 400, (204,243,196), (109,170,152))
			drawSolidMountain()
			drawMountain()
			drawTree()

			drawSolidSlope()

			startButton = font1.render("Press Space for Home Screen", 1, BLACK)
			gameDisplay.blit(startButton, (35, 2 * screen_height // 3))

			startButton = titleFont.render("GAMEOVER", 1, BLACK)
			gameDisplay.blit(startButton, (145, 130))

			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						helpScreen = False
						splash = True
						gameOver = False
						gameLoop()

		gradient(0, screen_width, 0, 400, (204,243,196), (109,170,152))

		#gameDisplay.fill(background)

		if (currSlopeX + screen_width - 200 > listp[len(listp) - 1][0]):
			if (len(listp) == 3):
				pastListp = copy.deepcopy(listp)
			else:
				pastListp = listp[3:]
			newList = [listp[len(listp) - 1]]
			newList = generateSlope(newList)
			listp = pastListp + newList
			perm = makeControl(listp)
			allPoints = createPoints()
			allPointsFake = copy.deepcopy(allPoints) 
			adjustCoords()
			pastPoints = copy.deepcopy(allPoints)
			createHills()
			rockPoints = generateRocks()
			pastRockPoint = copy.deepcopy(rockPoints)
			treePoints = generateTreePoints()
			pastTreePoints = copy.deepcopy(treePoints)
			coinPointsPast = copy.deepcopy(coinPoints)

		if (touching == False):
			timer += 1

		if (drawn == False):
			mass = 100000
			radius = 75
			inertia = pymunk.moment_for_circle(mass, 300, radius, (80, 60))
			body = pymunk.Body(mass, inertia)
			x = 200
			y = 575
			body.position = (x, y)
			shape1 = pymunk.Circle(body, radius, (0, -1))
			shape1.elasticity = 0
			shape1.friction = 5000000
			space.add(body, shape1)
			drawn = True

		findAngle()

		player.anglePerson = anglePerson

		distance = shape1.body.position[0] - 200
		score = distance * 0.4 + bonus

		if (touching == False):
			anglePerson -= 0.01
			if (flip == True):
				#anglePerson -= 0.11
				pass

		if (touching == True):
			timer = 0

		if (prevPressedSpace):
			if (prevTimer[0] == False and prevTimer[1] > 14 and flip == True):
				if (touching == True and timer < 5):
					diff = abs(prevAngle + 6.283 - angleSlope)
					diff1 = abs(prevAngle - 6.283 - angleSlope)
					diff2 = abs(prevAngle - angleSlope)
					if (diff2 < 1):
						pass
					elif (diff > 1 and diff1 > 1):
						gameOver = True
						helpScreen = False
						splash = False
						gameLoop()
					else:
						if (diff < 1):
							backFlip = True
						if (diff1 < 1):
							frontFlip = True
						timerBonusPlus = 50
						bonus += 5000

		if (timerBonusPlus > 1):
			if (coinBonusTime > 1):
				gameDisplay.blit(coinBonus, (10, 180))
				gameDisplay.blit(coinText, (10, 210))
			timerBonusPlus -= 1
			if (backFlip == True):
				gameDisplay.blit(backFlipBonus, (10, 120))
				gameDisplay.blit(backFlipText, (10, 150))
			elif (frontFlip == True):
				gameDisplay.blit(backFlipBonus, (10, 120))
				gameDisplay.blit(frontFlipText, (10, 150))
		elif (coinBonusTime > 1):
			coinBonusTime -= 1
			gameDisplay.blit(coinBonus, (10, 120))
			gameDisplay.blit(coinText, (10, 150))
		else:
			frontFlip = False
			backFlip = False
			pass

		if (timer <= 14):
			flip = False

		#Drawing the background Mountain
		drawSolidMountain()
		drawMountain()

		checkRockCollision()
		checkCoinCollision()
		# if (touchedCoin == True):
		# 	bonus += 1000
		touchedCoin = False
		if (gameOver == True):
			gameLoop()

		# surface1 = pygame.Surface((50,50))
		# surface1.set_colorkey((0,0,0))
		# surface1.set_alpha(20)
		# pygame.draw.circle(surface1, (0,255,0), (50,50), 50)

		# gameDisplay.blit(surface1, (500,100))

		#Update the snow fall
		updateSnow(snow_list)

		drawClouds()

		#Shifts the slopes based on where the ball is on the Secondary Slope
		shiftSlope()

		drawTree()

		drawSolidSlope()

		drawCoin()

		for i in range(len(rockPoints)):
			gameDisplay.blit(rock_img, (int(rockPoints[i][0]), screen_height - int(rockPoints[i][1]) - 26))

		distanceLabel = font.render(str(int(distance / 100)) + " m", 1, BLACK)
		scoreLabel = font.render(str(int(score / 100)) + " Points", 1, BLACK)
		velocity = velocityText.render(str(int(shape1.body.velocity[0]) // 10) + " m/s", 1, BLACK)

		gameDisplay.blit(distanceLabel, (10, 10))
		gameDisplay.blit(scoreLabel, (10, 55))
		gameDisplay.blit(velocity, (590, 20))

		# center = (200, 410)

		# y = 20 * math.sin(angleSlope)
		# x = 20 * math.cos(angleSlope)

		# p1 = (200 - int(x), 410 - int(y))
		# p2 = (200 + int(x), 410 + int(y))

		#pygame.draw.aaline(gameDisplay, BLACK, p1, p2, 5)

		allSprites.update()       
		allSprites.draw(gameDisplay)
		   
		#space.debug_draw(draw_options)       
		#print(touching)

		prevTimer = [touching, timer]
		prevAngle = anglePerson
		touching = False

		### Update physics
		dt = 1.0 / 60.0
		space.step(dt)

		pygame.display.update()
		clock.tick(30)
		pygame.display.set_caption("fps: " + str(clock.get_fps()))

		prevPressedSpace = pressedSpace

		if (touching):
			pressedSpace = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if (pressedSpace == True):
					break
				if event.key == pygame.K_SPACE:
					timer = 15
					touching = False
					shape1.body.velocity = (400, 1200)
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					pressedSpace = True

		keys = pygame.key.get_pressed()  #checking pressed keys
		if keys[pygame.K_LEFT]:
			if (touching == True):
				continue
			timer = 15
			touching = False
			flip = True
			anglePerson -= 0.19
		if keys[pygame.K_RIGHT]:
			if (touching == True):
				continue
			timer = 15
			touching = False
			flip = True
			anglePerson += 0.19

gameLoop()