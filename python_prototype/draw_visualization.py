import sys
import pygame
from pygame.locals import KEYDOWN, K_q
import hazard_pathfinder

"""
Original Pygame grid visualization code by Keno Leon:
https://betterprogramming.pub/making-grids-in-python-7cf62c95f413
GitHub: https://gist.github.com/KenoLeon/bbbbe02f38e32af53ae134d8fdad0de0#file-pygamereadmaptogrid-py

Modified to visualize shortest paths algorithms on a 2D grid.
Numbering begins in the top left corner
row = x
column = y

To use with Safe* and A* search:
 Inputs:
 size: an integer for the (square) grid side length
 obstacles: a list of coordinates describing the shape of obstacles in the format (from top left) 
            [[topleftx, toplefty], verticalheightdown = int, horizontal_width_right = int]
 exits = List of [x,y] coordinates of exit(s)
 hazards = List of [x,y] coordinates of hazard(s)
 start = [x,y] coordinate of start location
 
 Output:
 The grid with:
  Obstacle/blocked squares marked in black.
  hazard Location(s) marked in red.
  Start Location marked in blue.
  Exit(s) marked in green.
  The Safe* Path is marked in purple.
  The A* Path is marked in orange. (in the case they share the same square Safe* is colored over by A*)  
"""


# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 140, 0)
GREY = (160, 160, 160)

# 2D GRID MAP:

# FIGURE 1 - Safe Exit
# 9x9 Small Grid Demonstration
# Comment out this section to the next comment to change visualization
"""obstacles = [[[1, 1], 1, 3],
             [[1, 1], 4, 1],
             [[3, 3], 2, 1],
             [[1, 5], 4, 1],
             [[1, 7], 1, 2],
             [[4, 7], 1, 2],
             [[6, 0], 1, 5],
             [[6, 4], 2, 1],
             [[6, 6], 1, 3],
             [[8, 6], 1, 1]]
exits = [[3, 8], [8, 0]]
hazards = [[0, 6]]
size = 9
start = [1, 4]"""
# Comment to here

# FIGURE 2 - Safe Exit
# 13x13 Medium Grid Demonstration
# Comment out this section to the next comment to change visualization
"""obstacles = [[[1, 1], 3, 1],
                 [[1, 3], 1, 3],
                 [[1, 6], 4, 1],
                 [[1, 8], 2, 1],
                 [[1, 10], 1, 2],
                 [[1, 11], 4, 1],
                 [[4, 3], 1, 4],
                 [[4, 8], 1, 4],
                 [[6, 0], 1, 3],
                 [[6, 4], 6, 1],
                 [[6, 6], 4, 1],
                 [[6, 8], 1, 4],
                 [[6, 11], 3, 1],
                 [[9, 0], 2, 3],
                 [[9, 6], 1, 6],
                 [[11, 6], 2, 1],
                 [[11, 6], 1, 3],
                 [[11, 10], 1, 3],
                 [[12, 2], 1, 1]]
exits = [[8, 0], [5, 12]]
hazards = [[0, 11]]
size = 13
start = [8, 10]"""
# Comment to here

# FIGURE 3 - Safe Exit
# 13x13 Medium Grid Demonstration
# Comment out this section to the next comment to change visualization
obstacles = [[[1, 1], 3, 1],
                 [[1, 3], 1, 3],
                 [[1, 6], 4, 1],
                 [[1, 8], 2, 1],
                 [[1, 10], 1, 2],
                 [[1, 11], 4, 1],
                 [[4, 3], 1, 4],
                 [[4, 8], 1, 4],
                 [[6, 0], 1, 3],
                 [[6, 4], 6, 1],
                 [[6, 6], 4, 1],
                 [[6, 8], 1, 4],
                 [[6, 11], 3, 1],
                 [[9, 0], 2, 3],
                 [[9, 6], 1, 6],
                 [[11, 6], 2, 1],
                 [[11, 6], 1, 3],
                 [[11, 10], 1, 3],
                 [[12, 2], 1, 1]]
exits = [[0, 6], [5, 0], [12, 5], [5, 12]]
hazards = [[3, 12], [3, 0]]
size = 13
start = [8, 10]
# Comment to here

