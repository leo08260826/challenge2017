from model_const import *
class player(object):
    def __init__(self, name, index, is_AI, AI = None):
        self.name = name        
        self.index = index
		self.position = player_init_pos[index]
		self.direction = dir_const[0]
		self.mode = 1
		self.is_freeze = 0
		self.power = 30
		self.score = 0
		self.skillcard = None
		self.is_takeball = 0
		self.is_AI = is_AI
		self.AI = AI

