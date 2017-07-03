import time
import random
import itertools

from EventManager import *
from const_main import *
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
        self.balls   = []
        self.quaffles = []
        self.barriers = []
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
        elif isinstance(event, Event_EveryTick):
            self.UpdateObjects()
            self.Bump()
        # leave the parameter lists blank until event specs are stable
        elif isinstance(event, Event_PlayerMove):
            self.SetPlayerDirection()
        elif isinstance(event, Event_PlayerShot):
            self.PlayerShot()
        elif isinstance(event, Event_PlayerModeChange):
            self.ChangePlayerMode()
        elif isinstance(event, Event_PlayerTimeup):
            pass
        elif isinstance(event, Event_SkillCard):
            self.ApplySkillCard()
        elif isinstance(event, Event_Action):
            self.ApplyAction()

    def SetPlayer(self):
        for i in range(PlayerNum):
            if self.AIList[i] != None:
                Tmp_P = player(self.AIList[i])
                Tmp_P.IS_AI = True
            else:
                Tmp_P = player("Default")
                Tmp_P.IS_AI = False
            self.players.append(Tmp_P)

    def SetQuaffle(self):
        for quaffleId in range(0, numberOfQuaffles):
            quaffleTemp = quaffles(quaffleId)
            quaffles.push(quaffleTemp)

    def SetGoldenSnitch(self):
        goldenSnitch = GoldenSnitch()

    def UpdateObjects(self):
        # Update players
        for player in self.players:
            player.tickCheck()
        # Update quaffles
        for quaffle in self.quaffles:
            quaffle.tickCheck()
        # Update golden snitch
        self.goldenSnitch.tickCheck()
        # Update barriers
        for barrier in self.barriers:
            barrier.tickCheck()

    def Bump(self):
        # player to player
        for players in itertools.combinations(self.players, 2):
            lostBalls = players[0].bump(players[1])
            for lostBall in lostBalls:
        # player to golden snitch
        distToGoldenSnitch = []
        for player in self.players:
            if player.takeball == -1:
                distSquare = (player.position[0] - goldenSnitch.position[0]) ** 2 + \
                             (player.position[1] - goldenSnitch.position[1]) ** 2
                distToGoldenSnitch.append((distSquare ** (1/2), player.index))
        if not distToGoldenSnitch:
            dist, playerIndex = min(distToGoldenSnitch)
            if dist < distToCatchGoldenSnitch:
                self.players[playerIndex].score += scoreOfGoldenSnitch
                self.evManager(Event_Timeup)
        # player to quaffle
        for quaffle in self.quaffles:
            if quaffle.state != 1:
                distToQuaffle = []
                for player in self.players:
                    if player.takeball == -1:
                        distSquare = (player.position[0] - quaffle.position[0]) ** 2 + \
                                     (player.position[1] - quaffle.position[1]) ** 2
                        distToQuaffle.append((distSquare ** (1/2), player.index))
                if not distToQuaffle:
                    dist, playerIndex = min(distToGoldenSnitch)
                    if dist < distToCatchQuaffle:
                        self.players[playerIndex].score += scoreOfQuaffle[quaffle.state]
                        self.players[playerIndex].takeball = quaffle.index
                        quaffle.catch(playerIndex)
        # barrier to player

        # barrier to quaffle

    def ChangePlayerMode(self, playerIndex):
        if self.players[playerIndex] != None:
            player = self.players[playerIndex]
            player.freeze(ChangeModeFreezeTime);
            player.mode = 1 - player.mode

    def PlayerShot(self, playerIndex):
        if self.players[playerIndex] != None:
            player = self.players[playerIndex]
            ballID = player.shot()
            if ballID != -1:
                self.balls[ballID].state = 2

    def ApplySkillCard(self, playerIndex, skillIndex):
        pass

    def ApplyAct(self, playerIndex, actionIndex):
        pass

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
