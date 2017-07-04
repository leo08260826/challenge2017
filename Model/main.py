import time
import random
import itertools

from EventManager import *
from Model.GameObject.model_const import *
from Model.StateMachine import *
from Model.GameObject.Player import *
from Model.GameObject.Ball import *
from Model.GameObject.Barrier import *



class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, evManager, AIList):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
            running (bool): True while the engine is online. Changed via Event_Quit().
            state (StateMachine()): control state change, stack data structure.
            AIList (list.str): all AI name list.
            player (list.player()): all player object.
            TurnTo (int): current player
        """
        self.evManager = evManager
        evManager.RegisterListener(self)

        self.running = False
        self.state = StateMachine()
        self.AIList = AIList
        self.players = []
        self.quaffles = []
        self.barriers = []
        self.timer = 0
        self.TurnTo = 0

        random.seed(time.time())

    def notify(self, event):
        """
        Called by an event in the message queue.
        """
        if isinstance(event, Event_StateChange):
            # if event.state is None >> pop state.
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.Post(Event_Quit())
            else:
                # push a new state on the stack
                self.state.push(event.state)
        elif isinstance(event, Event_Quit):
            self.running = False
        elif isinstance(event, Event_Initialize):
            self.SetPlayer()
            self.SetQuaffle()
            self.SetGoldenSnitch()
            self.timer = initTime
        elif isinstance(event, Event_EveryTick):
            self.UpdateObjects()
            self.Bump()
        elif isinstance(event, Event_EverySec):
            self.timer -= 1
        elif isinstance(event, Event_Move):
            self.SetPlayerDirection(event.PlayerIndex, event.Direction)
        elif isinstance(event, Event_PlayerModeChange):
            self.ChangePlayerMode(event.PlayerIndex)
        elif isinstance(event, Event_TimeUp):
            self.state.push(STATE_RECORD)
        elif isinstance(event, Event_SkillCard):
            self.ApplySkillCard(event.PlayerIndex, event.SkillIndex)
        elif isinstance(event, Event_Action):
            self.ApplyAction(event.PlayerIndex, event.ActionIndex)

    def SetPlayer(self):
        count = 0
        MinAINum = PlayerNum - MaxManualPlayer
        DefautAINum = MinAINum - len(self.AIList) if len(self.AIList) < MinAINum else 0
        for i in range(DefautAINum):
            self.AIList.append("default")

        ManualPlayerNum = PlayerNum - len(self.AIList) if len(self.AIList) < PlayerNum else 0
        for i in range(ManualPlayerNum):
            Tmp_P = player("manual", count)
            Tmp_P.IS_AI = False
            self.players.append(Tmp_P)
            count = count + 1

        AINum = len(self.AIList)
        for i in range(AINum):
            Tmp_P = player(self.AIList[i], count)
            Tmp_P.IS_AI = True
            self.players.append(Tmp_P)
            count = count + 1

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
            score, playerIndex = quaffle.tickCheck()
            if playerIndex in range(PlayerNum):
                self.players[playerIndex].score += score
        # Update golden snitch
        self.goldenSnitch.tickCheck(self.players)
        # Update barriers
        for barrier in self.barriers:
            barrier.tickCheck()

    def Bump(self):
        # player to player
        for players in itertools.combinations(self.players, 2):
            lostBalls = players[0].bump(players[1])
            for lostBall in lostBalls:
                self.balls[lostBall[0]].deprive(lostBall[1])
        # player to golden snitch
        distToGoldenSnitch = []
        for player in self.players:
            if player.takeball == -1 and not player.isFreeze:
                distSquare = (player.position[0] - self.goldenSnitch.position[0]) ** 2 + \
                             (player.position[1] - self.goldenSnitch.position[1]) ** 2
                distToGoldenSnitch.append((distSquare ** (1/2), player.index))

        distToGoldenSnitch.sort()
        for dist in distToGoldenSnitch:
            if dist[0] < distToCatchGoldenSnitch and not self.players[dist[1]].isFreeze:
                self.players[playerIndex].score += scoreOfGoldenSnitch
                self.evManager.Post(Event_Timeup)
                break

        # player to quaffle
        for quaffle in self.quaffles:
            if quaffle.state != 1:
                distToQuaffle = []
                for player in self.players:
                    if player.takeball == -1 and not player.isFreeze:
                        distSquare = (player.position[0] - quaffle.position[0]) ** 2 + \
                                     (player.position[1] - quaffle.position[1]) ** 2
                        distToQuaffle.append((distSquare ** (1/2), player.index))
                if distToQuaffle:
                    dist = min(distToQuaffle)
                    playerIndex = distToQuaffle.index(dist)
                    if dist[0] < distToCatchQuaffle:
                        self.players[playerIndex].score += scoreOfQuaffles[quaffle.state]
                        self.players[playerIndex].takeball = quaffle.index
                        quaffle.catch(playerIndex)
        # barrier to player
        for barrier in self.barriers:
            for player in self.players:
                if not barrier.playerIndex == player.index and barrier.bump(player):
                    player.position[0] -= dirConst[player.direction][0]*playerSpeed
                    player.position[1] -= dirConst[player.direction][1]*playerSpeed
        # barrier to quaffle
        for barrier in self.barriers:
            for quaffle in self.quaffles:
                if barrier.bump(quaffle):
                    if quaffle.isStrengthened:
                        barriers.remove(barrier)
                    elif barrier.direction in (1,5):
                        quaffle.direction = dirBounce[0][quaffle.direction]
                    elif barrier.direction in (2,6):
                        quaffle.direction = dirBounce[2][quaffle.direction]
                    elif barrier.direction in (3,7):
                        quaffle.direction = dirBounce[1][quaffle.direction]
                    elif barrier.direction in (4,8):
                        quaffle.direction = dirBounce[3][quaffle.direction]

    def SetPlayerDirection(self, playerIndex, direction):
        if self.players[playerIndex] != None:
            player = self.players[playerIndex]
            player.direction = direction;

    def ChangePlayerMode(self, playerIndex):
        if self.players[playerIndex] != None and self.players[playerIndex].modeTimer <= 0:
            player = self.players[playerIndex]
            player.freeze(ChangeModeFreezeTime);
            player.mode = 1 - player.mode

    def PlayerShot(self, playerIndex, isStrengthened):
        if self.players[playerIndex] != None:
            player = self.players[playerIndex]
            ballID = player.shot()
            if ballID != -1:
                self.quaffles[ballID].throw(player.direction, isStrengthened)

    def ApplySkillCard(self, playerIndex, skillIndex):
        pass

    def ApplyAction(self, playerIndex, actionIndex):
        #ACTION_0 = 0   power throw / barrier
        #ACTION_1 = 1   stun / mask
        #ACTION_2 = 2   general throw
        if self.players[playerIndex] != None:
            if actionIndex == 0:
                if self.players[playerIndex].mode == 0:
                    ballData = self.players[playerIndex].shot()
                    quaffles[ballData[0]].throw(ballData[1],True)
                elif players[playerIndex].mode == 1:
                    ballData = self.players[playerIndex].setBarrier()
                    barriers.append(Barrier(playerIndex,ballData[0],ballData[1]))

            elif actionIndex == 1:
                if self.players[playerIndex].mode == 0:
                     for player in self.players:
                        if player == self.players[playerIndex]:
                            continue
                        else:
                            distSquare = (player.position[0] - players[playerIndex].position[0]) ** 2 + \
                                    (player.position[1] - players[playerIndex].position[1]) ** 2
                            if (distSquare < (2 * mc.playerBumpDistance) ** 2):
                                player.freeze(mc.stunFreezeTime)

                elif players[playerIndex].mode == 1:
                    players[playerIndex].isMask = True
                    players[playerIndex].maskTimer = maskTime
            elif  actionIndex == 2:
                player = self.players[playerIndex]
                ballID = player.shot()
                if ballID != -1:
                    quaffles[ballData[0]].throw(ballData[1])

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
