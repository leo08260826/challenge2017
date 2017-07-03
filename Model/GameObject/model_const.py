ballRandomLower = 270
ballRandomUpper = 470
numberOfQuaffles = 2
quaffleSize = 35
scoreOfQuaffles = [1,0,4,8,12,16]

quaffleSpeed = 3
goldenSnitchSpeed = 8
playerSpeed = 4

playerInitPos = [[70,70],[70,670],[670,70],[670,670]]
powerMax = 1000
freezeTime = 60
playerBumpDistance = 625
barrierPowerCost = 180
PlayerNum = 4

gameRange = 700
gameRangeLower = 20
gameRangeUpper = gameRangeLower + gameRange


goalRange = 180
goalRangeLower = gameRangeLower + (gameRange - goalRange) / 2
goalRangeUpper = goalRangeLower + goalRange

goldenSnitchSize = 10
scoreOfGoldenSnitch = 32
numberOfQuaffles = 2


#direction x, y bounce 
dirConst = [[0,0],[0,1],[0.707,-0.707],[1,0],[0.707,0.707],[0,-1],[-0.707,0.707],[-1,0],[-0.707,-0.707]]
dirBounce = [[0, 1, 8, 7, 6, 5, 4, 3, 2], [0, 5, 4, 3, 2, 1, 8, 7, 6]]
playerSpeed = 4