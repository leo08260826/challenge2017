import random
import Model.const as mc

class OriginalBall(object):
    def __init__(self, index):
        self.index = index
        self.position = [random.randrange(mc.ballRandomLower, mc.ballRandomUpper),\
                         random.randrange(mc.ballRandomLower, mc.ballRandomUpper)]
        """
        0: belongs to nobody
        1: belongs to somebody
        2: being thrown
        3: waiting to re-appear
        """
        self.state = 0
        # 1~8: eight directions
        self.direction = random.randrange(1, 9)
        self.playerIndex = -1
        self.tickTime = -1
        self.isStrengthened = False
        self.hasCaught = []
        self.hasPassed = [[False] * 4 for _ in range(4)]

    def throw(self, direction, position, isStrengthened = False):
        # invalid request prevention
        if self.state != 1:
            return
        if direction == 0:
            self.direction = 5
        else:
            self.direction = direction
        self.isStrengthened = isStrengthened
        self.state = 2
        self.speed = mc.shotSpeed
        # add a safe distance to avoid re-catch the ball after shooting
        self.position[0] = position[0] + mc.dirConst[self.direction][0] * 35
        self.position[1] = position[1] + mc.dirConst[self.direction][1] * 35

    def modifyPosition(self):
        for index, element in enumerate(self.position):
            if element < mc.gameRangeLower:
                self.position[index] = mc.gameRangeLower * 2 - element
                self.direction = mc.dirBounce[index][self.direction]
            if element > mc.gameRangeUpper:
                self.position[index] = mc.gameRangeUpper * 2 - element
                self.direction = mc.dirBounce[index][self.direction]

    def tickCheck(self):
        pass

    def checkWhoseGoal(self, position, barriers):
        checkGoal = mc.reachNothing
        if position[0] < mc.gameRangeLower:
            if mc.goalRangeLower < position[1] < mc.goalRangeUpper:
                checkGoal = 3
            elif position[1] > mc.cornerGoalRangeUpper:
                checkGoal = 6
            elif position[1] < mc.cornerGoalRangeLower:
                checkGoal = 7
            else:
                checkGoal = mc.reachWall
        elif position[0] > mc.gameRangeUpper:
            if mc.goalRangeLower < position[1] < mc.goalRangeUpper:
                checkGoal = 1
            elif position[1] > mc.cornerGoalRangeUpper:
                checkGoal = 5
            elif position[1] < mc.cornerGoalRangeLower:
                checkGoal = 4
            else:
                checkGoal = mc.reachWall
        elif position[1] < mc.gameRangeLower:
            if mc.goalRangeLower < position[0] < mc.goalRangeUpper:
                checkGoal = 0
            elif position[0] > mc.cornerGoalRangeUpper:
                checkGoal = 4
            elif position[0] < mc.cornerGoalRangeLower:
                checkGoal = 7
            else:
                checkGoal = mc.reachWall
        elif position[1] > mc.gameRangeUpper:
            if mc.goalRangeLower < position[0] < mc.goalRangeUpper:
                checkGoal = 2
            elif position[0] > mc.cornerGoalRangeUpper:
                checkGoal = 5
            elif position[0] < mc.cornerGoalRangeLower:
                checkGoal = 6
            else:
                checkGoal = mc.reachWall
        if not self.isStrengthened:
            for barrier in barriers:
                if checkGoal == barrier.playerIndex:
                    checkGoal = mc.reachWall
                    break
        return checkGoal

