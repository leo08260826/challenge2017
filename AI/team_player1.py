from AI.base import BaseAI

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.skill = []
        self.helper = helper

    def decide( self ):
        pass