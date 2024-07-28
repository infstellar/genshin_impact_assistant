import time

from source.util import *
from source.interaction.interaction_template import InteractionTemplate
from source.common import vkcode, static_lib
import win32api, win32con
import pyautogui
from source.common.base_threading import ProcessThreading

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
            wparam = 0
            lparam = 0 << 16 | 0
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_LBUTTONDOWN, wparam, lparam)
            time.sleep(0.06)
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_LBUTTONUP, wparam, lparam)
    
    def left_down(self):
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = 0 << 16 | 0
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_LBUTTONDOWN, wparam, lparam)
            time.sleep(0.01)
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_LBUTTONDOWN, wparam, lparam)
            time.sleep(0.01)
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_LBUTTONDOWN, wparam, lparam)
    
    def left_up(self):
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = 0 << 16 | 0
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_LBUTTONUP, wparam, lparam)
            time.sleep(0.01)
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_LBUTTONUP, wparam, lparam)
            time.sleep(0.01)
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_LBUTTONUP, wparam, lparam)
    
    def left_double_click(self, dt):
        if not self.CONSOLE_ONLY:
            self.left_click()
            time.sleep(dt)
            self.left_click()
    
    def right_click(self):
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = 0 << 16 | 0
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_RBUTTONDOWN, wparam, lparam)
            time.sleep(0.06)
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_RBUTTONUP, wparam, lparam)
    
    def middle_click(self):
        pyautogui.click(button='middle')
    
    def key_down(self, key):
        if key == 'w':
            static_lib.W_KEYDOWN = True

        if not self.CONSOLE_ONLY:
            vk_code = self.get_virtual_keycode(key)
            scan_code = self.MapVirtualKeyW(vk_code, 0)
            wparam = vk_code
            lparam = (scan_code << 16) | 1
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_KEYDOWN, wparam, lparam)
    
    def key_up(self, key):
        if key == 'w':
            static_lib.W_KEYDOWN = False

        if not self.CONSOLE_ONLY:
            vk_code = self.get_virtual_keycode(key)
            scan_code = self.MapVirtualKeyW(vk_code, 0)
            # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
            wparam = vk_code
            lparam = (scan_code << 16) | 0XC0000001
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_KEYUP, wparam, lparam)
    
    def key_press(self, key):
        if not self.CONSOLE_ONLY:
            vk_code = self.get_virtual_keycode(key)
            scan_code = self.MapVirtualKeyW(vk_code, 0)
            wparam = vk_code
            lparam = (scan_code << 16) | 1
            lparam2 = (scan_code << 16) | 0XC0000001
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_KEYDOWN, wparam, lparam)
            time.sleep(0.05)
            self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_KEYUP, wparam, lparam2)
    
    def move_to(self, x: int, y: int, relative=False, isBorderlessWindow=False):
        x = int(x)
        y = int(y)

        if relative:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)
        else:

            wx, wy, w, h = win32gui.GetWindowRect(static_lib.HANDLEOBJ.get_handle())
            x += wx
            if isBorderlessWindow:
                y += wy
            else:
                y = y + wy + 26
                
            win32api.SetCursorPos((x, y))

# ittN = InteractionNormal()

KEY_DOWN = 'KeyDown'
KEY_UP = 'KeyUp'

class Operation():

    def __str__(self):
        return f'Operation: {self.key} {self.type}'
    def __init__(self, key:str, type, operation_start=time.time(), operation_end = time.time()):
        self.key = key
        self.type = type
        self.operation_start = operation_start
        self.operation_end = operation_end
        self.operated = False



class InteractionController(ProcessThreading):
    def __init__(self):
        super().__init__()
        self.operation_list:t.List[Operation] = []

    def key_down(self, key):
        self.operation_list.append(Operation(key, KEY_DOWN))

    def exec_operation(self, op:Operation):
        if op.type == KEY_DOWN:
            print(f'key down: {op.key}')
            ittN.key_down(op.key)
        elif op.type == KEY_UP:
            print(f'key up: {op.key}')
            ittN.key_up(op.key)

    def loop(self):
        for i in self.operation_list:
            print('looping')
            if time.time() > i.operation_start:
                if not i.operated:
                    self.exec_operation(i)
                    return
                else:
                    if time.time() > i.operation_end:
                        logger.trace(f'pop op: {i}')
                        self.operation_list.pop(self.operation_list.index(i))
                        return



if __name__ == '__main__':
    itc = InteractionController()
    itc.start()
    itc.continue_threading()
    while 1:
        time.sleep(0.5)
        itc.key_down('w')
        # itc.left_click()
    