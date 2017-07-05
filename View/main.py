import pygame as pg

import Model.main as model
from EventManager import *
from const_main import *
from View.const import *

# import Model.GameObject.model_const as mc

numberOfQuaffles = 2

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
        self.player_bias = []
        self.stuns = []
    
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
        elif isinstance(event, Event_Action):
            player = self.model.players[event.PlayerIndex]
            if event.ActionIndex == 1 and player.mode == 0:
                self.stuns[player.index] = [player.positon, 0]
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
        self.screen.blit(self.background,(0,0))
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
            
        for i in range(numberOfQuaffles):
            self.render_quaffle(i)
        self.render_goldenSnitch()

        for stun in self.stuns:
            if stun[1] in range(9):
                self.blit_at_center(self.stun_images[stun[1]], stun[0])
                stun[1] += 1
        for barrier in self.model.barriers:
            self.render_barrier(barrier)

        # update surface
        pg.display.flip()
        
        
    def render_stop(self):
        """
        Render the stop screen.
        """
        # draw background
        self.screen.blit(self.background,(0,0))
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
        self.stuns = [[(0,0),-1] for _ in range(PlayerNum)]
        # load images
        ''' backgrounds '''
        self.map = pg.image.load('View/image/background/map.png')
        self.map_gray = pg.image.load('View/image/background/map_grayscale.png')
        self.time = pg.image.load('View/image/background/time.png')
        self.background = pg.image.load('View/image/background/backgroundfill.png')
        self.playerInfo = [ pg.image.load('View/image/background/info'+str(i+1)+'.png') for i in range(PlayerNum) ]
        ''' icons '''
        self.mode_images = [ pg.image.load('View/image/icon/icon_attack.png'),
                            pg.image.load('View/image/icon/icon_protectmode.png')]
        self.player_status0 = pg.image.load('View/image/icon/dizzyOninfo.png')
        self.player_status1 = pg.image.load('View/image/icon/shieldOninfo.png')
        self.player_status2 = pg.image.load('View/image/icon/shadowOninfo.png')
        self.player_status_A = pg.image.load('View/image/icon/attackmodeOninfo.png')
        self.player_status_P = pg.image.load('View/image/icon/protectmodeOninfo.png')
        ''' skills '''
        self.stun_images = [ pg.image.load('View/image/skill/magicfield_'+str(i+1)+'.png') for i in range(9) ]
        self.mask_images = [ pg.image.load('View/image/skill/shield_'+str(i+1)+'.png' )for i in range(12) ]
        self.barrier_images = [ [pg.image.load('View/image/barrierSimple/barrier'+str(j%4+1)+'.png') for j in range(4)] for i in range(PlayerNum) ]
        ''' balls '''
        self.ball_powered_images = [ pg.image.load('View/image/ball/ball'+str(i%2+1)+'_powered.png') for i in range(numberOfQuaffles) ]
        self.ball_normal_images = [ pg.image.load('View/image/ball/ball'+str(i%2+1)+'.png') for i in range(numberOfQuaffles) ]
        self.goldenSnitch_images = [ pg.image.load('View/image/ball/goldball_'+str(i+1)+'.png') for i in range(2) ]
        ''' characters '''
        self.take_ball_images = [ pg.image.load('View/image/icon/icon_haveball'+str(i%2+1)+'.png') for i in range(numberOfQuaffles)]
        directions = ['_leftup', '_left', '_leftdown', '_down']
        colors = ['_blue', '_yellow', '_red', '_green']
        self.player_freeze_images = [pg.image.load('View/image/player/player_down'+colors[i]+'_frost.png') for i in range(4)]
        
        def get_player_image(colorname, direction, suffix):
            if direction == 0:
                direction = 5
            if direction == 1:
                return pg.transform.flip(pg.image.load('View/image/player/player_down'+colorname+suffix+'.png'), 0, 1)
            elif direction in range(2,6):
                return pg.transform.flip(pg.image.load('View/image/player/player'+directions[direction-2]+colorname+suffix+'.png'), 1, 0)
            else:
                return pg.image.load('View/image/player/player'+directions[8-direction]+colorname+suffix+'.png')
        self.player_images = [ [get_player_image(colors[i],direction,'') for direction in range(9)] for i in range(4) ]
        self.player_invisable_images = [ [get_player_image(colors[i],direction,'_invisible') for direction in range(9)] for i in range(4) ]
        
    def render_background(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.map, Pos_map)
        self.screen.blit(self.time, Pos_time)
        
    def render_player_status(self, index):
        player = self.model.players[index]
        info = pg.image.load('View/image/background/info'+str(index+1)+'.png')
        self.blit_at_center(info,(980,100+180*index))
        player = self.model.players[index]
        info = self.playerInfo[index]
        pos_x , pos_y = 750 , 20 + 180*index
        pos = (pos_x,pos_y)
        self.screen.blit(info,pos)
        
#unfinished        
#        if player.isFreeze:
#            self.screen.blit(self.player_status0,)
        pass

    def render_player_character(self, index):
        player = self.model.players[index]
        if pg.time.get_ticks() % (FramePerSec*3) == biasrand[index]:
            self.player_bias[index] = ( self.player_bias[index] + 1 ) % 2
        bias = (2,2) if self.player_bias[index] else (-2,-2)
        position = (player.position[0] - bias[0], player.position[1] - bias[1])
        # body
        if player.isVisible == False:
            direction = player.direction
            self.blit_at_center(self.player_invisible_images[index][direction], position)
        elif player.isFreeze == 1:
            self.blit_at_center(self.player_freeze_images[index], position)
        else:
            direction = player.direction
            self.blit_at_center(self.player_images[index][direction], position)
        # mode
        self.blit_at_center(self.mode_images[player.mode], position)
        # ball
        ball = player.takeball
        if ball != -1:
            self.blit_at_center(self.take_ball_images[ball], position)

        # mask
        if player.isMask == True:
            self.blit_at_center(self.mask_images[pg.time.get_ticks() % 12], position)

    def render_quaffle(self, index):
        quaffle = self.model.quaffles[index]
        if quaffle.state != 1:
            if quaffle.isStrengthened == True:
                self.blit_at_center(self.ball_powered_images[index], quaffle.position)
            else:
                self.blit_at_center(self.ball_normal_images[index], quaffle.position)

    def render_goldenSnitch(self):
        if self.model.goldenSnitch.state != 1:
            self.blit_at_center(self.goldenSnitch_images[pg.time.get_ticks() % 2], self.model.goldenSnitch.position)

    def render_barrier(self,barrier):
        self.blit_at_center(self.barrier_images[barrier.playerIndex][barrier.direction], barrier.position)
        
    def blit_at_center(self, surface, position):
        (Xsize, Ysize) = surface.get_size()
        self.screen.blit(surface, (position[1]-Xsize/2, position[1]-Ysize/3))
