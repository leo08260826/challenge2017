from AI.base import *
from random import randint

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = [0,1,2]

    def decide( self ):
        a = randint(1,100)
        if a%10:
            return 16
