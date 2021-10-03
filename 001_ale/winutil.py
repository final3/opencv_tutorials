import win32gui

# TO-DO LIST: set_foreground_window https://www.programcreek.com/python/example/81370/win32gui.GetForegroundWindow

class WinUtil:

    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                wname = win32gui.GetWindowText(hwnd)    
                print (hex(hwnd), '*' + wname + '*[', len(wname), ']')

        win32gui.EnumWindows( winEnumHandler, None )

    def get_window_coord(wname):
        hwnd = None
        hwnd = win32gui.FindWindow(None, wname)
        coord = [-1, -1, -1, -1]
        if hwnd:
            coord = win32gui.GetWindowRect(hwnd)
            print('Window: *', wname, '* found - ', coord)
        else:
            print('Window: *', wname, '* NOT found - ', coord)            
        return(coord)

    def get_window_size(wname):
        size = [-1, -1]
        coord = WinUtil.get_window_coord(wname)
        if (sum(coord)):
            print('Window: *', wname, '* found - ', coord)
            size[0] = coord[2] - coord [0]
            size[1] = coord[3] - coord[1]
        return(size)           
    
    def moveresize_window(wname, neworigin, newsize):
        hwnd = win32gui.FindWindow(None, wname) 
        if (hwnd):            
            coord = [neworigin[0], neworigin[1], neworigin[0]+newsize[0], neworigin[1]+newsize[1]]
            print('Window: *', wname, '* movedresized - ', coord)
            win32gui.MoveWindow(hwnd, neworigin[0], neworigin[1], neworigin[0]+newsize[0], neworigin[1]+newsize[1], True)
        else:
            print('Window: *', wname, '* NOT found - ')  
        return(hwnd)
           