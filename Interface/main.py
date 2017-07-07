import imp, traceback

import Model.main as model
from EventManager import *

from Interface.helper import Helper
from Interface.const import *
from Controller.const import *

class Interface(object):
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
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
                if decide == AI_U:
                    self.evManager.Post(Event_Move(player.index, DIR_U))
                elif decide == AI_RU:
                    self.evManager.Post(Event_Move(player.index, DIR_RU))
                elif decide == AI_R:
                    self.evManager.Post(Event_Move(player.index, DIR_R))
                elif decide == AI_RD:
                    self.evManager.Post(Event_Move(player.index, DIR_RD))
                elif decide == AI_D:
                    self.evManager.Post(Event_Move(player.index, DIR_D))
                elif decide == AI_LD:
                    self.evManager.Post(Event_Move(player.index, DIR_LD))
                elif decide == AI_L:
                    self.evManager.Post(Event_Move(player.index, DIR_L))
                elif decide == AI_LU:
                    self.evManager.Post(Event_Move(player.index, DIR_LU))
                elif decide == AI_ACTION_1:
                    self.evManager.Post(Event_Action(player.index, ACTION_0))
                elif decide == AI_ACTION_2:
                    self.evManager.Post(Event_Action(player.index, ACTION_1))
                elif decide == AI_THROW:
                    self.evManager.Post(Event_Action(player.index, ACTION_2))
                elif decide == AI_MODECHANGE:
                    self.evManager.Post(Event_ModeChange(player.index))
                elif decide == AI_SKILLCARD_HIDE:
                    if SKILLCARD_0 in self.model.players[player.index].AI.skill:
                        self.evManager.Post(Event_SkillCard(player.index, SKILLCARD_0))
                elif decide == AI_SKILLCARD_DEMENTOR:
                    if SKILLCARD_1 in self.model.players[player.index].AI.skill:
                        self.evManager.Post(Event_SkillCard(player.index, SKILLCARD_1))
                elif decide == AI_SKILLCARD_STUNALL:
                    if SKILLCARD_2 in self.model.players[player.index].AI.skill:
                        self.evManager.Post(Event_SkillCard(player.index, SKILLCARD_2))
                elif decide == AI_CallMe:
                    self.evManager.Post(Event_CallMe(player.index))
                elif decide == AI_NoUseSkillCard:
                    self.evManager.Post(Event_NoUseSkillCard())
        
    def initialize(self):
        for index, player in enumerate(self.model.players):
            if player.name == "manual":
                continue

            # load TeamAI .py file
            try:
                loadtmp = imp.load_source('', './AI/team_' + player.name + '.py')
            except:
                print( "player:["+ str(index) +"]team_"+ player.name +"'s AI can't load." )
                player.name, player.IS_AI, player.AI= "Error" , False, None
                continue
            print("Load ["+ str(index) +"]team_" + player.name + ".py")
            # init TeamAI class
            try:
                player.AI = loadtmp.TeamAI( Helper(self.model, index) )
            except:
                print( "player:["+ str(index) +"]team_"+ player.name +"'s AI __init__ is crashed." )
                traceback.print_exc()
                player.name, player.IS_AI, player.AI= "Error" , False, None
                continue
            print("Successful to Load ["+ str(index) +"]team_" + player.name + ".py")
    
