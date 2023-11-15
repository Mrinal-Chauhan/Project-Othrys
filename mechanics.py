import pygame
import settings
from random import randint,uniform, choices
from colorsys import hsv_to_rgb


class Collision: 

    def __init__(self,player,spawner,group, stats):
        self.screen = pygame.display.get_surface()
        self.player = player
        self.spawner = spawner
        self.stats = stats
        self.group = group

        self.enemy_pos = 0
        self.DEATH = pygame.USEREVENT + 1
        self.coins = pygame.sprite.Group()
        self.health_pu = pygame.sprite.Group()
        self.particle_instance = ParticleSystem()
        self.time = pygame.time.get_ticks()

        self.hit_sound1 = pygame.mixer.Sound(r'data/sfx/hit.wav')
        self.hit_sound2 = pygame.mixer.Sound(r'data/sfx/aa.mp3')
        self.hit_sound3 = pygame.mixer.Sound(r'data/sfx/hamla.mp3')
        
        self.choices = [self.hit_sound1,self.hit_sound2,self.hit_sound3]
        self.probabilities = [0.55,0.30,0.15]

    def check(self):

        for spawner in self.spawner.spawner_group.sprites():

            for enemy in spawner.enemy_group.sprites():

                if pygame.sprite.collide_rect(self.player,enemy):

                    if self.player.shield > 0: 
                        self.player.shield -= settings.enemy_dmg
                    else:
                        self.player.health -= settings.enemy_dmg
                    pygame.sprite.Sprite.kill(enemy)
                    settings.shake_timer = 20
                    settings.shake_intensity = 5
                    choice = choices(self.choices,self.probabilities,k=1)[0]
                    # choice.play()
                    self.hit_sound1.play()

                    # player death
                    if self.player.health <= 0:
                            pygame.event.post(pygame.event.Event(self.DEATH))


                for laser in enemy.lasers.sprites():

                    if pygame.sprite.collide_rect(self.player,laser):
                        if self.player.shield > 0:
                            self.player.shield -= settings.enemy_dmg
                        else:
                            self.player.health -= settings.laser_dmg
                        pygame.sprite.Sprite.kill(laser)
                        settings.shake_timer = 10
                        settings.shake_intensity = 4
                        choice = choices(self.choices,self.probabilities,k=1)[0]
                        # choice.play()
                        self.hit_sound1.play()

                        # player death
                        if self.player.health <= 0:
                            pygame.event.post(pygame.event.Event(self.DEATH))

                # deleting lasers off screen
                    if (laser.rect.x <= -6000) or (laser.rect.x >= 6000) or (laser.rect.y <= -6000) or (laser.rect.y >= 6000) :
                        pygame.sprite.Sprite.kill(laser)


                for laser_player in self.player.lasers.sprites():

                    if pygame.sprite.collide_rect(enemy,laser_player):
                        enemy.health -= settings.player_dmg
                        pygame.sprite.Sprite.kill(laser_player)

                        # enemy death
                        if enemy.health <= 0:
                            pygame.sprite.Sprite.kill(enemy)
                            self.coins.add(Coin(self.group,enemy.rect.center))
                            self.stats.score += randint(16,20)
                            self.particle_instance.emit_particles_1(enemy.rect.center)

                    # deleting lasers off screen
                    if (laser_player.rect.x <= -6000) or (laser_player.rect.x >= 6000) or (laser_player.rect.y <= -6000) or (laser_player.rect.y >= 6000) :
                        pygame.sprite.Sprite.kill(laser_player)

        if pygame.time.get_ticks() - self.time >= settings.healthpu_time:
            self.time = pygame.time.get_ticks()
            for spawner in self.spawner.spawner_group.sprites():
                x,y = randint(-300,300), randint(-300,300)
                self.health_pu.add(HealthPowerup(self.group,(spawner.rect.x+x, spawner.rect.y+y)))

        for pu in self.health_pu.sprites():
            if pygame.sprite.collide_rect(self.player,pu):
                self.player.health += settings.healthpu_heal
                if self.player.health > 100: self.player.health = 100
                pygame.sprite.Sprite.kill(pu)

        for coin in self.coins.sprites():
            if pygame.sprite.collide_rect(self.player, coin):
                self.stats.coins += randint(10,20)
                pygame.sprite.Sprite.kill(coin)

    def call(self):
        self.check()
        self.coins.update()
        


