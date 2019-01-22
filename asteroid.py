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

    pygame.display.set_caption('Asteroids')

    #initialize

    ship = Ship()
    #TODO: asteroids
    

    DISPLAYSURF.fill(BGCOLOR)
    
    while True: # main game loop
        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        draw(ship)

        #continue

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
        ship.move();
 
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def draw(ship):
    """points = [ [ ship.pos[0], ship.pos[1] ],
               [ ship.pos[0] + SHIPSIZE * math.cos(ship.orientation), ship.pos[0] + SHIPSIZE * math.sin(ship.orientation)],
               [ ship.pos[0] - SHIPSIZE * math.cos(ship.orientation), ship.pos[0] - SHIPSIZE * math.sin(ship.orientation)],
            ] # funny 3D rotating triangle
    """
    surf = pygame.Surface((SHIPSIZE, SHIPSIZE))
    #surf.fill((255,100,100))
    surf.set_colorkey((0, 0, 0))



    points = [ [ ship.pos[0], ship.pos[1] ],
               [ship.pos[0] - SHIPSIZE/2, ship.pos[1] + SHIPSIZE],
               [ship.pos[0] + SHIPSIZE/2, ship.pos[1] + SHIPSIZE]
            ]
    points = [ [ SHIPSIZE/2, 0  ],
               [0, SHIPSIZE],
               [SHIPSIZE, SHIPSIZE]
            ]
    #the rotating part doesnt work yet as it should
    pygame.draw.polygon(surf, WHITE, points, 2)
    where = [ ship.pos[0], ship.pos[1]]
    blittedRect = DISPLAYSURF.blit(surf, where)

    oldCenter = blittedRect.center
    rotatedSurf = pygame.transform.rotate(surf, math.degrees(ship.orientation))

    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter
    
    DISPLAYSURF.blit(rotatedSurf, rotRect)


class Ship:
    maxSpeed = 100
    
    def __init__(self):
        self.pos = [int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)]
        self.orientation = - math.pi/2
        self.vel = [0, 0]

    def accelerate(self):
        self.vel[0] += math.cos(self.orientation)/5
        self.vel[1] += math.sin(self.orientation)/5
        print('velocity: ',self.vel)
        #TODO limit to max vel

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
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
        self.orientation += math.pi / 18
        print('orientation: ', self.orientation)

    def rotateLeft(self):
        self.orientation -= math.pi / 18
        print('orientation: ', self.orientation)

    def shoot(self):
        pass
        #to implement
        

    


if __name__ == '__main__':
    main()
