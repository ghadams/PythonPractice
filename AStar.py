import pygame
import math

WINDOW_SIZE = [600, 600]
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


BLACK = (0,0,0)

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
YELLOW = (225, 225, 0)
RED = (200, 0, 0)
PURPLE = (150,0,255)
GREY = (160, 160, 160)
LPURPLE = (150, 150, 255)

G_EMPTY = 0
G_START = 1
G_END = 2
G_WALL = 3
G_PATH = 4
G_OPEN = 5
G_CLOSED = 6

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

# Function to remove the items from the grid
def remove(items):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if grid[r][c] in items:
                grid[r][c] = G_EMPTY

def cleargrid():
    for r in range(ROWS):
        for c in range(COLUMNS):
            grid[r][c] = G_EMPTY

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
                if grid[newy][newx] == G_WALL or n == start or n in closed:
                    continue
                elif n == end:
                    p = []
                    while current != start:
                        p.append(current.position)
                        current = current.parent
                    closed.extend([])
                    return p[::-1], [n.position for n in open], [m.position for m in closed]
                else:
                    #grid[newy][newx] = G_OPEN
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
    return [],[],[]


grid = []
for row in range(ROWS):
    grid.append([])
    for column in range(COLUMNS):
        grid[row].append(G_EMPTY)

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
                # Erase old items
                remove([G_OPEN, G_PATH, G_CLOSED])
                path, opened, closed = findpath(start, end)
                if path:
                    for c in closed[1:]:
                        grid[c[1]][c[0]] = G_CLOSED
                    for p in path:
                        grid[p[1]][p[0]] = G_PATH
                    for o in opened:
                        grid[o[1]][o[0]] = G_OPEN

                else:
                    print("No path found")
            elif event.key == pygame.K_BACKSPACE:
                cleargrid()
                start = (0,0)
                end = (0,0)
            elif event.key == pygame.K_s:
                x, y = getloc()
                remove([G_START])
                grid[y][x] = G_START
                start = (x,y)
            elif event.key == pygame.K_f:
                x, y = getloc()
                remove([G_END])
                grid[y][x] = G_END
                end = (x,y)

    click = pygame.mouse.get_pressed()
    if click[0]:
        x, y = getloc()
        grid[y][x] = G_WALL
    elif click[1]:
        remove([G_WALL])
    elif click[2]:
        x, y = getloc()
        grid[y][x] = G_EMPTY


    screen.fill(BLACK)
    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE
            if grid[row][column] == G_START:
                color = GREEN
            elif grid[row][column] == G_END:
                color = YELLOW
            elif grid[row][column] == G_WALL:
                color = RED
            elif grid[row][column] == G_PATH:
                color = PURPLE
            elif grid[row][column] == G_OPEN:
                color = GREY
            elif grid[row][column] == G_CLOSED:
                color = LPURPLE
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
    clock.tick(60)

    pygame.display.flip()

pygame.quit()
