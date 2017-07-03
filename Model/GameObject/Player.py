from model_const import *
class player(object):
    def __init__(self, name, index, is_AI, AI = None):
        self.name = name        
        self.index = index
		self.position = player_init_pos[index]
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

	def hide(self):
		self.isVisible = True
		self.invisibleTime = invisibleTime 

	def set_barrier(self):

	def attack(self):

	def shot(self):
