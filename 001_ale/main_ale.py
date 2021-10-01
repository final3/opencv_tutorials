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

wu.WinUtil.list_window_names()

loop_time = 1
frame_count = 0

while (True):
    wu.WinUtil.find_window_coord(pacman.PACMAN_WINDOW_NAME)
    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()
    frame_count += 1
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


print('Done.')