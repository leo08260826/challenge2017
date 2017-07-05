"""
define Application Programming Interface(API) 
"""
class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.index = index
    
    # map info
    def getCaptureDir(self, pos):
    	self.

    def getScoringDir(self, goal_id):
    	self.
    
    def getNearestGoal(self, pos):
    	self.
    
    def getTimeLeft(self):
    	self.
    
    def isBall(self, pos):
    	self.
    
    def isWall(self, pos):
    	self.
    
    def isPlayer(self, pos):
    	self.
    
    def isBarrier(self, pos):
    	self.
    
    # ball info
    def getFreeBallPos(self):
    	self.

    def getHoldBallPos(self):
    	self.
    	
    def getFlyBallPos(self):
    	self.
    	
    def getGoldBallPos(self):
    	self.
    	
    def getNearBall(self):
    	self.
    	
    def checkBallState(self, pos):
    	self.
    	
    # my info
    def getMyIndex(self):
    	return

	def getMyPos(self):
    	return

    def getMyState(self):
    	return

    def getMyScore(self):
    	return

    def getMyMana(self):
    	return

    def getStunPlayer(self):
    	return

    def getMyCD(self):
    	return

    def checkMeHold(self):
    	return 

    def checkMeStun(self):
    	return

    def checkMeProtected(self):
    	return

    def checkScoring(self, goal_id, dir):
    	return

    def useAction(self, action_id):
    	return

    def checkDir(self, dir):
    	return

    def getInvDir(self, dir):
    	return

    # player info
    def getPlayerPos(self, player_id):
    	return

    def getPlayerState(self, player_id):
    	return

    def getPlayerScore(self, player_id):
    	return

    def getPlayerMana(self, player_id):
    	return

    def getPlayerCD(self, player_id):
    	return

    def checkPlayerHold(self, player_id):
    	return

    def checkPlayerStun(self, player_id):
    	return

    def checkPlayerProtected(self, player_id):
    	return

    def getNearPlayer(self):
    	return

    def getTopPlayer(self):
    	return

    #god
    def askGodDir(self, god_name):

    def askGodPos(self, god_name):

    def callme(self):

    #skillcard
    def SkillHide(self):

    def dkillDementor(slef):

    def skillStunAll(self):
