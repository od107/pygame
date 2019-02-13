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
    pygame.key.set_repeat(1, 100) #still makes sense or not?

    pygame.display.set_caption('Asteroids')

    #initialize
    score = 0
    ship = Ship()
    bullets = []
    asteroids = []
    shipImg = pygame.image.load('ship.png').convert()
    shipImg.set_colorkey((0, 0, 0))
    astrospawn = pygame.USEREVENT + 1
    pygame.time.set_timer(astrospawn, 5000)

    DISPLAYSURF.fill(BGCOLOR)

    while True: # main game loop
        DISPLAYSURF.fill(BGCOLOR)
        draw(shipImg, ship, bullets, asteroids)

        #TODO: change repetition speed of shooting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == astrospawn:
                asteroids.append(Asteroid())
            #elif event.type == KEYDOWN and event.key == K_SPACE:
            #    bullets.append(ship.shoot())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_UP]:
            ship.accelerate()
        if keys[pygame.K_SPACE]:
            bullets.append(ship.shoot())
        if keys[pygame.K_RIGHT]:
            ship.rotateRight()
        if keys[pygame.K_LEFT]:
            ship.rotateLeft()

        # Update positions
        ship.move()

        for asteroid in asteroids:
            if asteroid.move():
                asteroids.remove(asteroid)

        for bullet in bullets:
            if bullet.move():
                bullets.remove(bullet)

        pygame.display.update()

        #collission detection
        for bullet in bullets:
            for asteroid in asteroids:
                if distance(bullet.pos, asteroid.pos) < asteroid.size:
                    bullets.remove(bullet)
                    pieces = asteroid.hit()
                    if pieces is not None:
                        for new_asteroid in pieces:
                            asteroids.append(new_asteroid)
                    asteroids.remove(asteroid)
                    score += 10
                    break

        #TODO display score
        #TODO spaceship collission


        FPSCLOCK.tick(FPS)
        #print(FPSCLOCK.get_fps())


def distance(posA, posB):
    return math.sqrt(math.pow(posA[0]-posB[0], 2) + math.pow(posA[1]-posB[1], 2))


def draw(shipImg, ship, bullets, asteroids):
    #TODO fix border transitions
    #should the draw function be part of an object? Or be a separate part of the program?

    blittedRect = DISPLAYSURF.blit(shipImg, ship.pos) # convert should be moved elsewhere

    oldCenter = blittedRect.center
    rotatedSurf = pygame.transform.rotate(shipImg, math.degrees(ship.orientation - math.pi/2))

    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(rotatedSurf, rotRect)

    for bullet in bullets:
        pygame.draw.rect(DISPLAYSURF, WHITE, ((bullet.pos), (BULLETSIZE, BULLETSIZE)))

    for asteroid in asteroids:
        pygame.draw.circle(DISPLAYSURF, WHITE, (int(asteroid.pos[0]),int(asteroid.pos[1])), asteroid.size, 3)

    #for testing purposes
    #pygame.draw.rect(DISPLAYSURF, GREEN, ((ship.pos), (1, 1)))


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

    def rotateLeft(self):
        self.orientation += math.pi / 18

    def shoot(self):
        bullet = Bullet(self.pos, self.orientation, self.vel)
        return bullet


class Bullet:
    shootSpeed = 5

    def __init__(self, shippos, shiporientation, shipvel):
        self.pos = [shippos[0] + SHIPSIZE/2,
                    shippos[1] + SHIPSIZE/2]
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
            return True


class Asteroid:
    Lsize = 30
    Msize = 15
    Ssize = 5

    Lspeed = 2
    Mspeed = 3
    Sspeed = 5

    def __init__(self, position=None, direction=None, speed=Lspeed, size=Lsize):
        if position is not None:
            self.pos = position
            self.dir = direction


        else:
            #self.size = self.Lsize
            edge = random.randint(0, 3)
            if edge == 2:
                self.pos = [random.randint(0, WINDOWWIDTH-1), 0]
            elif edge == 3:
                self.pos = [0, random.randint(0, WINDOWHEIGHT-1)]
            elif edge == 0:
                self.pos = [random.randint(0, WINDOWWIDTH-1), WINDOWHEIGHT-1]
            elif edge == 1:
                self.pos = [WINDOWWIDTH-1, random.randint(0, WINDOWHEIGHT-1)]

            self.dir = random.uniform(0, math.pi) + edge * math.pi / 2

        self.vel = [speed * math.cos(self.dir), speed * math.sin(self.dir)]
        self.size = size

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] -= self.vel[1]

        if(self.pos[0] > WINDOWWIDTH + MARGIN or
           self.pos[1] > WINDOWHEIGHT + MARGIN or
           self.pos[0] < 0 - MARGIN or
           self.pos[1] < 0 - MARGIN):
            return True

    def hit(self):
        angle = math.pi / 9

        if self.size == self.Lsize:
            speed = self.Mspeed
            size = self.Msize
        elif self.size == self.Msize:
            speed = self.Sspeed
            size = self.Ssize
        elif self.size == self.Ssize:
            return None

        pieces = [Asteroid(self.pos.copy(), self.dir + angle, speed, size),
                  Asteroid(self.pos.copy(), self.dir - angle, speed, size)]

        return pieces


if __name__ == '__main__':
    main()
