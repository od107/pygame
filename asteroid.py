# my second taste of python
# asteroid game

import math
import pygame
import random
import sys

FPS = 30  # frames per second, the general speed of the program
WINDOWWIDTH = 640  # size of window's width in pixels
WINDOWHEIGHT = 480  # size of windows' height in pixels
SHIPSIZE = 20
MARGIN = 50 # needs to be bigger than SHIPSIZE
BULLETSIZE = 3

#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
DGREEN = (0, 100, 0)
BLACK = (0, 0, 0)

BGCOLOR = BLACK
LIGHTBGCOLOR = YELLOW

RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'

GODMODE = False

ASTEROID_SPAWN_TIME = 5000


def main():
    global FPSCLOCK, DISPLAYSURF, score, SHIP_IMG, GAMESURFACE
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    GAMESURFACE = pygame.Surface((WINDOWWIDTH + 2 * MARGIN, WINDOWHEIGHT + 2 * MARGIN))
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Asteroids')
    SHIP_IMG = pygame.image.load('ship.png').convert()  # on this location or in the class
    SHIP_IMG.set_colorkey(BLACK)

    # initialize
    score = 0
    ship = Ship()
    bullets = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    asteroid_spawn = pygame.USEREVENT + 1
    pygame.time.set_timer(asteroid_spawn, ASTEROID_SPAWN_TIME)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(ship)

    DISPLAYSURF.fill(BGCOLOR)
    running = True

    while running:  # main game loop

        # all_sprites.draw(DISPLAYSURF)
        draw(ship, bullets, asteroids)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == asteroid_spawn:
                asteroid = Asteroid()
                asteroids.add(asteroid)
                all_sprites.add(asteroid)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_UP]:
            ship.accelerate()
        if keys[pygame.K_SPACE]:
            bullet = ship.shoot()
            if bullet:
                bullets.add(bullet)
                all_sprites.add(bullet)
        if keys[pygame.K_RIGHT]:
            ship.rotate_right()
        if keys[pygame.K_LEFT]:
            ship.rotate_left()

        # Update positions
        all_sprites.update()

        # collision detection
        # TODO: change bullet collision to sprite collision
        for bullet in bullets:
            for asteroid in asteroids:
                if distance(bullet.pos, asteroid.pos) < asteroid.size:
                    bullet.kill()
                    pieces = asteroid.hit()
                    asteroid.kill()
                    if pieces is not None:
                        for new_asteroid in pieces:
                            asteroids.add(new_asteroid)
                            all_sprites.add(new_asteroid)
                    break

        hits_asteroid = pygame.sprite.spritecollide(ship, asteroids, False, pygame.sprite.collide_circle)

        if hits_asteroid:
            # print("hit by" + str(hits_asteroid))
            pygame.event.wait()
            # TODO display game over
            running = False

        FPSCLOCK.tick(FPS)
        # print(FPSCLOCK.get_fps())


def distance(pos_a, pos_b):
    return math.sqrt(math.pow(pos_a[0] - pos_b[0], 2) + math.pow(pos_a[1] - pos_b[1], 2))


def draw(ship, bullets, asteroids):
    #TODO implement/override sprite.draw function

    draw_ship(ship)

    for bullet in bullets:
        pygame.draw.rect(DISPLAYSURF, WHITE, (bullet.pos, (BULLETSIZE, BULLETSIZE)))

    for asteroid in asteroids:
        pygame.draw.circle(DISPLAYSURF, WHITE, (int(asteroid.pos[0]), int(asteroid.pos[1])), asteroid.size, 3)
        # pygame.draw.rect(DISPLAYSURF, RED, asteroid.rect, 2)

    draw_score()


def draw_ship(ship):
    # ship_topleft = [int(ship.pos[0] - SHIPSIZE / 2), int(ship.pos[1] - SHIPSIZE / 2)]

    rotated_surf = pygame.transform.rotate(SHIP_IMG, math.degrees(ship.orientation - math.pi / 2))
    rot_rect = rotated_surf.get_rect()
    rot_rect.center = ship.pos
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(rotated_surf, rot_rect)

    # pygame.draw.rect(DISPLAYSURF, RED, rot_rect, 2)

def draw_score():
    font_obj = pygame.font.Font('freesansbold.ttf', 32)
    text_surface_obj = font_obj.render(str(score), True, GREEN)
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.top = 10
    text_rect_obj.right = (WINDOWWIDTH - 10)
    DISPLAYSURF.blit(text_surface_obj, text_rect_obj)


