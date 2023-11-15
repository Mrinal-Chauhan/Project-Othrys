import pygame
import settings
from random import randint

class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.group = pygame.sprite.Group()

        # self.images()
        self.ground = pygame.image.load(f'data/graphics/backgrounds/{randint(1,17)}.png').convert_alpha()
        self.ground_rect = self.ground.get_rect(center = (settings.WIDTH/2,settings.HEIGHT/2))

        self.ground_pos = pygame.Rect((-1500 + settings.WIDTH//2,-1500 + settings.HEIGHT//2,3000,3000))
        self.offset = pygame.math.Vector2()  

    def center_target_camera(self,player):
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
    
        self.offset.x = player.rect.centerx - settings.WIDTH/2   + mouse_x//2 - settings.WIDTH//4
        self.offset.y = player.rect.centery - settings.HEIGHT/2  + mouse_y//2 - settings.HEIGHT//4 

        self.ground_pos.topleft -= self.offset
        # self.ground_pos.x -= (self.offset.x)//2
        # self.ground_pos.y -= (self.offset.y)//2

        if self.ground_pos.x >=0:
            self.offset.x = self.ground_rect.x
            self.ground_pos.x = 0

        if self.ground_pos.y >=0:
            self.offset.y = self.ground_rect.y
            self.ground_pos.y = 0
        
        if self.ground_pos.y <= (settings.HEIGHT - 3000):
            self.offset.y = self.ground_rect.y + 3000 - settings.HEIGHT
            self.ground_pos.y = settings.HEIGHT - 3000

        if self.ground_pos.x <= (settings.WIDTH - 3000):
            self.offset.x = self.ground_rect.x + 3000 - settings.WIDTH
            self.ground_pos.x = settings.WIDTH - 3000

    def bring_instances(spawner,collision):
        global spawner_instance,collision_instance
        spawner_instance = spawner
        collision_instance = collision

    def camera_shake(self,offset):
        offset.x += randint(-settings.shake_intensity, settings.shake_intensity)
        offset.y += randint(-settings.shake_intensity, settings.shake_intensity)

    def custom_draw(self,player):

        self.center_target_camera(player)
        # self.rotate()

        if settings.shake_timer > 0:
            self.camera_shake(self.offset)
            settings.shake_timer -= 1

        # Ground
        self.ground_rect.topleft -= self.offset
        self.surface.blit(self.ground,self.ground_rect.topleft)

        # Spawner
        for spawner in spawner_instance.spawner_group.sprites():
            spawner.rect.topleft -= self.offset
            self.surface.blit(spawner.image,spawner.rect.topleft)

        # Particles
        particles = collision_instance.particle_instance.particles
        for particle in particles:
            particle.x -= self.offset.x
            particle.y -= self.offset.y
            particle.move()
            particle.draw()
            if particle.lifespan <= particle.size:
                particle.size -= 1
            if particle.lifespan < 0:
                particles.remove(particle)

        # Active elements
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):    
            if not sprite in spawner_instance.spawner_group.sprites():                    
                sprite.rect.topleft -= self.offset
                self.surface.blit(sprite.image,sprite.rect.topleft) 


#### Background Image Cycle Code ####

    #     self.counter = 0
    #     self.time = 0
    #     self.animation_time = 5000

    # def images(self):
    #     self.images = []
    #     for counter in range(1,17):
    #         self.images.append(pygame.image.load(f"data/graphics/backgrounds/{counter}.png").convert_alpha())

    # def rotate(self):

    #     self.current_time = pygame.time.get_ticks()
    #     if self.current_time - self.time >= self.animation_time:

    #         # self.org_image = self.images[self.counter]
    #         self.ground = self.images[self.counter]
    #         self.counter += 1
    #         if self.counter >= 16:
    #             self.counter = 0
    #         self.time = self.current_time