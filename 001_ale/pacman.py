import numpy as np
import cv2 as cv
import os
import time
import win32gui, win32ui, win32con, win32api
import pyautogui
import mss
import mss.tools
import random
import pytesseract
from vision import Vision
import sys
import math

# WARNING ALL THE ABS COORDINATES ARE AT 67% ZOOM  

##### Definitions
# Screen = pixel map including perimeter captured via screenshot
# Map    = pixel map exluding perimeter captured via screenshot
# Board  = char representation of the map including perimenter used for navidation

PACMAN_WINDOW_NAME = 'World\'s Biggest PAC-MAN - Google Chrome'

# browser window
PACMAN_WINDOW_MINWIDTH = 966 # 928    # minimum browser window size
PACMAN_WINDOW_MINHEIGHT = 940 # 902
# pixel representation of the board
PACMAN_SCREEN_X = 274 # 294           # pacman map rectangle including perimeter  
PACMAN_SCREEN_Y = 246 # 264      
PACMAN_SCREEN_WIDTH  = 652 # 590 
PACMAN_SCREEN_HEIGHT = 652 # 590    

PACMAN_SCREEN_PERIMETER_THICKNESS = 12 # 13 
PACMAN_MAP_X = PACMAN_SCREEN_X + PACMAN_SCREEN_PERIMETER_THICKNESS            # pacman map rectangle perimeter excluded PACMAN_SCREEN_ +/- THICKNESS
PACMAN_MAP_Y = PACMAN_SCREEN_Y + PACMAN_SCREEN_PERIMETER_THICKNESS
PACMAN_MAP_WIDTH  = (PACMAN_SCREEN_WIDTH - 2 * PACMAN_SCREEN_PERIMETER_THICKNESS)   
PACMAN_MAP_HEIGHT = (PACMAN_SCREEN_HEIGHT - 2 * PACMAN_SCREEN_PERIMETER_THICKNESS) 

# pixel representation of map pbject cell
PACMAN_MAP_CELL     = 19        # cell square avg size
PACMAN_MAP_CELL_ERR = 1         # cell square tollerance

PACMAP_GHOST_WIDTH  = 30
PACMAN_GHOST_HEIGHT = 30
PACMAN_GHOST_CELL   = 30

PACMAN_PLAYERSCORE_X = 350      # player1 score rectangle
PACMAN_PLAYERSCORE_Y = 226
PACMAN_PLAYERSCORE_WIDTH  = 150
PACMAN_PLAYERSCORE_HEIGHT = 28