# FIGURE 4 - Too many hazards example
# 13x13 Medium Grid Demonstration
# Comment out this section to the next comment to change visualization
"""obstacles = [[[1, 1], 3, 1],
                 [[1, 3], 1, 3],
                 [[1, 6], 4, 1],
                 [[1, 8], 2, 1],
                 [[1, 10], 1, 2],
                 [[1, 11], 4, 1],
                 [[4, 3], 1, 4],
                 [[4, 8], 1, 4],
                 [[6, 0], 1, 3],
                 [[6, 4], 6, 1],
                 [[6, 6], 4, 1],
                 [[6, 8], 1, 4],
                 [[6, 11], 3, 1],
                 [[9, 0], 2, 3],
                 [[9, 6], 1, 6],
                 [[11, 6], 2, 1],
                 [[11, 6], 1, 3],
                 [[11, 10], 1, 3],
                 [[12, 2], 1, 1]]
exits = [[0, 6], [5, 0], [12, 5], [5, 12]]
hazards = [[9, 12], [3, 0], [0, 8], [12, 3]]
size = 13
start = [8, 10]"""
# Comment to here

# FIGURE 5 - Exits too far away example
# 13x13 Medium Grid Demonstration
# Comment out this section to the next comment to change visualization
"""obstacles = [[[1, 1], 3, 1],
                 [[1, 3], 1, 3],
                 [[1, 6], 4, 1],
                 [[1, 8], 2, 1],
                 [[1, 10], 1, 2],
                 [[1, 11], 4, 1],
                 [[4, 3], 1, 4],
                 [[4, 8], 1, 4],
                 [[6, 0], 1, 3],
                 [[6, 4], 6, 1],
                 [[6, 6], 4, 1],
                 [[6, 8], 1, 4],
                 [[6, 11], 3, 1],
                 [[9, 0], 2, 3],
                 [[9, 6], 1, 6],
                 [[11, 6], 2, 1],
                 [[11, 6], 1, 3],
                 [[11, 10], 1, 3],
                 [[12, 2], 1, 1]]
exits = [[12, 0], [0, 0], [5, 12]]
hazards = [[0, 11]]
size = 13
start = [1, 9]"""
# Comment to here


# initialize hazard_pathfinding
hazard_pathfinder.graph = hazard_pathfinder.Graph(size, obstacles, exits)
hazard_pathfinder.graph.graph_initialize()
hazard_pathfinder.graph.node_get_neighbors()
hazard_pathfinder.graph.node_set_d_exit()
hazard_pathfinder.graph.hazard_wavefront(hazards)
# Find Safe* path
safest_shortest_path = hazard_pathfinder.graph.safest_escape_path(start)

# Find A* path
a_star_shortest_path = hazard_pathfinder.graph.regular_a_star(start)

# Create copy of grid for visualization
cellMAP = hazard_pathfinder.grid_construct(size, obstacles)

# Mark all Safe* path locations
for node in safest_shortest_path:
    coordinate = hazard_pathfinder.graph.nodes[node-1].coords
    cellMAP[coordinate[0]][coordinate[1]] = 2

# Mark all A* path locations
for node in a_star_shortest_path:
    coordinate = hazard_pathfinder.graph.nodes[node-1].coords
    cellMAP[coordinate[0]][coordinate[1]] = 3

# Mark hazard locations
for hazard in hazards:
    if type(hazard) == list:
        cellMAP[hazard[0]][hazard[1]] = 4
    else:
        cellMAP[hazard] = 4

# Mark the start location
cellMAP[start[0]][start[1]] = 5

# Mark Exits
for location in exits:
    if type(location) == list:
        cellMAP[location[0]][location[1]] = 6
    else:
        cellMAP[location] = 6


_VARS = {'surf': False, 'gridWH': 400,
         'gridOrigin': (200, 100), 'gridCells': cellMAP.shape[0], 'lineWidth': 2}


