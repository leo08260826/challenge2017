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
        self.direction = [random.randrange(1,5), random.randrange(1,5)]


    def tick_check(self, players):
        fleeDirectionList = []
        # the golden snitch will flee if some player's distance to it is smaller than alertRadius
        alertRadius = 50

        for player in players:
            distance = ((player[0] - self.position[0])**2 + (player[1] - self.position[1])**2) ** 0.5
            if (distance <= alertRadius)
            fleeDirectionList.append((self.position[0] - player[0], self.position[1] - player[1]))

        # if there's no need to flee, don't change the direction. Move with half speed
        if not fleeDirectionList:
            self.position = [x + y * 0.5 for x, y in zip(self.position, self.direction)]
            return

        # calculate the vector sum of fleeDirectionList
        vectorSum = [0, 0]
        for vector in fleeDirectionList:
            vectorSum[0] += vector[0]
            vectorSum[1] += vector[1]


        # if 2 players are approaching form opposite direction
        if (fleeDirectionList.len() >= 2 &&\
            ((vectorSum[0] ** 2 + vectorSum[1] ** 2) ** 0.5) == 0 ||\
             (fleeDirectionList[0][0] / fleeDirectionList[1][0] ==  fleeDirectionList[1][0] / fleeDirectionList[1][1]\
                && fleeDirectionList[0][0] / fleeDirectionList[1][0] < 0):
            vectorSum[0] = fleeDirectionList[0][1]
            vectorSum[1] = fleeDirectionList[0][0]

        # adjust the magnitude of the vector sum
        scaleFactor = self.speed / ((vectorSum[0] ** 2 + vectorSum[1] ** 2) ** 0.5)
        self.direction[0] = vectorSum[0] * scaleFactor
        self.direction[1] = vectorSum[1] * scaleFactor

        # update position
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]

