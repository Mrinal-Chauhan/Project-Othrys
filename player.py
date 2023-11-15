import pygame
from math import atan2, degrees, atan2
from settings import *


class Player(pygame.sprite.Sprite):

    def __init__(self,pos,group):
        super().__init__(group)
        spaceship_image = pygame.image.load(r'data\graphics\spaceship.png')#.convert_alpha()
        self.org_image = pygame.transform.smoothscale(spaceship_image,spaceship_size)
        self.rect = self.org_image.get_rect(center = pos)
        
        self.health = player_health
        self.target_health = player_health
        self.score = 0
        self.player_vel = [0,0] #x,y

        self.shield = 0
        self.target_shield = 0
        self.speed_flag = False

        self.ready = True
        self.laser_time = 0
        self.camera_group = group

        self.lasers = pygame.sprite.Group()
        self.laser_sound = pygame.mixer.Sound(r'data/sfx/laser2.mp3')

    def movement(self):
        
        events_list = pygame.event.get()
        powerup_event = pygame.USEREVENT + 2
        for event in events_list:
            if event.type == powerup_event:
                self.pre_time = pygame.time.get_ticks()
                self.speed_flag = True
        
        keys = pygame.key.get_pressed()

        if not self.speed_flag:

            if ( keys[pygame.K_RIGHT] or keys[pygame.K_d] ) and ( (self.camera_group.ground_rect.x + 3000 - self.rect.x) >100 ):
                self.player_vel[0] = player_velocity

            if ( keys[pygame.K_LEFT] or keys[pygame.K_a] ) and ((self.rect.x - self.camera_group.ground_rect.x) > 20):
                self.player_vel[0] = -player_velocity

            if ( keys[pygame.K_UP] or keys[pygame.K_w] ) and ( (self.rect.y - self.camera_group.ground_rect.y) > 20):
                self.player_vel[1] = player_velocity

            if keys[pygame.K_DOWN] or keys[pygame.K_s] and ( (self.camera_group.ground_rect.y + 3000 - self.rect.y) >100 ):
                self.player_vel[1] = -player_velocity
            
            self.rect.x += self.player_vel[0]
            self.rect.y -= self.player_vel[1]

            if self.player_vel[0] > 0:
                self.player_vel[0] -= player_friction
            if self.player_vel[0] < 0:
                self.player_vel[0] += player_friction
            if self.player_vel[1] > 0:
                self.player_vel[1] -= player_friction
            if self.player_vel[1] < 0:
                self.player_vel[1] += player_friction
            # BUG FIX
            if player_friction > self.player_vel[0] > 0:
                self.player_vel[0] = 0
            if player_friction > self.player_vel[1] > 0:
                self.player_vel[1] = 0        

        else:

            if pygame.time.get_ticks() - self.pre_time > speed_pu_time:
                self.speed_flag = False

            if ( keys[pygame.K_RIGHT] or keys[pygame.K_d] ) and ( (self.camera_group.ground_rect.x + 3000 - self.rect.x) >100 ):
                self.rect.x += velocity_pu

            if ( keys[pygame.K_LEFT] or keys[pygame.K_a] ) and ((self.rect.x - self.camera_group.ground_rect.x) > 20):
                self.rect.x -= velocity_pu

            if ( keys[pygame.K_UP] or keys[pygame.K_w] ) and ( (self.rect.y - self.camera_group.ground_rect.y) > 20):
                self.rect.y -= velocity_pu

            if keys[pygame.K_DOWN] or keys[pygame.K_s] and ( (self.camera_group.ground_rect.y + 3000 - self.rect.y) >100 ):
                self.rect.y += velocity_pu
   
    def rotation(self):
        # getting rotation value
        mouse_x, mouse_y = pygame.mouse.get_pos()
        correction_angle = 90
        self.theta = degrees(atan2(mouse_y - self.rect.y - spaceship_size[1]/2 , self.rect.x + spaceship_size[0]/2 - mouse_x)) + correction_angle
        # rotating by theta
        self.image = pygame.transform.rotate(self.org_image,self.theta)
        self.rect = self.image.get_rect(center = self.rect.center)

    def shoot(self):
        time_since_shoot = pygame.time.get_ticks() - self.laser_time
        if time_since_shoot >= player_shoot_cooldown:
            self.ready = True   
        if pygame.mouse.get_pressed()[0] == True and self.ready:
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

            self.lasers.add(Laser(self.rect.center,self.theta,self.camera_group))
            self.laser_sound.play()

    def update(self):
        self.movement()
        self.rotation()
        self.shoot()
        self.lasers.update()


class Laser(pygame.sprite.Sprite):

    def __init__(self,pos,angle,group):
        super().__init__(group)
        image = pygame.image.load('data/graphics/laser1.png').convert_alpha()
        self.org_image = pygame.transform.smoothscale(image,laser_size)
        self.rect = self.org_image.get_rect(center = pos)
        
        self.image = pygame.transform.rotate(self.org_image,angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.health = player_health
        self.dirvect = pygame.math.Vector2(mouse_x - self.rect.centerx, mouse_y - self.rect.centery)

    def update(self):
        if not self.dirvect == pygame.Vector2():
            self.dirvect.normalize_ip()
            self.dirvect.scale_to_length(player_laser_velocity)
        self.rect.move_ip(self.dirvect)