def main():
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        drawSquareGrid(
         _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
        placeCells()
        pygame.display.update()


# NEW METHOD FOR ADDING CELLS :
def placeCells():
    # GET CELL DIMENSIONS...
    cellBorder = 6
    celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)
    # Color the squares with correct colors
    for row in range(cellMAP.shape[0]):
        for column in range(cellMAP.shape[1]):
            # Is the grid cell tiled ?
            if(cellMAP[column][row] == 0):
                drawWallCell(
                    _VARS['gridOrigin'][0] + (celldimY*row)
                    + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                    _VARS['gridOrigin'][1] + (celldimX*column)
                    + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2,
                    celldimX, celldimY)
            if (cellMAP[column][row] == 3):
                drawAStarPathCell(
                    _VARS['gridOrigin'][0] + (celldimY * row)
                    + cellBorder + (2 * row * cellBorder) + _VARS['lineWidth'] / 2,
                    _VARS['gridOrigin'][1] + (celldimX * column)
                    + cellBorder + (2 * column * cellBorder) + _VARS['lineWidth'] / 2,
                    celldimX, celldimY)
            if (cellMAP[column][row] == 2):
                drawSafePathCell(
                    _VARS['gridOrigin'][0] + (celldimY * row)
                    + cellBorder + (2 * row * cellBorder) + _VARS['lineWidth'] / 2,
                    _VARS['gridOrigin'][1] + (celldimX * column)
                    + cellBorder + (2 * column * cellBorder) + _VARS['lineWidth'] / 2,
                    celldimX, celldimY)
            if (cellMAP[column][row] == 4):
                drawhazardCell(
                    _VARS['gridOrigin'][0] + (celldimY * row)
                    + cellBorder + (2 * row * cellBorder) + _VARS['lineWidth'] / 2,
                    _VARS['gridOrigin'][1] + (celldimX * column)
                    + cellBorder + (2 * column * cellBorder) + _VARS['lineWidth'] / 2,
                    celldimX, celldimY)
            if (cellMAP[column][row] == 5):
                drawStartCell(
                    _VARS['gridOrigin'][0] + (celldimY * row)
                    + cellBorder + (2 * row * cellBorder) + _VARS['lineWidth'] / 2,
                    _VARS['gridOrigin'][1] + (celldimX * column)
                    + cellBorder + (2 * column * cellBorder) + _VARS['lineWidth'] / 2,
                    celldimX, celldimY)
            if (cellMAP[column][row] == 6):
                drawExitCell(
                    _VARS['gridOrigin'][0] + (celldimY * row)
                    + cellBorder + (2 * row * cellBorder) + _VARS['lineWidth'] / 2,
                    _VARS['gridOrigin'][1] + (celldimX * column)
                    + cellBorder + (2 * column * cellBorder) + _VARS['lineWidth'] / 2,
                    celldimX, celldimY)

# Draw filled rectangle at coordinates for each color/type
def drawWallCell(x, y, dimX, dimY):
    pygame.draw.rect(
     _VARS['surf'], BLACK,
     (x, y, dimX, dimY)
    )

def drawhazardCell(x, y, dimX, dimY):
    pygame.draw.rect(
     _VARS['surf'], RED,
     (x, y, dimX, dimY)
    )

def drawStartCell(x, y, dimX, dimY):
    pygame.draw.rect(
     _VARS['surf'], BLUE,
     (x, y, dimX, dimY)
    )

def drawSafePathCell(x, y, dimX, dimY):
    pygame.draw.rect(
     _VARS['surf'], PURPLE,
     (x, y, dimX, dimY)
    )

def drawAStarPathCell(x, y, dimX, dimY):
    pygame.draw.rect(
     _VARS['surf'], ORANGE,
     (x, y, dimX, dimY)
    )

def drawExitCell(x, y, dimX, dimY):
    pygame.draw.rect(
     _VARS['surf'], GREEN,
     (x, y, dimX, dimY)
    )


def drawSquareGrid(origin, gridWH, cells):

    CONTAINER_WIDTH_HEIGHT = gridWH
    cont_x, cont_y = origin

    # DRAW Grid Border:
    # TOP lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (cont_x, cont_y),
      (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y), _VARS['lineWidth'])
    # # BOTTOM lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (cont_x, CONTAINER_WIDTH_HEIGHT + cont_y),
      (CONTAINER_WIDTH_HEIGHT + cont_x,
       CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])
    # # LEFT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (cont_x, cont_y),
      (cont_x, cont_y + CONTAINER_WIDTH_HEIGHT), _VARS['lineWidth'])
    # # RIGHT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y),
      (CONTAINER_WIDTH_HEIGHT + cont_x,
       CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])

    # Get cell size, just one since its a square grid.
    cellSize = CONTAINER_WIDTH_HEIGHT/cells

    # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
    for x in range(cells):
        pygame.draw.line(
           _VARS['surf'], BLACK,
           (cont_x + (cellSize * x), cont_y),
           (cont_x + (cellSize * x), CONTAINER_WIDTH_HEIGHT + cont_y), 2)
    # # HORIZONTAl DIVISIONS
        pygame.draw.line(
          _VARS['surf'], BLACK,
          (cont_x, cont_y + (cellSize*x)),
          (cont_x + CONTAINER_WIDTH_HEIGHT, cont_y + (cellSize*x)), 2)


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
