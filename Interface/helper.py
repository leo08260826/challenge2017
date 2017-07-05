from Model.GameObject.model_const import *
import math
"""
define Application Programming Interface(API) 
"""
class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.index = index

    def CountDist(Pos1,Pos2):
        return (Pos2[0]-Pos1[0])**2+(Pos2[1]-Pos1[1])**2
    def CountTan(Pos1,Pos2):
        return tan(Pos2[1]-Pos1[1]/Pos2[0]-Pos1[0])

    # map info
    def getCaptureDir(self, pos):
    	My_dir=[0,1,2,3,4,5,6,7,8]
        tan=[100,2.414213,0.414213,-0.414213,-2.414213,2.414213,0.414213,-0.414213,-2.414213]
        Pos1 = self.model.players[self.index].position
        Pos2 = pos
        tmpTan = CountTan(Pos1,Pos2)
        if Pos2[0] >= Pos1[0] and Pos2[1] >= Pos1[1]:
            if tmpTan <= tan[1] and tmpTan >= tan[2]:
                return My_dir[2]
            elif tmpTan > tan[1]:
                return My_dir[1]
            elif tmpTan < tan[2]:
                return My_dir[3]
        elif Pos2[0] >= Pos1[0] and Pos2[1] <= Pos1[1]:
            if tmpTan >= tan[3]:
                return My_dir[3]
            elif tmpTan >= tan[4] and tmpTan <= tan[3]:
                return My_dir[4]
            elif tmpTan <= tan[4]:
                return My_dir[5]
        elif Pos2[0] <= Pos1[0] and Pos2[1] <= Pos1[1]:
            if tmpTan >= tan[5]:
                return My_dir[5]
            elif tmpTan >= tan[6] and tmpTan <= tan[5]:
                return My_dir[6]
            elif tmpTan <= tan[6]:
                return My_dir[7]
        elif Pos2[0] <= Pos1[0] and Pos2[1] >= Pos1[1]:
            if tmpTan >= tan[7]:
                return My_dir[7]
            elif tmpTan <= tan[7] and tmpTan >= tan[8]:
                return My_dir[8]:
            elif tmpTan <= tan[8]:
                return My_dir[1]

    def getScoringDir(self, goal_id):
    	self.
    
    def getNearestGoal(self, pos):
    	board = [gameRangeLower,cornerGoalRangeLower,gateRangeLower,gateRangeUpper,cornerGoalRangeUpper,gameRangeUpper]
        gate = [((board[2]+board[3])/2,board[0]),(board[5],(board[2]+board[3])/2),((board[2]+board[3])/2,board[5]),\
                 (board[0],(board[2]+board[3])/2),((board[4]+board[5])/2,(board[0]+board[1])/2),((board[4]+board[5])/2,(board[4]+board[5])/2),\
                 ((board[0]+board[1])/2,(board[4]+board[5])/2),((board[0],board[1])/2,(board[0]+board[1])/2)]
        MinIndex = 0
        Mini = 99999999
        for i in range(8):
            tmp = [gate[i][0],gate[i][1]]
            if (CountDist(tmp,pos) < Mini):
                Mini = CountDist(tmp,pos)
                MinIndex = i
        return MinIndex
        
    def getTimeLeft(self):
    	return self.model.time
 
    # ball info
    def getFreeBallPos(self):
    	Pos_list=[]
        for i in range(numberOfQuaffles):
            if self.model.quaffles[i].state == 0:
                Pos_list.append(self.model.quaffles[i].position)
        return Pos_list

    def getHoldBallPos(self):
    	Pos_list=[]
        for i in range(numberOfQuaffles):
            if self.model.quaffles[i].state == 1:
                Pos_list.append(self.model.players[self.model.quaffles[i].playerIndex].position)
        return Pos_list

    def getFlyBallPos(self):
    	Pos_list=[]
        for i in range(numberOfQuaffles):
            if self.model.quaffles[i].state == 2:
                Pos_list.append(self.model.quaffles[i].position)
    	return Pos_list

    def getGoldBallPos(self):
    	return self.goldenSnitch.position
    	
    def getNearBallInfo(self):
        Info_list=[]
        for i in range(numberOfQuaffles):
            tmp = []
            tmp[0] = self.model.quaffles[i].position[0]
            tmp[1] = self.model.quaffles[i].position[1]
            tmp[2] = self.model.quaffles[i].state
            tmpDist = 99999999
            if tmp[2] == 1:
                tmpDist = CountDist(self.model.players[self.model.quaffles[i].playerIndex].position,self.model.players[self.index].position)
            elif tmp[2] == 0 or tmp[2] == 2:
                tmpDist = CountDist(self.model.quaffles[i].position,self.model.players[self.index].position)
            tmp[3] = tmpDist
        tmp2 = [self.model.goldenSnitch.position[0],self.model.goldenSnitch.position[1],4,CountDist(self.model.goldenSnitch.position,self.model.players[self.index])]
        Info_list.append(tmp2)
        Sort_Info = sorted(Info_list,key=itemgetter(3))
        return Sort_Info 

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
        self.model.evManager.Post(Event_SkillCard(self.index,0))
    def dkillDementor(slef):
        self.model.evManager.Post(Event_SkillCard(self.index,1))
    def skillStunAll(self):
        self.model.evManager.Post(Event_SkillCard(self.index,2))
