import win32gui

# TO-DO LIST: set_foreground_window https://www.programcreek.com/python/example/81370/win32gui.GetForegroundWindow

class WinUtil:

    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                wname = win32gui.GetWindowText(hwnd)    
                print (hex(hwnd), '*' + wname + '*[', len(wname), ']')

        win32gui.EnumWindows( winEnumHandler, None )

    def find_window_coord(wname):
        hwnd = None
        hwnd = win32gui.FindWindow(None, wname)
        if hwnd:
            print('Window: *', wname, '* found - ', hex(hwnd))
            coord = win32gui.GetWindowRect(hwnd)
            print(coord)
        else:
            print('Window: *', wname, '* NOT found - ')
            return((-1, -1, -1, -1))