# 2D matrix representation of the board
PACMAN_MAXPILL = 30             # max pill number per row or col
PACMAN_BOARD_WIDTH = 32         # 30 pills + 2 walls
PACMAN_BOARD_CAGE_WIDTH  = 5    # middle of the board ghostcage width
PACMAN_BOARD_CAGE_HEIGHT = 3    # middle of the board ghostcage height 
PACMAN_BOARD_NM = ' '           # NaM marker
PACMAN_BOARD_WALL = '▓'         # wall marker
PACMAN_BOARD_SPILL = '•'        # small pill marker
PACMAN_BOARD_BPILL = 'ʘ'        # big pill marker (power-up)
PACMAN_BOARD_GHOST = 'G'        # bad ghost marker
PACMAN_BOARD_PRAY = 'g'         # good ghost marker
PACMAN_BOARD_PMAN = '℗'         # pacman marker
PACMAN_BOARD_BLANK = ' '        # empty cell marker

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class PacManBot:
    score = -1          # player1 latest score
    windowname = ''     # window name 
    hwnd = None         # game window handle
    board = [[PACMAN_BOARD_NM for j in range(PACMAN_BOARD_WIDTH)] for i in range(PACMAN_BOARD_WIDTH)]     # board map
    mapscreenshot = None# latest screenshot

    ghosts = [[14, 16], [16, 14], [16, 15], [16, 16]]       # list of all the ghosts on the map
    ghostmap = [PACMAN_BOARD_BLANK, PACMAN_BOARD_BLANK, PACMAN_BOARD_BLANK, PACMAN_BOARD_BLANK]
    pacman = [23, 16]                                    # pacman starting coordinates
    directions = [[-1,0], [0,1], [1,0], [0,-1]]         # up, right, down, left
    keycursors = [38, 39, 40, 37]                       #VK_LEFT = 37, VK_UP = 38, VK_RIGHT = 39, VK_DOWN = 40
    keylabels ={38 : 'up', 39 : 'right', 40 : 'down', 37 : 'left'}

    def __init__(self, wname):
        self.score = 0
        self.windowname = wname

    def calibrate_map(self, color):
        return 1

    def get_distance(self, v1, v2):
        dist = [(a - b)**2 for a, b in zip(v1, v2)]
        dist = math.sqrt(sum(dist))
        return dist

    def move(self):
        print('pacman: ', self.pacman)
        minimap = [PACMAN_BOARD_NM for i in range(4)]
        moves = []
        mapoff = []
        for i in range (4): 
            minimap[i] = self.board[self.pacman[0] + self.directions[i][0]][self.pacman[1] + self.directions[i][1]]
            if ((minimap[i] != PACMAN_BOARD_GHOST) and (minimap[i] != PACMAN_BOARD_WALL)):
                moves.append(self.keycursors[i])
                mapoff.append(self.directions[i])
        print('New Minimap: ', minimap)
        print('Moves: ', moves)

        gdistance = 50
        closestghost = None
        dis1 = self.pacman
        v1 = np.array(dis1)
        for ghost in self.ghosts:
            dis2 = ghost
            v2 = np.array(dis2)
            gdis = self.get_distance(v1, v2)
            if (gdis < gdistance):
                closestghost = ghost
                gdistance = gdis     
      
        if (len(moves)):
            print('move list len: ', len(moves))
            if (len(moves) > 1):
                key = random.randrange(len(moves) - 1)
            else: 
                key = 0
            direction = moves[key]
            print('going: ', self.keylabels[direction])
            VirtualKey = win32api.MapVirtualKey(direction, 0)
            win32gui.PostMessage(self.hwnd, win32con.WM_KEYDOWN, direction, 0x0001|VirtualKey<<16)
            time.sleep(0.05)    # pacman takes about 3.8" to move across the 30 dots --> 0.12" per map cell
            win32gui.PostMessage(self.hwnd, win32con.WM_KEYUP, direction, 0x0001|VirtualKey<<16|0xC0<<24);      
##            print('old pacman: ', self.pacman)
##            self.board[self.pacman[0]][self.pacman[1]] = PACMAN_BOARD_NM 
##            self.pacman[0] += self.directions[key][0]
##            self.pacman[1] += self.directions[key][1]
##            self.board[self.pacman[0]][self.pacman[1]] = PACMAN_BOARD_PMAN
##            print('new pacman: ', self.pacman)
            

    def find_onematch(self, x, y, edge, mask):     # find if at least one of the bit of the squared patch (edge) in mask at origin (x, y) is set to 1 
        for row in range(edge-4):
            for col in range (edge-4):
                if mask[x + row][y + col]:
                    return 1
        return 0

    def find_nmatch(self, n, x, y, edge, mask):     # find if at least one of the bit of the squared patch (edge) in mask at origin (x, y) is set to 1 
        cc = 0
        for row in range(edge-4):
            for col in range (edge-4):
                if mask[x + row][y + col]:
                    cc += 1
                if (cc > n):
                    return 1
        return 0

    def find_match(self, x, y, edge, mask):     # find if at least 'min' of the bit of the squared patch (edge) in mask at origin (x, y) is set to 1 
        cc = 0
        for row in range(edge):
            for col in range (edge):
                if mask[x + row][y + col]:
                    cc += 1
        return cc

    def get_movingcharacters(self):
        gshot = self.mapscreenshot.copy()
        lower_val = np.array([255, 255, 255])        # set color filter for the white part of the ghost eyes
        upper_val = np.array([255, 255, 255])
        gmask = cv.inRange(gshot, lower_val, upper_val)
        hasghost = np.sum(gmask)
        if hasghost > 0:
            print('Ghosts detected')
        else:
            print('Ghosts NOT detected')

        res = cv.bitwise_and(gshot, gshot, mask=gmask)
        fin = np.hstack((gshot, res))