class Quaffle(OriginalBall):
    def __init__(self, index):
        super(Quaffle, self).__init__(index)
        self.speed = mc.quaffleSpeed
        self.ballsize = mc.quaffleSize / 2

    def catch(self, playerIndex):
        prevPlayerIndex = self.playerIndex
        prevState = self.state
        self.playerIndex = playerIndex
        self.state = 1
        self.isStrengthened = False

        if prevPlayerIndex == -1 and prevState == 0:
            if playerIndex in self.hasCaught:
                return True
            else:
                self.hasCaught.append(playerIndex)
                return False
        elif prevPlayerIndex != -1 and prevState == 2:
            if self.hasPassed[prevPlayerIndex][playerIndex]:
                return True
            else:
                self.hasPassed[prevPlayerIndex][playerIndex] = True
                return False
        else:
            assert False, "Model's Ball Bug"


    def deprive(self, direction, position):
        self.state = 0
        self.playerIndex = -1
        self.isStrengthened = False
        if direction == 0:
            self.direction = 5
        else:
            self.direction = direction
        self.speed = mc.depriveSpeed
        self.position[0] = position[0] + mc.dirConst[direction][0] * 35
        self.position[1] = position[1] + mc.dirConst[direction][1] * 35

    def tickCheck(self, barriers):
        tmpScore = 0
        tmpPlayerIndex = self.playerIndex
        checkGoal = -1
        if self.state in (0, 2):

            self.position[0] += mc.dirConst[self.direction][0] * self.speed
            self.position[1] += mc.dirConst[self.direction][1] * self.speed
            checkGoal = self.checkWhoseGoal(self.position, barriers)


            if checkGoal != mc.reachNothing:
                self.playerIndex = -1
                self.state = 0
                self.isStrengthened = False
                self.speed = mc.quaffleSpeed
                if checkGoal == tmpPlayerIndex:
                    tmpScore = 0
                elif checkGoal in (4, 5, 6, 7):
                    tmpScore = mc.scoreOfQuaffles[5]
                elif (checkGoal - tmpPlayerIndex) in (-2, 2):
                    tmpScore = mc.scoreOfQuaffles[4]
                elif checkGoal == mc.reachWall:
                    tmpScore = 0
                else:
                    tmpScore = mc.scoreOfQuaffles[3]

                if checkGoal == mc.reachWall:
                    self.modifyPosition()
                else:
                    self.hasCaught = []
                    self.hasPassed = [[False] * 4 for _ in range(4)]
                    self.tickTime = 60
                    self.state = 3
                    self.position = [-1, -1]
                    self.direction = random.randrange(1, 9)
        elif self.state == 3:
            if self.tickTime > 0:
                self.tickTime -= 1
            elif self.tickTime <= 0:
                self.state = 0
                self.position = [random.randrange(mc.ballRandomLower, mc.ballRandomUpper),\
                                 random.randrange(mc.ballRandomLower, mc.ballRandomUpper)]
                self.tickTime = -1
        return (tmpScore, tmpPlayerIndex, mc.scoreOfQuaffles[1], checkGoal)

