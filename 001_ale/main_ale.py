import pacman
import hci
import winutil as wu
import cv2 as cv
import time
import os
import sys

import win32gui, win32ui, win32con, win32api
import pyautogui
import mss
import mss.tools
import random


########################
# __main__
########################

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(chr(27) + "[2J") # clear console screencls
print('====================================================================================')
print('===========================     Initializing     ===================================')

loop_time = 1
frame_count = 0
pmbot = pacman.PacManBot(pacman.PACMAN_WINDOW_NAME)

wu.WinUtil.list_window_names()

coord = wu.WinUtil.get_window_coord(pacman.PACMAN_WINDOW_NAME)
if (sum(coord)):
    pmbot.hwnd = wu.WinUtil.moveresize_window(pacman.PACMAN_WINDOW_NAME, [0, 0], [pacman.PACMAN_WINDOW_MINWIDTH, pacman.PACMAN_WINDOW_MINHEIGHT])
else:
    print('Window NOT found - Done.')
    sys.exit()
cv.waitKey(1000)            # required to give time to complete WinUtil.moveresize 

region = {'top': pacman.PACMAN_MAP_Y, 'left': pacman.PACMAN_MAP_X, 'width': pacman.PACMAN_MAP_WIDTH, 'height': pacman.PACMAN_MAP_HEIGHT}
pmbot.get_mapscreenshot(region)
pmbot.get_walls()
pmbot.set_board()

loop_time = time.time()
frame_count = 0

print('pmbot: ', pmbot.hwnd)

print('===========================       Playing!       ===================================')

while(True):
    pmbot.print_board()
    pmbot.get_movingcharacters()
    pmbot.move()
    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()
    frame_count += 1
    if cv.waitKey(10) == ord('q'):
        cv.destroyAllWindows()
        break
    pmbot.get_mapscreenshot(region)


pmbot.print_board()
print('CV coordinates are still not accurate enought')
print('Done.')