#        cv.imshow("Ghost Mask", gmask) 
#        print('Mask shape: ', np.shape(gmask))
        g2rgb = cv.cvtColor(gmask,cv.COLOR_GRAY2RGB)
        gc = 0
        if len(self.ghosts) and len(self.ghostmap):
            for ghost in self.ghosts:
                self.board[ghost[0]][ghost[1]] = self.ghostmap[gc]  # restore old board[][] on the ghost location
                gc += 1
            self.ghosts.clear()
            self.ghostmap.clear()
        print('old ghosts: ', self.ghosts)
        gc = 0
        for x in range (PACMAN_BOARD_WIDTH):
            for y in range(PACMAN_BOARD_WIDTH):        
                if (self.find_onematch(x * PACMAN_MAP_CELL, y * PACMAN_MAP_CELL, PACMAN_MAP_CELL, gmask)):
                    if (self.board[x][y] != PACMAN_BOARD_WALL):
                        self.ghostmap.append(self.board[x][y])      # backup old board[x][y] before the ghost stepped over it
                        self.board[x][y] = PACMAN_BOARD_GHOST       # set ghost on board[x][y] 
                        self.ghosts.append([x, y])                  # track ghost [x][y] coordinates
                    g2rgb = cv.rectangle(g2rgb, (y * PACMAN_MAP_CELL, x * PACMAN_MAP_CELL), ((y + 1) * PACMAN_MAP_CELL, (x + 1) * PACMAN_MAP_CELL), (255, 0, 0), 1)
#        cv.imshow('Ghost matches', g2rgb)
        print('new ghosts: ', self.ghosts)

        lower_val = np.array([255, 255, 0])        # set color filter for the pacman yellow
        upper_val = np.array([255, 255, 0])
        pmask = cv.inRange(gshot, lower_val, upper_val)
        haspac = np.sum(pmask)
        if haspac > 0:
            print('PacMan detected')
        else:
            print('Pacman NOT detected')
        res = cv.bitwise_and(gshot, gshot, mask=pmask)
        fin = np.hstack((gshot, res))
        cv.imshow("PacMan Mask", pmask) 
        print('Mask shape: ', np.shape(gmask))
        g2rgb = cv.cvtColor(pmask,cv.COLOR_GRAY2RGB)
        for x in range (PACMAN_BOARD_WIDTH):
            for y in range(PACMAN_BOARD_WIDTH):        
                if (self.find_onematch(x * PACMAN_MAP_CELL, y * PACMAN_MAP_CELL, PACMAN_MAP_CELL, pmask)):
                    if (self.board[x][y] != PACMAN_BOARD_WALL):
                        print('old pacman: ', self.pacman)
                        print('x: ', x, ' y: ', y)
                        self.board[self.pacman[0]][self.pacman[1]] = PACMAN_BOARD_BLANK
                        self.board[x][y] = PACMAN_BOARD_PMAN
                        self.pacman[0] = x
                        self.pacman[1] = y
                        g2rgb = cv.rectangle(g2rgb, (y * PACMAN_MAP_CELL, x * PACMAN_MAP_CELL), ((y + 1) * PACMAN_MAP_CELL, (x + 1) * PACMAN_MAP_CELL), (255, 0, 0), 1)
                        # cv.imshow('PacMan matches', g2rgb)
                        print('new pacman: ', self.pacman)
                        return


    def get_ghosts(self):
        gshot = self.mapscreenshot.copy()
        lower_val = np.array([255, 255, 255])        # set color filter for the blue shades of the walls
        upper_val = np.array([255, 255, 255])
        gmask = cv.inRange(gshot, lower_val, upper_val)
        hasghost = np.sum(gmask)
        if hasghost > 0:
            print('Ghosts detected')
        else:
            print('Ghosts NOT detected')
        res = cv.bitwise_and(gshot, gshot, mask=gmask)
        fin = np.hstack((gshot, res))