class GoldenSnitch(OriginalBall):
    def __init__(self, index):
        super(GoldenSnitch, self).__init__(index)
        self.speed = mc.goldenSnitchSpeed
        self.direction = [random.randrange(1,5), random.randrange(1,5)]
        self.ballSize = mc.goldenSnitchSize / 2

    def modifyPosition(self):
        for index, element in enumerate(self.position):
            if element < mc.gameRangeLower:
                self.position[index] = mc.gameRangeLower * 2 - element
                self.direction[index] *= -1
            if element > mc.gameRangeUpper:
                self.position[index] = mc.gameRangeUpper * 2 - element
                self.direction[index] *= -1

    def isInWall(self, pos):
        for element in pos:
            if element < mc.gameRangeLower or element > mc.gameRangeUpper:
                return True

        return False

    def decaySpeed(self):
        self.speed -= mc.goldenSnitchSpeedDecayPerSec

    # multiply 2 matrix. Works only when matrix1 is 2*2 and matrix2 is 2*1
    def multiply(matrix1, matrix2):
        answer = [0, 0]
        answer[0] = matrix1[0][0] * matrix2[0] + matrix1[0][1] * matrix2[1]
        answer[1] = matrix1[1][0] * matrix2[0] + matrix1[1][1] * matrix2[1]
        return answer


    # calculates the alert score of golden snitch. A high alert score means that the golden snitch is in trouble.
    def calculateAlertScore(self, players, newGoldenSnitchPos):
        alertScore = 0
        for player in players:
            distance = ((player.position[0] - newGoldenSnitchPos[0])**2 + (player.position[1] - newGoldenSnitchPos[1])**2) ** 0.5
            if (distance <= mc.goldenSnitchAlertRadius):
                alertScore += 100000 / (distance**2)

        return alertScore


    def tickCheck(self, players):
        fleeDirectionList = []
        nearestPlayerDist = 10000
        nearestPlayerIndex = None
        for index, player in enumerate(players):
            distance = ((player.position[0] - self.position[0])**2 + (player.position[1] - self.position[1])**2) ** 0.5
            if (distance <= mc.goldenSnitchAlertRadius):
                fleeDirectionList.append((self.position[0] - player.position[0], self.position[1] - player.position[1]))
            if distance < nearestPlayerDist:
                nearestPlayerDist = distance
                nearestPlayerIndex = index

        # if there's no need to flee, don't change the direction. Move with half speed
        if not fleeDirectionList:
            # scale to half speed
            scaleFactor = (self.speed /2) / ((self.direction[0] ** 2 + self.direction[1] ** 2) ** 0.5)
            self.direction[0] *= scaleFactor
            self.direction[1] *= scaleFactor

            self.position = [x + y * 0.5 for x, y in zip(self.position, self.direction)]
            self.modifyPosition()
            return

        # scale direction to flee speed

        # if only 1 player is in the alert radius
        elif len(fleeDirectionList) == 1:
            self.direction = list(fleeDirectionList[0])
            # adjust the magnitude of the vector sum
            scaleFactor = self.speed / ((self.direction[0] ** 2 + self.direction[1] ** 2) ** 0.5)
            self.direction[0] *= scaleFactor
            self.direction[1] *= scaleFactor

        # if more than 1 player is threatening golden snitch, try 8 directions and find the min of the
        # evaluation function.
        elif len(fleeDirectionList) >= 2:
            # adjust the magnitude of the vector sum
            scaleFactor = self.speed / ((self.direction[0] ** 2 + self.direction[1] ** 2) ** 0.5)
            self.direction[0] *= scaleFactor
            self.direction[1] *= scaleFactor

            newDirection = self.direction
            bestDirection = self.direction
            lowestAlertScore = 9999999

            for i in range(8):
                rotationMatrix45Deg = [[0.7071, -0.7071], [0.7071, 0.7071]];
                newDirection = GoldenSnitch.multiply(rotationMatrix45Deg, newDirection)
                newPos = []
                for k in range(2):
                    newPos.append(self.position[k] + newDirection[k])
                
                newAlertScore = self.calculateAlertScore(players, newPos)
                if (newAlertScore < lowestAlertScore):
                    bestDirection = newDirection
                    lowestAlertScore = newAlertScore

            self.direction = bestDirection


        pendingPosition = [self.position[0] + self.direction[0], self.position[1] + self.direction[1]]

        # check if pendingPos is in wall
        if (self.isInWall(pendingPosition)):
            # if still in wall, rotate direction +90 degree, and check if it is moving away from the nearest threat
            pendingDirection = [None, None]
            pendingDirection[0] , pendingDirection[1] = self.direction[1], self.direction[0]
            pendingPosition = [self.position[0] + pendingDirection[0], self.position[1] + pendingDirection[1]]

            if (nearestPlayerDist ** 2 >\
                 (players[nearestPlayerIndex].position[0] - pendingPosition[0]) ** 2\
              + (players[nearestPlayerIndex].position[1] - pendingPosition[1]) ** 2):
                # if rotating +90 degree is not moving away from threat, rotate -90 degree instead
                pendingDirection[0] *= -1
                pendingDirection[1] *= -1

            self.direction[0], self.direction[1] = pendingDirection[0], pendingDirection[1]

        # update position
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]

        self.modifyPosition()
