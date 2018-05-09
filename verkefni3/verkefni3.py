import pygame, sys, random
from pygame.locals import *



pygame.init()
mainClock = pygame.time.Clock()

width = 800
height = 700
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption('space invaders')


moveLeft = False
moveRight = False
moveUp = False
moveDown = False

DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9
LEFT = 4
RIGHT = 6
UP = 8
DOWN = 2

YELLOW = (255,255,0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (135, 206, 250)

bg = (152, 155, 221)
paddle = (195, 197, 240)

MOVESPEED = 11
MOVE = 1
SHOOT = 15


score = 0


font = pygame.font.SysFont('calibri', 50)

def makeplayer():
    player = pygame.Rect(370, 635, 60, 25)
    return player

def makeinvaders(invaders):
    y = 0
    for i in invaders:
        x = 0
        for j in range(11):
            invader = pygame.Rect(75+x, 75+y, 50, 20)
            i.append(invader)
            x += 60
        y += 45
    return invaders

def makewalls(walls):
    wall1 = pygame.Rect(60, 520, 120, 30)
    wall2 = pygame.Rect(246, 520, 120, 30)
    wall3 = pygame.Rect(432, 520, 120, 30)
    wall4 = pygame.Rect(618, 520, 120, 30)
    walls = [wall1, wall2, wall3, wall4]
    return walls

def movepaddle(player):
    if moveLeft and player.left > 0:
        player.left -= MOVESPEED
    if moveRight and player.right < width:
        player.right += MOVESPEED
    return player

def moveinvaders(invaders, invader_dir):
    for row in invaders:
        for invader in row:
            if invader_dir == RIGHT and row[len(row)-1].right < width:
                invader.right += MOVE
            elif row[len(row)-1].right >= width:
                invader.left -= MOVE
                invader_dir = LEFT
            elif invader_dir == LEFT and row[0].left > 0:
                invader.left -= MOVE
            elif row[0].left <= 0:
                invader.right += MOVE
                invader_dir = RIGHT
    return invader_dir

def doRectsOverlap(bullet, invader):
    for a, b in [(bullet, invader), (invader, bullet)]:
        if ((isPointInsideRect(a.left, a.top, b)) or
            (isPointInsideRect(a.left, a.bottom, b)) or
            (isPointInsideRect(a.right, a.top, b)) or
            (isPointInsideRect(a.right, a.bottom, b))):
            return True
    return False

def isPointInsideRect(x, y, invader):
    if (x > invader.left) and (x < invader.right) and (y > invader.top) and (y <
        invader.bottom):
        return True
    else:
        return False

def invaderdead(bullets, invaders):
    for bullet in bullets:
        for row in invaders:
            for invader in row:
                if doRectsOverlap(bullet, invader):
                    row.remove(invader)
                    bullets.remove(bullet)
    return invaders

def wallhit(bullets, walls):
    for bullet in bullets:
        for wall in walls:
            if doRectsOverlap(bullet, wall):
                bullets.remove(bullet)
                wall.height -= 10
                if wall.height <= 0:
                    walls.remove(wall)
    return bullets,walls

def movebullets(bullets):
    for bullet in bullets:
        bullet.top -= SHOOT

def moveenemybullets(bullets):
    for bullet in bullets:
        bullet.bottom += SHOOT

def gameend(invaders):
    if invaders == [[],[],[],[],[]]:
        screen.fill(BLACK)
        drawText('You win.', font, screen , 300, 300, RED)

def drawplayerinvaderbullet(player, invaders, bullets):
    pygame.draw.rect(screen, RED, player)
    for i in invaders:
        for invader in i:
            if invader in invaders[0]:
                pygame.draw.rect(screen, RED, invader)
            elif invader in invaders[1]:
                pygame.draw.rect(screen, BLUE, invader)
            elif invader in invaders[2]:
                pygame.draw.rect(screen, YELLOW, invader)
            elif invader in invaders[3]:
                pygame.draw.rect(screen, WHITE, invader)
            elif invader in invaders[4]:
                pygame.draw.rect(screen, GREEN, invader)
    for w in walls:
        pygame.draw.rect(screen, GREEN, w)
    for x in bullets:
        pygame.draw.rect(screen, RED, x)

def drawText(text, font, surface, x, y, color):
    text = font.render(text, 1, color)
    textrect = text.get_rect()
    textrect.topleft = (x, y)
    surface.blit(text, textrect)

timer = mainClock.tick()
time = 0
invaders = [[],[],[],[],[]]
invader_dir = RIGHT
bullets = []
walls = []

player = makeplayer()
invaders = makeinvaders(invaders)
walls = makewalls(walls)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT   or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_SPACE:
                bullet = pygame.Rect(player.left+28, player.top-8, 5, 8)
                bullets.append(bullet)
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
    time += timer

    screen.fill(BLACK)
    drawplayerinvaderbullet(player, invaders, bullets)
    invader_dir = moveinvaders(invaders, invader_dir)
    movebullets(bullets)
    if time % 5000 == 0:
        x = random.choice([1,2,3,4,5])
        list1 = invaders[x-1]
        y = random.choice([1,2,3,4,5,6,7,8,9,10,11])
        invader = list1[y-1]
        bullet = pygame.Rect(invader.right+28, invader.bottom-8, 5, 8)
        bullets.append(bullet)
        moveenemybullets(bullets)
    gameend(invaders)
    invaders = invaderdead(bullets, invaders)
    bullets, walls = wallhit(bullets, walls)
    player = movepaddle(player)
    pygame.display.update()
    mainClock.tick(60)
