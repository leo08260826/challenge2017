from AI.base import *

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []
        
        self.WallConst = [20,110,280,460,630,720]
        self.ContinueAction = False
        self.StartAction = True
        self.holdBall = helper.checkMeHold()
        self.ModeChange = helper.checkMeModeChange()
        self.Dir = helper.getMyDir()
                    
    def CountTwoPointDist(self,pos1,pos2):
        return ((pos2[0]-pos1[0])**2+(pos2[1]-pos1[1])**2)**0.5        

    def IsInRebornArea(self):
        pos = self.helper.getMyPos()
        if pos[0] > 470 or pos[0] < 270 :
            return 0
        if pos[1] > 470 or pos[1] < 270 :
            return 0
        return 1
        
    def IsGoldenTime(self):
        TimeLeft = helper.getTimeLeft()
        if (TimeLeft) > 36:
            return 0
        else:
            return 1
    
    def GetNearestPlayerInfo(self):
        NearestId = self.helper.getNearPlayer()
        Pos = self.helper.getPlayerPos(NearestId[0])
        Mode = self.helper.getPlayerPos(NearestId[0])
        Score = self.helper.getPlayerPos(NearestId[0])
        Dist = self.CountTwoPointDist(helper.getMyPos,Pos)
        Info = []
        Info.append(Pos)
        Info.append(Mode)
        Info.append(Score)
        Info.append(Dist)
        return Info
    
    def decide( self ):
        if not self.IsGoldenTime() :
                        









        else:

    


