import random
from model_const import *

class OriginalBall(object):
    def __init__(self, index):
        self.index = index
        self.position = [random.randrange(ballRandomLower, ballRandomUpper),\
                         random.randrange(ballRandomLower, ballRandomUpper)]
        self.state = 0
        self.direction = 0
        self.playerIndex = -1   
    
    def catch(self, playerIndex):
        self.playerIndex = playerIndex
        self.state = 1
        
    def throw(self, direction):
        self.direction = direction
        
    def tick_check(self):
        if self.state == 2:
            self.position = [x + y * self.speed for x, y in \
                            zip(self.position, dir_const[self.direction])]
        
class Quaffle(OriginalBall):
    def __init__(self, index):
        super(Quaffle, self).__init__(id, index)
        self.speed = quaffleSpeed
    
    
class GoldenSnitch(OriginalBall):
    def __init__(self, index):
        super(Quaffle, self).__init__(id, index)    
        self.speed = goldenSnitchSpeed
        
