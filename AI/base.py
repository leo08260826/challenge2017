"""
const of AI code use.
"""
#action
AI_U  = 1
AI_RU = 2
AI_R  = 3
AI_RD = 4
AI_D  = 5
AI_LD = 6
AI_L  = 7
AI_LU = 8

AI_ATTACK_POWERTHROW = 9
AI_ATTACK_STUN = 10

AI_DEFEND_BARRIER = 9
AI_DEFEND_MASK = 10

AI_THROWBALL = 11
AI_MODECHANGE = 12
AI_SKILLCARD_HIDE = 13
AI_SKILLCARD_DEMENTOR = 14
AI_SKILLCARD_STUNALL = 15
AI_SKILLCARD_SPECIAL = 16

AI_CALLME = 17

#constant
PLAYER_U = 0
PLAYER_R = 1
PLAYER_D = 2
PLAYER_L = 3

BALL_BLUE = 0
BALL_RED  = 1
BALL_GOLD = 2

GOAL_U  = 0
GOAL_R  = 1
GOAL_D  = 2
GOAL_L  = 3
GOAL_RU = 4
GOAL_RD = 5
GOAL_LD = 6
GOAL_LU = 7

ACTION_POWERTHROW = 0
ACTION_STUN = 1
ACTION_BARRIER = 0
ACTION_MASK = 1

DIR_U  = 1
DIR_RU = 2
DIR_R  = 3
DIR_RD = 4
DIR_D  = 5
DIR_LD = 6
DIR_L  = 7
DIR_LU = 8

MODE_ATTACK = 0
MODE_DEFEND = 1

STATE_FREE   = 0
STATE_HOLD   = 1
STATE_FLY    = 2
STATE_REBORN = 3
STATE_GOLD   = 4

HIDE = 0 # invisible
DEMENTOR = 1 # empty power
STUNALL = 2 # stun all enermy
SPECIAL = 3 # SPECIAL

"""
a base of AI.
"""
import Interface.helper as helper
class BaseAI:
    def __init__( self , helper ):
        self.effect = 0
        self.skill = {
            HIDE:0,
            DEMENTOR:0,
            STUNALL:0,
            SPECIAL:0
        }
        self.helper = helper

    def decide( self ):
        pass