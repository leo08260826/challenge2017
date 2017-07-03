import random
from model_const import *

class OriginalBall(object):
    def __init__(self, index):
        self.index = index
        self.position = [random.randrange(ballRandomLower, ballRandomUpper),\
                         random.randrange(ballRandomLower, ballRandomUpper)]
        # 0: belongs to nobody, 1: belongs to somebody, 2: being thrown
        self.state = 0
        # 1~8: eight directions
        self.direction = random.randrange(1, 9)
        self.playerIndex = -1
        self.isStrengthened = False
    
    def catch(self, playerIndex):
        self.playerIndex = playerIndex
        self.state = 1
    
    def throw(self, direction, isStrengthened = False):
        self.direction = direction
        self.isStrengthened = isStrengthened
        self.state = 2
        self.speed = shotSpeed
        
    def tickCheck(self):
        if self.state in (0, 2):            
            self.position = [x + y * self.speed for x, y in \
                            zip(self.position, dirConst[self.direction])]
            
            tmpPosition = self.position
            for index, element in enumerate(position):
                if element < gameRangeLower:
                    self.position[index] = gameRangeLower * 2 - element 
                    self.direction = dirBounce[index][self.direction]
                    
                if element > gameRangeUpper:
                    self.position[index] = gameRangeUpper * 2 - element
                    self.direction = dirBounce[index][self.direction]

            tmpScore = self.checkWhoseGoal(self, tmpPosition)
            self.playerIndex = -1
            self.state = 0
            self.isStrengthened = False
            return tmpScore

    def checkWhoseGoal(self, position):
        checkGoal = -1;
        if position[0] < gameRangeLower:
            if goalRangeLower < position[1] < goalRangeUpper:
                checkGoal = 3
            elif position[1] > goalRangeUpper or position[1] < goalRangeLower:
                checkGoal = 4
        elif position[0] > gameRangeUpper:
            if goalRangeLower < position[1] < goalRangeUpper:
                checkGoal = 1                
            elif position[1] > goalRangeUpper or position[1] < goalRangeLower:
                checkGoal = 4
        elif position[1] < gameRangeLower:
            if goalRangeLower < position[0] < goalRangeUpper:
                checkGoal = 0
            elif position[0] > goalRangeUpper or position[0] < goalRangeLower:
                checkGoal = 4
        elif position[1] > gameRangeLower:
            if goalRangeLower < position[0] < goalRangeUpper:
                checkGoal = 2
            elif position[0] > goalRangeUpper or position[0] < goalRangeLower:
                checkGoal = 4

        if checkGoal in (-1, self.playerIndex):
            return 0
        elif checkGoal == 4:
            return scoreOfQuaffles[5]
        elif (checkGoal - self.playerIndex) in (-2, 2):
            return scoreofQuaffles[4]
        else:
            return scoreofQuaffles[3]
                
class Quaffle(OriginalBall):
    def __init__(self, index):
        super(Quaffle, self).__init__(id, index)
        self.speed = quaffleSpeed
        self.ballsize = quaffleSize / 2
        
    def deprive(self, direction):
        self.state = 0
        self.isStrengtheend = False
        self.direction = direction

    def tickCheck(self):
        super(GoldenSnitch, self).tickCheck(self)

class GoldenSnitch(OriginalBall):
    def __init__(self, index):
        super(GoldenSnitch, self).__init__(id, index)    
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
                && fleeDirectionList[0][0] / fleeDirectionList[1][0] < 0)):
            vectorSum[0] = fleeDirectionList[0][1]
            vectorSum[1] = fleeDirectionList[0][0]

        # adjust the magnitude of the vector sum
        scaleFactor = self.speed / ((vectorSum[0] ** 2 + vectorSum[1] ** 2) ** 0.5)
        self.direction[0] = vectorSum[0] * scaleFactor
        self.direction[1] = vectorSum[1] * scaleFactor

        # update position
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]
        self.ballSize = goldenSnitchSize / 2
        
    def deprive(self, direction = 1):
        super(GoldenSnitch, self).deprive(self)
        self.direction = random.randrange(1, 9)

