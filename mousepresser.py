import win32api
import win32con
import time
import math

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    
    
def drag(x,y,x2,y2):

    sleep = 0.025
    delta = 140

    win32api.SetCursorPos((x,y))    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(sleep)
    
    c_x = x
    c_y = y
    d_x = math.copysign(1, x2-x)
    d_y = math.copysign(1, y2-y)

    while c_x != x2 or c_y != y2:
        c_x += int(d_x * delta)
        c_y += int(d_y * delta)
        
        if d_x == 1 and c_x > x2 or d_x == -1 and c_x < x2:
            c_x = x2
        if d_y == 1 and c_y > y2 or d_y == -1 and c_y < y2:
            c_y = y2
            
        win32api.SetCursorPos((c_x, c_y))
        time.sleep(sleep)
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x2,y2,0,0)