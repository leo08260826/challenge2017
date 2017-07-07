import pygame as pg
import random

import Model.main as model
from EventManager import *
from View.const import *

import Model.const as modelConst

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

        self.sound = []
        self.menu_music = None
        self.shoot_music = None

        self.love_images = []
        self.light_images = []
        self.not18_images = []
        self.rose_images = []
        self.rain_images = []
        
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick) and self.isinitialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            elif cur_state == model.STATE_PLAY:
                self.render_play()
            elif cur_state == model.STATE_STOP:
                self.render_stop()
            elif cur_state == model.STATE_PRERECORD:
                self.render_prerecord()
            elif cur_state == model.STATE_RECORD:
                self.render_record()

            self.display_fps()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(FramePerSec)
        elif isinstance(event, Event_ConfirmAction):
            player = self.model.players[event.PlayerIndex]
            if event.ActionIndex == 1 and player.mode == 0:
                self.stuns[player.index] = [player.position, 0]
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
        #music
        pg.mixer.music.pause()
        if pg.mixer.get_busy() == False:
            self.menu_music.play()
        
        # draw backgound
        menu = pg.image.load('View/image/background/menu.png')
        self.screen.blit(menu,(0,0))
        # write some word
        somewords = self.smallfont.render(
                    "Press 'Space' to play, 'Esc' to exit.", 
                    True, (255,200, 14))
        (SurfaceX, SurfaceY) = somewords.get_size()
        pos_x = (ScreenSize[0] - SurfaceX)/2
        pos_y = (ScreenSize[1] - SurfaceY)/2 + 180
        self.screen.blit(somewords, (pos_x, pos_y))
        # update surface
        pg.display.flip()
        
    def render_play(self):
        """
        Render the game play.
        """
        # music
        pg.mixer.music.unpause()
        self.menu_music.stop()
        
        # draw backgound
        self.render_background()
        self.render_timebar()

        for i in range(modelConst.PlayerNum):
            self.render_player_status(i)

        for stun in self.stuns:
            if stun[1] in range(9):
                self.blit_at_center(self.stun_images[stun[1]], stun[0])
                stun[1] += 1
        for i in range(modelConst.PlayerNum):
            self.render_player_character(i)
            
        for i in range(modelConst.numberOfQuaffles):
            self.render_quaffle(i)
        self.render_goldenSnitch()

        for barrier in self.model.barriers:
            self.render_barrier(barrier)

        # update surface
        pg.display.flip()
        
        
    def render_stop(self):
        """
        Render the stop screen.
        """
        # music
        pg.mixer.music.pause()
        
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

    def render_prerecord(self):
        pass

    def render_record(self):
        pass

    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(GameCaption, self.clock.get_fps())
        pg.display.set_caption(caption)
        
    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        #music
        pg.mixer.init()
        self.menu_music=pg.mixer.Sound('View/music/harry.ogg')
        choose_music=random.randint(1,5)
        pg.mixer.music.load('View/music/playmusic'+str(choose_music)+'.ogg')
        self.shoot_music=pg.mixer.Sound('View/music/shoot.ogg')
        for i in range(5):
            self.sound.append(pg.mixer.Sound('View/music/magic'+str(i+1)+'.ogg'))

        self.menu_music.set_volume(menu_music_volume)
        pg.mixer.music.set_volume(background_music_volume)
        
        #playmusic
        pg.mixer.music.play(-1)
        pg.mixer.music.pause()
        
        result = pg.init()
        pg.font.init()
        pg.display.set_caption(GameCaption)
        self.screen = pg.display.set_mode(ScreenSize)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(None, 40)
        self.isinitialized = True
        self.stuns = [[(0,0),-1] for _ in range(modelConst.PlayerNum)]
        # load images
        ''' backgrounds '''
        self.map = pg.image.load('View/image/background/map.png')
        self.map_gray = pg.image.load('View/image/background/map_grayscale.png')
        self.time = pg.image.load('View/image/background/time.png')
        self.background = pg.image.load('View/image/background/backgroundfill.png')
        self.playerInfo = [ pg.image.load('View/image/background/info'+str(i+1)+'.png') for i in range(modelConst.PlayerNum) ]
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
        self.barrier_images = [ [pg.image.load('View/image/barrierSimple/barrier'+str(j%4+1)+'.png') for j in range(9)] for i in range(modelConst.PlayerNum) ]
        ''' balls '''
        self.ball_powered_images = [ pg.image.load('View/image/ball/ball'+str(i%2+1)+'_powered.png') for i in range(modelConst.numberOfQuaffles) ]
        self.ball_normal_images = [ pg.image.load('View/image/ball/ball'+str(i%2+1)+'.png') for i in range(modelConst.numberOfQuaffles) ]
        self.goldenSnitch_images = [ pg.image.load('View/image/ball/goldball_'+str(i+1)+'.png') for i in range(2) ]
        ''' characters '''
        self.take_ball_images = [ pg.image.load('View/image/icon/icon_haveball'+str(i%2+1)+'.png') for i in range(modelConst.numberOfQuaffles)]
        directions = ['_leftup', '_left', '_leftdown', '_down']
        colors = ['blue', 'red', 'yellow', 'green']
        self.player_freeze_images = [pg.transform.scale(pg.image.load('View/image/player/player_down_'+colors[i]+'_frost.png'),Player_Size) for i in range(4)]
        charactor_name =['cat','black','shining','silver']
        self.player_photo = [pg.image.load('View/image/'+charactor_name[i]+'/'+charactor_name[i]+'-normal-'+colors[i]+'.png') for i in range(modelConst.PlayerNum)]
        self.player_photo_hurt = [pg.image.load('View/image/'+charactor_name[i]+'/'+charactor_name[i]+'-hurt-'+colors[i]+'.png') for i in range(modelConst.PlayerNum)]

        # visual effect
        self.love_images = [pg.image.load('View/image/visual_effect/love/love_'+str(i%4+1)+'.png') for i in range(4) ]
        self.light_images = [pg.image.load('View/image/visual_effect/light3/light3_'+str(i%4+1)+'.png') for i in range(4) ]
        self.not18_images = [pg.image.load('View/image/visual_effect/18/18_'+str(i%4+1)+'.png') for i in range(4) ]
        self.rain_images = [pg.image.load('View/image/visual_effect/rain/rain_'+str(i%4+1)+'.png') for i in range(4) ]
        
        self.photo_effect = [pg.image.load('View/image/visual_effect/photo_effect/effect_'+str(i)+'.png') for i in range(6)]
        
        def get_player_image(colorname, direction, suffix):
            if direction == 0:
                direction = 5
            if direction == 1:
                return pg.transform.flip(pg.image.load('View/image/player/player_down_'+colorname+suffix+'.png'), 0, 1)
            elif direction in range(2,6):
                return pg.transform.flip(pg.image.load('View/image/player/player'+directions[direction-2]+'_'+colorname+suffix+'.png'), 1, 0)
            else:
                return pg.image.load('View/image/player/player'+directions[8-direction]+'_'+colorname+suffix+'.png')
        self.player_images = [ [pg.transform.scale(get_player_image(colors[i],direction,''), Player_Size) for direction in range(9)] for i in range(modelConst.PlayerNum) ]
        self.player_invisible_images = [ [pg.transform.scale(get_player_image(colors[i],direction,'_invisible'), Player_Size) for direction in range(9)] for i in range(4) ]

    def render_background(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.map, Pos_map)
    def render_timebar(self):
        self.screen.blit(self.time, Pos_time)
        pg.draw.rect(self.screen, (136, 0, 21), [Pos_time[0]+60,Pos_time[1],635*(1-self.model.timer/modelConst.initTime),40])

    def render_player_status(self, index):
        player = self.model.players[index]
        pos_x , pos_y = 750 , (20 + 180*index)
            
 #     background display        
        info = self.playerInfo[index]
        self.screen.blit(info,(pos_x,pos_y))

 #      player photo display
        if player.isFreeze :
             self.screen.blit(self.player_photo_hurt[index], (pos_x+20,pos_y+20))
        else:
             self.screen.blit(self.player_photo[index],(pos_x+20,pos_y+20))
         
 #       icon display       
        if player.isFreeze:
             self.screen.blit(self.player_status0,(pos_x+150,pos_y + 20))
        if player.isMask:       
             self.screen.blit(self.player_status1,(pos_x+150,pos_y + 50))   
        if not player.isVisible:
             self.screen.blit(self.player_status2,(pos_x+150,pos_y + 80))
        if player.mode == 1:
             self.screen.blit(self.player_status_P,(pos_x+150,pos_y + 110))
        elif player.mode == 0:
             self.screen.blit(self.player_status_A,(pos_x+150,pos_y + 110))
