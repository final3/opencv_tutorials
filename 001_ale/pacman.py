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

# WARNING ALL THE ABS COORDINATES ARE AT 67% ZOOM  

##### Definitions
# Screen = pixel map including perimeter captured via screenshot
# Map    = pixel map exluding perimeter captured via screenshot
# Board  = char representation of the map including perimenter used for navidation

PACMAN_WINDOW_NAME = 'World\'s Biggest PAC-MAN - Google Chrome'

# browser window
PACMAN_WINDOW_MINWIDTH = 928    # minimum browser window size
PACMAN_WINDOW_MINHEIGHT = 902

# pixel representation of the board
PACMAN_SCREEN_X = 298           # pacman map rectangle including perimeter  
PACMAN_SCREEN_Y = 266       
PACMAN_SCREEN_WIDTH  = 584  
PACMAN_SCREEN_HEIGHT = 584     
PACMAN_SCREEN_PERIMETER_THICKNESS = 13 
PACMAN_MAP_X = PACMAN_SCREEN_X + PACMAN_SCREEN_PERIMETER_THICKNESS            # pacman map rectangle perimeter excluded PACMAN_SCREEN_ +/- THICKNESS
PACMAN_MAP_Y = PACMAN_SCREEN_Y + PACMAN_SCREEN_PERIMETER_THICKNESS
PACMAN_MAP_WIDTH  = (PACMAN_SCREEN_WIDTH - 2 * PACMAN_SCREEN_PERIMETER_THICKNESS)   
PACMAN_MAP_HEIGHT = (PACMAN_SCREEN_HEIGHT - 2 * PACMAN_SCREEN_PERIMETER_THICKNESS) 

# pixel representation of map pbject cell
PACMAN_MAP_CELL     = 18        # cell square avg size
PACMAN_MAP_CELL_ERR = 2         # cell square tollerance


PACMAN_PLAYERSCORE_X = 350      # player1 score rectangle
PACMAN_PLAYERSCORE_Y = 226
PACMAN_PLAYERSCORE_WIDTH  = 150
PACMAN_PLAYERSCORE_HEIGHT = 28

# 2D matrix representation of the board
PACMAN_MAXPILL = 30     # max pill number per row or col
PACMAN_BOARD_WIDTH = 32 # 30 pills + 2 walls
PACMAN_BOARD_NM = '-'   # NaM marker
PACMAN_BOARD_WALL = 'w' # wall marker
PACMAN_BOARD_SPILL = '.'# small pill marker
PACMAN_BOARD_BPILL = '*'# big pill marker (power-up)
PACMAN_BOARD_GHOST = 'G'# bad ghost marker
PACMAN_BOARD_PRAY = 'g' # good ghost marker
PACMAN_BOARD_PMAN = '@' # pacman marker
PACMAN_BOARD_BLANK = ' '# empty cell marker

class PacManBot:

    score = -1          # player1 latest score
    windowname = ''     # window name 
    hwnd = None         # game window handle
    board = [[PACMAN_BOARD_NM for j in range(PACMAN_BOARD_WIDTH)] for i in range(PACMAN_BOARD_WIDTH)]     # board map
    mapscreenshot = None# latest screenshot

    def __init__(self, wname):
        self.score = 0
        self.windowname = wname

    def get_mapscreenshot(self):
        region = {'top': PACMAN_MAP_Y, 'left': PACMAN_MAP_X, 'width': PACMAN_MAP_WIDTH, 'height': PACMAN_MAP_HEIGHT}
        self.mapscreenshot = mss.mss().grab(region)
        self.mapscreenshot = np.array(self.mapscreenshot)
        self.mapscreenshot = cv.cvtColor(self.mapscreenshot, cv.COLOR_RGB2BGR)
        cv.imshow('MapScreen', self.mapscreenshot)
        hwnd2 = win32gui.FindWindow(None, 'MapScreen')
        win32gui.MoveWindow(hwnd2, 200, 1000, PACMAN_MAP_WIDTH+150, PACMAN_MAP_HEIGHT+150, True)


#######        

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
        self.board[17][0] = PACMAN_BOARD_BLANK      # 4 board exits
        self.board[17][PACMAN_BOARD_WIDTH-1] = PACMAN_BOARD_BLANK
        self.board[0][17] = PACMAN_BOARD_BLANK
        self.board[PACMAN_BOARD_WIDTH-1][17] = PACMAN_BOARD_BLANK

    def print_board(self):
        for x in range(PACMAN_BOARD_WIDTH):
            row = ''
            for y in range(PACMAN_BOARD_WIDTH):
                row += self.board[x][y]
            print(row)

    def print_board_row(self, rnum):
        row = ''
        for y in range(PACMAN_BOARD_WIDTH):
            row += self.board[rnum][y]
        print(row)

    def update_board(self):
        vision_smalldot = Vision('smalldot.png')
        points = vision_smalldot.find(self.mapscreenshot, 0.60, 'rectangles')
#        for point in points:
        for point in points[:32]:
            y = int(np.floor((point[0] + PACMAN_MAP_CELL_ERR) / PACMAN_MAP_CELL) + 1)
            x = int(np.floor((point[1] + PACMAN_MAP_CELL_ERR) / PACMAN_MAP_CELL) + 1)
            self.board[x][y] = PACMAN_BOARD_SPILL
            print('point: ', point, '[', y, ',', x,']')
            self.print_board_row(x)
#        print(points)
