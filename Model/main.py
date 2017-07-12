import time, random, itertools

from EventManager import *
from Model.const import *
# import Model.const as MC

from Model.StateMachine import *
from Model.GameObject.Player import *
from Model.GameObject.Ball import *
from Model.GameObject.Barrier import *

class GameEngine(object):
    # Tracks the game state.
    def __init__(self, evManager, AINames):
        # evManager (EventManager): Allows posting messages to the event queue.
        #
        # Attributes:
        #     running (bool): True while the engine is online. Changed via Event_Quit().
        #     state (StateMachine()): control state change, stack data structure.
        #     AINames (list.str): all AI name list.
        #     player (list.player()): all player object.
        #     TurnTo (int): current player

        self.evManager = evManager
        evManager.RegisterListener(self)

        self.running = False
        self.state = StateMachine()
        self.AINames = AINames
        self.players = []
        self.quaffles = []
        self.barriers = []
        self.goldenSnitch = None
        self.timer = 0
        self.TurnTo = 0

        random.seed(time.time())

    def notify(self, event):
        # Called by an event in the message queue.
        if isinstance(event, Event_EveryTick):
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                self.UpdateObjects()
                self.Bump()
        elif isinstance(event, Event_EverySec):
            self.goldenSnitch.decaySpeed()
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                self.timer -= 1
            if self.timer <= 0:
                self.evManager.Post(Event_TimeUp())
        elif isinstance(event, Event_Move):
            self.SetPlayerDirection(event.PlayerIndex, event.Direction)
        elif isinstance(event, Event_ModeChange):
            self.ChangePlayerMode(event.PlayerIndex)
        elif isinstance(event, Event_SkillCard):
            self.ApplySkillCard(event.PlayerIndex, event.SkillIndex)
        elif isinstance(event, Event_Action):
            isConfirmed = self.ApplyAction(event.PlayerIndex, event.ActionIndex)
            if isConfirmed:
                self.evManager.Post(Event_ConfirmAction(event.PlayerIndex, event.ActionIndex))
        elif isinstance(event, Event_StateChange):
            # if event.state is None >> pop state.
            if event.state == None:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.Post(Event_Quit())
            elif event.state == STATE_RESTART:
                self.state.clear()
                self.state.push(STATE_MENU)
            else:
                # push a new state on the stack
                self.state.push(event.state)
        elif isinstance(event, Event_TimeUp):
            self.evManager.Post(Event_StateChange(STATE_PRERECORD))
        elif isinstance(event, Event_Initialize) or \
             isinstance(event, Event_Restart):
            self.Initialize()
        elif isinstance(event, Event_Quit):
            self.running = False

    def Initialize(self):
        self.players = []
        self.quaffles = []
        self.barriers = []
        self.SetPlayer()
        self.SetQuaffle()
        self.SetGoldenSnitch()
        self.timer = initTime

    def SetPlayer(self):
        # set AI Names List
        # "_" ==> default AI, "~" ==> manual player
        ManualPlayerNum = 0
        for index in range(PlayerNum):
            if len(self.AINames) > index:
                PlayerName = self.AINames[index]
                if PlayerName == "~":
                    if ManualPlayerNum < MaxManualPlayerNum:
                        ManualPlayerNum += 1
                    else:
                        self.AINames[index] = "_"
            else:
                if ManualPlayerNum < MaxManualPlayerNum:
                    ManualPlayerNum += 1
                    self.AINames.append("~")
                else:
                    self.AINames.append("_")

        # init Player object
        for index in range(PlayerNum):
            if self.AINames[index] == "~":
                Tmp_P = player("manual", index, False)
            elif self.AINames[index] == "_":
                Tmp_P = player("default", index, True)
            else:
                Tmp_P = player(self.AINames[index], index, True)
            self.players.append(Tmp_P)

    def SetQuaffle(self):
        for quaffleId in range(0, numberOfQuaffles):
            quaffleTemp = Quaffle(quaffleId)
            self.quaffles.append(quaffleTemp)

    def SetGoldenSnitch(self):
        self.goldenSnitch = GoldenSnitch(0)

    def UpdateObjects(self):
        # Update players
        for player in self.players:
            player.tickCheck()
        # Update quaffles
        for quaffle in self.quaffles:
            score, playerIndex, minusScore, beShotPlayer = quaffle.tickCheck(self.barriers)
            for barrier in self.barriers:
                if beShotPlayer == barrier.playerIndex:
                    barrier.inactive()
            if playerIndex in range(PlayerNum):
                self.players[playerIndex].score += score
            if beShotPlayer in range(PlayerNum):
                self.players[beShotPlayer].score += minusScore
                if self.players[beShotPlayer].score < 0:
                    self.players[beShotPlayer].score = 0
        # Update golden snitch
        self.goldenSnitch.tickCheck(self.players)
        # Update barriers
        for barrier in self.barriers:
            # if barrier is inactive, remove it.
            if not barrier.tickCheck():
                self.barriers.remove(barrier)

    def Bump(self):
        # player to player
        for players in itertools.combinations(self.players, 2):
            lostBalls = players[0].bump(players[1])
            for lostBall in lostBalls:
                self.quaffles[lostBall[0]].deprive(lostBall[1], lostBall[2])
        # player to golden snitch
        distToGoldenSnitch = []
        for player in self.players:
            if player.takeball == -1 and not player.isFreeze and \
               player.mode == 1:
                distSquare = (player.position[0] - self.goldenSnitch.position[0]) ** 2 + \
                             (player.position[1] - self.goldenSnitch.position[1]) ** 2
                distToGoldenSnitch.append((distSquare ** (1/2), player.index))

        if distToGoldenSnitch:
            dist, playerIndex = min(distToGoldenSnitch)
            if dist < distToCatchGoldenSnitch:
                self.players[playerIndex].takeball = 100
                self.players[playerIndex].score += scoreOfGoldenSnitch
                self.evManager.Post(Event_TimeUp())

        # player to quaffle
        for quaffle in self.quaffles:
            if quaffle.state in [0, 2]:
                distToQuaffle = []
                for player in self.players:
                    if player.takeball == -1 and not player.isFreeze:
                        distSquare = (player.position[0] - quaffle.position[0]) ** 2 + \
                                     (player.position[1] - quaffle.position[1]) ** 2
                        distToQuaffle.append((distSquare ** (1/2), player.index))
                if distToQuaffle:
                    dist = min(distToQuaffle)
                    playerIndex = dist[1]
                    if dist[0] < distToCatchQuaffle:
                        self.players[playerIndex].takeball = quaffle.index
                        tmpQuaffleState = quaffle.state
                        hasCaught = quaffle.catch(playerIndex)
                        if not hasCaught:
                            self.players[playerIndex].score += scoreOfQuaffles[tmpQuaffleState]

        # # barrier to player
        # for barrier in self.barriers:
        #     for player in self.players:
        #         if not barrier.playerIndex == player.index and \
        #                 barrier.bump(player, playerSpeed[player.mode]):
        #             player.position[0] -= dirConst[player.direction][0]*playerSpeed[player.mode]
        #             player.position[1] -= dirConst[player.direction][1]*playerSpeed[player.mode]
        # # barrier to quaffle
        # for barrier in self.barriers:
        #     for quaffle in self.quaffles:
        #         if quaffle.state in [0, 2] and barrier.bump(quaffle, quaffle.speed):
        #             if quaffle.isStrengthened:
        #                 barrier.inactive()
        #             else:
        #                 quaffle.state = 0
        #                 quaffle.playerIndex = -1
        #                 if barrier.direction in (1,5):
        #                     quaffle.direction = dirBounce[1][quaffle.direction]
        #                 if barrier.direction in (2,6):
        #                     quaffle.direction = dirBounce[2][quaffle.direction]
        #                 if barrier.direction in (3,7):
        #                     quaffle.direction = dirBounce[0][quaffle.direction]
        #                 if barrier.direction in (4,8):
        #                     quaffle.direction = dirBounce[3][quaffle.direction]

    def SetPlayerDirection(self, playerIndex, direction):
        if self.players[playerIndex] != None and self.players[playerIndex].isFreeze != True:
            player = self.players[playerIndex]
            player.direction = direction;

    def ChangePlayerMode(self, playerIndex):
        if self.players[playerIndex] != None and self.players[playerIndex].power >= modeChangePower and self.players[playerIndex].isFreeze == False:
            player = self.players[playerIndex]
            player.mode = 1 - player.mode
            player.isMask = False
            player.power -= modeChangePower

    def ApplySkillCard(self, playerIndex, skillIndex):
        # 0 = inVisible
        # 1 = empty power
        # 2 = stun all enermy
        # 3 = fake position
        if self.players[playerIndex] != None and skillIndex in self.players[playerIndex].AI.skill:
            Nowplayer = self.players[playerIndex]
            if skillIndex == 0:
                Nowplayer.isVisible = False
                Nowplayer.invisibleTimer = invisibleTime
            elif skillIndex == 1:
                for player in self.players:
                    if player.index !=  playerIndex:
                        player.power = 0
            elif skillIndex == 2:
                for player in self.players:
                    if player.index !=  playerIndex:
                        player.isFreeze = True
                        player.freezeTimer = 57
            addindex = self.players[playerIndex].AI.skill.index(skillIndex)
            self.players[playerIndex].AI.skill[addindex] += 10




    def ApplyAction(self, playerIndex, actionIndex):
        #ACTION_0 = 0   power throw / barrier
        #ACTION_1 = 1   stun / mask
        #ACTION_2 = 2   general throw
        if self.players[playerIndex] != None and self.players[playerIndex].isFreeze != True:
            player = self.players[playerIndex]
            if actionIndex == 0 and player.power >= powerShotPowerCost:
                if player.mode == 0:
                    ballData = self.players[playerIndex].shot()
                    if ballData != -1:
                        self.quaffles[ballData].throw(player.direction,player.position,True)
                        player.power -= powerShotPowerCost
                        return True
                elif player.mode == 1 and player.power >= barrierPowerCost:
                    self.players[playerIndex].setBarrier()
                    if playerIndex == 0:
                        self.barriers.append(Barrier(playerIndex,[370, 0],1))
                    elif playerIndex == 1:
                        self.barriers.append(Barrier(playerIndex,[720, 370],3))
                    elif playerIndex == 2:
                        self.barriers.append(Barrier(playerIndex,[370, 720],5))
                    elif playerIndex == 3:
                        self.barriers.append(Barrier(playerIndex,[0, 370],7))
                    return True

            elif actionIndex == 1:
                if player.mode == 0 and player.power >= stunPowerCost:
                    player.power -= stunPowerCost
                    for playercheck in self.players:
                        if playercheck == player:
                            continue
                        else:
                            distSquare = (playercheck.position[0] - player.position[0]) ** 2 + \
                                    (playercheck.position[1] - player.position[1]) ** 2
                            if distSquare < (stunDistance) ** 2:
                                if playercheck.isMask == False:
                                    if playercheck.takeball != -1:
                                        ballData = playercheck.takeball
                                        if player.takeball != -1:
                                            playercheck.takeball = -1
                                            self.quaffles[ballData].deprive(playercheck.direction, playercheck.position)
                                        else:
                                            playercheck.takeball = -1
                                            player.takeball = ballData
                                            self.quaffles[ballData].playerIndex = player.index
                                    playercheck.freeze()
                                else:
                                    playercheck.maskTimer = 0
                                    playercheck.isMask = False
                    return True
                elif player.mode == 1 and player.power >= maskPowerCost:
                    player.isMask = True
                    player.maskTimer = maskTime
                    player.power -= maskPowerCost
                    return True
            elif  actionIndex == 2 and player.mode == 0:
                ballData = player.shot()
                if ballData != -1:
                    self.quaffles[ballData].throw(player.direction, player.position)
                    return True
            return False

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.running = True
        self.evManager.Post(Event_Initialize())
        self.state.push(STATE_MENU)
        while self.running:
            newTick = Event_EveryTick()
            self.evManager.Post(newTick)
