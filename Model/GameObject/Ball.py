import random
from model_const import *

class OriginalBall(object):
    def __init__(self, index):
        self.index = index
        self.position = [random.randrange(ballRandomLower, ballRandomUpper),\
                         random.randrange(ballRandomLower, ballRandomUpper)]
        # 0: belongs to nobody, 1: belongs to somebody, 2: being thrown
        self.state = 0
        self.direction = random.randrange(1, 9)
        self.playerIndex = -1
        self.isStrengthened = False
    
    def catch(self, playerIndex):
        self.playerIndex = playerIndex
        self.state = 1
    
    def deprive(self):
        self.state = 0
        self.isStrengthened = False
    
    def throw(self, direction, isStrengthened = False):
        self.direction = direction
        self.isStrengthened = isStrengthened
        self.state = 2
        
    def tickCheck(self):
        if self.state in (0, 2):            
            self.position = [x + y * self.speed for x, y in \
                            zip(self.position, dirConst[self.direction])]

class Quaffle(OriginalBall):
    def __init__(self, index):
        super(Quaffle, self).__init__(id, index)
        self.speed = quaffleSpeed
        self.ballsize = quaffleSize / 2
        
    def deprive(self, direction):
        super(Quaffle, self).deprive(self)
        self.direction = direction

    def tickCheck(self):
        super(GoldenSnitch, self).tickCheck(self)

class GoldenSnitch(OriginalBall):
    def __init__(self, index):
        super(GoldenSnitch, self).__init__(id, index)    
        self.speed = goldenSnitchSpeed
        self.ballSize = goldenSnitchSize / 2
        
    def deprive(self, direction = 1):
        super(GoldenSnitch, self).deprive(self)
        self.direction = random.randrange(1, 9)
        
    def tickCheck(self):
        super(GoldenSnitch, self).tickCheck(self)
        

