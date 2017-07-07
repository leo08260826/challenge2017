from AI.base import *

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []

    def dist(pos1, pos2):
        return ((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2) ** 0.5

    def decide( self ):
        selfPos = self.helper.getMyPos()
        directionList = [0,AI_U, AI_RU, AI_R, AI_RD, AI_D, AI_LD, AI_L, AI_LU]

        nearestGoalId = self.helper.getNearestGoal(selfPos)
        dir2NearestGoal = self.helper.getScoringDir(selfPos)

        if self.helper.getMyMode() == 1 and self.helper.checkMeHold():
            # has ball but in defense mode
            return AI_MODECHANGE
        elif self.helper.checkMeHold() and self.lastDirection == directionList[dir2NearestGoal]:
            return AI_ACTION_1
        elif self.helper.checkMeHold():
            direction = directionList[dir2NearestGoal]
            self.lastDirection = direction
            return direction
        elif self.helper.getMyMode() == 0:
            return AI_MODECHANGE

        action = None


        # head towards a free ball near self
        freeBallPosList = self.helper.getFreeBallPos()
        nearestDist = 180
        nearestBallPos = None
        for freeBallPos in freeBallPosList:
            if TeamAI.dist(freeBallPos, selfPos) <= nearestDist:
                nearestBallPos = freeBallPos
                nearestDist = TeamAI.dist(freeBallPos, selfPos)
       
        if nearestBallPos != None:
            action = directionList[self.helper.getCaptureDir(nearestBallPos)]
        else:
            action = directionList[self.helper.getCaptureDir((370, 370))]

        self.lastDirection = action
        return action


