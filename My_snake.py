#my first taste of python
#snake game

import random, pygame, sys
from pygame.locals import *

FPS = 10 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
BOXSIZE = 20 # size of box height & width in pixels
GAPSIZE = 2 # size of gap between boxes in pixels
BOARDWIDTH = 20 # number of columns of icons
BOARDHEIGHT = 20 # number of rows of icons
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
assert(XMARGIN > 0 and YMARGIN > 0), "Boxes don't fit in the window"

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

BGCOLOR = DGREEN
LIGHTBGCOLOR = YELLOW
BOXCOLOR = GRAY
HIGHLIGHTCOLOR = WHITE
SNAKECOLOR = WHITE
FOODCOLOR = RED

RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'

GODMODE = False

SNAKELENGTH = 3

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('My snake')

    #initialize board, snake, food(later)
    mainBoard = initBoard()
    snakeHead = [int(BOARDWIDTH/2), int(BOARDHEIGHT/2)]
    snakeDirection = RIGHT
    snake = initSnake(snakeHead)
    food = initFood(snake)
    

    DISPLAYSURF.fill(BGCOLOR)
    
    while True: # main game loop
        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, snake, food)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP and snakeDirection != DOWN:
                    snakeDirection = UP
                if event.key == K_DOWN and snakeDirection != UP:
                    snakeDirection = DOWN
                if event.key == K_RIGHT and snakeDirection != LEFT:
                    snakeDirection = RIGHT
                if event.key == K_LEFT and snakeDirection != RIGHT:
                    snakeDirection = LEFT
    
        # Update snake head
        if(snakeDirection == RIGHT):
            snakeHead[0] = snakeHead[0] + 1 
        if(snakeDirection == LEFT):
            snakeHead[0] = snakeHead[0] - 1
        if(snakeDirection == UP):
            snakeHead[1] = snakeHead[1] - 1
        if(snakeDirection == DOWN):
            snakeHead[1] = snakeHead[1] + 1
        
        if(GODMODE == True):
            if(snakeHead[0]>=BOARDWIDTH):
                snakeHead[0]=0
            if(snakeHead[1]>=BOARDHEIGHT):
                snakeHead[1]=0
            if(snakeHead[0]<0):
                snakeHead[0]=BOARDWIDTH-1
            if(snakeHead[1]<0):
                snakeHead[1]=BOARDHEIGHT-1
        else:         
            if(snakeHead[0]>=BOARDWIDTH or snakeHead[1]>=BOARDHEIGHT
               or snakeHead[0]<0 or snakeHead[1]<0
               or snakeHead in snake):
                #game is lost
                gameLostAnimation(mainBoard, snake, food)
                mainBoard = initBoard()
                #put these things in initialisation function
                snakeHead = [int(BOARDWIDTH/2), int(BOARDHEIGHT/2)]
                snakeDirection = RIGHT
                snake = initSnake(snakeHead)
                #food =
                initFood(snake)

        #update snake
        snake.insert(0, snakeHead[:])
        if(snakeHead != food):
            snake.pop()
        else:
            food = initFood(snake, food)
            
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def initBoard():
     # Create the board data structure, probably faster way to do this
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append([])
        board.append(column)
    return board

def initSnake(snakeHead):
    snake = []
    #snake = [snakeHead]
    assert (snakeHead[0]-SNAKELENGTH+1 > 0) , "initial snake too big"
    for i in range(SNAKELENGTH):
        segment = [snakeHead[0]-(i), snakeHead[1]]
        snake.append(segment)
    return snake

def initFood(snake, food=None):
    #make sure food doesnt drop under snake
    #isn't this possible without returning the food?
    while(food in snake or food == None):
        food = [random.randint(0,BOARDWIDTH-1), random.randint(0,BOARDHEIGHT-1)]
    return food

        
def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)



def drawBoard(board, snake, food):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if [boxx, boxy] in snake:
                pygame.draw.rect(DISPLAYSURF, SNAKECOLOR, (left, top, BOXSIZE, BOXSIZE))
            elif [boxx, boxy] == food:
                pygame.draw.rect(DISPLAYSURF, FOODCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            


def gameLostAnimation(board, snake, food):
    # flash the background color when the player has lost
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, snake, food)
        pygame.display.update()
        pygame.time.wait(300)

if __name__ == '__main__':
    main()
