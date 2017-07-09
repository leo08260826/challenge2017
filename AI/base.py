"""
const of AI code use.
"""
AI_U  = 1
AI_RU = 2
AI_R  = 3
AI_RD = 4
AI_D  = 5
AI_LD = 6
AI_L  = 7
AI_LU = 8

AI_ACTION_1 = 9
AI_ACTION_2 = 10
AI_ACTION_3 = 11

AI_MODECHANGE = 12
AI_SKILLCARD_1 = 13
AI_SKILLCARD_2 = 14
AI_SKILLCARD_3 = 15

HIDE = 0 # invisible
DEMENTOR = 1 # empty power
STUNALL = 2 # stun all enermy


"""
a base of AI.
"""
import Interface.helper as helper
class BaseAI:
    def __init__( self , helper ):
        self.skill = []
        self.helper = helper

    def decide( self ):
        pass
