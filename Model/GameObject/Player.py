from Model.GameObject.model_const import *
class player(object):
    def __init__(self, name, index, AI = None):
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
        if AI == None:
        	self.is_AI = False
        else:
        	self.is_AI = True

        self.AI = AI

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

        #invisible data
        self.isVisible = True
        self.invisibleTime = 0

    def freeze(self):

        if self.isFreeze == True and self.freezeTimer < 58:
            self.freezeTimer = freezeTime
        else:
            self.isFreeze = True
            self.freezeTimer = freezeTime
            if self.direction != 0:
                self.direction == (self.direction+4)%8
                if self.direction == 0:
                    self.direction = 8


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
            if self.freezeTimer < 58 and self.freezeTimer > 0:
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

        if self.position[0] + dirConst[self.direction][0]*playerSpeed[speedmode] < 47 \
            or self.position[0] + dirConst[self.direction][0]*playerSpeed[speedmode]> 693 :
            self.direction = dirBounce[0][self.direction]
        elif self.position[1] + dirConst[self.direction][1]*playerSpeed[speedmode] < 47 \
            or self.position[1] + dirConst[self.direction][1]*playerSpeed[speedmode] > 693 :
            self.direction = dirBounce[1][self.direction]

        if self.isMask == True:
            self.maskTimer = self.maskTimer - 1
            if self.maskTimer <= 0:
                self.isMask = False

         
        self.position[0] += dirConst[self.direction][0]*playerSpeed[speedmode]
        self.position[1] += dirConst[self.direction][1]*playerSpeed[speedmode]

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

            if selfFreeze == True:
                self.freeze()   
                if self.takeball != -1:
                    outData.append( (self.takeball, self.direction, self.position) )
                    self.takeball = -1

            if targetFreeze == True:
                target.freeze()
                if target.takeball != -1:
                    outData.append( (target.takeball, target.direction, target.position) )
                    target.takeball = -1

        return outData


