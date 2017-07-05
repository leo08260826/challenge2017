import pygame as pg

import Model.main as model
import Model.GameObjcet.model_const as mc
from EventManager import *
from const_main import *
from View.const import *

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick) and self.isinitialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            if cur_state == model.STATE_PLAY:
                self.render_play()
            if cur_state == model.STATE_STOP:
                self.render_stop()

            self.display_fps()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(FramePerSec)
        elif isinstance(event, Event_Quit):
            # shut down the pygame graphics
            self.isinitialized = False
            pg.quit()
        elif isinstance(event, Event_Initialize):
            self.initialize()
    
    def render_menu(self):
        """
        Render the game menu.
        """
        # draw backgound
        self.screen.fill(Color_Black)
        # write some word
        somewords = self.smallfont.render(
                    'You are in the Menu. Space to play. Esc exits.', 
                    True, (0, 255, 0))
        (SurfaceX, SurfaceY) = somewords.get_size()
        pos_x = (ScreenSize[0] - SurfaceX)/2
        pos_y = (ScreenSize[1] - SurfaceY)/2
        self.screen.blit(somewords, (pos_x, pos_y))
        # update surface
        pg.display.flip()
        
    def render_play(self):
        """
        Render the game play.
        """
        # draw backgound
        self.screen.fill(Color_White)
        # write some word
        somewords = self.smallfont.render(
                    'Play game!', 
                    True, (0, 255, 0))
        (SurfaceX, SurfaceY) = somewords.get_size()
        pos_x = (ScreenSize[0] - SurfaceX)/2
        pos_y = (ScreenSize[1] - SurfaceY)/2
        self.screen.blit(somewords, (pos_x, pos_y))
        
        surface = pg.display.get_surface()

        # draw players
        for player in self.model.players:
            # Blue : defense, Red : attack
            if player.mode == 0:
                pg.draw.rect(surface, Color_Red, (round(player.position[0]) - 20 , round(player.position[1]) - 20, 40, 40))
            elif player.mode == 1:
                pg.draw.rect(surface, Color_Blue, (round(player.position[0]) - 20, round(player.position[1]) - 20, 40, 40))

        # draw quaffle
        for quaffle in self.model.quaffles:
            if not quaffle.mode == 1:
                if quaffle.isStrengthened:
                    pg.draw.circle(surface, pg.Color("Orange"), (round(quaffle.position[0]), round(quaffle.position[1])), 20)
                else:
                    pg.draw.circle(surface, Color_Green, (round(quaffle.position[0]), round(quaffle.position[1])), 20)



        # draw golden snitch
        pg.draw.circle(surface, pg.Color("Yellow"), (round(self.model.goldenSnitch.position[0]), round(self.model.goldenSnitch.position[1])), 10)

        # draw barrier
        for barrier in self.model.barriers:
            # veritcal barrier
            if barrier.direction in [1, 5]:
                pg.draw.line(surface, pg.Color("Black"), False\
                 [round(barrier.position[0] - barrierWidth/2), round(barrier.position[1])],\
                  [round(barrier.position[0] + barrierWidth/2), round(barrier.position[1])], 3)
            # NE - SW barrier
            elif barrier.direction in [2, 6]:
                pg.draw.line(surface, pg.Color("Black"), False\
                 [round(barrier.position[0] - barrierWidth/4), round(barrier.position[1] + barrierWidth/4)],\
                  [round(barrier.position[0] + barrierWidth/4), round(barrier.position[1] - barrierWidth/4)], 3)
            # horizontal barrier
            elif barrier.direction in [3, 7]:
                pg.draw.line(surface, pg.Color("Black"), False\
                 [round(barrier.position[0]), round(barrier.position[1] - barrierWidth/2)],\
                  [round(barrier.position[0]), round(barrier.position[1] + barrierWidth/2)], 3)
            # NW - SE barrier
            elif barrier.direction in [4, 8]:
                pg.draw.line(surface, pg.Color("Black"), False\
                 [round(barrier.position[0] + barrierWidth/4), round(barrier.position[1] + barrierWidth/4)],\
                  [round(barrier.position[0] - barrierWidth/4), round(barrier.position[1] - barrierWidth/4)], 3)
        # update surface
        pg.display.flip()
        
    def render_stop(self):
        """
        Render the stop screen.
        """
        # draw backgound
        self.screen.fill(Color_Black)
        # write some word
        somewords = self.smallfont.render(
                    'stop the game. space, escape to return the game.', 
                    True, (0, 255, 0))
        (SurfaceX, SurfaceY) = somewords.get_size()
        pos_x = (ScreenSize[0] - SurfaceX)/2
        pos_y = (ScreenSize[1] - SurfaceY)/2
        self.screen.blit(somewords, (pos_x, pos_y))
        # update surface
        pg.display.flip()

    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(GameCaption, self.clock.get_fps())
        pg.display.set_caption(caption)
        
    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        result = pg.init()
        pg.font.init()
        pg.display.set_caption(GameCaption)
        self.screen = pg.display.set_mode(ScreenSize)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(None, 40)
        self.isinitialized = True