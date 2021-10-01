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

import pacman

from vision import Vision
from windowcapture import WindowCapture

# Stanford PACMAN paper http://cs229.stanford.edu/proj2017/final-reports/5241109.pdf
# YOUTUBE video https://youtu.be/WymCpVUPWQ4?t=1135

# SEND KEY TO INACTIVE WINDOW https://stackoverflow.com/questions/12996985/send-some-keys-to-inactive-window-with-python

def list_window_names():
    def winEnumHandler(hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            print (hex(hwnd), win32gui.GetWindowText( hwnd ))

    win32gui.EnumWindows( winEnumHandler, None )




########################
# __main__
########################

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# list_window_names()
# wincap = WindowCapture('''World\'s Biggest PAC-MAN - Internet Explorer''',511, 511, 255, 176, 766, 693)
# wincap = WindowCapture('''World\'s Biggest PAC-MAN - Internet Explorer''')

loop_time = time.time()
frame_count = 0


while(True):
#    screenshot = wincap.get_screenshot(frame_count)

#### screenshot via pyatuoguy
#    screenshot = pyautogui.screenshot(None, [286, 262, 617, 658])
#    screenshot = np.array(screenshot)
#    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    region = {'top': 264, 'left': 292, 'width': 617, 'height': 658}
    screenshot = mss.mss().grab(region)
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)


#### CV recognition and localization
# draw rectangle example
#    cv.rectangle( screenshot, (19, 19), (38, 38), (0, 0, 255))

# find all the dots
#    vision_smalldot = Vision('badghost.png')
#    vision_smalldot = Vision('fit.jpg')
#    vision_smalldot = Vision('smalldot.png')
    vision_smalldot = Vision('wall3.png')
    points = vision_smalldot.find(screenshot, 0.75, 'rectangles')

#    points = vision_smalldot.find(screenshot, 0.35, 'rectangles')
#    for bbox in points:
#        cv.rectangle(screenshot, bbox, (bbox[0]+19, bbox[1]+19), (0, 0, 255))
    print(len(points))
    

#move & dispaly screenshot
    cv.imshow('Computer Vision', screenshot)
    hwnd = win32gui.FindWindow(None, 'Computer Vision')
    win32gui.MoveWindow(hwnd, 3200, 1000, 617, 658, True)

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



####### keystrokes
    hwnd = win32gui.FindWindow(None, "World's Biggest PAC-MAN - Google Chrome")
    direction = win32con.VK_LEFT    #VK_LEFT = 37, VK_UP = 38, VK_RIGHT = 39, VK_DOWN = 40
    direction += random.randint(0, 3)
    VirtualKey = win32api.MapVirtualKey(direction, 0)
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, direction, 0x0001|VirtualKey<<16)
    time.sleep(0.05)
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, direction, 0x0001|VirtualKey<<16|0xC0<<24);  
#######


    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()
    frame_count += 1
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


print('Done.')