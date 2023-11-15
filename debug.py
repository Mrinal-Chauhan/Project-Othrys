import pygame
import random
from colorsys import hsv_to_rgb

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

class Particle:
    def __init__(self, position, size, color, speed):
        self.x, self.y = position
        self.size = size
        self.color = color
        self.speed = speed
        self.vx, self.vy = random.uniform(-1, 1), random.uniform(-1, 1)
        self.lifespan = random.randint(10,100)

    def update(self):
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed
        self.lifespan -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

def random_color():
    h,s,v = random.randint(355, 360), random.randint(77, 100), random.randint(50, 75)
    r,g,b = hsv_to_rgb(h/360,s/100,v/100)
    color = (int(r*255), int(g*255), int(b*255))
    return color

def emit_particles(position):
    for _ in range(10):
        size = random.randint(5, 20)
        color = random_color()
        speed = random.uniform(0.5, 2.5)
        particles.append(Particle(position, size, color, speed))

particles = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        emit_particles(pygame.mouse.get_pos())

    screen.fill((0, 0, 0))
    for p in particles:
        p.update()
        p.draw(screen)

    particles = [p for p in particles if p.lifespan > 0]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
