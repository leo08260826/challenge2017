import pygame as pg

import Model.main as model
from EventManager import *
from const_main import *
from Controller.const import *

class Control(object):
    """
    Handles control input.
    """
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
            # Called for each game tick. We check our keyboard presses here.
            for event in pg.event.get():
                # handle window manager closing our window
                if event.type == pg.QUIT:
                    self.evManager.Post(Event_Quit())
                else:
                    cur_state = self.model.state.peek()
                    if cur_state == model.STATE_MENU:
                        self.ctrl_menu(event)
                    elif cur_state == model.STATE_PLAY:
                        self.ctrl_play(event)
                    elif cur_state == model.STATE_STOP:
                        self.ctrl_stop(event)
                    elif cur_state == model.STATE_PRERECORD:
                        self.ctrl_prerecord(event)
                    elif cur_state == model.STATE_RECORD:
                        self.ctrl_record(event)
        elif isinstance(event, Event_Initialize):
            self.initialize()

    def ctrl_menu(self, event):
        """
        Handles menu events.
        """
        if event.type == pg.KEYDOWN:
            # escape to pop the menu
            if event.key == pg.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
            # space to play the game
            if event.key == pg.K_SPACE:
                self.evManager.Post(Event_StateChange(model.STATE_PLAY))

    def ctrl_play(self, event):
        """
        Handles play events.
        """
        if event.type == pg.USEREVENT:
            self.evManager.Post(Event_EverySec())
        elif event.type == pg.KEYDOWN:
            # escape to pop the menu
            if event.key == pg.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
                self.evManager.Post(Event_Restart())
            # space to stop the game
            elif event.key == pg.K_SPACE:    
                self.evManager.Post(Event_StateChange(model.STATE_STOP))
            # player controler
            for player in self.model.players:
                if player.IS_AI:
                    continue
                DirKeys = PlayerKeys[player.index][0:4]
                if event.key in DirKeys:
                    NowPressedKeys = self.GetPressIn(DirKeys)
                    DirHashValue = self.GetDirHashValue(NowPressedKeys, DirKeys)
                    if DirHash[DirHashValue] != 0:
                        self.evManager.Post(Event_Move(player.index, DirHash[DirHashValue]))
                # change mode 
                elif event.key == PlayerKeys[player.index][4]:
                    self.evManager.Post(Event_PlayerModeChange(player.index))
                # use action
                elif event.key == PlayerKeys[player.index][5]:
                    self.evManager.Post(Event_Action(player.index, ACTION_0))
                elif event.key == PlayerKeys[player.index][6]:
                    self.evManager.Post(Event_Action(player.index, ACTION_1))
                elif event.key == PlayerKeys[player.index][7]:
                    self.evManager.Post(Event_Action(player.index, ACTION_2))
        elif event.type == pg.KEYUP:
            # player controler
            for player in self.model.players:
                if player.IS_AI:
                    continue
                DirKeys = PlayerKeys[player.index][0:4]
                if event.key in DirKeys:
                    NowPressedKeys = self.Get_KeyPressIn(DirKeys)
                    DirHashValue = self.Get_DirHashValue(NowPressedKeys, DirKeys)
                    if DirHash[DirHashValue] != 0:
                        self.evManager.Post(Event_Move(player.index, DirHash[DirHashValue]))

    def ctrl_stop(self, event):
        """
        Handles stop events.
        """
        if event.type == pg.KEYDOWN:
            # space to back the game
            if event.key == pg.K_SPACE:
                self.evManager.Post(Event_StateChange(None))

    def ctrl_prerecord(self, event):
        """
        Handles prerecord events.
        """
        if event.type == pg.KEYDOWN:
            # space to pop the scoreboard
            if event.key == pg.K_SPACE:
                self.evManager.Post(Event_StateChange(model.STATE_RECORD))

    def ctrl_record(self, event):
        """
        Handles record events.
        """
        if event.type == pg.KEYDOWN:
            # escape to back the menu
            if event.key == pg.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
                self.evManager.Post(Event_StateChange(None))
                self.evManager.Post(Event_StateChange(None))
                self.evManager.Post(Event_Restart())

    def initialize(self):
        """
        init pygame event and set timer
        
        # Document
        pg.event.Event(event_id)
        pg.time.set_timer(event_id, TimerDelay)
        """
        pg.time.set_timer(pg.USEREVENT,1000)
    
    def Get_KeyPressIn(self, keylist):
        return [key for key, value in enumerate(pg.key.get_pressed()) if value == 1 and key in keylist]

    def Get_DirHashValue(self, PressList, DirKeyList):
        HashValue = 0
        for index, key in enumerate(DirKeyList):
            if key in PressList:
                HashValue += 2**index
        return HashValue