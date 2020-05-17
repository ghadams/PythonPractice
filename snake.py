import pygame
import math
import random
## Make an Item Class that contains two variables, index and color
## Create items list with each 'item' type (wall, empty, etc)
## Or maybe this isn't worth doing

# Maybe create dict of item:color pairs so that you can do colors[WALL] or whatever
TICKSPEED = 10
WINDOW_SIZE = [600, 600]
ROWS = 25
COLUMNS = 25
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
DGREEN = (0,125,0)
PURPLE = (255,0,255)
# Dynamically determined margin, width, and height so you can make squares larger/smaller
MARGIN = (WINDOW_SIZE[0]+WINDOW_SIZE[1])//((ROWS+COLUMNS)*20)
WIDTH = (WINDOW_SIZE[0]-(COLUMNS+1)*MARGIN)/COLUMNS
HEIGHT = (WINDOW_SIZE[1]-(ROWS+1)*MARGIN)/ROWS
# Adjusting window size slightly so there isn't dead space on the bottom and right side
WINDOW_SIZE[0] -= int((WIDTH%1)*COLUMNS)
WINDOW_SIZE[1] -= int((HEIGHT%1)*ROWS)
# Convert to ints now that the window size fits these grid dimensions nicely
WIDTH = int(WIDTH)
HEIGHT = int(HEIGHT)

grid = []
open = []
for row in range(ROWS):
    grid.append([])
    for column in range(COLUMNS):
        grid[row].append(BLACK)
        open.append((row, column))



def randopen():
    return open[random.randint(0,len(open)-1)]

def getAdjacentOpen(coord):
    x,y = coord
    dirs = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    for point in dirs:
        if point in open:
            return point



class Snake():
    def __init__(self):
        self.head = randopen()
        while self.head[0] < ROWS/2:
            self.head = randopen()
        self.len = 3
        self.dir = pygame.K_UP
        self.body = [self.head]
        self.food = randopen()
        while len(self.body) < self.len:
            self.body.append(getAdjacentOpen(self.body[-1]))

    def isValid(self):
        ret = True
        x,y = self.head
        if x < 0 or x >= COLUMNS:
            ret = False
        elif y < 0 or y >= ROWS:
            ret = False
        elif self.head in self.body[1:]:
            ret = False
        return ret

    def move(self):
        next = self.head
        if(self.dir == pygame.K_UP):
            next = (self.head[0]-1, self.head[1])
        elif(self.dir == pygame.K_DOWN):
            next = (self.head[0]+1, self.head[1])
        elif(self.dir == pygame.K_LEFT):
            next = (self.head[0], self.head[1]-1)
        elif(self.dir == pygame.K_RIGHT):
            next = (self.head[0], self.head[1]+1)
        self.head = next
        self.body.insert(0, self.head)

        if not self.isValid():
            return False
        open.remove(next)

        if self.head == self.food:
            self.food = randopen()
            self.len = self.len + 1
        else:
            open.append(self.body[-1])
            self.body = self.body[:-1]
        return True



snake = Snake()



pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Snake")

done = False

clock = pygame.time.Clock()
start = (0,0)
end = (0,0)
goodmove = True

while not done:
    newdir = snake.dir
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.dir != pygame.K_RIGHT:
                newdir = pygame.K_LEFT
            elif event.key == pygame.K_RIGHT and snake.dir != pygame.K_LEFT:
                newdir = pygame.K_RIGHT
            elif event.key == pygame.K_DOWN and snake.dir != pygame.K_UP:
                newdir = pygame.K_DOWN
            elif event.key == pygame.K_UP and snake.dir != pygame.K_DOWN:
                newdir = pygame.K_UP

    #screen.fill(WHITE)
    for row in range(ROWS):
        for column in range(COLUMNS):
            color = BLACK
            if (row,column) in snake.body:
                color = GREEN if goodmove else DGREEN
            elif (row,column) == snake.food:
                color = PURPLE
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
    if goodmove:
        snake.dir = newdir
        goodmove = snake.move()
        
    clock.tick(TICKSPEED)

    pygame.display.flip()

pygame.quit()
