#ball const
ballRandomLower = 270
ballRandomUpper = 470
numberOfQuaffles = 2
quaffleSize = 35
scoreOfQuaffles = [1,0,4,8,12,16]
distToCatchQuaffle = 30 

#speed
quaffleSpeed = 3
goldenSnitchSpeed = 8
playerSpeed = 4
shotSpeed = 5
depriveSpeed = 5

#view const
gameRange = 700
gameRangeLower = 20
gameRangeUpper = gameRangeLower + gameRange

#player const
playerInitPos = [[370,70],[670,370],[370,670],[70,370]]
powerMax = 100
freezeTime = 60
playerBumpDistance = 25
barrierPowerCost = 18
PlayerNum = 4
MaxManualPlayer = 2
playerSpeed = 4
stunFreezeTime = 60

#golden snitch
goldenSnitchSize = 10
scoreOfGoldenSnitch = 32
distToCatchGoldenSnitch = 10 

#dir const
dirConst = [[0,0],[0,1],[0.707,-0.707],[1,0],[0.707,0.707],[0,-1],[-0.707,0.707],[-1,0],[-0.707,-0.707]]
dirBounce = [[0, 1, 8, 7, 6, 5, 4, 3, 2], [0, 5, 4, 3, 2, 1, 8, 7, 6], \
             [0, 7, 6, 5, 8, 3, 2, 1, 4], [0, 3, 6, 1, 8, 7, 2, 5, 3]]

#gate const
goalRange = 180
goalRangeLower = gameRangeLower + (gameRange - goalRange) / 2
goalRangeUpper = goalRangeLower + goalRange

#barrier const
barrierTimer = 120
barrierWidth = 180

#goal check
reachNothing = -1
reachCornerGoal = 4
reachWall = 10

#game const
initTime = 180
ticktime = 30
