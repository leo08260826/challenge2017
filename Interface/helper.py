from Model.GameObject.model_const import *
import math
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
    	return self.index

	def getMyPos(self):
    	return self.model.players[self.index].position

    def getMyMode(self):
    	return self.model.players[self.index].mode

    def getMyScore(self):
    	return self.model.players[self.index].score

    def getMyMana(self):
    	return self.model.players[self.index].power

    def getStunPlayer(self):
    	result = []
    	for i in range(PlayerNum):
    		if i != self.index:
    			tmpPos = self.model.players[i].position
    			if self.CountDist(myPos, tmpPos) < stunDistance ** 2 and self.checkPlayerProtected(i) == False:
    				result.append(i)
    	return result

    def getMyCD(self):
    	return self.model.players[self.index].modeTimer

    def checkMeHold(self):
    	return self.model.players[self.index].takeball > -1

    def checkMeStun(self):
    	return self.model.players[self.index].isFreeze

    def checkMeProtected(self):
    	return self.model.players[self.index].isMask

    def checkScoring(self, goal_id, dir):
    	myPos = self.getMyPos()
    	if dir == 1:#DIR_U
    		myPos[1] = gameRangeLower - 1
    	elif dir == 2:#DIR_RU
    		if (gameRangeUpper - myPos[0]) > (myPos[1] - gameRangeLower):
    			tmp = myPos[1] - gameRangeLower + 1
    		else:
    			tmp = gameRangeUpper - myPos[0] + 1
    		myPos[0] = myPos[0] + tmp
    		myPos[1] = myPos[1] - tmp
    	elif dir == 3:#DIR_R
    		myPos[0] = gameRangeUpper + 1
    	elif dir == 4:#DIR_RD
    		if (gameRangeUpper - myPos[0]) > (gameRangeUpper - myPos[1]):
    			tmp = gameRangeUpper - myPos[1] + 1
    		else:
    			tmp = gameRangeUpper - myPos[0] + 1
    		myPos[0] = myPos[0] + tmp
    		myPos[1] = myPos[1] + tmp
    	elif dir == 5:#DIR_D
    		myPos[1] = gameRangeUpper + 1
    	elif dir == 6:#DIR_LD
    		if (myPos[0] - gameRangeLower) > (gameRangeUpper - myPos[1]):
    			tmp = gameRangeUpper - myPos[1] + 1
    		else:
    			tmp = myPos[0] - gameRangeLower + 1
    		myPos[0] = myPos[0] - tmp
    		myPos[1] = myPos[1] + tmp
    	elif dir == 7:#DIR_L
    		myPos[0] = gameRangeLower - 1
    	elif dir == 8:#DIR_LU
    		if (myPos[0] - gameRangeLower) > (myPos[1] - gameRangeLower):
    			tmp = myPos[1] - gameRangeLower + 1
    		else:
    			tmp = myPos[0] - gameRangeLower + 1
    		myPos[0] = myPos[0] - tmp
    		myPos[1] = myPos[1] - tmp

    	if goal_id == self.model.quaffles[0].checkWhoseGoal(myPos):
    		return True
    	else:
    		return False

    def useAction(self, action_id):
    	myMode = self.getMyMode()
    	myMana = self.getMyMana()
    	if myMode == 0:
    		if action_id == 0 and myMana >= powerShotPowerCost:
    			return True
    		elif action_id == 1 and myMana >= stunPowerCost:
    			return True
    		else:
    			return False
    	elif myMode == 1:
    		if action_id == 0 and myMana >= barrierPowerCost:
    			return True
    		elif action_id == 1 and myMana >= maskPowerCost:
    			return True
    		else:
    			return False
    	else:
    		return False

    def checkDir(self, dir):
    	pass

    def getInvDir(self, dir):
    	if dir < 5:
    		return dir+4
    	else:
    		return dir-4


    # player info
    def getPlayerPos(self, player_id):
    	return self.model.players[player_id].position

    def getPlayerState(self, player_id):
    	return self.model.players[player_id].mode

    def getPlayerScore(self, player_id):
    	return self.model.players[player_id].score

    def getPlayerMana(self, player_id):
    	return self.model.players[player_id].power

    def getPlayerCD(self, player_id):
    	return self.model.players[player_id].modeTimer

    def checkPlayerHold(self, player_id):
    	return self.model.players[player_id].takeball > -1

    def checkPlayerStun(self, player_id):
    	return self.model.players[player_id].isFreeze

    def checkPlayerProtected(self, player_id):
    	return self.model.players[player_id].isMask

    def getNearPlayer(self):
    	myPos = self.model.players[self.index].position
    	dist = []
    	for i in range(PlayerNum):
    		if i != self.index:
    			tmpPos = self.model.players[i].position
    			dist.append([self.CountDist(myPos, tmpPos), i])
    	sort_dist = sorted(dist, key=itemgetter(0))

    	result = []
    	for i in range(PlayerNum-1):
    		result.append(sort_dist[i][1])
    	return result

    def getTopPlayer(self):
    	rank = []
    	for i in range(PlayerNum):
    		if i != self.index:
    			tmpScore = self.model.players[i].score
    			rank.append([tmpScore, i])
    	sort_rank = sorted(rank, key=itemgetter(0), reverse=True)
    	
    	result = []
    	for i in range(PlayerNum-1):
    		result.append(sort_rank[i][1])
    	return result

    #god
    def askGodDir(self, god_name):

    def askGodPos(self, god_name):

    def callme(self):

    #skillcard
    def SkillHide(self):

    def dkillDementor(slef):

    def skillStunAll(self):
