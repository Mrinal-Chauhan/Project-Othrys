import pygame
from sys import exit
from pickle import load, dump
from settings import *
from player import Player
from camera import Camera
from enemy import EnemyHandle
from mechanics import Collision, Draw, Stats

class Game:
    
    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Etheral')
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        self.run = True
        
        self.state = 'start screen'   
        self.game_restart = True
        self.quit_flag = True
        

    def splash_screen(self):
        cover_img = pygame.image.load(r'data/graphics/cover.png')
        cover_image = pygame.transform.scale(cover_img,(600,600))
        black_img = pygame.image.load(r'data/graphics/black.jpg')
        black_image = pygame.transform.scale(black_img,(WIDTH,HEIGHT))

        self.alpha = 0
        time = pygame.time.get_ticks()
        black_image.set_alpha(self.alpha)

        pygame.mixer.music.load(r'data/sfx/bgm.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        self.load()

        while True:   #thread.is_alive() and pygame.time.get_ticks() - time > 5000:
            self.screen.fill((60, 65, 105))
            self.screen.blit(cover_image,(WIDTH/2 - 300,100))
            self.screen.blit(black_image,(0,0))

            if  pygame.time.get_ticks() - time > 3000:
                black_image.set_alpha(self.alpha)
                self.alpha += 2

            if self.alpha >= 255:
                self.alpha = 255
                if pygame.time.get_ticks() - time > 7000:
                    return

            pygame.display.update()
            self.clock.tick(60)


    def load(self):

        shop_shield = pygame.image.load(r'data/graphics/shield.jpeg').convert_alpha()
        self.shield_image = pygame.transform.scale(shop_shield,(164,164))
        self.shield_image_big = pygame.transform.scale(shop_shield,(256,256))
        shop_bullet = pygame.image.load(r'data/graphics/bullet.jpeg').convert_alpha()
        self.bullet_image = pygame.transform.scale(shop_bullet,(164,164))
        self.bullet_image_big = pygame.transform.scale(shop_bullet,(256,256))
        shop_burst = pygame.image.load(r'data/graphics/burst.jpeg').convert_alpha()
        self.burst_image = pygame.transform.scale(shop_burst,(164,164))
        self.burst_image_big = pygame.transform.scale(shop_burst,(256,256))
        shop_speed = pygame.image.load(r'data/graphics/speed.jpeg').convert_alpha()
        self.speed_image = pygame.transform.scale(shop_speed,(164,164))
        self.speed_image_big = pygame.transform.scale(shop_speed,(256,256))
        shop_teleport = pygame.image.load(r'data/graphics/teleport.jpeg').convert_alpha()
        self.teleport_image = pygame.transform.scale(shop_teleport,(164,164))
        self.teleport_image_big = pygame.transform.scale(shop_teleport,(256,256))
        self.frame_image = pygame.image.load(r'data/graphics/frame.png').convert_alpha()
        self.frame_image_big = pygame.image.load(r'data/graphics/frame_big2.png').convert_alpha()

        self.start_bg = pygame.image.load(r"data/space background godot/1/3.png").convert_alpha()
        death_bg_image = pygame.image.load(r'data/graphics/death.jpg')
        self.death_bg = pygame.transform.scale(death_bg_image,(WIDTH, HEIGHT))
        shop_back = pygame.image.load(r'data/graphics/127.png').convert_alpha()
        self.shop_back = pygame.transform.scale(shop_back,(50,50))

        self.purchase_sound = pygame.mixer.Sound(r'data/sfx/purchase.mp3')
        self.bgm = pygame.mixer.Sound(r'data/sfx/bgm.mp3')
        self.endscreen_font = pygame.font.Font(r'data/fonts/Burbank.otf',100)


    def game_init(self):

        # Initialize
        self.camera_group = Camera()
        self.stats = Stats()
        self.player_sprite = Player((WIDTH/2,HEIGHT/2),self.camera_group)
        self.player = pygame.sprite.Group(self.player_sprite)
        self.enemy_handle = EnemyHandle(self.camera_group,self.player_sprite)
        self.collision_instance = Collision(player=self.player_sprite, spawner=self.enemy_handle, group=self.camera_group, stats=self.stats)
        self.draw = Draw()
        self.speedpuflag = False
        Camera.bring_instances(self.enemy_handle,self.collision_instance)

        self.pause_flag = True     
        self.shop_flag = True
        self.death_flag = True
        self.score_flag = True

        # Spawner/Enemy function call  and powerup function call
        self.enemy_handle.update()


    def game_loop(self):

        while self.run:

            self.clock.tick(FPS)

            if self.state == 'start screen':

                events_list = pygame.event.get()

                for event in events_list:
                    if event.type == pygame.QUIT:
                        self.run = False
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'quit'

                bg = pygame.transform.smoothscale(self.start_bg,(WIDTH,WIDTH))
                self.screen.blit(bg,(0,-300))

                font_title = pygame.font.Font(r'data/fonts/AC.otf',100)
                text_title = font_title.render('PROJECT OTHRYS', True,(255,255,255))
                textRect = text_title.get_rect(center = (WIDTH/2,200))
                self.screen.blit(text_title, textRect)

                font_button = pygame.font.Font(r'data/fonts/AC.otf',55)
                box = pygame.transform.box_blur(bg,10)

                # Button1
                text_b1 = font_button.render('  CLASSIC  ',True,(255,255,255)) 
                rect11 = text_b1.get_rect(midtop = (WIDTH/2,350-5))
                rect12 = text_b1.get_rect(midtop = (WIDTH/2,300+350-5))
                button1 = pygame.Surface.subsurface(box,rect12)
                self.screen.blit(button1,rect11)
                self.screen.blit(text_b1, text_b1.get_rect(midtop = (WIDTH//2,350)))

                


                # Button2
                text_b2 = font_button.render('  SETTINGS  ',True,(255,255,255))
                rect21 = text_b2.get_rect(midtop = (WIDTH/2,350-5 + 80))
                rect22 = text_b2.get_rect(midtop = (WIDTH/2,300+350-5 + 80))
                button2 = pygame.Surface.subsurface(box,rect22)
                self.screen.blit(button2,rect21)
                self.screen.blit(text_b2, text_b2.get_rect(midtop = (WIDTH//2,350 + 80)))

                # Button3
                text_b3 = font_button.render('  QUIT  ',True,(255,255,255))
                rect31 = text_b3.get_rect(midtop = (WIDTH/2,350-5 + 160))
                rect32 = text_b3.get_rect(midtop = (WIDTH/2,300+350-5 + 160))
                button3 = pygame.Surface.subsurface(box,rect32)
                self.screen.blit(button3,rect31)
                self.screen.blit(text_b3, text_b3.get_rect(midtop = (WIDTH//2,350 + 160)))

                mouse = pygame.mouse.get_pos()
                if rect11.collidepoint(mouse):
                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.state = 'game'

                if rect21.collidepoint(mouse):
                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pass

                if rect31.collidepoint(mouse):
                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.state = 'quit'

                

                pygame.display.update()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_KP_ENTER]:
                    self.state = 'game'


            if self.state == 'game':

                if self.game_restart:
                    self.game_init()
                    self.game_restart = False
                    
                mouse = pygame.mouse.get_pos()
                events_list = pygame.event.get()
                death = pygame.USEREVENT + 1

                for event in events_list:

                    if event.type == pygame.QUIT:
                        self.run = False

                    if event.type == death:
                        self.game_restart = True
                        self.state = 'death screen'

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'pause'
                            self.pause_flag = True

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if self.draw.menu_rect.collidepoint(mouse):
                            self.state = 'pause'

                        if self.draw.shop_rect.collidepoint(mouse):
                            self.state = 'shop'

                if self.speedpuflag:
                    speed_event = pygame.USEREVENT + 2
                    pygame.event.post(pygame.event.Event(speed_event))
                    self.speedpuflag = False

                self.player.update()
                self.camera_group.update()
                self.collision_instance.call()
                
                self.camera_group.custom_draw(self.player_sprite)
                self.draw.draw(player=self.player_sprite, stats=self.stats)

                pygame.display.update()


            if self.state == 'pause':

                events_list = pygame.event.get()
                for event in events_list:
                    if event.type == pygame.quit:
                        pygame.quit()  
                        exit()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_ESCAPE:
                            pygame.mouse.set_pos(mouse_pos)
                            self.pause_flag = True
                            self.state = 'game'

                if self.pause_flag:
                    self.screen_pause = self.screen
                    self.time = pygame.time.get_ticks()
                    mouse_pos = pygame.mouse.get_pos()
                    self.screens_list = []
                    self.pause_flag = False
                
                if pygame.time.get_ticks() - self.time <= 2000:
                    self.screen_pause = pygame.transform.box_blur(self.screen_pause,1)
                    self.screens_list.append(self.screen_pause)

                self.screen.blit(self.screen_pause,(0,0))
                # BUTTONS
                # Button1
                text_b1 = font_button.render('RESUME',True,(255,255,255))
                rect1 = text_b1.get_rect(center= (WIDTH//2,300))
                self.screen.blit(text_b1, rect1)

                # Button2
                text_b2 = font_button.render('SETTINGS',True,(255,255,255))
                rect2 = text_b2.get_rect(center= (WIDTH//2,400))
                self.screen.blit(text_b2, rect2)

                # Button3
                text_b3 = font_button.render('EXIT',True,(255,255,255))
                rect3 = text_b3.get_rect(center= (WIDTH//2,500))
                self.screen.blit(text_b3, rect3)

                mouse = pygame.mouse.get_pos()
                if rect1.collidepoint(mouse):
                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pygame.mouse.set_pos(mouse_pos)
                            self.pause_flag = True
                            self.state = 'game'
                
                if rect2.collidepoint(mouse):
                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.pause_flag = True
                            # self.state = 'settings'
                
                if rect3.collidepoint(mouse):
                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.pause_flag = True
                            self.game_restart = True
                            self.state = 'start screen'

                pygame.display.update()


            if self.state == 'death screen':

                events_list = pygame.event.get()

                for event in events_list:
                    if event.type == pygame.QUIT:
                        self.run = False
                        
                if self.death_flag:
                    self.death_flag = False
                    self.screen_pause = self.screen
                    self.time = pygame.time.get_ticks()
                    # count = 1
                
                if pygame.time.get_ticks() - self.time <= 2500:
                    # if count%2 == 0:
                    self.screen_pause = pygame.transform.box_blur(self.screen_pause,1)
                    # count+=1

                    self.screen.blit(self.screen_pause,(0,0))
                
                else:
                    
                    self.screen.blit(self.screen_pause,(0,0))
                                

                    # BUTTONS
                    # Button1
                    text_b1 = font_button.render('NEW GAME',True,(255,255,255))
                    rect1 = text_b1.get_rect(center= (WIDTH//2,400))
                    self.screen.blit(text_b1, rect1)

                    # Button2
                    text_b2 = font_button.render('SETTINGS',True,(255,255,255))
                    rect2 = text_b2.get_rect(center= (WIDTH//2,500))
                    self.screen.blit(text_b2, rect2)

                    # Button3
                    text_b3 = font_button.render('EXIT',True,(255,255,255))
                    rect3 = text_b3.get_rect(center= (WIDTH//2,600))
                    self.screen.blit(text_b3, rect3)

                    mouse = pygame.mouse.get_pos()

                    if rect1.collidepoint(mouse):
                        for event in events_list:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                self.pause_flag = True
                                self.state = 'game'
                    
                    if rect2.collidepoint(mouse):
                        for event in events_list:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                self.pause_flag = True
                                self.state = 'settings'
                    
                    if rect3.collidepoint(mouse):
                        for event in events_list:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                self.pause_flag = True
                                self.state = 'start screen'


                    ######## SCORE  ########
                    if self.score_flag:
                        self.score_flag = False
                        scores = []
                        with open('score.et','ab') as file:
                            dump(self.stats.score,file)
                        with open('score.et','rb') as file:
                            while True:
                                try:
                                    scores.append(load(file))
                                except EOFError:
                                    break
                            if max(scores) == self.stats.score:
                                self.highscore = True
                            else:
                                self.highscore = False

                    if not self.highscore:
                        
                        highscore_text = self.endscreen_font.render('SYSTUM DOWN',True,(255,255,255))
                        highscore_rect = highscore_text.get_rect(center= (WIDTH//2,150))
                        self.screen.blit(highscore_text,highscore_rect)

                    else:
                        highscore_text = self.endscreen_font.render('HIGHSCORE',True,(255,255,255))
                        highscore_rect = highscore_text.get_rect(center= (WIDTH//2,150))
                        self.screen.blit(highscore_text,highscore_rect)

                pygame.display.update()          


            if self.state == 'shop':

                events_list = pygame.event.get()

                for event in events_list:
                    if event.type == pygame.QUIT:
                        self.run = False

                if self.shop_flag:
                    self.screen_shop = self.screen
                    self.time = pygame.time.get_ticks()
                    mouse_pos = pygame.mouse.get_pos()
                    self.shop_flag = False
                
                if pygame.time.get_ticks() - self.time <= 2000:
                    self.screen_shop = pygame.transform.box_blur(self.screen_shop,1)

                self.screen.blit(self.screen_shop,(0,0))
                
                
                self.font = pygame.font.Font(r'data/fonts/AC.otf',65)
                
                # SURFACES/RECTS
                text_shield = self.font.render('S H I E L D',True,(255,255,255))
                text_speed = self.font.render('S P E E D',True,(255,255,255))
                text_bullet = self.font.render('B U L L E T',True,(255,255,255))
                text_burst = self.font.render('B U R S T   F I R E',True,(255,255,255))
                text_teleport = self.font.render('T E L E P O R T',True,(255,255,255))

                self.shield_rect = self.shield_image.get_rect(midleft = (73, HEIGHT/2))
                self.bullet_rect = self.bullet_image.get_rect(midleft = (73+164+100, HEIGHT/2))
                self.speed_rect = self.speed_image.get_rect(midleft = (73+164*2+100*2, HEIGHT/2))
                self.burst_rect = self.burst_image.get_rect(midleft = (73+164*3+100*3, HEIGHT/2))
                self.teleport_rect = self.teleport_image.get_rect(midleft = (73+164*4+100*4, HEIGHT/2))

                self.back_rect = self.shop_back.get_rect(bottomright = (WIDTH-10,HEIGHT-10))

                # BLIT
                self.screen.blit(self.shield_image,self.shield_rect)     
                self.screen.blit(self.bullet_image,self.bullet_rect)
                self.screen.blit(self.speed_image,self.speed_rect)
                self.screen.blit(self.burst_image,self.burst_rect)
                self.screen.blit(self.teleport_image,self.teleport_rect)

                self.screen.blit(self.frame_image,(69,HEIGHT/2-86))
                self.screen.blit(self.frame_image,(69+164+100,HEIGHT/2-86))
                self.screen.blit(self.frame_image,(69+164*2+100*2,HEIGHT/2-86))
                self.screen.blit(self.frame_image,(69+164*3+100*3,HEIGHT/2-86))
                self.screen.blit(self.frame_image,(69+164*4+100*4,HEIGHT/2-86))

                self.draw.coins(self.stats)
                self.screen.blit(self.shop_back,self.back_rect)


                mouse = pygame.mouse.get_pos()

                if self.shield_rect.collidepoint(mouse):
                    shield_price = 10
                    self.screen.blit(self.shield_image_big, self.shield_image_big.get_rect(midleft = (73-46, HEIGHT/2)) )
                    self.screen.blit(self.frame_image_big, self.frame_image_big.get_rect(midleft = (73-46-6,HEIGHT/2)))
                    self.screen.blit(text_shield,text_shield.get_rect(midbottom = (27+128,HEIGHT/2 - 130)))

                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONUP:
                            if self.stats.coins >= shield_price:
                                self.player_sprite.shield = shield_health
                                self.player_sprite.target_shield = shield_health
                                self.stats.coins -= shield_price
                                self.purchase_sound.play()


                if self.bullet_rect.collidepoint(mouse):
                    bullet_price = 10
                    self.screen.blit(self.bullet_image_big, self.bullet_image_big.get_rect(midleft = (27+164+100, HEIGHT/2)) )
                    self.screen.blit(self.frame_image_big, self.frame_image_big.get_rect(midleft = (21+164+100,HEIGHT/2)))
                    self.screen.blit(text_bullet,text_bullet.get_rect(midbottom = (27+128+100+164,HEIGHT/2 - 130)))

                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONUP:
                            if self.stats.coins >= bullet_price:
                                pass

                if self.speed_rect.collidepoint(mouse):
                    speed_price = 10
                    self.screen.blit(self.speed_image_big, self.speed_image_big.get_rect(midleft = (27+164*2+100*2, HEIGHT/2)) )
                    self.screen.blit(self.frame_image_big, self.frame_image_big.get_rect(midleft = (21+164*2+100*2,HEIGHT/2)))
                    self.screen.blit(text_speed,text_speed.get_rect(midbottom = (27+128+162*2+100*2,HEIGHT/2 - 130)))

                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONUP:
                            if self.stats.coins >= speed_price:
                                self.speedpuflag = True
                                self.stats.coins -= speed_price
                                self.purchase_sound.play()

                if self.burst_rect.collidepoint(mouse):
                    self.screen.blit(self.burst_image_big, self.burst_image_big.get_rect(midleft = (27+164*3+100*3, HEIGHT/2)) )
                    self.screen.blit(self.frame_image_big, self.frame_image_big.get_rect(midleft = (21+164*3+100*3,HEIGHT/2)))
                    self.screen.blit(text_burst,text_burst.get_rect(midbottom = (27+128+164*3+100*3,HEIGHT/2 - 130)))

                if self.teleport_rect.collidepoint(mouse):
                    self.screen.blit(self.teleport_image_big, self.teleport_image_big.get_rect(midleft = (27+164*4+100*4, HEIGHT/2)) )
                    self.screen.blit(self.frame_image_big, self.frame_image_big.get_rect(midleft = (21+164*4+100*4,HEIGHT/2)))
                    self.screen.blit(text_teleport,text_teleport.get_rect(midbottom = (27+128+164*4+100*4,HEIGHT/2 - 130)))

                if self.back_rect.collidepoint(mouse):
                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.state = 'game'
                            self.shop_flag = True

                pygame.display.update()


            if self.state == 'quit':

                events_list = pygame.event.get()

                for event in events_list:
                    if event.type == pygame.QUIT:
                        self.run = False
                        
                if self.quit_flag:
                    self.screen_pause = self.screen
                    self.time = pygame.time.get_ticks()
                    self.quit_flag = False
                
                if pygame.time.get_ticks() - self.time <= 2000:
                    self.screen_pause = pygame.transform.box_blur(self.screen_pause,1)

                self.screen.blit(self.screen_pause,(0,0))

                window_rect = pygame.Rect((WIDTH//3 , 3*(HEIGHT//8)+50),(WIDTH//3,HEIGHT//4-50))
                yes_rect = pygame.Rect((WIDTH//3+4 , 3*(HEIGHT//8) + 150),(WIDTH//6-4,40))
                no_rect = pygame.Rect((WIDTH//2+3,3*(HEIGHT//8)+150),(WIDTH//6-6,40))

                pygame.draw.rect(self.screen,(200,157,88),window_rect)
                pygame.draw.rect(self.screen,(97, 117, 122),yes_rect)
                pygame.draw.rect(self.screen,(97, 117, 122),no_rect)

                font = pygame.font.Font(r'data/fonts/ChaletComprime.otf',40)
                text = font.render('ARE YOU SURE YOU WANT TO EXIT?',True,(255,255,255))
                text_yes = font.render('YES',True,(255,255,255))
                text_no = font.render('NO',True,(255,255,255))
                text_rect = text.get_rect(center=(WIDTH//2,HEIGHT//2))
                text_yes_rect = text_yes.get_rect(center = (yes_rect.centerx,yes_rect.centery))
                text_no_rect = text_no.get_rect(center = (no_rect.centerx,no_rect.centery))
                self.screen.blit(text,text_rect)
                self.screen.blit(text_yes,text_yes_rect)
                self.screen.blit(text_no,text_no_rect)
                
                mouse = pygame.mouse.get_pos()

                if yes_rect.collidepoint(mouse):
                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONUP:
                            self.run = False
                if no_rect.collidepoint(mouse):
                    for event in events_list:
                        if event.type == pygame.MOUSEBUTTONUP:
                            self.quit_flag = True
                            self.state = 'start screen'

                pygame.display.update()



if __name__ == '__main__':
    
    game = Game()
    game.splash_screen()
    # game.load()
    # game.new()
    game.game_loop()
