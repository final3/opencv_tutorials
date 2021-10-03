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

PACMAN_BOARD_W = 32
PACMAN_BOARD_H = 32

# WARNING ALL THE ABS COORDINATES ARE AT 67% ZOOM  

# printscreen offset with IE 

PACMAN_SCREEN_X = 286
PACMAN_SCREEN_Y = 262
PACMAN_SCREEN_W = 617
PACMAN_SCREEN_H = 658

PACMAN_SQUARE = 511

PACMAN_WINDOW_NAME = 'World\'s Biggest PAC-MAN - Google Chrome'
PACMAN_WINDOW_MINWIDTH = 928
PACMAN_WINDOW_MINHEIGHT = 902

# This is how the screenshot is taken when the Chrome window starts at 0,0 @ 67% zoom
# screenshot = pyautogui.screenshot(None, [286, 262, 617, 658])

#### OCR Player1 score
# 1UP score absolute coordinates (x: 282, y: 107, w: 160, h: 64)
#    region2 = {'top': 195, 'left': 269, 'width': 160, 'height': 64}
#    region2 = {'top': 227, 'left': 349, 'width': 160, 'height': 27}
#    screenshot2 = mss.mss().grab(region2)
#    screenshot2 = np.array(screenshot2)
#    screenshot2 = cv.cvtColor(screenshot2, cv.COLOR_RGB2BGR)
#    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
#    text = pytesseract.image_to_string(screenshot2)
#    print(text[:text.find('\n')])
#    cv.imshow('OCR', screenshot2)
#    hwnd2 = win32gui.FindWindow(None, 'OCR')
#    win32gui.MoveWindow(hwnd2, 3200, 10, 160, 464, True)

class PacManBot:

    score = -1
    windowname = ''

    def __init__(self, wname):
        self.score = 0
        self.windowname = wname

    def get_player1_score(self):
        region = {'top': 226, 'left': 350, 'width': 150, 'height': 28}
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
