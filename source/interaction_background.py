import inspect
import math
import random
import string
import time
from ctypes.wintypes import HWND

import cv2
import numpy as np
import win32api
import win32con
import win32gui

import img_manager
import posi_manager
import static_lib
import vkcode
from unit import *


class InteractionBGD:
    '''
    default size:1920x1080
    support size:1920x1080
    thanks for https://zhuanlan.zhihu.com/p/361569101
    '''

    def __init__(self, hwndname="原神"):
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
        self.WM_MOUSEMOVE = 0x0200
        self.WM_LBUTTONDOWN = 0x0201
        self.WM_LBUTTONUP = 0x202
        self.WM_MOUSEWHEEL = 0x020A
        self.WM_RBUTTONDOWN = 0x0204
        self.WM_RBUTTONDBLCLK = 0x0206
        self.WM_RBUTTONUP = 0x0205
        self.WM_KEYDOWN = 0x100
        self.WM_KEYUP = 0x101
        self.WHEEL_DELTA = 120
        self.DEFAULT_DELAY_TIME = 0.05
        self.DEBUG_MODE = False
        self.CONSOLE_ONLY = False

        self.handle = ctypes.windll.user32.FindWindowW(None, hwndname)

        if self.handle == 0:
            logger.error("未找到句柄，请确认原神窗口是否开启。")

    def capture(self, posi=None, shape='yx', jpgmode=None):
        """窗口客户区截图

        Args:
            handle (HWND): 要截图的窗口句柄

        Returns:
            numpy.ndarray: 截图数据
        """

        '''
        jpgmode:
        0:return png;
        1:return bg,black
        2:return ui,black
        '''
        # handle=self.handle
        # # 获取窗口客户区的大小
        # r = RECT()
        # self.GetClientRect(handle, ctypes.byref(r))
        # width, height = r.right, r.bottom
        # # 开始截图
        # dc = self.GetDC(handle)
        # cdc = self.CreateCompatibleDC(dc)
        # bitmap = self.CreateCompatibleBitmap(dc, width, height)
        # self.SelectObject(cdc, bitmap)
        # self.BitBlt(cdc, 0, 0, width, height, dc, 0, 0, self.SRCCOPY)
        # # 截图是BGRA排列，因此总元素个数需要乘以4
        # total_bytes = width*height*4
        # buffer = bytearray(total_bytes)
        # byte_array = ctypes.c_ubyte*total_bytes
        # self.GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
        # self.DeleteObject(bitmap)
        # self.DeleteObject(cdc)
        # self.ReleaseDC(handle, dc)
        # # 返回截图数据为numpy.ndarray

        # ret=np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)

        ret = static_lib.SCREENCAPTURE.get_capture()

        if posi != None:
            ret = ret[posi[0]:posi[2], posi[1]:posi[3]]
        if jpgmode == 0:
            pass
        elif jpgmode == 1:
            ret = self.png2jpg(ret, bgcolor='black', channel='bg')
        elif jpgmode == 2:
            ret = self.png2jpg(ret, bgcolor='black', channel='ui')
        elif jpgmode == 3:
            ret = ret[:, :, :3]
        return ret

    def match_img(self, img_name: str, is_show_res: bool = False):
        image = self.capture()
        # image = (image/(image[3]+10)).astype(int)

        # 转为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        # 读取图片，并保留Alpha通道
        template = cv2.imread('imgs/' + img_name, cv2.IMREAD_UNCHANGED)
        # template = template/template[3]
        # 取出Alpha通道
        alpha = template[:, :, 3]
        template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
        # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
        result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED, mask=alpha)
        # 获取结果中最大值和最小值以及他们的坐标
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if is_show_res:
            cv2.imshow('template', template)
            cv2.imshow('gray', gray)
            cv2.waitKey()
        top_left = max_loc
        h, w = template.shape[:2]
        bottom_right = top_left[0] + w, top_left[1] + h
        # 在窗口截图中匹配位置画红色方框
        if is_show_res:
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
            cv2.imshow('Match Template', image)
            cv2.waitKey()
        matching_rate = max_val
        return matching_rate, top_left, bottom_right

    def similar_img(self, img, target, is_gray=False, is_show_res: bool = False):

        if is_gray:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            target = cv2.cvtColor(target, cv2.COLOR_BGRA2GRAY)
        # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
        result = cv2.matchTemplate(img, target, cv2.TM_CCORR_NORMED)  # TM_CCOEFF_NORMED
        # 获取结果中最大值和最小值以及他们的坐标
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if is_show_res:
            cv2.imshow('template', target)
            cv2.imshow('gray', img)
            cv2.waitKey()
        # 在窗口截图中匹配位置画红色方框
        matching_rate = max_val
        return matching_rate

    def similar_img_pixel(self, img, target, is_gray=False):
        img1 = img.astype('int')
        target1 = target.astype('int')
        # cv2.imshow('1',img)
        # cv2.imshow('2',target)
        # cv2.waitKey(0)
        s = np.sum(img1 - target1)
        s = abs(s)
        matching_rate = 1 - s / ((img1.shape[0] * img1.shape[1]) * 765)
        return matching_rate

    def get_img_existence(self, imgname, jpgmode=2, is_gray=False, min_rate=0.95, is_log=False):
        upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if imgname in img_manager.alpha_dict:
            cap = self.capture()
            cap = self.png2jpg(cap, bgcolor='black', channel='ui', alpha_num=img_manager.alpha_dict[imgname])
        else:
            cap = self.capture(posi=posi_manager.get_posi_from_str(imgname), jpgmode=jpgmode)

        matching_rate = self.similar_img(img_manager.get_img_from_name(imgname), cap)

        if is_log:
            logger.debug(
                'imgname: ' + imgname + 'matching_rate: ' + str(matching_rate) + ' |function name: ' + upper_func_name)

        if matching_rate >= min_rate:
            return True
        else:
            return False

    def appear_then_click(self, imgname, jpgmode=2, is_gray=False, min_rate=0.95):
        upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if imgname in img_manager.alpha_dict:
            cap = self.capture()
            cap = self.png2jpg(cap, bgcolor='black', channel='ui', alpha_num=img_manager.alpha_dict[imgname])
        else:
            cap = self.capture(posi=posi_manager.get_posi_from_str(imgname), jpgmode=jpgmode)
        # min_rate = img_manager.matching_rate_dict[imgname]

        matching_rate = self.similar_img(img_manager.get_img_from_name(imgname), cap, is_gray=is_gray)

        logger.debug(
            'imgname: ' + imgname + 'matching_rate: ' + str(matching_rate) + ' |function name: ' + upper_func_name)

        if matching_rate >= min_rate:
            p = posi_manager.get_posi_from_str(imgname)
            center_p = [(p[1] + p[3]) / 2, (p[0] + p[2]) / 2]
            self.move_to(center_p[0], center_p[1])
            self.left_click()
            return True
        else:
            return False

    def appear_then_press(self, imgname, key_name, jpgmode=2, is_gray=False, min_rate=0.95):
        upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if imgname in img_manager.alpha_dict:
            cap = self.capture()
            cap = self.png2jpg(cap, bgcolor='black', channel='ui', alpha_num=img_manager.alpha_dict[imgname])
        else:
            cap = self.capture(posi=posi_manager.get_posi_from_str(imgname), jpgmode=jpgmode)
        # min_rate = img_manager.matching_rate_dict[imgname]

        matching_rate = self.similar_img(img_manager.get_img_from_name(imgname), cap, is_gray=is_gray)

        logger.debug(
            'imgname: ' + imgname + 'matching_rate: ' + str(
                matching_rate) + 'key_name:' + key_name + ' |function name: ' + upper_func_name)

        if matching_rate >= min_rate:
            self.key_press(key_name)
            return True
        else:

            return False

    def extract_white_letters(image, threshold=128):
        r, g, b = cv2.split(cv2.subtract((255, 255, 255, 0), image))
        minimum = cv2.min(cv2.min(r, g), b)
        maximum = cv2.max(cv2.max(r, g), b)
        return cv2.multiply(cv2.add(maximum, cv2.subtract(maximum, minimum)), 255.0 / threshold)

    def png2jpg(self, png, bgcolor='black', channel='bg', alpha_num=50):
        if bgcolor == 'black':
            bgcol = 0
        else:
            bgcol = 255

        jpg = png[:, :, :3]
        if channel == 'bg':
            over_item_list = png[:, :, 3] > alpha_num
        else:
            over_item_list = png[:, :, 3] < alpha_num
        jpg[:, :, 0][over_item_list] = bgcol
        jpg[:, :, 1][over_item_list] = bgcol
        jpg[:, :, 2][over_item_list] = bgcol
        return jpg

    def color_SD(self, x_col, target_col):  # standard deviation
        ret = 0
        for i in range(min(len(x_col), len(target_col))):
            t = abs(x_col[i] - target_col[i])
            math.pow(t, 2)
            ret += t
        return math.sqrt(ret / min(len(x_col), len(target_col)))

    def delay(self, x, randtime=True, isprint=True, comment=''):
        upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        a = random.randint(-10, 10)
        if randtime:
            a = a * x * 0.02
            if x > 0.2 and isprint:
                logger.debug('delay: ' + str(x) + ' rand: ' +
                             str(x + a) + ' |function name: ' + upper_func_name + ' |comment: ' + comment)
            time.sleep(x + a)
        else:
            if x > 0.2 and isprint:
                logger.debug('delay: ' + str(x) + ' |function name: ' + upper_func_name + ' |comment: ' + comment)
            time.sleep(x)

    def get_mouse_point(self):
        p = win32api.GetCursorPos()
        # print(p[0],p[1])
        #  GetWindowRect 获得整个窗口的范围矩形，窗口的边框、标题栏、滚动条及菜单等都在这个矩形内 
        x, y, w, h = win32gui.GetWindowRect(self.handle)
        # 鼠标坐标减去指定窗口坐标为鼠标在窗口中的坐标值
        pos_x = p[0] - x
        pos_y = p[1] - y
        return (pos_x, pos_y)

    def get_virtual_keycode(self, key: str):
        """根据按键名获取虚拟按键码

        Args:
            key (str): 按键名

        Returns:
            int: 虚拟按键码
        """
        if len(key) == 1 and key in string.printable:
            # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
            return self.VkKeyScanA(ord(key)) & 0xff
        else:
            return self.VK_CODE[key]

    def left_click(self, x=-1, y=-1):
        if type(x) == list:  # x为list类型时
            y = x[1]
            x = x[0]
        if x == -1:  # x为空时
            x, y = self.get_mouse_point()
        x = int(x)
        y = int(y)
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = y << 16 | x
            self.PostMessageW(self.handle, self.WM_LBUTTONDOWN, wparam, lparam)
            self.delay(0.06, randtime=False, isprint=False)
            self.PostMessageW(self.handle, self.WM_LBUTTONUP, wparam, lparam)
        logger.debug('left click ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def left_down(self, x=-1, y=-1):
        if x == -1:
            x, y = self.get_mouse_point()
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = y << 16 | x
            self.PostMessageW(self.handle, self.WM_LBUTTONDOWN, wparam, lparam)

        logger.debug('left down' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def left_up(self, x=-1, y=-1):
        if x == -1:
            x, y = self.get_mouse_point()
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = y << 16 | x
            self.PostMessageW(self.handle, self.WM_LBUTTONUP, wparam, lparam)
        logger.debug('left up ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def left_double_click(self, dt=0.05):
        if not self.CONSOLE_ONLY:
            self.left_click()
            self.delay(0.06, randtime=False, isprint=False)
            self.left_click()
        logger.debug('leftDoubleClick ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def right_click(self, x=-1, y=-1):
        if x == -1:
            x, y = self.get_mouse_point()
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = y << 16 | x
            self.PostMessageW(self.handle, self.WM_RBUTTONDOWN, wparam, lparam)
            self.delay(0.06, randtime=False, isprint=False)
            self.PostMessageW(self.handle, self.WM_RBUTTONUP, wparam, lparam)
            # pyautogui.rightClick()
        logger.debug('rightClick ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])
        self.delay(0.05)

    def key_down(self, key, is_log=True):
        if not self.CONSOLE_ONLY:
            vk_code = self.get_virtual_keycode(key)
            scan_code = self.MapVirtualKeyW(vk_code, 0)
            # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
            wparam = vk_code
            lparam = (scan_code << 16) | 1
            self.PostMessageW(self.handle, self.WM_KEYDOWN, wparam, lparam)
        if is_log:
            logger.debug(
                "keyDown " + key + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def key_up(self, key, is_log=True):
        if not self.CONSOLE_ONLY:
            vk_code = self.get_virtual_keycode(key)
            scan_code = self.MapVirtualKeyW(vk_code, 0)
            # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
            wparam = vk_code
            lparam = (scan_code << 16) | 0XC0000001
            self.PostMessageW(self.handle, self.WM_KEYUP, wparam, lparam)
        if is_log:
            logger.debug("keyUp " + key + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def key_press(self, key):
        if not self.CONSOLE_ONLY:
            vk_code = self.get_virtual_keycode(key)
            scan_code = self.MapVirtualKeyW(vk_code, 0)
            wparam = vk_code
            lparam = (scan_code << 16) | 1
            lparam2 = (scan_code << 16) | 0XC0000001
            self.PostMessageW(self.handle, self.WM_KEYDOWN, wparam, lparam)
            time.sleep(0.05)
            self.PostMessageW(self.handle, self.WM_KEYUP, wparam, lparam2)
            # self.delay(self.DEFAULT_DELAY_TIME)
        logger.debug("keyPress " + key + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def move_to(self, x: int, y: int, relative=False):
        """移动鼠标到坐标（x, y)

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        x = int(x)
        y = int(y)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousemove

        if relative:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)
        else:

            # print(x,y)

            # lx,ly,w,h = win32gui.GetWindowRect(self.handle)

            # pyautogui.moveRel()
            # p = win32api.GetCursorPos()
            # mx=p[0]
            # my=p[1]
            # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)
            wx, wy, w, h = win32gui.GetWindowRect(self.handle)
            # x+=wx
            # y+=wy
            # print(mx,my)
            # print(int((x-mx)/1.5), int((y-my)/1.5))
            # pydirectinput.moveTo(wx+x,wy+y)
            # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int((x-mx)/1.5), int((y-my)/1.5))
            win32api.SetCursorPos((wx + x, wy + y))

    def crop_image(self, imsrc, posilist):
        return imsrc[posilist[0]:posilist[2], posilist[1]:posilist[3]]


if __name__ == '__main__':
    ib = InteractionBGD()
    rootpath = "D:\Program Data\\vscode\GIA\genshin_impact_assistant\dist\imgs"
    # ib.similar_img_pixel(cv2.imread(rootpath+"\\yunjin_q.png"),cv2.imread(rootpath+"\\zhongli_q.png"))

    # print(win32api.GetCursorPos())
    # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 150, 150)
    # print(win32api.GetCursorPos())
    while 1:
        time.sleep(1)
        print(ib.get_img_existence(img_manager.F_BUTTON, jpgmode=2))
        # print(ib.get_img_existence(img_manager.USE_20X2RESIN_DOBLE_CHOICES))
        # ib.appear_then_click(imgname=img_manager.USE_20RESIN_DOBLE_CHOICES)
        # ib.move_to(100,100)
