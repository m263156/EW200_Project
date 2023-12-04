import random

import pygame

#Groups
all_sprites_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Game setup
WIDTH = 1152
HEIGHT = 648
FPS = 60
LEVEL = 0

# Player Settings
PLAYER_START_X = 2000
PLAYER_START_Y = 2000
PLAYER_SIZE = 1
PLAYER_SPEED = 8
GUN_OFFSET_X = 50
GUN_OFFSET_Y = 5
PLAYER_HEALTH = 100
death_x = 0
death_y = 0

# Bullet Settings
SHOOT_COOLDOWN = 10
BULLET_SIZE = 1.2
BULLET_SPEED = 50
BULLET_LIFETIME = 750

#Enemy Settings
ENEMY_SPEED = 4
ENEMY_SIZE = 1

#Background
TILE_SIZE = 64
BACKGROUND_COLOR = (18, 22, 64)


#UI
points = 0