class Ship(pygame.sprite.Sprite):
    SHOOT_DELAY_INIT = 5
    global SHIP_IMG

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = SHIP_IMG
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.pos = [int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)]
        self.orientation = math.pi / 2
        self.vel = [0, 0]
        self.shoot_delay = self.SHOOT_DELAY_INIT
        self.shot = False

    def accelerate(self):
        self.vel[0] += math.cos(self.orientation) / 5
        self.vel[1] += math.sin(self.orientation) / 5

    def update(self):
        # update shoot timer
        if self.shot:
            self.shoot_delay -= 1
            if self.shoot_delay < 1:
                self.shoot_delay = self.SHOOT_DELAY_INIT
                self.shot = False

        # update ship position
        self.pos[0] += self.vel[0]
        self.pos[1] -= self.vel[1]

        # this is needed for sprite collisions
        self.rect.center = self.pos

        #TODO update this
        if self.pos[0] > WINDOWWIDTH + MARGIN:
            self.pos[0] = 0 - MARGIN
        elif self.pos[1] > WINDOWHEIGHT + MARGIN:
            self.pos[1] = 0 - MARGIN
        elif self.pos[0] < 0 - MARGIN:
            self.pos[0] = WINDOWWIDTH + MARGIN
        elif self.pos[1] < 0 - MARGIN:
            self.pos[1] = WINDOWHEIGHT + MARGIN

    def rotate_right(self):
        self.orientation -= math.pi / 18

    def rotate_left(self):
        self.orientation += math.pi / 18

    def shoot(self):
        if not self.shot:
            self.shot = True
            bullet = Bullet(self.pos, self.orientation, self.vel)
            return bullet


class Bullet(pygame.sprite.Sprite):
    shootSpeed = 5

    def __init__(self, ship_pos, ship_orientation, ship_vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([BULLETSIZE, BULLETSIZE])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(BULLETSIZE / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect = self.image.get_rect()
        self.pos = [ship_pos[0] , ship_pos[1]]
        self.vel = [ship_vel[0] + self.shootSpeed * math.cos(ship_orientation),
                    ship_vel[1] + self.shootSpeed * math.sin(ship_orientation)]

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] -= self.vel[1]

        if (self.pos[0] > WINDOWWIDTH + MARGIN or
                self.pos[1] > WINDOWHEIGHT + MARGIN or
                self.pos[0] < 0 - MARGIN or
                self.pos[1] < 0 - MARGIN):
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    Lsize = 30
    Msize = 15
    Ssize = 5

    Lspeed = 2
    Mspeed = 3
    Sspeed = 5

    def __init__(self, position=None, direction=None, speed=Lspeed, size=Lsize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([2 * size, 2 * size])
        self.rect = self.image.get_rect()

        self.radius = size

        if position is not None:
            self.pos = position
            self.dir = direction

        else:
            edge = random.randint(0, 3)
            if edge == 2:
                self.pos = [random.randint(0, WINDOWWIDTH - 1), 0]
            elif edge == 3:
                self.pos = [0, random.randint(0, WINDOWHEIGHT - 1)]
            elif edge == 0:
                self.pos = [random.randint(0, WINDOWWIDTH - 1), WINDOWHEIGHT - 1]
            elif edge == 1:
                self.pos = [WINDOWWIDTH - 1, random.randint(0, WINDOWHEIGHT - 1)]

            self.dir = random.uniform(0, math.pi) + edge * math.pi / 2

        self.vel = [speed * math.cos(self.dir), speed * math.sin(self.dir)]
        self.size = size
        self.rect.center = self.pos

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] -= self.vel[1]

        self.rect.center = self.pos

        if (self.pos[0] > WINDOWWIDTH + MARGIN or
                self.pos[1] > WINDOWHEIGHT + MARGIN or
                self.pos[0] < 0 - MARGIN or
                self.pos[1] < 0 - MARGIN):
            self.kill()

    def hit(self):
        angle = math.pi / 9
        global score

        if self.size == self.Lsize:
            speed = self.Mspeed
            size = self.Msize
            score += 20
        elif self.size == self.Msize:
            speed = self.Sspeed
            size = self.Ssize
            score += 50
        else:
            score += 100
            return None

        pieces = [Asteroid(self.pos.copy(), self.dir + angle, speed, size),
                  Asteroid(self.pos.copy(), self.dir - angle, speed, size)]

        return pieces


if __name__ == '__main__':
    main()
