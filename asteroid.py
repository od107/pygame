#my second taste of python
#asteroid game

import random, pygame, sys, math
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
SHIPSIZE = 20
MARGIN = 50
BULLETSIZE = 3

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
DGREEN   = (0  , 100,   0)
BLACK    = (  0,   0,   0)

BGCOLOR = BLACK
LIGHTBGCOLOR = YELLOW


RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'

GODMODE = False


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.key.set_repeat(1, 100)

    pygame.display.set_caption('Asteroids')

    #initialize
    ship = Ship()
    bullets = []
    asteroids = []

    DISPLAYSURF.fill(BGCOLOR)

    while True: # main game loop
        DISPLAYSURF.fill(BGCOLOR)
        draw(ship, bullets, asteroids)

        #TODO: change keyup with keypressed

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    ship.accelerate()
                if event.key == K_SPACE:
                    bullets.append(ship.shoot())
                if event.key == K_RIGHT:
                    ship.rotateRight()
                if event.key == K_LEFT:
                    ship.rotateLeft()

        # Update position
        ship.move()

        for asteroid in asteroids:
            asteroid.move()

        for bullet in bullets:
            if bullet.move():
                bullets.remove(bullet)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        #print(FPSCLOCK.get_fps())



def draw(ship, bullets, asteroids):
    #TODO fix border transitions and add asteroids
    #TODO change the position of the ship image to be at the tip of the ship


    blittedRect = DISPLAYSURF.blit(ship.img.convert(), ship.pos)

    oldCenter = blittedRect.center
    rotatedSurf = pygame.transform.rotate(ship.img, math.degrees(ship.orientation - math.pi/2))

    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter

    DISPLAYSURF.blit(rotatedSurf, rotRect)

    for bullet in bullets: #is there a way to blit multiple images?
        #DISPLAYSURF.blit(bullet.img, bullet.pos)
        pygame.draw.rect(DISPLAYSURF, WHITE, ((bullet.pos), (BULLETSIZE, BULLETSIZE)))


class Ship:
    maxSpeed = 100
    img = pygame.image.load('ship.png')
    img.set_colorkey((0, 0, 0))

    def __init__(self):
        self.pos = [int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)]
        self.orientation = math.pi/2
        self.vel = [0, 0]


    def accelerate(self):
        self.vel[0] += math.cos(self.orientation)/5
        self.vel[1] += math.sin(self.orientation)/5
        #print('velocity: ',self.vel)
        #TODO limit to max vel

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] -= self.vel[1]

        #pos is the topleft most position of the ship image
        if(self.pos[0] > WINDOWWIDTH + MARGIN + SHIPSIZE):
            self.pos[0] = 0 - MARGIN
        elif(self.pos[1] > WINDOWHEIGHT + MARGIN + SHIPSIZE):
            self.pos[1] = 0 - MARGIN
        elif(self.pos[0] < 0 - MARGIN):
            self.pos[0] = WINDOWWIDTH + MARGIN
        elif(self.pos[1] < 0 - MARGIN):
            self.pos[1] = WINDOWHEIGHT + MARGIN


    def rotateRight(self):
        self.orientation -= math.pi / 18
        #print('orientation: ', self.orientation)

    def rotateLeft(self):
        self.orientation += math.pi / 18
        #print('orientation: ', self.orientation)

    def shoot(self):
        bullet = Bullet(self.pos, self.orientation, self.vel)
        return bullet
        print('position: ', self.pos)
        #to implement

class Bullet():
    shootSpeed = 5

    def __init__(self, shippos, shiporientation, shipvel):
        self.pos = shippos.copy()
        self.vel = [shipvel[0] + self.shootSpeed * math.cos(shiporientation),
                    shipvel[1] + self.shootSpeed * math.sin(shiporientation)]

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] -= self.vel[1]

        #pos is the topleft most position of the ship image
        if(self.pos[0] > WINDOWWIDTH + MARGIN + SHIPSIZE or
            self.pos[1] > WINDOWHEIGHT + MARGIN + SHIPSIZE or
            self.pos[0] < 0 - MARGIN or
            self.pos[1] < 0 - MARGIN):
            del(self)
            return True



if __name__ == '__main__':
    main()
