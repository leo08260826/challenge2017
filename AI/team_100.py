from AI.base import *
import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []

    def decide( self ):
        if self.getMyState == 1 and self.checkMeHold:
            # has ball but in defense mode
            return AI_MODECHANGE
        elif self.checkMeHold() and self.lastDirection in [DIR_RU, DIR_RD, DIR_LD, DIR_LU]:
            return AI_ACTION_1
        elif self.checkMeHold():
            direction = random.choice([DIR_RU, DIR_RD, DIR_LD, DIR_LU])
            self.lastDirection = direction
            return direction

        directionList = [DIR_U, DIR_RU, DIR_R, DIR_RD, DIR_D, DIR_LD, DIR_L, DIR_LU]
        action = None

        selfPos = helper.getMyPos()

        # head towards a free ball near self
        freeBallPosList = helper.getFreeBallPos()
        nearestDist = 180
        nearestBallPos = None
        for freeBallPos in freeBallList:
            if dist(freeBallPos, selfPos) <= nearestDist:
                nearestBallPos = freeBallPos
                nearestDist = dist(freeBallPos, selfPos)
       
        if nearestBallPos != None:
            action = directionList[helper.getCaptureDir(nearestBallPos)]
        else:
            action = directionList[helper.getCaptureDir(370, 370)]

        self.lastDirection = AI_U
        return AI_U


    def dist(pos1, pos2):
        return ((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2) ** 0.5