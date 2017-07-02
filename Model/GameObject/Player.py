from model_const import *
class player(object):
    def __init__(self, name, index, is_AI, AI = None):
        self.name = name        
        self.index = index
		self.position = playerInitPos[index]
		self.direction = 0
		self.mode = 1
		self.is_freeze = False
		self.freeze_timer = 0
		self.power = 30
		self.score = 0
		self.skillcard = None
		self.takeball = -1
		self.is_AI = is_AI
		self.AI = AI
		self.isVisible = True
		self.invisibleTime = 0

	def freeze(self, freezeTime):
		self.is_freeze = True
		self.freeze_timer = freezeTime

	def setBarrier(self):
		
	def hide(self):
		self.isVisible = True
		self.invisibleTime = invisibleTime 

	def set_barrier(self):

	def changeDirection(self, direction):
		self.direction = direction


	def tickCheck(self):
		if self.isFreeze == True:
			self.freezeTimer = self.freezeTimer - 1
			self.direction = 0
			if self.freezeTimer == 0:
				self.isFreeze = False
		if self.power <= powerMax:
			#add power
		self.position[0] += dirConst[self.direction][0]
		self.position[1] += dirConst[self.direction][1]

	def shot(self):
		ballIndex = self.takeball
		self.takeball = -1
		return ballIndex

	def bump(self, target):
		if (self.direction[0]-target.direction[0])**2+(self.direction[1]-target.direction[1])**2 <= playerBumpDistance :
			if self.mode == target.mode :
				self.freeze
				target.freeze
			elif self.mode == 0:
				self.freeze
			else
				target.freeze




