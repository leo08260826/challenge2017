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
        pass