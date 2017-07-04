import pygame as pg

import Model.main as model
from EventManager import *
from const_main import *
from View.const import *

import time

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
        self.player_images = []
        self.player_bais = []
        self.ticks = 0
    
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
        self.render_background()

        for i in range(PlayerNum):
            self.render_player_status(i)
        for i in range(PlayerNum):
            self.render_player_character(i)
        # update surface
        pg.display.flip()
        self.ticks += 1
        
    def render_stop(self):
        """
        Render the stop screen.
        """
        # draw backgound
        self.screen.blit(self.map_gray,(0,0))
        # display words
        somewords = self.smallfont.render(
                    'Pause',
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
        self.player_bias = [0, 0, 0, 0]
        # load images
        ''' backgrounds '''
        self.map = pg.image.load('View/image/background/map.png')
        self.map_gray = pg.image.load('View/image/background/map_grayscale.png')
        self.time = pg.image.load('View/image/background/time.png')
        ''' icons '''
        self.icon_dizzy = pg.image.load('View/image/icon/icon_dizzy.png')
        self.icon_attack = pg.image.load('View/image/icon/icon_attack.png')
        self.icon_protect = pg.image.load('View/image/icon/icon_protectmode.png')
        ''' characters '''
        directions = ['_leftup', '_left', '_leftdown', '_down']
        colors = ['_blue', '_yellow', '_red', '_green']
        self.player_freeze_images = [pg.image.load('View/image/player/player_down'+colors[i]+'_frost.png') for i in range(4)]
        def get_player_image(colorname, direction):
            if direction == 0:
                direction = 5
            if direction == 1:
                return pg.transform.flip(pg.image.load('View/image/player/player_down'+colorname+'.png'), 0, 1)
            elif direction in range(2,6):
                return pg.transform.flip(pg.image.load('View/image/player/player'+directions[direction-2]+colorname+'.png'), 1, 0)
            else:
                return pg.image.load('View/image/player/player'+directions[8-direction]+colorname+'.png')
        self.player_images = [ [get_player_image(colors[i],direction) for direction in range(9)] for i in range(4) ]
        

    def render_background(self):
        self.screen.blit(self.map, Pos_map)
        self.screen.blit(self.time, Pos_time)
        self.blit_at_center(self.player_images[3][1], (100,100))
        self.blit_at_center(self.icon_attack, (100,100))
        self.blit_at_center(self.player_images[3][2], (100,500))
        self.blit_at_center(self.icon_attack, (100,500))
        self.blit_at_center(self.player_images[3][3], (100,300))
        self.blit_at_center(self.icon_attack, (100,300))
        
        
    def render_player_status(self, index):
        pass

    def render_player_charcter(self, index):
        if self.ticks % (FramePerSec*3) == biasrand[index]:
            bias[index] = ( bias[index] + 1 ) % 2
        bias = (2,2) if self.player_bias[index] else (-2,-2)
        position = map(sum, zip(self.evManager.player[index].position, bias))
        if self.evManager.player[index].is_freeze == 1:
            self.blit_at_center(self.player_freeze_images[index], position)
            self.blit_at_center(self.icon_dizzy, postion)
        else:
            direction = self.evManager.player[index].direction
            self.blit_at_center(self.player_images[index][direction], position)
        if self.evManager.player[index].mode == 0:
            self.blit_at_center(self.icon_attack, position)
        else:
            self.blit_at_center(self.icon_protect, position)
        
    def blit_at_center(self, surface, position):
        (Xsize, Ysize) = surface.get_size()
        self.screen.blit(surface, (position[0]-Xsize/2, position[1]-Ysize/2))


