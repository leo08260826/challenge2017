import random
from model_const import *

class OriginalBall(object):
    def __init__(self, index):
        self.index = index
        self.position = random.randrange(ballRandomLower, ballRandomUpper)
        self.state = 0
        self.direction = dir_const[0]
        self.playerIndex = -1
        
    def move(self):
        pass
        
class Quaffle(OriginalBall):
    def __init__(self, index):
        super(Quaffle, self).__init__(id, index)
        self.speed = quaffleSpeed
    
    
class GoldenSnitch(OriginalBall):
    def __init__(self, index):
        super(Quaffle, self).__init__(id, index)    
        self.speed = goldenSnitchSpeed
        
