import os,random
import pygame


class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(32, 32, 16, 16)

    def move(self, dx, dy):


        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, bx, by):


        self.rect.x += bx
        self.rect.y += by


        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if bx > 0:
                    self.rect.right = wall.rect.left
                if bx < 0:
                    self.rect.left = wall.rect.right
                if by > 0:
                    self.rect.bottom = wall.rect.top
                if by < 0:
                    self.rect.top = wall.rect.bottom


class Wall(object):

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()


pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()
walls = []
player = Player()


level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"WWWW                            W      W",
"WW W WWWWW  WWWWWWWWW  W WWWWWW W      W",
"WW W W   W  W       W  W      W WWWWWW W",
"WW W W   W  W WWWW  W  W      W        W",
"WW   W   W  W W  W  W  WWWWWWWWWWWWWWW W",
"WWWWWW   W  W W  W  W     WWW   W W W  W",
"W        W  W W  WW WWWWWWWWW   W W W  W",
"W        W  W W           W W   W W W  W",
"W  W        W W           W W       W  W",
"W  WWWWWWWWWW WWWWWWWW    W W  WWWWWW  W",
"W  W                 W                 W",
"W  W       WWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"WWWW                   W               W",
"W    WWWWWWWWWWWWWWWWWWW    WWWWWWWWW  W",
"W    W                      W          W",
"W    W    WWWWWWWWWWWWWWWWWWW   W      W",
"W    W           W  W           W      W",
"W    W           W  WWWWWWWWW   WWWWWWWW",
"W    WWWWWWWWW   W                     W",
"W    W       W   W     WWW WWWWWWWWWWW W",
"W            W   W     W W W           W",
"W WWWWWWWWWWWW   W     W   W     WWWW  W",
"W      W     W   W    WWWWWW     W  W  W",
"W WWWWWW WWWWW WWWWW       W     W  W  W",
"W                          W     W  W  W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW  W  W",
"W                                   W  W",
"W                                   W EW",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",




]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 16, 16)
        x += 16
    y += 16
    x = 0

running = True
while running:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        raise SystemExit, "You win!"

    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.display.flip()
