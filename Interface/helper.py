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
    	return self.model.timer
     
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
        self.model.evManager.Post(Event_SkillCard(self.index,0))
    def dkillDementor(slef):
        self.model.evManager.Post(Event_SkillCard(self.index,1))
    def skillStunAll(self):
        self.model.evManager.Post(Event_SkillCard(self.index,2))
