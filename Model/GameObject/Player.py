from model_const import *
class player(object):
    def __init__(self, name, index, is_AI, AI = None):
        self.name = name        
        self.index = index
		self.position = playerInitPos[index]
		self.direction = 0
		self.mode = 1
		# 0 = attack
		# 1 = defense
		self.isFreeze = False
		self.freezeTimer = 0
		self.modeTimer = 0
		self.power = 30
		self.score = 0
		self.skillcard = None
		self.takeball = -1
		self.is_AI = is_AI
		self.AI = AI
		self.isVisible = True
		self.invisibleTime = 0

	def freeze(self, freezeTime):
		self.isFreeze = True
		self.freezeTimer = freezeTime
		self.direction = 0

	def hide(self):
		self.isVisible = True
		self.invisibleTime = invisibleTime 

	def setBarrier(self):
		self.power -= barrierPowerCost
		return (self.position, self.direction)

	def shot(self):
		ballIndex = self.takeball
		self.takeball = -1
		return (ballIndex, self.direction)

	def changeDirection(self, direction):
		self.direction = direction

	def tickCheck(self):
		self.position[0] += dirConst[self.direction][0]*playerSpeed
		self.position[1] += dirConst[self.direction][1]*playerSpeed
		if self.isFreeze == True:
			self.freezeTimer = self.freezeTimer - 1
			self.direction = 0

			if self.freezeTimer == 0:
				self.isFreeze = False
		if self.power <= powerMax:
			self.power += 1
		if self.modeTimer > 0:
			self.modeTimer = self.modeTimer - 1

		if self.position[0] < 47 or self.position[0] > 693 :
			self.direction = dirConst[0][self.direction]
		elif self.position[1] < 47 or self.position[1] > 693 :
			self.direction = dirConst[1][self.direction]		

	def bump(self, target):
		if (self.direction[0]-target.direction[0])**2+(self.direction[1]-target.direction[1])**2 <= playerBumpDistance ** 2 :
			if self.mode == target.mode :
				self.freeze()
				target.freeze()
				if self.takeball == -1 and target.takeball == -1:
					return []
				elif target.takeball == -1:
					return [(self.takeball, self.direction)]
				elif self.takeball == -1:
					return [(target.takeball, target.direction)]
				else :
					return [(self.takeball, self.direction), (target.takeball, target.direction)]
			elif self.mode == 0:
				self.freeze()
				if self.takeball != -1 :
					return [(self.takeball, self.direction)]
				else :
					return []
			else:
				target.freeze()
				if target.takeball != -1:
					return [(target.takeball, target.direction)]
				else :
					return []
