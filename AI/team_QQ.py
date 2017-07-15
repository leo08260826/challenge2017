from AI.base import *

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.effect = EF_LOVE
        self.skill = {
            HIDE:1,
            DEMENTOR:1,
            STUNALL:1,
            SPECIAL:1,
        }
        self.helper = helper

    def decide( self ):
        return AI_SKILLCARD_STUNALL