#        cv.imshow("Ghost Mask", gmask) 
#        print('Mask shape: ', np.shape(gmask))
        g2rgb = cv.cvtColor(gmask,cv.COLOR_GRAY2RGB)
        self.ghosts.clear()
        for x in range (PACMAN_BOARD_WIDTH):
            for y in range(PACMAN_BOARD_WIDTH):        
                if (self.find_onematch(x * PACMAN_MAP_CELL, y * PACMAN_MAP_CELL, PACMAN_MAP_CELL, gmask)):
                    if (self.board[x][y] != PACMAN_BOARD_WALL):
                        self.board[x][y] = PACMAN_BOARD_GHOST
                        self.ghosts.append([x, y])
                    g2rgb = cv.rectangle(g2rgb, (y * PACMAN_MAP_CELL, x * PACMAN_MAP_CELL), ((y + 1) * PACMAN_MAP_CELL, (x + 1) * PACMAN_MAP_CELL), (255, 0, 0), 1)
#        cv.imshow('Ghost matches', g2rgb)

    def get_walls(self):    
        wshot = self.mapscreenshot.copy()
        lower_val = np.array([8, 8, 45])        # set color filter for the blue shades of the walls
        upper_val = np.array([33, 33, 254])
        mask = cv.inRange(wshot, lower_val, upper_val)
        haswall = np.sum(mask)
        if haswall > 0:
            print('Walls detected!')
        res = cv.bitwise_and(wshot, wshot, mask=mask)
        fin = np.hstack((wshot, res))
        #cv.imshow("Wall Mask", mask)    
        print('Mask shape: ', np.shape(mask))
        g2rgb = cv.cvtColor(mask,cv.COLOR_GRAY2RGB)
        for x in range (PACMAN_BOARD_WIDTH):
            for y in range(PACMAN_BOARD_WIDTH):
                if (self.find_nmatch(2, x * PACMAN_MAP_CELL, y * PACMAN_MAP_CELL, PACMAN_MAP_CELL, mask)):
                    self.board[x][y] = PACMAN_BOARD_WALL
                    g2rgb = cv.rectangle(g2rgb, (y * PACMAN_MAP_CELL, x * PACMAN_MAP_CELL ), ((y + 1) * PACMAN_MAP_CELL, (x + 1) * PACMAN_MAP_CELL ), (255, 0, 0), 1)
        cv.imshow('Wall matches', g2rgb)
        print('Keeping pacman in thu current maze by sealing the exists')
        self.board[16][0] = PACMAN_BOARD_WALL      # 4 board exits
        self.board[16][PACMAN_BOARD_WIDTH-1] = PACMAN_BOARD_WALL
        self.board[0][16] = PACMAN_BOARD_WALL
        self.board[PACMAN_BOARD_WIDTH-1][16] = PACMAN_BOARD_WALL
        print('Closing ghost cage')
        self.board[15][16] = PACMAN_BOARD_WALL

    def get_mapscreenshot(self, region):
        self.mapscreenshot = mss.mss().grab(region)
        self.mapscreenshot = np.array(self.mapscreenshot)
        self.mapscreenshot = cv.cvtColor(self.mapscreenshot, cv.COLOR_RGB2BGR)
