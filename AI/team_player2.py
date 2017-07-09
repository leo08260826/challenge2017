from AI.base import *
import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = [0]

    def decide( self ):
        h = self.helper
        if not h.checkMeHold():
            if h.getMyMode() == 0 and h.checkMeModeChange():
                return AI_MODECHANGE
            bpos = h.getFreeBallPos()
            if bool(bpos):
                return h.getCaptureDir(bpos[0])
        else:
            if h.getMyMode() == 1 and h.checkMeModeChange():
                return AI_MODECHANGE
            g = h.getNearestGoal(h.getMyPos())
            for i in range(0,8):
                if h.checkScoring(g,i):
                    if h.getMyDir() == i:
                        return AI_ACTION_3
                    else:
                        return i
            a = h.getScoringDir(i)
            return a