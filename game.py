import pygame
from sys import exit
import math
from settings import *
from player import *
from enemy import *
import random


pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)

pygame.init()

# Creating the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombies!")
clock = pygame.time.Clock()

# Loading images
background = pygame.image.load("background/ground.png").convert()


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = background.get_rect(topleft = (0, 0))

    def custom_draw(self):
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2

        floor_offset_pos = self.floor_rect.topleft - self.offset
        screen.blit(background, floor_offset_pos)

        for sprite in all_sprites_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)

def spawn_enemies(LEVEL):
    for i in range(LEVEL):
        enemy = Enemy((random.randint(400, 2000), random.randint(400, 2000)), player)
        all_sprites_group.add(enemy)
        enemy_group.add(enemy)

button_shoot = False
camera = Camera()
player = Player()
all_sprites_group.add(player)

while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.JOYBUTTONDOWN:
            if pygame.joystick.Joystick(0).get_button(5):
                player.shoot = True
                player.is_shooting()
    if player.alive():
        if not enemy_group:
            LEVEL+= 1
            spawn_enemies(LEVEL)



    screen.blit(background, (0, 0))
    camera.custom_draw()
    all_sprites_group.update()
    #pygame.draw.rect(screen, "red", player.hitbox, width=2)
    #pygame.draw.rect(screen, "yellow", player.rect, width=2)

    pygame.display.update()
    clock.tick(FPS)
