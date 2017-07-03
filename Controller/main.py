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
                    if cur_state == model.STATE_PLAY:
                        self.ctrl_play(event)
                    if cur_state == model.STATE_STOP:
                        self.ctrl_stop(event)
        elif isinstance(event, Event_Initialize):
            self.initialize()

    def ctrl_menu(self, event):
        """
        Handles menu events.
        """
        if event.type == pg.KEYDOWN:
            # escape pops the menu
            if event.key == pg.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
            # space plays the game
            if event.key == pg.K_SPACE:
                self.evManager.Post(Event_StateChange(model.STATE_PLAY))

    def ctrl_stop(self, event):
        """
        Handles help events.
        """
        if event.type == pg.KEYDOWN:
            # space, enter or escape pops help
            if event.key == pg.K_SPACE:
                self.evManager.Post(Event_StateChange(None))

    def ctrl_play(self, event):
        """
        Handles play events.
        """
        if event.type == pg.KEYDOWN:
            # escape pops the menu
            if event.key == pg.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
            # key space to stop the game
            elif event.key == pg.K_SPACE:    
                self.evManager.Post(Event_StateChange(model.STATE_STOP))
            # player1
            if event.key == pg.K_w:
                if pg.key.get_pressed()[pg.K_d] == 1 and pg.key.get_pressed()[pg.K_s] == 0 and  pg.key.get_pressed()[pg.K_a] == 0 :
                    self.evManager.Post(Event_Move(1,DIR_RU))
                elif pg.key.get_pressed()[pg.K_d] == 0 and pg.key.get_pressed()[pg.K_s] == 0 and  pg.key.get_pressed()[pg.K_a] == 1 :
                    self.evManager.Post(Event_Move(1,DIR_LU))
                elif pg.key.get_pressed()[pg.K_d] == 0 and pg.key.get_pressed()[pg.K_s] == 0 and  pg.key.get_pressed()[pg.K_a] == 0 :
                    self.evManager.Post(Event_Move(1,DIR_U))
            elif event.key == pg.K_s:
                if pg.key.get_pressed()[pg.K_d] == 1 and pg.key.get_pressed()[pg.K_w] == 0 and  pg.key.get_pressed()[pg.K_a] == 0 :
                    self.evManager.Post(Event_Move(1,DIR_RD))
                elif pg.key.get_pressed()[pg.K_d] == 0 and pg.key.get_pressed()[pg.K_w] == 0 and  pg.key.get_pressed()[pg.K_a] == 1 :
                    self.evManager.Post(Event_Move(1,DIR_LD))
                elif pg.key.get_pressed()[pg.K_d] == 0 and pg.key.get_pressed()[pg.K_w] == 0 and  pg.key.get_pressed()[pg.K_a] == 0 :
                    self.evManager.Post(Event_Move(1,DIR_D))
            elif event.key == pg.K_d:
                if pg.key.get_pressed()[pg.K_w] == 1 and pg.key.get_pressed()[pg.K_s] == 0 and  pg.key.get_pressed()[pg.K_a] == 0 :
                    self.evManager.Post(Event_Move(1,DIR_RU))
                elif pg.key.get_pressed()[pg.K_w] == 0 and pg.key.get_pressed()[pg.K_s] == 1 and  pg.key.get_pressed()[pg.K_a] == 0 :
                    self.evManager.Post(Event_Move(1,DIR_RD))
                elif pg.key.get_pressed()[pg.K_w] == 0 and pg.key.get_pressed()[pg.K_s] == 0 and  pg.key.get_pressed()[pg.K_a] == 0 :
                    self.evManager.Post(Event_Move(1,DIR_R))
            elif event.key == pg.K_a:
                if pg.key.get_pressed()[pg.K_d] == 0 and pg.key.get_pressed()[pg.K_s] == 1 and  pg.key.get_pressed()[pg.K_w] == 0 :
                    self.evManager.Post(Event_Move(1,DIR_LD))
                elif pg.key.get_pressed()[pg.K_d] == 0 and pg.key.get_pressed()[pg.K_s] == 0 and  pg.key.get_pressed()[pg.K_w] == 1 :
                    self.evManager.Post(Event_Move(1,DIR_LU))
                elif pg.key.get_pressed()[pg.K_d] == 0 and pg.key.get_pressed()[pg.K_s] == 0 and  pg.key.get_pressed()[pg.K_w] == 0 :
                    self.evManager.Post(Event_Move(1,DIR_L))
            
    def initialize(self):
        """
        init pygame event and set timer
        
        # Document
        pg.event.Event(event_id)
        pg.time.set_timer(event_id, TimerDelay)
        """
        pg.time.set_timer(pg.USEREVENT,1000)
