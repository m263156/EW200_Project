import time
from sys import exit
from player import *
import random
import pickle

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

pygame.init()

try:
    with open('high_score.dat', 'rb') as file:
        high_score = pickle.load(file)
except:
    high_score = 0

# Creating the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombies!")
clock = pygame.time.Clock()

# Loading images
background = pygame.image.load("background/ground.png").convert()
blue_tiles = pygame.image.load("background/blue_tile.png").convert()
wall_left = pygame.image.load("background/wall_right.png").convert_alpha()
wall_right = pygame.image.load("background/wall_right.png").convert_alpha()
wall_top = pygame.transform.rotozoom(pygame.image.load("background/wall_right.png").convert_alpha(),
                                               270, 1)
wall_bottom = pygame.transform.rotozoom(pygame.image.load("background/wall_right.png").convert_alpha(),
                                               90, 1)
block_middle = pygame.transform.rotozoom(pygame.image.load("background/block_middle.png").convert_alpha(), 90, 2)
block_top = pygame.transform.rotozoom(pygame.image.load("background/block_cap.png").convert_alpha(),
                                               180, 2)
block_bottom = pygame.transform.rotozoom(pygame.image.load("background/block_cap.png").convert_alpha(),
                                               0, 2)
#Game Fonts
title_font = pygame.font.Font("fonts/Kenney High.ttf", 128)
end_font = pygame.font.Font("fonts/Kenney High.ttf", 450)
small_font = pygame.font.Font("fonts/Kenney High.ttf", 32)
title_text = title_font.render("Zombies!", True, (255, 69, 0))
if [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]:
    instructions_text = small_font.render(f"LS to move, RS to aim, RB to shoot", True, (255, 69, 0))
else:
    instructions_text = small_font.render(f"WASD to move, Point to aim, Click to shoot", True, (255, 69, 0))
start_text = small_font.render("Press SPACE to start game", True, (255, 69, 0))
end_text = end_font.render("You died", True, (0, 0, 0))
points_font = pygame.font.Font("fonts/Kenney High.ttf", 64)
UI_font = pygame.font.Font("fonts/Kenney High.ttf", 32)

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
    for i in range(LEVEL * 2):
        locations = [(800, random.randint(800, 3300)), (3300, random.randint(800, 3300)),
                     (random.randint(800, 3300), 800), (random.randint(800, 3300), 3300)]
        enemy = Enemy(locations[random.randint(0, 3)], player)
        enemy.speed = (LEVEL // 4) + 3
        all_sprites_group.add(enemy)
        enemy_group.add(enemy)

def draw_background():
    background.fill(BACKGROUND_COLOR)
    for i in range(30):
        for j in range(30):
            background.blit(blue_tiles, (1000 + TILE_SIZE * i, 1000 + TILE_SIZE * j))
    for i in range(30):
        background.blit(wall_left, (1000, 1000 + TILE_SIZE * i))
        background.blit(wall_top, (1000 + TILE_SIZE * i, 1000))
        background.blit(wall_right, (2920, 1000 + TILE_SIZE * i))
        background.blit(wall_bottom, (1000 + TILE_SIZE * i, 2816))
    background.blit(block_top, (1498, 1498))
    for i in range(5):
        background.blit(block_middle, (1500, 1628 + TILE_SIZE * 2 * i))
    background.blit(block_bottom, (1499, 2269))
    # block_rect = pygame.draw.rect()
while True:
    camera = Camera()
    player = Player()
    all_sprites_group.add(player)

    background.fill((0, 0, 0))
    screen.blit(start_text,(WIDTH // 2.8, HEIGHT // 1.3))
    screen.blit(title_text,(WIDTH // 3.1, HEIGHT // 3))
    screen.blit(instructions_text,(WIDTH // 3.5, HEIGHT // 1.5))
    pygame.display.update()
    game_start = False
    while game_start == False:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if keys[pygame.K_SPACE]:
                game_start = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(5):
                    player.shoot = True
                    player.is_shooting()
        if player.alive():
            draw_background()
            if not enemy_group:
                LEVEL += 1
                level_screen = title_font.render(f"Level {LEVEL}", True, (255, 69, 0))
                screen.fill((0, 0, 0))
                screen.blit(level_screen, (WIDTH // 2, HEIGHT // 2))
                pygame.display.update()
                time.sleep(2)
                spawn_enemies(LEVEL)
            camera.custom_draw()
            all_sprites_group.update()
            level_text = points_font.render(f"Level: {LEVEL}", True, (255, 69, 0))
            screen.blit(level_text, (WIDTH - 200, 0))
            kills_text = points_font.render(f"Points: {len(kill_counter)}", True, (255, 69, 0))
            screen.blit(kills_text, (WIDTH - 500, 0))
            if len(kill_counter) > high_score:
                high_score = len(kill_counter)
            high_score_text = points_font.render(f"Highscore: {high_score}", True, (255, 69, 0))
            screen.blit(high_score_text, (50, 0))
            pygame.display.update()
            clock.tick(FPS)
        else:
            screen.fill((255, 69, 0))
            screen.blit(end_text, (death_x + 25, death_y + 150))
            kills_text = points_font.render(f"Points: {len(kill_counter)}", True, (0, 0, 0))
            screen.blit(kills_text, (death_x + 25, death_y))
            pygame.display.update()
            clock.tick(FPS)
            with open('high_score.dat', 'wb') as file:
                pickle.dump(high_score, file)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
