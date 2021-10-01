import win32gui, win32ui, win32con, win32api
import pyautogui
import mss
import sys
import time

class Hci:

    target_hwnd = None
    window_name = None

## constructor binding hci to a specific wname window
    def __init__ (self, wname):
        hwnd = None
        hwnd = win32gui.FindWindow(None, wname)
        if hwnd:
            self.target_window = hwnd
            self.window_name = wname 
            print('Virtual HCI for window: \'', self.window_name, '\' created - ', hex(self.target_window)) 
        else:
            sys.exit('ERROR Window: \'', self.window_name, '\' NOT found')
            

## simulate press & release of key on the keyboard for self.window_name
## win32con.VK_LEFT = 37, win32con.VK_UP = 38, win32con.VK_RIGHT = 39, win32con.VK_DOWN = 40
    def input_keyboard (self, key, modifier):
        if (self.target_hwnd): 
            VirtualKey = win32api.MapVirtualKey(key, 0)
            win32gui.PostMessage(self.target_hwnd, win32con.WM_KEYDOWN, key, 0x0001|VirtualKey<<16)
            time.sleep(0.05)
            win32gui.PostMessage(self.target_hwnd, win32con.WM_KEYUP, key, 0x0001|VirtualKey<<16|0xC0<<24); 
        else:
            sys.exit('Hci class not initialized: target_hwnd == None')




##    hwnd = win32gui.FindWindow(None, "World's Biggest PAC-MAN - Google Chrome")
##    direction = win32con.VK_LEFT    #VK_LEFT = 37, VK_UP = 38, VK_RIGHT = 39, VK_DOWN = 40
##    direction += random.randint(0, 3)
##    VirtualKey = win32api.MapVirtualKey(direction, 0)
##    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, direction, 0x0001|VirtualKey<<16)
##    time.sleep(0.05)
##    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, direction, 0x0001|VirtualKey<<16|0xC0<<24); 