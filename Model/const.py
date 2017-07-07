#ball const
ballRandomLower = 270
ballRandomUpper = 470
numberOfQuaffles = 2
quaffleSize = 35
scoreOfQuaffles = [1,0,4,8,12,16]
distToCatchQuaffle = 30


#view const
gameRange = 700
gameRangeLower = 20
gameRangeUpper = gameRangeLower + gameRange
gameMid = (gameRangeUpper + gameRangeLower) / 2

#player const
playerInitPos = [[370,70],[670,370],[370,670],[70,370]]
powerMax = 100
playerBumpDistance = 25
PlayerNum = 4
MaxManualPlayer = 4
powerAdd = [1,2]


#time const
freezeTime = 60
stunFreezeTime = 60
maskTime = 100
invisibleTime = 300

#cost const
modeChangePower = 10
barrierPowerCost = 18
stunPowerCost = 30
maskPowerCost = 20
powerShotPowerCost = 18

#golden snitch
goldenSnitchSize = 10
scoreOfGoldenSnitch = 32
distToCatchGoldenSnitch = 20
goldenSnitchAlertRadius = 150


#dir const
dirConst = [[0,0],[0,-1],[0.707,-0.707],[1,0],[0.707,0.707],[0,1],[-0.707,0.707],[-1,0],[-0.707,-0.707]]
dirBounce = [[0, 1, 8, 7, 6, 5, 4, 3, 2], [0, 5, 4, 3, 2, 1, 8, 7, 6], \
             [0, 7, 6, 5, 8, 3, 2, 1, 4], [0, 3, 6, 1, 8, 7, 2, 5, 4]]

#gate const
goalRange = 180
goalRangeLower = gameRangeLower + (gameRange - goalRange) / 2
goalRangeUpper = goalRangeLower + goalRange
cornerGoalRange = goalRange / 2
cornerGoalRangeLower = gameRangeLower + cornerGoalRange
cornerGoalRangeUpper = gameRangeUpper - cornerGoalRange

#barrier const
barrierTimer = 120
barrierWidth = 180

#stun const
stunDistance = 75

#goal check
reachNothing = -1
reachCornerGoal = 4
reachWall = 10

#game const
initTime = 180
ticktime = 30

#speed
quaffleSpeed = 3
goldenSnitchSpeed = 8
goldenSnitchTerminalSpeed = 3
goldenSnitchSpeedDecayPerSec = (goldenSnitchSpeed - goldenSnitchTerminalSpeed) / initTime
playerSpeed = [3,5,12]
shotSpeed = 6
depriveSpeed = 6