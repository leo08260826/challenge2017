from AI.base import *

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.effect = EF_NONE
        self.skill = {
            HIDE:0,
            DEMENTOR:0,
            STUNALL:0,
            SPECIAL:0,
        }
        self.helper = helper

    def decide( self ):
        helper = self.helper
        if not helper.checkMeHold():
            if helper.getMyMode() == 0 and helper.checkMeModeChange():
                return AI_MODECHANGE
            fbpos = helper.getFreeBallPos()
            if bool(fbpos):
                return helper.getCaptureDir(fbpos[0])
        else:
            if helper.getMyMode() == 1 and helper.checkMeModeChange():
                return AI_MODECHANGE

            goal = helper.getNearGoal(helper.getMyPos())
            if goal[0] == helper.getMyIndex():
                shotGoal = goal[1]
            else:
                shotGoal = goal[0]

            for i in range(1,9):
                if helper.checkScoring(shotGoal,i):
                    if helper.getMyDir() == i:
                        return AI_THROWBALL
                    else:
                        return i
            ToNextDir = helper.getScoringDir(shotGoal)
            return ToNextDir