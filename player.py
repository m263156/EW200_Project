import pygame
import math
from settings import *



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.velocity_x = None
        self.velocity_y = None
        self.angle = None
        self.y_change_mouse_player = None
        self.x_change_mouse_player = None
        self.mouse_coords = None
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("sprites/player_handgun.png").convert_alpha(),
                                               0, PLAYER_SIZE)
        self.base_player_image = self.image
        self.hitbox = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.hitbox.copy()
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0
        self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y)

    def player_rotation(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0] - WIDTH //2)
        self.y_change_mouse_player = (self.mouse_coords[1] - HEIGHT //2)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if pressed_keys[pygame.K_s]:
            self.velocity_y = self.speed
        if pressed_keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if pressed_keys[pygame.K_d]:
            self.velocity_x = self.speed

        if self.velocity_y != 0 and self.velocity_x != 0:
            self.velocity_y /= math.sqrt(2)
            self.velocity_x /= math.sqrt(2)

        if pygame.mouse.get_pressed() == (1,0,0) or pressed_keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)


    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox.center = self.pos
        self.rect.center = self.hitbox.center

    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("bullets/1.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED
        self.x = x
        self.y = y
        self.angle = angle
        self.x_vel = math.cos(self.angle * (2*math.pi/360)) * self.speed
        self.y_vel = math.sin(self.angle * (2*math.pi/360)) * self.speed
        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()


    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def update(self):
        self.bullet_movement()
