from Model.const import *

class player(object):
    def __init__(self, name, index):
        # basic data
        self.name = name
        self.index = index
        self.mode = 1
        self.modeTimer = 0
        # 0 = attack
        # 1 = defense
        self.power = 30
        self.powertmp = 0
        self.score = 0
        self.skillcard = None
        self.takeball = -1
        self.IS_AI = False
        self.AI = None

        # move data
        self.position = list(playerInitPos[index])

        #debug part
        if index == 2:
            self.direction = 3
        else:
            self.direction = 0

        #mask data
        self.isMask = False
        self.maskTimer = 0

        #freeze data
        self.isFreeze = False
        self.freezeTimer = 0

        #inVisible data
        self.isVisible = True
        self.invisibleTimer = 0

    def freeze(self, directionIn = 0):

        if self.isFreeze == True and self.freezeTimer < 58:
             self.freezeTimer = freezeTime
        else:
            self.isFreeze = True
            self.freezeTimer = freezeTime
            if self.direction != 0:
                self.direction = ( self.direction + 4 ) % 8
                if self.direction == 0:
                    self.direction = 8
            elif directionIn != 0:
                self.direction = directionIn
            else :
                self.direction = 0
                
                


    def hide(self):
        self.isVisible = False
        self.invisibleTime = invisibleTime

    def setBarrier(self):
        self.power = self.power - barrierPowerCost
        return (self.position, self.direction)

    def shot(self):
        ballIndex = self.takeball
        self.takeball = -1
        return ballIndex

    def changeDirection(self, direction):
        self.direction = direction

    def reSetMask(self):
        self.isMask = False
        self.maskTimer = 0

    def tickCheck(self):
        
        if self.isFreeze == True:
            self.freezeTimer = self.freezeTimer - 1
            if 0 < self.freezeTimer < 58 :
                self.direction = 0
            elif self.freezeTimer == 0:
                self.isFreeze = False

        if self.powertmp < ticktime and self.isFreeze == False:
            self.powertmp = self.powertmp + 1
        elif self.powertmp == ticktime and self.power < powerMax:
            self.powertmp = 0
            self.power = self.power + powerAdd[self.mode]
            if self.power > powerMax:
                self.power = powerMax

        if self.modeTimer > 0:
            self.modeTimer = self.modeTimer - 1

        speedmode = self.mode + self.isFreeze * 1

        if self.position[0] + dirConst[self.direction][0]*playerSpeed[speedmode] < 40 \
            or self.position[0] + dirConst[self.direction][0]*playerSpeed[speedmode]> 700 :
            self.direction = dirBounce[0][self.direction]
        elif self.position[1] + dirConst[self.direction][1]*playerSpeed[speedmode] < 40 \
            or self.position[1] + dirConst[self.direction][1]*playerSpeed[speedmode] > 700 :
            self.direction = dirBounce[1][self.direction]
        else :
            self.position[0] += dirConst[self.direction][0]*playerSpeed[speedmode]
            self.position[1] += dirConst[self.direction][1]*playerSpeed[speedmode]

        if self.isMask == True:
            self.maskTimer = self.maskTimer - 1
            if self.maskTimer <= 0:
                self.isMask = False

        if self.isVisible == False:
            self.invisibleTimer = self.invisibleTimer - 1
            if self.invisibleTimer <= 0:
                self.isVisible = True

         
        

    def bump(self, target):
        outData = []
        if (self.position[0]-target.position[0])**2 + (self.position[1]-target.position[1])**2 <= playerBumpDistance**2:
            selfFreeze = True
            targetFreeze = True

            if self.mode != target.mode:
                if self.mode == 1:
                    selfFreeze = False
                elif target.mode == 1:
                    targetFreeze = False
            selfNowDir = self.direction
            targetNowDir = target.direction

            if selfNowDir == targetNowDir:
                if self.mode > target.mode:
                    selfNowDir = (selfNowDir + 4 )%8
                    if selfNowDir == 0:
                        selfNowDir = 8
                elif self.mode < target.mode:
                    targetNowDir = (targetNowDir + 4 )%8
                    if targetNowDir == 0:
                        targetNowDir = 8
            

            if selfFreeze == True and self.isFreeze == False:
                self.freeze(targetNowDir)   
                if self.takeball != -1:
                    outData.append( (self.takeball, self.direction, self.position) )
                    self.takeball = -1

            if targetFreeze == True and target.isFreeze == False:
                target.freeze(selfNowDir)
                if target.takeball != -1:
                    outData.append( (target.takeball, target.direction, target.position) )
                    target.takeball = -1

        return outData