#       render effect
        effect_type = player_visual_effect[index]
        self.screen.blit(self.photo_effect[effect_type],(pos_x+20,pos_y+20))       
 #      mana and score and name
        score = self.smallfont.render(str(player.score),  True, (255,200, 14))
        mana = self.smallfont.render(str(player.power),  True, (255,200, 14))
        name = self.smallfont.render(player.name,True,(255,200,14))
        self.screen.blit(score,(pos_x + 215,pos_y + 95))
        self.screen.blit(mana,(pos_x + 335,pos_y + 95))
        self.screen.blit(name,(pos_x + 285,pos_y + 20))

    def render_player_character(self, index):
        player = self.model.players[index]
        position = player.position
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

        #visual effect
        visual_temp = self.get_frame() % 12
        if visual_temp <=2:
            visual_temp = 0
        elif visual_temp <= 5:
            visual_temp = 1
        elif visual_temp <= 8:
            visual_temp = 2
        elif visual_temp <= 11:
            visual_temp = 3
            
        if player_visual_effect[index] == 1:
            self.blit_at_center(self.love_images[visual_temp], position)
        if player_visual_effect[index] == 2:
            self.blit_at_center(self.light_images[visual_temp], position)
        if player_visual_effect[index] == 3:
            self.blit_at_center(self.not18_images[visual_temp], position)
        if player_visual_effect[index] == 5:
            self.blit_at_center(self.rain_images[visual_temp], position)
            
        # mask
        if player.isMask == True:
            self.blit_at_center(self.mask_images[self.get_frame() % 12], position)

    def render_quaffle(self, index):
        quaffle = self.model.quaffles[index]
        if quaffle.state != 1 and quaffle.state != 3:
            if quaffle.isStrengthened == True:
                self.blit_at_center(self.ball_powered_images[index], quaffle.position)
            else:
                self.blit_at_center(self.ball_normal_images[index], quaffle.position)

    def render_goldenSnitch(self):
        if self.model.goldenSnitch.state != 1:
            frame = self.get_frame() % 2
            self.blit_at_center(self.goldenSnitch_images[frame], self.model.goldenSnitch.position)
            

    def render_barrier(self,barrier):
        self.blit_at_center(self.barrier_images[barrier.playerIndex][barrier.direction], barrier.position)
        
    def blit_at_center(self, surface, position):
        (Xsize, Ysize) = surface.get_size()
        self.screen.blit(surface, (int(position[0]-Xsize/2), int(position[1]-Ysize/2)))

    def get_frame(self):
        return int(pg.time.get_ticks()*FramePerSec/1000)
