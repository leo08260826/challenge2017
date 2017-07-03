import time
import random

from EventManager import *
from const_main import *
from Model.StateMachine import *
from Model.GameObject.Player import *

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
        self.player = []
        self.quaffles = []
        # initialize quaffles
        for quaffleId in range(0, numberOfQuaffles):
            quaffleTemp = quaffles(quaffleId)
            quaffles.push(quaffleTemp)

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
            pass
        elif isinstance(event, Event_Action):
            pass
        elif isinstance(event, Event_Tick):
            pass
        elif isinstance(event, Event_SkillCard):
            if event.SkillIndex == 0:
                # invisible
                player[event.playerIndex].hide()
            if event.SkillIndex == 1:
                # Dementor
                player[event.target].power *= dementorAttackFactor

    def SetPlayer(self):
        for i in range(PlayerNum):
            if self.AIList[i] != None:
                Tmp_P = player(self.AIList[i])
                Tmp_P.IS_AI = True
            else:
                Tmp_P = player("Default")
                Tmp_P.IS_AI = False
            self.player.append(Tmp_P)

    def SetPlayerDirection(self, playerIndex, direction):
        if self.AIList[playerIndex] != None:
            player = self.AIList[playerIndex]
            player.direction = direction;

    def ChangePlayerMode(self, playerIndex):
        if self.AIList[playerIndex] != None:
            player = self.AIList[playerIndex]
            player.freeze(ChangeModeFreezeTime);
            player.mode = 1 - player.mode

    def PlayerShot(self, playerIndex):
        if self.AIList[playerIndex] != None:
            player = self.AIList[playerIndex]
            ballID = player.shot()

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
