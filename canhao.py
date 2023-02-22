import pygame
from pygame.locals import *
import math
from random import randint

class Shot:
    def __init__(self, pos_h=0, pos_v=0, gravity=10):
        self.pos_h = pos_h
        self.pos_v = pos_v
        self.speed_h = None
        self.speed_v = None
        self.time = None
        self.gravity = gravity

    def speed_selector(self, spd, ang):
        self.speed_h = math.sin(ang)*spd
        self.speed_v = math.cos(ang)*spd
        # self.time_max = self.speed_h/self.gravity*2
        self.time = 0

    def att_pos(self):
        self.pos_v = self.speed_v*self.time
        self.pos_h = (self.speed_h*self.time) - (self.gravity*self.time**2/2)
        self.time += 1/(FPS/10)

pygame.init()
pygame.font.init()
WIDTH = 1000
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0, 255)
GREEN = (0, 150, 0)
BLUE = (110, 80, 255)
GRAY = (50, 50, 50)
ORANGE = (255, 100, 0, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('tiro ao alvo')
font = pygame.font.SysFont(None, 30)
cannon_image00 = pygame.image.load('c00.png').convert_alpha()
cannon_image00 = pygame.transform.scale(cannon_image00, (42, 52))
cannon_image10 = pygame.transform.rotate(cannon_image00, 10)
cannon_image25 = pygame.transform.rotate(cannon_image00, 25)
cannon_image40 = pygame.transform.rotate(cannon_image00, 40)
cannon_image55 = pygame.transform.rotate(cannon_image00, 55)
cannon_image70 = pygame.transform.rotate(cannon_image00, 70)
cannon_image85 = pygame.transform.rotate(cannon_image00, 85)
timer = pygame.time.Clock()
FPS = 120


speed = 30
speed_add = 0
ang = 0
ang_add = 0
cannon = []
shots = 0
score = 0
target = (0, 0)
sair = False
while sair != True:
    timer.tick(FPS)
    screen.fill(BLUE)

    if target == (0, 0):
        target = (randint(50, WIDTH-20), randint(0, HEIGHT-50))
    pygame.draw.rect(screen, RED, [target[0], target[1], 20, 20])
    pygame.draw.rect(screen, WHITE, [target[0]+3, target[1]+3, 14, 14])
    pygame.draw.rect(screen, RED, [target[0]+6, target[1]+6, 8, 8])

    for shot in range(-len(cannon), 0):
        pygame.draw.circle(screen, GRAY, [int(cannon[shot].pos_v), int(HEIGHT-cannon[shot].pos_h)], 7)
        if cannon[shot].pos_v > target[0]-3 and cannon[shot].pos_v < target[0]+23:
            if cannon[shot].pos_h < HEIGHT-target[1]+3 and cannon[shot].pos_h > HEIGHT-target[1]-23:
                pygame.draw.circle(screen, ORANGE, (int(cannon[shot].pos_v), HEIGHT-int(cannon[shot].pos_h)), 30)
                del cannon[shot]
                target = (0, 0)
                score+=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sair = True
            if event.key == pygame.K_UP:
                ang_add += 0.1
            if event.key == pygame.K_DOWN:
                ang_add -= 0.1
            if event.key == pygame.K_RIGHT:
                speed_add += 0.5
            if event.key == pygame.K_LEFT:
                speed_add -= 0.5
            if event.key == pygame.K_SPACE:
                cannon.append(Shot())
                cannon[-1].speed_selector(speed, math.radians(ang))
                shots +=1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                ang_add = 0
            if event.key == pygame.K_DOWN:
                ang_add = 0
            if event.key == pygame.K_RIGHT:
                speed_add = 0
            if event.key == pygame.K_LEFT:
                speed_add = 0

    for shot in range(0, len(cannon)):
        try:
            cannon[shot].att_pos()
            if cannon[shot].pos_v > WIDTH or cannon[shot].pos_h < 0:
                del cannon[shot]
        except:
            pass

    speed += speed_add
    ang += ang_add
    if ang > 90:
        ang = 90
    if ang < 0:
        ang = 0
    if speed < 35:
        speed = 35
    if speed > 200:
        speed = 200

    pygame.draw.rect(screen, BLACK, [0, HEIGHT-3, WIDTH, 3])
    text_angle = font.render(f'angle:{ang:.1f} up/down', True, BLACK)
    text_speed = font.render(f'speed:{speed} left/right', True, BLACK)
    text_shot = font.render('press space to shoot', True, BLACK)
    text_score = font.render(f'score:{score}', True, BLACK)
    text_shots = font.render(f'shots:{shots}', True, BLACK)
    screen.blit(text_speed, (15, 10))
    screen.blit(text_angle, (15, 30))
    screen.blit(text_shot, (15, 50))
    screen.blit(text_score, (15, 90))
    screen.blit(text_shots, (15, 70))
    if ang < 17:
        screen.blit(cannon_image00, (-7, HEIGHT-32))
    elif ang < 27:
        screen.blit(cannon_image10, (-13, HEIGHT-37))
    elif ang < 37:
        screen.blit(cannon_image25, (-18, HEIGHT-40))
    elif ang < 51:
        screen.blit(cannon_image40, (-22, HEIGHT-42))
    elif ang < 64:
        screen.blit(cannon_image55, (-25, HEIGHT-43))
    elif ang < 77:
        screen.blit(cannon_image70, (-25, HEIGHT-43))
    elif ang < 91:
        screen.blit(cannon_image85, (-23, HEIGHT-38))

    pygame.display.update()

pygame.font.quit()
pygame.quit()