import string
import sys

import pyautogui
import win32gui
from util import *
from vkcode import VK_CODE

print('import: cv2')
import cv2

# print('import: paddleocr')
# from paddleocr import PaddleOCR
# from paddleocr import draw_ocr
print('import: numpy')
import numpy as np

print('import: PIL')
from PIL import ImageGrab, Image

# print('import: win32api,win32con,win32gui,random')

print('import: PyQt5.QtWidgets')
from PyQt5.QtWidgets import QApplication

print('import: matplotlib.pyplot')
PostMessageW = ctypes.windll.user32.PostMessageW
MapVirtualKeyW = ctypes.windll.user32.MapVirtualKeyW
VkKeyScanA = ctypes.windll.user32.VkKeyScanA
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x202
WM_MOUSEWHEEL = 0x020A
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONDBLCLK = 0x0206
WM_RBUTTONUP = 0x0205
WM_KEYDOWN = 0x100
WM_KEYUP = 0x101
WHEEL_DELTA = 120
DEFAULT_DELAY_TIME = 0.05
DEBUG_MODE = False
CONSOLE_ONLY = False
DEFAULT_HANDLE = ctypes.windll.user32.FindWindowW(None, "原神")


def get_virtual_keycode(key: str):
    """根据按键名获取虚拟按键码

    Args:
        key (str): 按键名

    Returns:
        int: 虚拟按键码
    """
    if len(key) == 1 and key in string.printable:
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
        return VkKeyScanA(ord(key)) & 0xff
    else:
        return VK_CODE[key]


class WinInfo:
    def __init__(self, x, y, w, h, mainHnd):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mainHnd = mainHnd
        self.winpos = [x, y]

    def get_rect(self, rangePosition=None):
        if rangePosition is None:
            rangePosition = [0, 0, 0, 0]
        return [self.x, self.y, self.w + self.x, self.h + self.y]


def win_move_to(posi, win_pos, max_float=3, duration_base=0.2, xadd=0, yadd=0, message=''):
    if posi == -1:
        print('\n\n\n\n\n ERROR: winMoveToError, please check up the program. \n\n\n\n\n')
        if True:
            raise RuntimeError('winMoveToError: posi should not be -1')
    x = posi[0]
    y = posi[1]
    k = 1000  # 放大倍率,越大随机数越准
    mouse_position = pyautogui.position()
    rel_x = x + xadd + win_pos[0] + random.randint(0, max_float)
    rel_y = y + yadd + win_pos[1] + random.randint(0, max_float)

    if duration_base == 0.2:
        distance = math.sqrt(((mouse_position[0] - rel_x) ** 2 + (mouse_position[1] - rel_y) ** 2))
        delaytime = distance / random.randint(35, 50)
        duration_base = delaytime / 100

    duration = (duration_base + (random.randint(int(-duration_base * k), int(k * duration_base))) / k)
    print('winMoveTo: ', message, posi)
    pyautogui.moveTo(rel_x, rel_y, duration=duration, tween=pytweening.easeInOutQuad)
    delay(0.1)


def get_screen_img():
    img = ImageGrab.grab()
    imsrc = np.array(img)
    return imsrc


def get_windows_info(classname, title):
    mainHnd = win32gui.FindWindow(classname, title)
    rect = win32gui.GetWindowRect(mainHnd)
    x, y = rect[0], rect[1]
    w, h = rect[2] - x, rect[3] - y
    y += 31
    x += 8
    return WinInfo(x, y, w, h, mainHnd)


def get_scr_windows_img(wininfo: WinInfo, range_position=None):
    if range_position is None:
        range_position = [0, 0, 0, 0]
    hwnd = wininfo.mainHnd
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    size = img.size()
    s = img.bits().asstring(size.width() * size.height() * img.depth() // 8)  # format 0xffRRGGBB
    arr = np.fromstring(s, dtype=np.uint8).reshape((size.height(), size.width(), img.depth() // 8))
    new_image = Image.fromarray(arr)
    bbox = wininfo.get_rect()
    bbox[2] = bbox[0] + range_position[2]
    bbox[3] = bbox[1] + range_position[3]
    bbox[0] += range_position[0]
    bbox[1] += range_position[1]

    imsrc = np.array(new_image)
    imsrc = imsrc[range_position[1]:range_position[3], range_position[0]:range_position[2], :3]
    # plt.imshow(imsrc)
    # plt.show()
    # plt.savefig('img.jpg')#
    imsrc = cv2.cvtColor(imsrc, cv2.COLOR_RGB2BGR)
    return imsrc, [bbox[0], bbox[1]]  # BGR


def leftClick(handle=DEFAULT_HANDLE, x: int = 961, y: int = 529):
    if not CONSOLE_ONLY:
        wparam = 0
        lparam = y << 16 | x
        PostMessageW(handle, WM_LBUTTONDOWN, wparam, lparam)
        PostMessageW(handle, WM_LBUTTONUP, wparam, lparam)
    print('left click')


def leftDoubleClick(dt=0.05):
    if not CONSOLE_ONLY:
        leftClick()
        leftClick()
    print('leftDoubleClick')


def rightClick(handle=DEFAULT_HANDLE, x: int = 961, y: int = 529):
    if not CONSOLE_ONLY:
        wparam = 0
        lparam = y << 16 | x
        PostMessageW(handle, WM_RBUTTONDOWN, wparam, lparam)
        PostMessageW(handle, WM_RBUTTONUP, wparam, lparam)
        # pyautogui.rightClick()
    print('rightClick')
    delay(0.05)


def leftDrag(target, win_pos, max_float=3, duration_base=0.2, xadd=0, yadd=0):
    if not CONSOLE_ONLY:
        pyautogui.mouseDown()
        delay(0.2)
        win_move_to(target, win_pos, max_float, duration_base, xadd, yadd)
        delay(0.4)
        pyautogui.mouseUp()
        delay(0.1)
    print("leftDrag")


def keyDown(key, handle=DEFAULT_HANDLE):
    if not CONSOLE_ONLY:
        vk_code = get_virtual_keycode(key)
        scan_code = MapVirtualKeyW(vk_code, 0)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
        wparam = vk_code
        lparam = (scan_code << 16) | 1
        PostMessageW(handle, WM_KEYDOWN, wparam, lparam)
    print("keyDown", key)


def keyUp(key, handle=DEFAULT_HANDLE):
    if not CONSOLE_ONLY:
        vk_code = get_virtual_keycode(key)
        scan_code = MapVirtualKeyW(vk_code, 0)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
        wparam = vk_code
        lparam = (scan_code << 16) | 0XC0000001
        PostMessageW(handle, WM_KEYUP, wparam, lparam)
    print("keyUp", key)


def keyPress(key):
    if not CONSOLE_ONLY:
        # win32api.keybd_event(key)
        keyDown(key)
        time.sleep(0.01)
        keyUp(key)
        delay(DEFAULT_DELAY_TIME)
    print("keyPress", key)


def getMousePosi(hwnd: WinInfo):
    p = pyautogui.position()
    return [p[0] - hwnd.x, p[1] - hwnd.y]


def delay(x, randtime=True, isprint=True):
    a = random.randint(-10, 10)
    if randtime:
        a = a * x * 0.02
        if x > 0.2 and isprint:
            print('delay: ', x, 'rand: ', x + a)
        time.sleep(x + a)
    else:
        if x > 0.2 and isprint:
            print('delay: ', x)
        time.sleep(x)


if __name__ == '__main__':
    pyautogui.keyDown('2')
    time.sleep(2)

    # w2
