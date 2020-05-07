import pygame
import math

WINDOW_SIZE = [600, 600]
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (155, 155, 155)
LGREEN = (0, 125, 0)
PURPLE = (255,0,255)

ROWS = 25
COLUMNS = 25

# Dynamically determined margin, width, and height so you can make squares larger/smaller
MARGIN = (WINDOW_SIZE[0]+WINDOW_SIZE[1])//((ROWS+COLUMNS)*5)
WIDTH = (WINDOW_SIZE[0]-(COLUMNS+1)*MARGIN)/COLUMNS
HEIGHT = (WINDOW_SIZE[1]-(ROWS+1)*MARGIN)/ROWS
# Adjusting window size slightly so there isn't dead space on the bottom and right side
WINDOW_SIZE[0] -= int((WIDTH%1)*COLUMNS)
WINDOW_SIZE[1] -= int((HEIGHT%1)*ROWS)
# Convert to ints now that the window size fits these grid dimensions nicely
WIDTH = int(WIDTH)
HEIGHT = int(HEIGHT)
DIAGONALS = True

def getloc():
    x,y = pygame.mouse.get_pos()
    xcord = x//(WIDTH+MARGIN)
    ycord = y//(HEIGHT+MARGIN)
    # Checking if user clicked far edge of grid which would be out of bounds
    if xcord == ROWS:
        xcord = xcord - 1
    if ycord == COLUMNS:
        ycord = ycord - 1
    return (xcord, ycord)

def clear(i):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if grid[r][c] == i:
                grid[r][c] = 0

def emptygrid():
    for r in range(ROWS):
        for c in range(COLUMNS):
            grid[r][c] = 0

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        # Parent used for backtracking
        self.parent = parent
        # G is the cost of the best known path from start to this node
        self.g = 0
        # H is an approximation of the cost from this node to the end
        self.h = 0
        # F is g + h
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.position == other.position

    def dist(self, end):
        x1, y1 = self.position
        x2, y2 = end.position
        return math.sqrt(abs(x1-x2)**2+abs(y1-y2)**2)


def findpath(s, e):
    start = Node(s)
    end = Node(e)

    open = [start]
    closed = []

    gscore = 0
    fscore = 0

    while len(open) > 0:
        print(len(open))
        open.sort()
        current = open.pop(0)
        closed.append(current)
        x,y = current.position

        neighbors = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        if DIAGONALS:
            neighbors.extend([(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)])

        for pos in neighbors:
            newx = pos[0]
            newy = pos[1]
            if COLUMNS > newx >= 0 and ROWS > newy >= 0:
                n = Node(pos, current)
                if grid[newy][newx] == 1 or n == start or n in closed:
                    continue
                elif n == end:
                    p = []
                    while current != start:
                        p.append(current.position)
                        current = current.parent
                    return p[::-1]
                else:
                    grid[newy][newx] = 5
                    n.g = n.dist(current)+current.g
                    n.h = n.dist(end)
                    n.f = n.g+n.h
                    ## Tried making this if not open: but the program freezes
                    if n not in open:
                        open.append(n)
                    else:
                        for i,o in enumerate(open):
                            if n == o:
                                if n < o:
                                    open.pop(i)
                                    open.append(n)
                                continue
    return None


grid = []
for row in range(ROWS):
    grid.append([])
    for column in range(COLUMNS):
        grid[row].append(0)

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("A* Algorithm")

done = False

clock = pygame.time.Clock()
start = (0,0)
end = (0,0)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                clear(4)
                clear(5)
                clear(6)
                path = findpath(start, end)
                if path:
                    for p in path:
                        grid[p[1]][p[0]] = 6
                else:
                    print("No path found")
            elif event.key == pygame.K_BACKSPACE:
                emptygrid()
            elif event.key == pygame.K_s:
                x, y = getloc()
                clear(2)
                grid[y][x] = 2
                start = (x,y)
            elif event.key == pygame.K_f:
                x, y = getloc()
                clear(3)
                grid[y][x] = 3
                end = (x,y)

    click = pygame.mouse.get_pressed()
    if click[0]:
        x, y = getloc()
        grid[y][x] = 1
    elif click[1]:
        clear(1)
    elif click[2]:
        x, y = getloc()
        grid[y][x] = 0


    screen.fill(BLACK)
    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE
            if grid[row][column] == 1:
                color = RED
            elif grid[row][column] == 2:
                color = LGREEN
            elif grid[row][column] == 3:
                color = YELLOW
            elif grid[row][column] == 4:
                color = GREEN
            elif grid[row][column] == 5:
                color = GREY
            elif grid[row][column] == 6:
                color = PURPLE
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
    clock.tick(60)

    pygame.display.flip()

pygame.quit()
