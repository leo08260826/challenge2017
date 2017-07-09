from Model.const import *
from math import sqrt
from operator import itemgetter
import random
"""
define Application Programming Interface(API) 
"""
class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.index = index

    # helper function
    def CountDist(self, Pos1, Pos2):
        return ((Pos2[0]-Pos1[0])**2 + (Pos2[1]-Pos1[1])**2)

    def CountTan(self, Pos1, Pos2):
        if Pos2[0] == Pos1[0]:
            if Pos2[1] > Pos1[1]:
                return 999
            else:
                return -999
        return ((Pos2[1]-Pos1[1]) / (Pos2[0]-Pos1[0]))

    def CountDistToLine(self, pos, CoeffX, CoeffY, Cons, Multier):
        X = pos[0]
        Y = pos[1]
        ans = (CoeffX*X + CoeffY*Y + Cons) * Multier
        return ans

    # map info
    def getCaptureDir(self, pos):
        My_dir=[0,1,2,3,4,5,6,7,8]
        My_tan=[100,2.414213,0.414213,-0.414213,-2.414213,2.414213,0.414213,-0.414213,-2.414213]
        Pos1 = self.model.players[self.index].position
        Pos2 = pos
        tmpTan = self.CountTan(Pos1,Pos2)
        if Pos2[0] >= Pos1[0] and Pos2[1] >= Pos1[1]:
            if tmpTan >= My_tan[1]:
                return My_dir[5]
            elif tmpTan < My_tan[1] and tmpTan >= My_tan[2]:
                return My_dir[4]
            elif tmpTan < My_tan[2]:
                return My_dir[3]
        elif Pos2[0] >= Pos1[0] and Pos2[1] < Pos1[1]:
            if tmpTan >= My_tan[3]:
                return My_dir[3]
            elif tmpTan >= My_tan[4] and tmpTan < My_tan[3]:
                return My_dir[2]
            elif tmpTan < My_tan[4]:
                return My_dir[1]
        elif Pos2[0] < Pos1[0] and Pos2[1] < Pos1[1]:
            if tmpTan >= My_tan[5]:
                return My_dir[1]
            elif tmpTan >= My_tan[6] and tmpTan < My_tan[5]:
                return My_dir[8]
            elif tmpTan < My_tan[6]:
                return My_dir[7]
        elif Pos2[0] < Pos1[0] and Pos2[1] >= Pos1[1]:
            if tmpTan >= My_tan[7]:
                return My_dir[7]
            elif tmpTan < My_tan[7] and tmpTan >= My_tan[8]:
                return My_dir[6]
            elif tmpTan < My_tan[8]:
                return My_dir[5]

    def getScoringDir(self, goal_id):
        x = sqrt(2)
        CoeffX=[9999,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0]
        CoeffY=[9999,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,1,1,1,1]
        Cons=[9999,130,300,480,650,830,1000,1180,1350,610,440,260,90,-90,-260,-440,-610,110,280,460,630,110,280,460,630]
        Multier=[9999,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,1,1,1,1,1,1,1,1]
        lineToGoal=[[2,3,10,11,18,19],[6,7,10,11,22,23],[6,7,14,15,18,19],[2,3,14,15,22,23],[4,5,9,20,21],[8,12,13,20,24],[4,5,16,17,24],[1,12,13,17,21]]

        for i in range(8):
            if (self.checkScoring(goal_id,i)) == True:
                return i

        # for i in range(len(lineToGoal)):
            # if (goal_id == i):
        i = goal_id
        MinIndex = 0
        Mini = 99999999
        for j in range(len(lineToGoal[i])):
            tmp = self.CountDistToLine(self.getMyPos(),CoeffX[lineToGoal[i][j]],CoeffY[lineToGoal[i][j]],-1*Cons[lineToGoal[i][j]],Multier[lineToGoal[i][j]])    
            if abs(tmp) < Mini:
                MinIndex = lineToGoal[i][j]
                Mini = tmp
                if tmp<0:
                    Switchdir = 1
                else:
                    Switchdir = 0

        origin = [CoeffX[MinIndex],CoeffY[MinIndex]]
        if origin[0] == 0 :
            if Switchdir == 1 :
                return 5
            elif Switchdir == 0 :
                return 1
        elif origin[1] == 0:
            if Switchdir == 1 :
                return 3
            elif Switchdir == 0 :
                return 7
        elif origin[0] == 1 and origin[1] == 1 :
            if Switchdir == 1:
                return 4
            elif Switchdir == 0:
                return 8
        elif origin[0] == 1 and origin[0] == -1 :
            if Switchdir == 1:
                return 2
            elif Switchdir == 0:
                return 6

    def getNearestGoal(self, pos):
        board = [gameRangeLower,cornerGoalRangeLower,goalRangeLower,goalRangeUpper,cornerGoalRangeUpper,gameRangeUpper]
        gate = [
            ((board[2]+board[3])/2,board[0]),
            (board[5],(board[2]+board[3])/2),
            ((board[2]+board[3])/2,board[5]),
            (board[0],(board[2]+board[3])/2),
            ((board[4]+board[5])/2,(board[0]+board[1])/2),
            ((board[4]+board[5])/2,(board[4]+board[5])/2),
            ((board[0]+board[1])/2,(board[4]+board[5])/2),
            ((board[0]+board[1])/2,(board[0]+board[1])/2)
        ]
        
        AllGoal = []
        for i in range(8):
            tmp = [gate[i][0],gate[i][1]]
            tmpDist = self.CountDist(tmp,pos)
            index = i
            AllGoal.append((tmpDist,index))
        SortAllGoal = sorted(AllGoal,key=itemgetter(0))

        IndexList = []    
        for i in range(8):
            IndexList.append(SortAllGoal[i][1])
        return IndexList
        
    def getTimeLeft(self):
        return self.model.timer
 
    # ball info
    def getBallPos(self, index):
        if self.model.quaffles[index].state == 1:
            return tuple(self.model.players[self.model.quaffles[index].playerIndex].position)
        else:
            return tuple(self.model.quaffles[index].position)

    def getBallDir(self, index):
        return self.model.quaffles[index].direction

    def getBallState(self, index):
        return self.model.quaffles[index].state

    def getBallPlayer(self, index):
        if self.model.quaffles[index].playerIndex == -1:
            return None
        else:
            return self.model.quaffles[index].playerIndex

    def checkBallPower(self, index):
        return self.model.quaffles[index].isStrengthened

    def getGoldPos(slef):
        return tuple(self.model.goldenSnitch.position)

    def getGoldDir(slef):
        return tuple(self.model.goldenSnitch.direction)

    def getFreeBallPos(self):
        Pos_list=[]
        for i in range(numberOfQuaffles):
            if self.model.quaffles[i].state == 0:
                Pos_list.append(tuple(self.model.quaffles[i].position))
        return Pos_list

    def getHoldBallPos(self):
        Pos_list=[]
        for i in range(numberOfQuaffles):
            if self.model.quaffles[i].state == 1:
                Pos_list.append(tuple(self.model.players[self.model.quaffles[i].playerIndex].position))
        return Pos_list

    def getFlyBallPos(self):
        Pos_list=[]
        for i in range(numberOfQuaffles):
            if self.model.quaffles[i].state == 2:
                Pos_list.append(tuple(self.model.quaffles[i].position))
        return Pos_list

    def getGoldBallPos(self):
        return tuple(self.model.goldenSnitch.position)
        
    def getNearBallInfo(self):
        Info_list=[]
        for i in range(numberOfQuaffles):
            tmp = [0,0,0,0]
            tmp[0] = self.model.quaffles[i].position[0]
            tmp[1] = self.model.quaffles[i].position[1]
            tmp[2] = self.model.quaffles[i].state
            tmpDist = 99999999
            if tmp[2] == 1:
                tmpDist = self.CountDist(self.model.players[self.model.quaffles[i].playerIndex].position, self.model.players[self.index].position)
            elif tmp[2] == 0 or tmp[2] == 2:
                tmpDist = self.CountDist(self.model.quaffles[i].position, self.model.players[self.index].position)
            tmp[3] = tmpDist
            Info_list.append(tmp)
        tmp2 = [self.model.goldenSnitch.position[0],
                self.model.goldenSnitch.position[1],
                4,
                self.CountDist(self.model.goldenSnitch.position, self.model.players[self.index].position)]
        Info_list.append(tmp2)
        Sort_Info = sorted(Info_list,key=itemgetter(3))
        return Sort_Info 

    # my info
    def getMyIndex(self):
        return self.index

    def getMyPos(self):
        return tuple(self.model.players[self.index].position)

    def getMyDir(self):
        return self.model.players[self.index].direction

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
                myPos = self.getMyPos()
                if self.CountDist(myPos, tmpPos) < (stunDistance ** 2) and self.model.players[i].isVisible == True:
                    result.append(i)
        return result

    def checkMeModeChange(self):
        return (self.model.players[self.index].power >= modeChangePower)

    def checkMeHold(self):
        return self.model.players[self.index].takeball > -1

    def checkMeStun(self):
        return self.model.players[self.index].isFreeze

    def checkMeProtected(self):
        return self.model.players[self.index].isMask

    def checkScoring(self, goal_id, myDir):
        myPos = list(self.getMyPos())
        if myDir == 1:#DIR_U
            myPos[1] = gameRangeLower - 1
        elif myDir == 2:#DIR_RU
            if (gameRangeUpper - myPos[0]) > (myPos[1] - gameRangeLower):
                tmp = myPos[1] - gameRangeLower + 1
            else:
                tmp = gameRangeUpper - myPos[0] + 1
            myPos[0] = myPos[0] + tmp
            myPos[1] = myPos[1] - tmp
        elif myDir == 3:#DIR_R
            myPos[0] = gameRangeUpper + 1
        elif myDir == 4:#DIR_RD
            if (gameRangeUpper - myPos[0]) > (gameRangeUpper - myPos[1]):
                tmp = gameRangeUpper - myPos[1] + 1
            else:
                tmp = gameRangeUpper - myPos[0] + 1
            myPos[0] = myPos[0] + tmp
            myPos[1] = myPos[1] + tmp
        elif myDir == 5:#DIR_D
            myPos[1] = gameRangeUpper + 1
        elif myDir == 6:#DIR_LD
            if (myPos[0] - gameRangeLower) > (gameRangeUpper - myPos[1]):
                tmp = gameRangeUpper - myPos[1] + 1
            else:
                tmp = myPos[0] - gameRangeLower + 1
            myPos[0] = myPos[0] - tmp
            myPos[1] = myPos[1] + tmp
        elif myDir == 7:#DIR_L
            myPos[0] = gameRangeLower - 1
        elif myDir == 8:#DIR_LU
            if (myPos[0] - gameRangeLower) > (myPos[1] - gameRangeLower):
                tmp = myPos[1] - gameRangeLower + 1
            else:
                tmp = myPos[0] - gameRangeLower + 1
            myPos[0] = myPos[0] - tmp
            myPos[1] = myPos[1] - tmp

        barrier = list(self.model.barriers)
        if goal_id == self.model.quaffles[0].checkWhoseGoal(myPos,barrier):
            return True
        else:
            return False

    def checkUseAction(self, action_id):
        myMode = self.getMyMode()
        myMana = self.getMyMana()
        if myMode == 0:
            if action_id == 0 and myMana >= powerShotPowerCost:
                return True
            elif action_id == 1 and myMana >= stunPowerCost:
                return True
            elif action_id == 2:
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

    def checkHitWall(self, myDir):
        speedmode = self.model.players[self.index].mode + self.model.players[self.index].isFreeze * 1
        if self.model.players[self.index].position[0] + dirConst[myDir][0]*playerSpeed[speedmode] < 40 \
            or self.model.players[self.index].position[0] + dirConst[myDir][0]*playerSpeed[speedmode]> 700 :
            return True
        elif self.model.players[self.index].position[1] + dirConst[myDir][1]*playerSpeed[speedmode] < 40 \
            or self.model.players[self.index].position[1] + dirConst[myDir][1]*playerSpeed[speedmode] > 700 :
            return True
        else :
            return False

    def getInvDir(self, myDir):
        if myDir < 5:
            return myDir+4
        else:
            return myDir-4

    # player info
    def getPlayerPos(self, player_id):
        if self.model.players[player_id].isVisible == True:
            return tuple(self.model.players[player_id].position)
        else:
            return None

    def getPlayerDir(self, player_id):
        if self.model.players[player_id].isVisible == True:
            return self.model.players[player_id].direction
        else:
            return None

    def getPlayerMode(self, player_id):
        if self.model.players[player_id].isVisible == True:
            return self.model.players[player_id].mode
        else:
            return None

    def getPlayerScore(self, player_id):
        if self.model.players[player_id].isVisible == True:
            return self.model.players[player_id].score
        else:
            return None

    def getPlayerMana(self, player_id):
        if self.model.players[player_id].isVisible == True:
            return self.model.players[player_id].power
        else:
            return None

    def checkPlayerModeChange(self, player_id):
        if self.model.players[player_id].isVisible == True:
            return (self.model.players[player_id].power > modeChangePower)
        else:
            return None

    def checkPlayerHold(self, player_id):
        if self.model.players[player_id].isVisible == True:
            return self.model.players[player_id].takeball > -1
        else:
            return None

    def checkPlayerStun(self, player_id):
        if self.model.players[player_id].isVisible == True:
            return self.model.players[player_id].isFreeze
        else:
            return None

    def checkPlayerProtected(self, player_id):
        if self.model.players[player_id].isVisible == True:
            return self.model.players[player_id].isMask
        else:
            return None

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
        return random.randrange(1, 9)

    def askGodPos(self, god_name):
        return [random.randrange(40, 700), random.randrange(40, 700)]