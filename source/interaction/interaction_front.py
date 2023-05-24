from source.util import *
from source.interaction.interaction_template import InteractionTemplate
from common import vkcode, static_lib
import win32api, win32con, pyautogui

class InteractionNormal(InteractionTemplate):
    
    def __init__(self):
        self.WM_MOUSEMOVE = 0x0200
        self.WM_LBUTTONDOWN = 0x0201
        self.WM_LBUTTONUP = 0x202
        self.WM_MOUSEWHEEL = 0x020A
        self.WM_RBUTTONDOWN = 0x0204
        self.WM_RBUTTONDBLCLK = 0x0206
        self.WM_RBUTTONUP = 0x0205
        self.WM_KEYDOWN = 0x100
        self.WM_KEYUP = 0x101
        self.GetDC = ctypes.windll.user32.GetDC
        self.CreateCompatibleDC = ctypes.windll.gdi32.CreateCompatibleDC
        self.GetClientRect = ctypes.windll.user32.GetClientRect
        self.CreateCompatibleBitmap = ctypes.windll.gdi32.CreateCompatibleBitmap
        self.SelectObject = ctypes.windll.gdi32.SelectObject
        self.BitBlt = ctypes.windll.gdi32.BitBlt
        self.SRCCOPY = 0x00CC0020
        self.GetBitmapBits = ctypes.windll.gdi32.GetBitmapBits
        self.DeleteObject = ctypes.windll.gdi32.DeleteObject
        self.ReleaseDC = ctypes.windll.user32.ReleaseDC
        self.VK_CODE = vkcode.VK_CODE
        self.PostMessageW = ctypes.windll.user32.PostMessageW
        self.MapVirtualKeyW = ctypes.windll.user32.MapVirtualKeyW
        self.VkKeyScanA = ctypes.windll.user32.VkKeyScanA
        self.WHEEL_DELTA = 120
        self.DEFAULT_DELAY_TIME = 0.05
        self.DEBUG_MODE = False
        self.CONSOLE_ONLY = False
        
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
                
            win32api.SetCursorPos((x, y))
            
if __name__ == '__main__':
    ittN = InteractionNormal()
    while 1:
        time.sleep(0.5)
        ittN.left_click()
    