class Coin(pygame.sprite.Sprite):

    def __init__(self,group,pos):
        super().__init__(group)
        
        self.images()
        self.org_image = pygame.image.load("data/coin/1.png").convert_alpha()
        self.image = pygame.transform.scale(self.org_image,(40,40))
        self.rect = self.image.get_rect(center = pos)
        self.counter = 0
        self.time = 0
        self.animation_time = 100
    
    def images(self):
        self.images = []
        for counter in range(1,7):
            self.images.append(pygame.image.load(f"data/coin/{counter}.png").convert_alpha())
        
    def rotate(self):

        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.time >= self.animation_time:

            self.org_image = self.images[self.counter]
            self.image = pygame.transform.scale(self.org_image,(50,50))
            self.counter += 1
            if self.counter >= 6:
                self.counter = 0
            self.time = self.current_time
    
    def update(self):
        self.rotate()


class HealthPowerup(pygame.sprite.Sprite):

    def __init__(self,group,pos):
        super().__init__(group)
        
        self.org_image = pygame.image.load("data/graphics/heart.png").convert_alpha()
        self.image = pygame.transform.scale(self.org_image,(70*2/3,60*2/3))
        self.rect = self.image.get_rect(center = pos)


class Stats():

    def __init__(self) -> None:
        self.coins = 0
        self.score = 0 


class Draw():

    def __init__(self) -> None:

        self.screen = pygame.display.get_surface()
        
        self.font_30 = pygame.font.Font('freesansbold.ttf', 30)
        self.font_45 = pygame.font.Font('freesansbold.ttf', 45)

        coin_org_image = pygame.image.load("data/coin/1.png").convert_alpha()
        self.coin_image = pygame.transform.smoothscale(coin_org_image,(30,30))

        shop_org_image = pygame.image.load('data/graphics/shop.png')
        self.shop_image = pygame.transform.scale(shop_org_image,(60,60))
        self.shop_rect = self.shop_image.get_rect(bottomright = (settings.WIDTH-10,settings.HEIGHT-10))

        menu_org_image = pygame.image.load('data/graphics/menu.png').convert_alpha()
        self.menu_image = pygame.transform.scale(menu_org_image,(50,50))
        self.menu_rect = self.menu_image.get_rect(topleft = (10,10))

    def health_bar(self,player):

        if player.shield > 0:
            if player.shield < player.target_shield:
                player.target_shield -= 0.2 #self.healthspeed = 0.2

            width_shield = player.target_shield/settings.shield_health * settings.WIDTH
            pygame.draw.rect(self.screen, (255,255,255) , (0,0,width_shield,5))


        else:
            if player.health < player.target_health:
                player.target_health -= 0.2 #self.healthspeed = 0.2

            width1 = (player.target_health/settings.player_health) * settings.WIDTH
            width2 = (player.health/settings.player_health) * settings.WIDTH
            pygame.draw.rect(self.screen, (255,0,0) , (0,0,width1,5))
            pygame.draw.rect(self.screen, (0,255,0) , (0,0,width2,5))
        # Other style health bar
            # pygame.draw.rect(self.screen, (0,255,0) , (15,15,800,25))
            # pygame.draw.rect(self.screen, (255,255,255), (15,15,800,25),3)

    def coins(self,stats):
        
        text = self.font_30.render(str(stats.coins), True,(255,255,255))
        textRect = text.get_rect(topright = (settings.WIDTH - 10,60))
        self.screen.blit(text, textRect)

        self.screen.blit(self.coin_image,(settings.WIDTH - textRect.width - 50,60))

    def score(self,stats):
        text = self.font_45.render(str(stats.score), True,(255,255,255))
        textRect = text.get_rect(topright = (settings.WIDTH - 10,10))
        self.screen.blit(text, textRect)

    def shop(self):
        self.screen.blit(self.shop_image,self.shop_rect)

    def menu(self):
        self.screen.blit(self.menu_image,self.menu_rect)

    def draw(self,player,stats):
        self.health_bar(player)
        self.coins(stats)
        self.score(stats)
        self.shop()
        self.menu()


class Particle():
        
        def __init__(self, position, size, color, speed):
            self.x, self.y = position
            self.size = size
            self.color = color
            self.speed = speed
            self.dx, self.dy = uniform(-1, 1), uniform(-1, 1)
            self.lifespan = randint(40,100)

        def move(self):
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed
            self.lifespan -= 1

        def draw(self):
            screen = pygame.display.get_surface()
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)




class ParticleSystem:

    def __init__(self) -> None:
        self.particles = []

    def emit_particles_1(self,position):

        for _ in range(40):
            size = randint(1, 20)
            h,s,v = randint(355, 360), randint(77, 100), randint(50, 75)
            r,g,b = hsv_to_rgb(h/360,s/100,v/100)
            color = (int(r*255), int(g*255), int(b*255))
            speed = uniform(0.5, 2.5)
            self.particles.append(Particle(position, size, color, speed))

    def update(self):
        for p in self.particles:
            p.move()
            p.draw()
        self.particles = [p for p in self.particles if p.lifespan>0]