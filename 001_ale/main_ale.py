import pacman
import hci
import winutil as wu

import cv2 as cv

import time
import os
import sys

########################
# __main__
########################

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(chr(27) + "[2J") # clear console screencls

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

pmbot.get_mapscreenshot()
cv.waitKey(10000)
pmbot.set_board_perimeter()
pmbot.print_board()
sys.exit()

while (True):
    pmbot.get_player1_score()
    if cv.waitKey(5) == ord('q'):
        cv.destroyAllWindows()
        break



print('Done.')