import sys
import os
import random, time
import pygame
from pygame.locals import *

pygame.init()

cur_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# CONSTANTS & FILE LOCATIONS
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join(cur_dir, "graphics/background.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
METEOR_SPRITES = [(pygame.image.load(os.path.join(cur_dir, "graphics/meteor_89x82.png")), (89, 82)),
           (pygame.image.load(os.path.join(cur_dir, "graphics/meteor_98x96.png")), (98, 96)),
           (pygame.image.load(os.path.join(cur_dir, "graphics/meteor_101x84.png")), (101, 84)),
           (pygame.image.load(os.path.join(cur_dir, "graphics/meteor_120x98.png")), (120, 98))]
PLAYER_SPRITE = (pygame.image.load(os.path.join(cur_dir, "graphics/player_blue.png")), (99, 75))
LASER_SPRITE = (pygame.image.load(os.path.join(cur_dir, "graphics/laser.png")), (9, 54))

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 189, 51)

FPS = 60
TICKER = pygame.time.Clock()

SCORE = 0
SPEED = 5

INC_SPEED = pygame.USEREVENT + 1
LASER_COOLDOWN = INC_SPEED + 1

can_shoot = True

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN.fill(WHITE)
pygame.display.set_caption("Game")

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.meteor_type = METEOR_SPRITES[random.randint(0, 3)]
        self.image = self.meteor_type[0]
        self.surf = pygame.Surface(self.meteor_type[1])
        self.rect = self.surf.get_rect(center = (random.randint(40, SCREEN_WIDTH - 40), 0))

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if(self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_SPRITE[0]
        self.surf = pygame.Surface(PLAYER_SPRITE[1])
        self.rect = self.surf.get_rect(center = (160, 520))

    def move(self):        
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
        if pressed_keys[K_SPACE] and can_shoot:
            return Laser((self.rect.left + self.surf.get_size()[0]/2, self.rect.top))
        else:
            return None

class Laser(pygame.sprite.Sprite):
    def __init__(self, loc):
        super().__init__()
        self.image = LASER_SPRITE[0]
        self.surf = pygame.Surface(LASER_SPRITE[1])
        self.rect = self.surf.get_rect(center = loc)
    
    def move(self):
        if(self.rect.top < 0):
            self.kill()
        else:
            self.rect.move_ip(0, -5)


P1 = Player()
enemies = pygame.sprite.Group()
lasers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

music = pygame.mixer.Sound(os.path.join(cur_dir, "sample_music.wav"))
music.play(loops=-1)

# #Menu selection
# in_menu = True
# while True:
#     for event in pygame.event.get():    
#         if event.type == QUIT:
#             music.stop()
#             pygame.quit()
#             sys.exit()
#     SCREEN.fill(WHITE)
#     SCREEN.blit(BACKGROUND, (0, 0))
#     #Draw menu options
#     title = font.render("ASTEROID ESCAPE", True, ORANGE)
#     SCREEN.blit(title, (13, 10))
#     pygame.display.update()
#     TICKER.tick(FPS)

pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop
while True:     
    for event in pygame.event.get():    
        if event.type == INC_SPEED:
            SPEED += 0.5     
        if event.type == LASER_COOLDOWN:
            can_shoot = True
        if event.type == QUIT:
            music.stop()
            pygame.quit()
            sys.exit()

    if len(enemies.sprites()) <= 0:
        E1 = Meteor()
        enemies.add(E1)
        all_sprites.add(E1)
     
    SCREEN.fill(WHITE)
    SCREEN.blit(BACKGROUND, (0, 0))
    scores = font_small.render("SCORE: " + str(SCORE), True, ORANGE)
    SCREEN.blit(scores, (10,10))
    
    for entity in all_sprites:
        SCREEN.blit(entity.image, entity.rect)
        if isinstance(entity, Player):
            newLaser = entity.move()
            if not newLaser is None:
                pygame.time.set_timer(LASER_COOLDOWN, 500)
                can_shoot = False
                lasers.add(newLaser)
                all_sprites.add(newLaser)
        else:
            entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        SCREEN.fill(RED)
        SCREEN.blit(game_over, (125, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        music.stop()
        pygame.quit()
        sys.exit()

    for l in lasers:
        e = pygame.sprite.spritecollideany(l, enemies)
        if not e is None:
            SCORE += 1
            e.kill()
            l.kill()
            continue



    pygame.display.update()
    TICKER.tick(FPS)


