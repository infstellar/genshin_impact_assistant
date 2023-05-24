from source.util import *
from source.interaction.interaction_template import InteractionTemplate
from common import vkcode, static_lib
import win32api, win32con, pyautogui, pydirectinput

class InteractionNormal(InteractionTemplate):
    isBorderlessWindow = GIAconfig.General_BorderlessWindow
    def __init__(self):
        self.DEBUG_MODE = False
        self.CONSOLE_ONLY = False
    
    def _fix_xy(self,x,y):
        wx, wy, w, h = win32gui.GetWindowRect(static_lib.HANDLE)
        x += wx
        if self.isBorderlessWindow:
            y += wy
        else:
            y = y + wy + 26
        return x,y
      
    def left_click(self):
        if not self.CONSOLE_ONLY:
            pyautogui.leftClick()
    
    def left_down(self):
        if not self.CONSOLE_ONLY:
            pyautogui.mouseDown(button='left')
    
    def left_up(self):
        if not self.CONSOLE_ONLY:
            pyautogui.mouseUp(button='left')
    
    def left_double_click(self, dt):
        if not self.CONSOLE_ONLY:
            pyautogui.doubleClick()
    
    def right_click(self):
        if not self.CONSOLE_ONLY:
            pyautogui.rightClick()
    
    def middle_click(self):
        pyautogui.click(button='middle')
    
    def key_down(self, key):
        if key == 'w':
            static_lib.W_KEYDOWN = True

        if not self.CONSOLE_ONLY:
            pyautogui.keyDown(key)
    
    def key_up(self, key):
        if key == 'w':
            static_lib.W_KEYDOWN = False

        if not self.CONSOLE_ONLY:
            pyautogui.keyUp(key)
    
    def key_press(self, key):
        if not self.CONSOLE_ONLY:
            pyautogui.press(key)
    
    def move_to(self, x: int, y: int, relative=False, isBorderlessWindow=False):
        x = int(x)
        y = int(y)

        if relative:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)
        else:
            wx, wy, w, h = win32gui.GetWindowRect(static_lib.HANDLE)
            x += wx
            if isBorderlessWindow:
                y += wy
            else:
                y = y + wy + 26
            pydirectinput.moveTo(x,y) 
            # win32api.SetCursorPos((x, y))
            
if __name__ == '__main__':
    ittN = InteractionNormal()
    ittN.move_to(100,100)
    # while 1:
    #     time.sleep(0.5)
    #     ittN.left_click()
    