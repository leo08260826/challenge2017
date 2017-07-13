import imp, traceback

import Model.main as model
from EventManager import *

from Interface.helper import Helper
import Model.const as MC
import Interface.const as IC
from Controller.const import *

class Interface(object):
    def __init__(self, evManager, model):

        # evManager (EventManager): Allows posting messages to the event queue.
        # model (GameEngine): a strong reference to the game Model.

        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_PLAY:
                self.API_play()
        elif isinstance(event, Event_Quit):
            pass
        elif isinstance(event, Event_Initialize) or \
             isinstance(event, Event_Restart):
            self.initialize()
    
    def API_play(self):
        for player in self.model.players:
            # print(player.IS_AI)
            if player.IS_AI:
                decide = player.AI.decide()
                if decide == IC.AI_U:
                    self.evManager.Post(Event_Move(player.index, DIR_U))
                elif decide == IC.AI_RU:
                    self.evManager.Post(Event_Move(player.index, DIR_RU))
                elif decide == IC.AI_R:
                    self.evManager.Post(Event_Move(player.index, DIR_R))
                elif decide == IC.AI_RD:
                    self.evManager.Post(Event_Move(player.index, DIR_RD))
                elif decide == IC.AI_D:
                    self.evManager.Post(Event_Move(player.index, DIR_D))
                elif decide == IC.AI_LD:
                    self.evManager.Post(Event_Move(player.index, DIR_LD))
                elif decide == IC.AI_L:
                    self.evManager.Post(Event_Move(player.index, DIR_L))
                elif decide == IC.AI_LU:
                    self.evManager.Post(Event_Move(player.index, DIR_LU))
                elif decide == IC.AI_ATTACK_POWERTHROW:
                    self.evManager.Post(Event_Action(player.index, ACTION_0))
                elif decide == IC.AI_ATTACK_STUN:
                    self.evManager.Post(Event_Action(player.index, ACTION_1))
                elif decide == IC.AI_THROWBALL:
                    self.evManager.Post(Event_Action(player.index, ACTION_2))
                elif decide == IC.AI_MODECHANGE:
                    self.evManager.Post(Event_ModeChange(player.index))
                elif decide == IC.AI_SKILLCARD_HIDE:
                    if self.model.players[player.index].AI.skill[MC.HIDE] > 0:
                        self.evManager.Post(Event_SkillCard(player.index, MC.HIDE))
                elif decide == IC.AI_SKILLCARD_DEMENTOR:
                    if self.model.players[player.index].AI.skill[MC.DEMENTOR] > 0:
                        self.evManager.Post(Event_SkillCard(player.index, MC.DEMENTOR))
                elif decide == IC.AI_SKILLCARD_STUNALL:
                    if self.model.players[player.index].AI.skill[MC.STUNALL] > 0:
                        self.evManager.Post(Event_SkillCard(player.index, MC.STUNALL))
                elif decide == IC.AI_SKILLCARD_SPECIAL:
                    if self.model.players[player.index].AI.skill[MC.SPECIAL] > 0:
                        self.evManager.Post(Event_SkillCard(player.index, MC.SPECIAL))
                elif decide == IC.AI_CALLME:
                    self.evManager.Post(Event_CallMe(player.index))
        
    def initialize(self):
        for index, player in enumerate(self.model.players):
            if player.name == "manual":
                continue

            # load TeamAI .py file
            try:
                loadtmp = imp.load_source('', './AI/team_' + player.name + '.py')
            except:
                print( "player:["+ str(index) +"]team_"+ player.name +"'s AI can't load." )
                traceback.print_exc()
                player.name, player.IS_AI, player.AI= "Error", False, None
                continue
            print("Load ["+ str(index) +"]team_" + player.name + ".py")
            # init TeamAI class
            try:
                player.AI = loadtmp.TeamAI( Helper(self.model, index) )
            except:
                print( "player:["+ str(index) +"]team_"+ player.name +"'s AI __init__ is crashed." )
                traceback.print_exc()
                player.name, player.IS_AI, player.AI= "Error", False, None
                continue
            print("Successful to Load ["+ str(index) +"]team_" + player.name + ".py")
    
