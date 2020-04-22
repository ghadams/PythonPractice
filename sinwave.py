

import math
import time
def game():
    gran = 40
    shift = 100/gran
    x = 0
    step = .2
    while 1:
        line = ['-']*gran
        yval = math.sin(x)
        x += step
        ind = round((yval*gran/2)+0.5)
        if ind > 0:
            line[int(gran/2)-1+ind] = "\\"
        elif ind == 0:
            line[int(gran/2)-1+ind] = '|'
        else:
            line[int(gran/2)-1+ind] = '/'
        print(''.join(line), )
        time.sleep(.1)

while 1:
    game()
