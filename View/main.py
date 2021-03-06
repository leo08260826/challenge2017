import pygame as pg
import random

import Model.main as model
from EventManager import *
from View.const import *

import Model.const as modelConst

class GraphicalView(object):
    # Draws the model state onto the screen.
    def __init__(self, evManager, model):
        # evManager (EventManager): Allows posting messages to the event queue.
        # model (GameEngine): a strong reference to the game Model.
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
        self.record_music = None
        self.record_haveplay = 0

        self.love_images = []
        self.light_images = []
        self.not18_images = []
        self.rose_images = []
        self.rain_images = []
        self.boss_images = []
        self.fly_images = []
        self.jump_status = []

        self.using_magic = [-1,-1,-1,-1]
        self.magic_timer = [0,0,0,0]

        self.winner = -1
        
    def notify(self, event):
        # Receive events posted to the message queue. 
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
        elif isinstance(event, Event_SkillCard):
            self.play_magic(event.PlayerIndex,event.SkillIndex)
        elif isinstance(event, Event_CallMe) and self.jump_status[event.PlayerIndex] == jump_frame:
            self.jump_status[event.PlayerIndex] = 0
        elif isinstance(event, Event_Initialize):
            self.initialize()
        elif isinstance(event, Event_Quit):
            # shut down the pygame graphics
            self.isinitialized = False
            pg.quit()
    
    def render_menu(self):
        # Render the game menu.
        try:
            #music
            pg.mixer.music.pause()
            if pg.mixer.get_busy() == False:
                self.menu_music.play()
        except:
            pass
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
        # Render the game play.
        try:
            
            # music
            pg.mixer.music.unpause()
            self.menu_music.stop()
            self.record_music.stop()
            self.record_haveplay = 0
        except:
            pass
        # draw backgound
        self.render_background()
            
        self.render_timebar()
        self.screen.blit(self.logo,(750,740))

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
            if barrier.playerIndex == 0:
                self.screen.blit(self.new_barrier_images_horizontal,(280,0))
            elif barrier.playerIndex == 1:
                self.screen.blit(self.new_barrier_images_vertical,(720,280))
            elif barrier.playerIndex == 2:
                self.screen.blit(self.new_barrier_images_horizontal,(280,720))
            elif barrier.playerIndex == 3:
                self.screen.blit(self.new_barrier_images_vertical,(0,280))
                
        self.render_magic_effect()
        
        # update surface
        pg.display.flip()
        
        
    def render_stop(self):
        # Render the stop screen.
        try:
            # music
            pg.mixer.music.pause()
        except:
            pass
        # draw background
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.map_gray,(0,0))
    
        # display words
        somewords = self.smallfont.render( 'Pause', True, (255, 0, 0))
        self.blit_at_center(somewords, (ScreenSize[0]/2, ScreenSize[1]/2))
        
        # update surface
        pg.display.flip()
    
    def render_record(self):
        # Render the Soreboard
        try:
            pg.mixer.music.pause()
            self.menu_music.stop()
            if pg.mixer.get_busy() == False and self.record_haveplay == 0:
                self.record_haveplay =1
                self.record_music.play(0)
        except:
            pass
        
        self.screen.blit(self.ending_background, (0,0))
        ranked = sorted(self.model.players, key=lambda player:-player.score)
        maxscore = max(ranked[0].score, 1)
        lastscore = maxscore+1
        lastrank = 0
        for i in range(modelConst.PlayerNum):
            score = ranked[i].score
            rank = i if score < lastscore else lastrank
            lastrank = rank
            lastscore = score
            height = score / maxscore * 450
            color = Player_Colors[ranked[i].index]
            pg.draw.rect(self.screen, Color_White, (260+200*i, 600-height, 120, height+1))
            self.screen.blit(self.pennant_images[ranked[i].index], (260+200*i,610-height))
            self.screen.blit(self.player_photo[ranked[i].index], (260+200*i,600))
            #visual effect
            if i == self.winner:
                self.screen.blit(self.win_hat,(260+200*i,600))
                    # render effect
            if self.model.players[ranked[i].index].IS_AI:
                ef = self.model.players[ranked[i].index].AI.effect
            else:
                ef = 0
            effect_type = ef
            self.screen.blit(self.photo_effect[effect_type],(260+200*i,600))
            
            pg.draw.rect(self.screen, Color_White, (260+200*i, 600-height, 120, 70))
            self.screen.blit(self.rank_images[rank], (260+200*i,600-height))
            score_surface = self.smallfont.render(str(score), True, color)
            self.blit_at_center(score_surface, (320+200*i, 655-height))

        # update surface
        pg.display.flip()


    def render_prerecord(self):
        try:
            # music
            pg.mixer.music.unpause()
            self.menu_music.stop()
            self.record_music.stop()
            self.record_haveplay = 0
        except:
            pass
        # draw backgound
        self.render_background()
            
        self.render_timebar()
        self.screen.blit(self.logo,(750,740))

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
            if barrier.playerIndex == 0:
                self.screen.blit(self.new_barrier_images_horizontal,(280,0))
            elif barrier.playerIndex == 1:
                self.screen.blit(self.new_barrier_images_vertical,(720,280))
            elif barrier.playerIndex == 2:
                self.screen.blit(self.new_barrier_images_horizontal,(280,720))
            elif barrier.playerIndex == 3:
                self.screen.blit(self.new_barrier_images_vertical,(0,280))
                
        self.render_magic_effect()
        

        somewords = self.smallfont.render( 'Time\'s up. Press space to see the record.', True, (255, 0, 1))
        self.blit_at_center(somewords, (ScreenSize[0]/2, ScreenSize[1]/2))

        # update surface
        pg.display.flip()


    def display_fps(self):
        # Show the programs FPS in the window handle.
        caption = "{} - FPS: {:.2f}".format(GameCaption, self.clock.get_fps())
        pg.display.set_caption(caption)
        
    def initialize(self):
        # Set up the pygame graphical display and loads graphical resources.
        #music
        try:
            pg.mixer.init()
            self.menu_music=pg.mixer.Sound('View/music/harry.ogg')
            if is_boss_music == 1:
                self.record_music=pg.mixer.Sound('View/music/laugh.ogg')
            else:
                self.record_music=pg.mixer.Sound('View/music/goldenhorse.ogg')
            choose_music=random.randint(1,4)
            if is_final_music == 1 or is_boss_music == 1:
                pg.mixer.music.load('View/music/finalgame.ogg')
            else:
                pg.mixer.music.load('View/music/playmusic'+str(choose_music)+'.ogg')
            self.shoot_music=pg.mixer.Sound('View/music/shoot.ogg')
            for i in range(4):
                self.sound.append(pg.mixer.Sound('View/music/magic'+str(i+1)+'.ogg'))

            self.menu_music.set_volume(menu_music_volume)
            self.record_music.set_volume(record_music_volume)
            pg.mixer.music.set_volume(background_music_volume)
            
            #playmusic
            pg.mixer.music.play(-1)
            pg.mixer.music.pause()
        except:
            print("no audio")
        #playmusic_end
        

        result = pg.init()
        pg.font.init()
        pg.display.set_caption(GameCaption)
        self.screen = pg.display.set_mode(ScreenSize)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(None, 40)
        self.stuns = [[(0,0),-1] for _ in range(modelConst.PlayerNum)]
        self.jump_status = [jump_frame]*modelConst.PlayerNum
        # load images
        ''' backgrounds '''
        directions = ['_leftup', '_left', '_leftdown', '_down']
        colors = ['blue', 'red', 'yellow', 'green']
        self.map = pg.image.load('View/image/background/map.png')
        self.map_gray = pg.image.load('View/image/background/map_grayscale.png')
        self.time = pg.image.load('View/image/background/timebar.png')
        self.background = pg.image.load('View/image/background/backgroundfill.png')
        self.ending_background = pg.image.load('View/image/background/ending.png')
        self.playerInfo = [ pg.image.load('View/image/background/info'+str(i+1)+'.png') for i in range(modelConst.PlayerNum) ]
        self.pennant_images = [ pg.image.load('View/image/scoreboard/pennant_'+colors[i]+'.png') for i in range(modelConst.PlayerNum) ]
        self.rank_images = [ pg.image.load('View/image/scoreboard/ranktag_'+str(i+1)+'.png') for i in range(modelConst.PlayerNum) ]
        self.logo = pg.image.load('View/image/logo/logo_proto.png')
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
        """self.barrier_images = [ [pg.image.load('View/image/barrierSimple/barrier'+str(j%4+1)+'.png') for j in range(9)] for i in range(modelConst.PlayerNum) ]"""
        self.new_barrier_images_vertical = pg.image.load('View/image/barrier/barrier_vertical.png')
        self.new_barrier_images_horizontal = pg.image.load('View/image/barrier/barrier_horizontal.png')
        ''' balls '''
        self.ball_powered_images = [ pg.image.load('View/image/ball/ball'+str(i%2+1)+'_powered.png') for i in range(modelConst.numberOfQuaffles) ]
        self.ball_normal_images = [ pg.image.load('View/image/ball/ball'+str(i%2+1)+'.png') for i in range(modelConst.numberOfQuaffles) ]
        self.goldenSnitch_images = [ pg.image.load('View/image/ball/goldball_'+str(i+1)+'.png') for i in range(2) ]
        ''' characters '''
        self.take_ball_images = [ pg.image.load('View/image/icon/icon_haveball'+str(i%2+1)+'.png') for i in range(modelConst.numberOfQuaffles)]
        self.take_goldenSnitch_image = pg.image.load('View/image/icon/icon_havegolden.png')
        self.player_freeze_images = [pg.transform.scale(pg.image.load('View/image/player/player_down_'+colors[i]+'_frost.png'),Player_Size) for i in range(4)]
        charactor_name =['cat','black','shining','silver']
        self.player_photo = [pg.image.load('View/image/'+charactor_name[i]+'/'+charactor_name[i]+'-normal-'+colors[i]+'.png') for i in range(modelConst.PlayerNum)]
        self.player_photo_hurt = [pg.image.load('View/image/'+charactor_name[i]+'/'+charactor_name[i]+'-hurt-'+colors[i]+'.png') for i in range(modelConst.PlayerNum)]

        # using magic
        self.magic_effect_image = [pg.image.load('View/image/magic/magic_'+str(i)+'.png') for i in range(3)]
        self.win_hat = pg.image.load('View/image/magic/win_hat.png')
        
        # visual effect
        self.love_images = [pg.image.load('View/image/visual_effect/love/love_'+str(i%4+1)+'.png') for i in range(4) ]
        self.light_images = [pg.image.load('View/image/visual_effect/light3/light3_'+str(i%4+1)+'.png') for i in range(4) ]
        self.not18_images = [pg.image.load('View/image/visual_effect/18/18_'+str(i%4+1)+'.png') for i in range(4) ]
        self.rain_images = [pg.image.load('View/image/visual_effect/rain2/rain2_'+str(i%4+1)+'.png') for i in range(4) ]
        self.boss_images = [pg.image.load('View/image/visual_effect/boss3/boss3_'+str(i%4+1)+'.png') for i in range(4) ]
        self.fly_images = [pg.image.load('View/image/visual_effect/fly/fly_'+str(i%4+1)+'.png') for i in range(4) ]
        self.rose_images = [pg.image.load('View/image/visual_effect/rose/rose_'+str(i%4+1)+'.png') for i in range(4) ]
        
        self.photo_effect = [pg.image.load('View/image/visual_effect/photo_effect/effect_'+str(i)+'.png') for i in range(8)]

        
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
        
        self.isinitialized = True

    def render_background(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.map, Pos_map)
    def render_timebar(self):
        self.screen.blit(self.time, Pos_time)
        pg.draw.rect(self.screen, (136, 0, 21), [Pos_time[0]+63,Pos_time[1],634*(1-self.model.timer/modelConst.initTime),40])

    def render_player_status(self, index):
        player = self.model.players[index]
        pos_x , pos_y = 750 , (20 + 180*index)
            
        # background display        
        info = self.playerInfo[index]
        self.screen.blit(info,(pos_x,pos_y))

        # player photo display
        if player.isFreeze :
             self.screen.blit(self.player_photo_hurt[index], (pos_x+20,pos_y+20-jump_frames[self.jump_status[index]]))
        else:
             self.screen.blit(self.player_photo[index],(pos_x+20,pos_y+20-jump_frames[self.jump_status[index]]))
        if self.jump_status[index] != jump_frame:
            self.jump_status[index] += 1
         
        if index == self.winner:
            self.screen.blit(self.win_hat,(pos_x+20,pos_y+20))
            
        # icon display       
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
        # render effect
        if self.model.players[index].IS_AI:
            ef = self.model.players[index].AI.effect
        else:
            ef = 0
        self.screen.blit(self.photo_effect[ef],(pos_x+20,pos_y+20))
        
        # mana and score and name
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
        
        if self.model.players[index].IS_AI:
            ef = self.model.players[index].AI.effect
        else:
            ef = 0
    
    
        if ef == 1:
            self.blit_at_center(self.love_images[visual_temp], position)
        elif ef == 2:
            self.blit_at_center(self.light_images[visual_temp], position)
        elif ef == 3:
            self.blit_at_center(self.not18_images[visual_temp], position)
        elif ef == 4:
            self.blit_at_center(self.rose_images[visual_temp], position)
        elif ef == 5:
            self.blit_at_center(self.rain_images[visual_temp], position)
        elif ef == 6:
            self.blit_at_center(self.fly_images[visual_temp], position)
        elif ef == 7:
            self.blit_at_center(self.boss_images[visual_temp], position)

        # mode
        self.blit_at_center(self.mode_images[player.mode], position)
        # ball
        ball = player.takeball
        if ball == 100:
            self.blit_at_center(self.take_goldenSnitch_image, position)
        elif ball != -1:
            self.blit_at_center(self.take_ball_images[ball], position)

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
            
        
    def blit_at_center(self, surface, position):
        (Xsize, Ysize) = surface.get_size()
        self.screen.blit(surface, (int(position[0]-Xsize/2), int(position[1]-Ysize/2)))

    def get_frame(self):
        return int(pg.time.get_ticks()*FramePerSec/1000)

    def play_magic(self,index_player,index_magic):
        if self.model.players[index_player].AI.skill[index_magic] >= 0:
            try:
                self.sound[index_magic].set_volume(magic_music_volume)
                self.sound[index_magic].play(0)
            except:
                pass
            if not index_magic == 3:
                self.using_magic[index_player] = index_magic
                self.magic_timer[index_player] = 50
            else:
                self.winner = index_player
            
    def render_magic_effect(self):
        for index in range(modelConst.PlayerNum):
            if not self.using_magic[index] == -1:
                self.magic_timer[index] = self.magic_timer[index] - 1
                if self.magic_timer[index] == 0:
                    self.using_magic[index] = -1

        for index in range(modelConst.PlayerNum):
            if not self.using_magic[index] == -1:
                pos_y = 20 + 180*index
                self.screen.blit(self.magic_effect_image[self.using_magic[index]],(0,pos_y))
