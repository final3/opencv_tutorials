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
# clear console screencls
print(chr(27) + "[2J")

pmbot = pacman.PacManBot(pacman.PACMAN_WINDOW_NAME)
loop_time = 1
frame_count = 0

wu.WinUtil.list_window_names()

coord = wu.WinUtil.get_window_coord(pacman.PACMAN_WINDOW_NAME)
if (sum(coord)):
    wu.WinUtil.moveresize_window(pacman.PACMAN_WINDOW_NAME, [0, 0], [pacman.PACMAN_WINDOW_MINWIDTH, pacman.PACMAN_WINDOW_MINHEIGHT])
else:
    print('Window NOT found - Done.')
    sys.exit()

while (True):
    coord = wu.WinUtil.get_window_coord(pacman.PACMAN_WINDOW_NAME)
    if (sum(coord)):
        pmbot.get_player1_score()        
        wu.WinUtil.moveresize_window(pacman.PACMAN_WINDOW_NAME, [0, 0], [pacman.PACMAN_WINDOW_MINWIDTH, pacman.PACMAN_WINDOW_MINHEIGHT])
        print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()
        frame_count += 1
    else:
        break
    if cv.waitKey(50) == ord('q'):
        cv.destroyAllWindows()
        break



print('Done.')