#        cv.imshow('MapScreen', self.mapscreenshot)
#        hwnd2 = win32gui.FindWindow(None, 'MapScreen')
#        win32gui.MoveWindow(hwnd2, 200, 1000, PACMAN_MAP_WIDTH+150, PACMAN_MAP_HEIGHT+150, True)

    def get_player1_score(self):
        region = {'top': PACMAN_PLAYERSCORE_Y, 'left': PACMAN_PLAYERSCORE_X, 'width': PACMAN_PLAYERSCORE_WIDTH, 'height': PACMAN_PLAYERSCORE_HEIGHT}
        screenshot = mss.mss().grab(region)
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        cv.imshow('OCR', screenshot)
        hwnd2 = win32gui.FindWindow(None, 'OCR')
        win32gui.MoveWindow(hwnd2, 200, 1000, 160, 464, True)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(screenshot)
        self.score = text[:text.find('\n')]
        print('Score updated: ', text[:text.find('\n')])

    def set_board_perimeter(self):
        for x in range(PACMAN_BOARD_WIDTH):         # top and bottom walls
            self.board[x][0] = PACMAN_BOARD_WALL
            self.board[x][PACMAN_BOARD_WIDTH-1] = PACMAN_BOARD_WALL   
        for y in range(PACMAN_BOARD_WIDTH):         # left and right walls
            self.board[0][y] = PACMAN_BOARD_WALL
            self.board[PACMAN_BOARD_WIDTH-1][y] = PACMAN_BOARD_WALL
        print('Keeping pacman in thu current maze by sealing the exists')
        #self.board[16][0] = PACMAN_BOARD_BLANK      # 4 board exits
        #self.board[16][PACMAN_BOARD_WIDTH-1] = PACMAN_BOARD_BLANK
        #self.board[0][16] = PACMAN_BOARD_BLANK
        #self.board[PACMAN_BOARD_WIDTH-1][16] = PACMAN_BOARD_BLANK

    def set_board_ghostcage(self):
        for y in range(PACMAN_BOARD_CAGE_WIDTH):
            self.board[15][14+y] = PACMAN_BOARD_WALL
            self.board[17][14+y] = PACMAN_BOARD_WALL
        self.board[16][14] = PACMAN_BOARD_WALL
        self.board[16][18] = PACMAN_BOARD_WALL        

    def print_board(self):
        row = "    "
        for x in range(PACMAN_BOARD_WIDTH):
            row += str(x % 10)
        print(row)
        for x in range(PACMAN_BOARD_WIDTH):
            row = "{:2n}".format(x) + ': '
            for y in range(PACMAN_BOARD_WIDTH):
                row += self.board[x][y]
            print(row)

    def print_board_row(self, rnum):
        row = ''
        for y in range(PACMAN_BOARD_WIDTH):
            row += self.board[rnum][y]
        print(row)

    def set_board(self):
        pshot = self.mapscreenshot.copy()
        vision_smallpill = Vision('smalldot.png')
        points = vision_smallpill.find(pshot, 0.60, 'rectangles')
        for point in points:
            y = int(np.floor((point[0] + PACMAN_MAP_CELL_ERR) / PACMAN_MAP_CELL))
            x = int(np.floor((point[1] + PACMAN_MAP_CELL_ERR) / PACMAN_MAP_CELL))
#            print('point: ', point, '[', x, ',', y,']')
            self.board[x][y] = PACMAN_BOARD_SPILL
        vision_bigpill = Vision('bigdot2.png') # bigdots needs to be detected after small dots because, the detection will find a small dot in a big dot
        points = vision_bigpill.find(pshot, 0.60, 'rectangles')
        for point in points:
            y = int(np.floor((point[0] + PACMAN_MAP_CELL_ERR) / PACMAN_MAP_CELL))
            x = int(np.floor((point[1] + PACMAN_MAP_CELL_ERR) / PACMAN_MAP_CELL))
            self.board[x][y] = PACMAN_BOARD_BPILL
#            print('point: ', point, '[', x, ',', y,']')
            self.print_board()
#        print(points)
        self.board[self.pacman[0]][self.pacman[1]] = PACMAN_BOARD_PMAN


