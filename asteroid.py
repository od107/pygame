#my second taste of python
#asteroid game

import random, pygame, sys, math
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
SHIPSIZE = 20
MARGIN = 50

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
    #TODO: asteroids
    

    DISPLAYSURF.fill(BGCOLOR)
    
    while True: # main game loop
        DISPLAYSURF.fill(BGCOLOR)
        draw(ship)

        #difference keyup and keypressed

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    ship.accelerate()
                if event.key == K_SPACE:
                    ship.fire()
                if event.key == K_RIGHT:
                    ship.rotateRight()
                if event.key == K_LEFT:
                    ship.rotateLeft()
    
        # Update position
        ship.move()

        pygame.display.update()
        FPSCLOCK.tick(FPS)



def draw(ship):
    #TODO fix border transitions

    blittedRect = DISPLAYSURF.blit(ship.img, ship.pos)

    oldCenter = blittedRect.center
    rotatedSurf = pygame.transform.rotate(ship.img, math.degrees(ship.orientation - math.pi/2))

    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter
    
    DISPLAYSURF.blit(rotatedSurf, rotRect)


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
        print('velocity: ',self.vel)
        #TODO limit to max vel

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] -= self.vel[1]
        #print('position: ',self.pos)
           
        if(self.pos[0] > WINDOWWIDTH + MARGIN):
            self.pos[0] = 0 - MARGIN
        elif(self.pos[1] > WINDOWHEIGHT + MARGIN):
            self.pos[1] = 0 - MARGIN
        elif(self.pos[0] < 0 - MARGIN):
            self.pos[0] = WINDOWWIDTH + MARGIN
        elif(self.pos[1] < 0 - MARGIN):
            self.pos[1] = WINDOWWIDTH + MARGIN
        

    def rotateRight(self):
        self.orientation -= math.pi / 18
        print('orientation: ', self.orientation)

    def rotateLeft(self):
        self.orientation += math.pi / 18
        print('orientation: ', self.orientation)

    def shoot(self):
        pass
        #to implement
        

    


if __name__ == '__main__':
    main()
