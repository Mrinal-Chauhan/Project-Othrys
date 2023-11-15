import pygame
from PIL import Image
from math import atan2,degrees
from random import randint
from settings import *

class EnemyHandle(pygame.sprite.Sprite):
    
    def __init__(self, group,player):
        super().__init__()

        self.group = group
        self.spawner_group = pygame.sprite.Group()
        self.player = player
        
        self.spawner_locations = []
    
    def spawner(self):
        # for _ in range(DIFFICULTY):
        #     rand_x = randint(0,1000)
        #     rand_y = randint(0,1000)
        #     self.spawner_group.add(Spawner(self.group,(rand_x,rand_y),self.player))
        #     # spawner_locations.append([rand_x,rand_y])

        while True:
            rand_x = randint(-1500+WIDTH/2+200,1500+WIDTH/2-200)
            rand_y = randint(-1500+HEIGHT/2+200,1500+HEIGHT/2-200)

            if len(self.spawner_locations)>0:
                temp_list = [i for i in self.spawner_locations if (  (abs( rand_x - i[0] ) > 500) and  (abs( rand_y - i[1] ) > 500)       )]

                if len(self.spawner_locations) == DIFFICULTY:
                    break
                if len(self.spawner_locations) == len(temp_list):
                    self.spawner_locations.append([rand_x,rand_y])
                
            else:
                self.spawner_locations.append([rand_x,rand_y])
        for location in self.spawner_locations:
            self.spawner_group.add(Spawner(self.group,(location[0],location[1]),self.player))

    def update(self):
        self.spawner()
        self.spawner_group.update()


class Spawner(pygame.sprite.Sprite):

    def __init__(self,group,pos,player):
        super().__init__(group)

        spawner_image = pygame.image.load('data/graphics/spawner.png').convert_alpha()
        self.image = pygame.transform.smoothscale(spawner_image,(250,250))
        self.rect = self.image.get_rect(center = pos)
        self.player = player

        self.group = group
        self.enemy_group = pygame.sprite.Group()
        self.pos = pos

        self.current_time = pygame.time.get_ticks()
        self.game_time = pygame.time.get_ticks()

    def spawn_enemy(self):

        if pygame.time.get_ticks() - self.game_time <= 60000:
            if (pygame.time.get_ticks() - self.current_time) >= enemy_cooldown1:
                self.enemy_group.add(Enemy(self.group, (self.rect.centerx,self.rect.centery) ,self.player))
                self.current_time = pygame.time.get_ticks()

        elif pygame.time.get_ticks() - self.game_time <= 120000:
            if (pygame.time.get_ticks() - self.current_time) >= enemy_cooldown2:
                self.enemy_group.add(Enemy(self.group, (self.rect.centerx,self.rect.centery) ,self.player))
                self.current_time = pygame.time.get_ticks()

        else:
            if (pygame.time.get_ticks() - self.current_time) >= enemy_cooldown3:
                self.enemy_group.add(Enemy(self.group, (self.rect.centerx,self.rect.centery) ,self.player))
                self.current_time = pygame.time.get_ticks()

    def update(self):
        self.spawn_enemy()


class Enemy(pygame.sprite.Sprite):

    def __init__(self,group,pos,player):
        super().__init__(group)

        img_path = f"data/graphics/enemy/{randint(1,11)}.png"
        enemy_image = pygame.image.load(img_path).convert_alpha()
        img = Image.open(img_path)
        width,height = img.size
        self.org_image = pygame.transform.smoothscale(enemy_image,(width/2,height/2))

        self.rect = self.org_image.get_rect(center = pos)
        self.camera_group = group

        self.health = enemy_health
        self.player = player
        self.rotation()
        self.lasers = pygame.sprite.Group()
        self.laser_time = pygame.time.get_ticks()

    def move_towards(self):

        dirvect = pygame.math.Vector2(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery)
        if not dirvect == pygame.Vector2():
            dirvect.normalize_ip()
            dirvect.scale_to_length(enemy_velocity)
        self.rect.move_ip(dirvect)

    def rotation(self):
        # getting rotation value
        correction_angle = 90
        self.angle = degrees(atan2(self.player.rect.y - self.rect.y - 50 , self.rect.x + 50 - self.player.rect.x)) + correction_angle
        # rotating by theta
        self.image = pygame.transform.rotate(self.org_image,self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

    def shoot(self):
        time_since_shoot = pygame.time.get_ticks() - self.laser_time
        if time_since_shoot >= enemy_shoot_cooldown:
            self.lasers.add(Laser(self.rect.center,self.angle,self.player,self.camera_group))
            self.laser_time = pygame.time.get_ticks()

    def update(self):
        self.move_towards()
        self.shoot()
        self.lasers.update()
        self.rotation()


class Laser(pygame.sprite.Sprite):
    
    def __init__(self,pos,angle,player,group) -> None:
        super().__init__(group)
        self.image = pygame.image.load('data/graphics/laser_enemy.png').convert_alpha()
        self.org_image = pygame.transform.smoothscale(self.image,laser_size)
        self.rect = self.org_image.get_rect(center = pos)

        self.image = pygame.transform.rotate(self.org_image,angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        
        self.player = player

        self.dirvect = pygame.math.Vector2(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery)

    def update(self):
        if not self.dirvect == pygame.Vector2():
            self.dirvect.normalize_ip()
            self.dirvect.scale_to_length(enemy_laser_velocity)
        self.rect.move_ip(self.dirvect)


class Missile(pygame.sprite.Sprite):

    def __init__(self,group,pos,player):
        super().__init__(group)
        enemy_image = pygame.image.load("data/graphics/circle.png").convert_alpha()
        self.org_image = pygame.transform.smoothscale(enemy_image,(80,80))
        self.rect = self.org_image.get_rect(center = pos)
        self.camera_group = group
        self.rotation_time = pygame.time.get_ticks()

    def rotation(self):

        correction_angle = 90
        self.angle = degrees(atan2(self.player.rect.y - self.rect.y - 50 , self.rect.x + 50 - self.player.rect.x)) + correction_angle

        self.image = pygame.transform.rotate(self.org_image,self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
    
    def move_towards(self):

        dirvect = pygame.math.Vector2(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery)
        if not dirvect == pygame.Vector2():
            dirvect.normalize_ip()
            dirvect.scale_to_length(enemy_velocity)
        self.rect.move_ip(dirvect)

    def update(self):
        self.move_towards()
        # self.shoot()
        self.lasers.update()
        self.rotation()

