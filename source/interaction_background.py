from util import *
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

import pyautogui
import pydirectinput
import img_manager
import posi_manager
import static_lib
import vkcode


IMG_RATE = 0
IMG_POSI = 1
IMG_POINT = 2
IMG_RECT = 3


class InteractionBGD:
    """
    default size:1920x1080
    support size:1920x1080
    thanks for https://zhuanlan.zhihu.com/p/361569101
    """

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

        self.isChromelessWindow = config_json["ChromelessWindow"]
        self.handle = ctypes.windll.user32.FindWindowW(None, hwndname)

        if self.handle == 0:
            self.handle = static_lib.get_handle()

        if self.handle == 0:
            logger.error("未找到句柄，请确认原神窗口是否开启。")

    def capture(self, posi=None, shape='yx', jpgmode=None):
        """窗口客户区截图

        Args:
            posi ( [y1,x1,y2,x2] ): 截图区域的坐标, y2>y1,x2>x1. 全屏截图时为None。
            shape (str): 为'yx'或'xy'.决定返回数组是[1080,1920]或[1920,1080]。
            jpgmode(int): 
                0:return jpg (3 channels, delete the alpha channel)
                1:return genshin background channel, background color is black
                2:return genshin ui channel, background color is black

        Returns:
            numpy.ndarray: 图片数组
        """

        ret = static_lib.SCREENCAPTURE.get_capture()
        if (ret.shape == (0, 0, 3)) or (ret.shape == (0, 0, 4)):
            logger.error("截图失败")
        # img_manager.qshow(ret)
        if posi is not None:
            ret = ret[posi[0]:posi[2], posi[1]:posi[3]]
        if jpgmode == 0:
            ret = ret[:, :, :3]
        elif jpgmode == 1:
            ret = self.png2jpg(ret, bgcolor='black', channel='bg')
        elif jpgmode == 2:
            ret = self.png2jpg(ret, bgcolor='black', channel='ui')  # before v3.1
            # ret = self.png2jpg(ret, bgcolor='black', channel='bg', alpha_num = 175)
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

    def match_multiple_img(self, img, template, is_gray=False, is_show_res: bool = False, ret_mode=IMG_POINT,
                           threshold=0.98):
        """多图片识别

        Args:
            img (numpy): 截图Mat
            template (numpy): 要匹配的样板图片
            is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.
            is_show_res (bool, optional): 结果显示. Defaults to False.
            ret_mode (int, optional): 返回值模式,目前只有IMG_POINT. Defaults to IMG_POINT. 
            threshold (float, optional): 最小匹配度. Defaults to 0.98.

        Returns:
            list[list[], ...]: 匹配成功的坐标列表
        """
        if is_gray:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
        res_posi = []
        result = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)  # TM_CCOEFF_NORMED
        # img_manager.qshow(template)
        h, w = template.shape[:2]  # 获取模板高和宽
        loc = np.where(result >= threshold)  # 匹配结果小于阈值的位置
        for pt in zip(*loc[::-1]):  # 遍历位置，zip把两个列表依次参数打包
            right_bottom = (pt[0] + w, pt[1] + h)  # 右下角位置
            if ret_mode == IMG_RECT:
                res_posi.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
            else:
                res_posi.append([pt[0] + w / 2, pt[1] + h / 2])
            # cv2.rectangle((show_img), pt, right_bottom, (0,0,255), 2) #绘制匹配到的矩阵
        if is_show_res:
            show_img = img.copy()
            # print(*loc[::-1])
            for pt in zip(*loc[::-1]):  # 遍历位置，zip把两个列表依次参数打包
                right_bottom = (pt[0] + w, pt[1] + h)  # 右下角位置
                cv2.rectangle((show_img), pt, right_bottom, (0, 0, 255), 2)  # 绘制匹配到的矩阵
            cv2.imshow("img", show_img)
            cv2.imshow("template", template)
            cv2.waitKey(0)  # 获取按键的ASCLL码
            cv2.destroyAllWindows()  # 释放所有的窗口

        return res_posi

    def similar_img(self, img, target, is_gray=False, is_show_res: bool = False, ret_mode=IMG_RATE):
        """单个图片匹配

        Args:
            img (numpy): Mat
            template (numpy): 要匹配的样板图片
            is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.
            is_show_res (bool, optional): 结果显示. Defaults to False.
            ret_mode (int, optional): 返回值模式. Defaults to IMG_RATE.

        Returns:
            float/(float, list[]): 匹配度或者匹配度和它的坐标
        """
        if is_gray:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            target = cv2.cvtColor(target, cv2.COLOR_BGRA2GRAY)
        # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
        # img_manager.qshow(img)
        result = cv2.matchTemplate(img, target, cv2.TM_CCORR_NORMED)  # TM_CCOEFF_NORMED
        # 获取结果中最大值和最小值以及他们的坐标
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if is_show_res:
            cv2.waitKey()
        # 在窗口截图中匹配位置画红色方框
        matching_rate = max_val
        if ret_mode == IMG_RATE:
            return matching_rate
        elif ret_mode == IMG_POSI:
            return matching_rate, max_loc

    # def similar_img_pixel(self, img, target, is_gray=False):
    #     """ABANDON

    #     Args:
    #         img (_type_): _description_
    #         target (_type_): _description_
    #         is_gray (bool, optional): _description_. Defaults to False.

    #     Returns:
    #         _type_: _description_
    #     """
    #     img1 = img.astype('int')
    #     target1 = target.astype('int')
    #     # cv2.imshow('1',img)
    #     # cv2.imshow('2',target)
    #     # cv2.waitKey(0)
    #     s = np.sum(img1 - target1)
    #     s = abs(s)
    #     matching_rate = 1 - s / ((img1.shape[0] * img1.shape[1]) * 765)
    #     return matching_rate

    def get_img_position(self, imgicon: img_manager.ImgIcon, is_gray=False, is_log=False):
        """获得图片在屏幕上的坐标

        Args:
            imgicon (img_manager.ImgIcon): imgicon对象
            is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.
            is_log (bool, optional): 是否打印日志. Defaults to False.

        Returns:
            list[]/bool: 返回坐标或False
        """
        upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # if imgname in img_manager.alpha_dict:
        #     cap = self.capture()
        #     cap = self.png2jpg(cap, bgcolor='black', channel='ui', alpha_num=img_manager.alpha_dict[imgname])
        # else:
        cap = self.capture(posi=imgicon.cap_posi, jpgmode=imgicon.jpgmode)

        matching_rate, max_loc = self.similar_img(cap, imgicon.image, ret_mode=IMG_POSI)

        if is_log:
            logger.debug(
                'imgname: ' + imgicon.name + 'max_loc: ' + str(max_loc) + ' |function name: ' + upper_func_name)

        if matching_rate >= imgicon.threshold:
            return max_loc
        else:
            return False

    def get_img_existence(self, imgicon: img_manager.ImgIcon, is_gray=False, is_log=False):
        """检测图片是否存在

        Args:
            imgicon (img_manager.ImgIcon): imgicon对象
            is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.
            is_log (bool, optional): 是否打印日志. Defaults to False.

        Returns:
            bool: bool
        """
        upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        cap = self.capture(posi=imgicon.cap_posi, jpgmode=imgicon.jpgmode)

        matching_rate = self.similar_img(cap, imgicon.image)
        # if matching_rate== 0:
        #     img_manager.qshow(cap)
        if is_log:
            logger.debug(
                'imgname: ' + imgicon.name + 'matching_rate: ' + str(
                    matching_rate) + ' |function name: ' + upper_func_name)

        if matching_rate >= imgicon.threshold:
            return True
        else:
            return False

    def appear_then_click(self, inputvar, is_gray=False):
        """appear then click

        Args:
            imgicon (img_manager.ImgIcon): imgicon对象
            is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.

        Returns:
            bool: bool,点击操作是否成功
        """
        if isinstance(inputvar, img_manager.ImgIcon):
            imgicon = inputvar
            upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]

            cap = self.capture(posi=imgicon.cap_posi, jpgmode=imgicon.jpgmode)
            # min_rate = img_manager.matching_rate_dict[imgname]

            matching_rate = self.similar_img(imgicon.image, cap, is_gray=is_gray)

            logger.debug(
                'imgname: ' + imgicon.name + 'matching_rate: ' + str(
                    matching_rate) + ' |function name: ' + upper_func_name)

            if matching_rate >= imgicon.threshold:
                p = imgicon.cap_posi
                center_p = [(p[1] + p[3]) / 2, (p[0] + p[2]) / 2]
                self.move_to(center_p[0], center_p[1])
                self.left_click()
                return True
            else:
                return False
        elif isinstance(inputvar, str):
            pass

    def appear_then_press(self, imgicon: img_manager.ImgIcon, key_name, is_gray=False):
        """appear then press

        Args:
            imgicon (img_manager.ImgIcon): imgicon对象
            key_name (str): key_name
            is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.

        Returns:
            bool: 操作是否成功
        """
        upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        cap = self.capture(posi=imgicon.cap_posi, jpgmode=imgicon.jpgmode)
        # min_rate = img_manager.matching_rate_dict[imgname]

        matching_rate = self.similar_img(imgicon.image, cap, is_gray=is_gray)

        logger.debug(
            'imgname: ' + imgicon.name + 'matching_rate: ' + str(
                matching_rate) + 'key_name:' + key_name + ' |function name: ' + upper_func_name)

        if matching_rate >= imgicon.threshold:
            self.key_press(key_name)
            return True
        else:

            return False

    def extract_white_letters(image, threshold=128):
        """_summary_

        Args:
            image (_type_): _description_
            threshold (int, optional): _description_. Defaults to 128.

        Returns:
            _type_: _description_
        """
        r, g, b = cv2.split(cv2.subtract((255, 255, 255, 0), image))
        minimum = cv2.min(cv2.min(r, g), b)
        maximum = cv2.max(cv2.max(r, g), b)
        return cv2.multiply(cv2.add(maximum, cv2.subtract(maximum, minimum)), 255.0 / threshold)

    # @staticmethod
    def png2jpg(self, png, bgcolor='black', channel='bg', alpha_num=50):
        """将截图的4通道png转换为3通道jpg

        Args:
            png (Mat/ndarray): 4通道图片
            bgcolor (str, optional): 背景的颜色. Defaults to 'black'.
            channel (str, optional): 提取背景或UI. Defaults to 'bg'.
            alpha_num (int, optional): 透明通道的大小. Defaults to 50.

        Returns:
            Mat/ndarray: 3通道图片
        """
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

    # @staticmethod
    def color_sd(self, x_col, target_col):  # standard deviation
        """Not in use

        Args:
            x_col (_type_): _description_
            target_col (_type_): _description_

        Returns:
            _type_: _description_
        """
        ret = 0
        for i in range(min(len(x_col), len(target_col))):
            t = abs(x_col[i] - target_col[i])
            math.pow(t, 2)
            ret += t
        return math.sqrt(ret / min(len(x_col), len(target_col)))

    # @staticmethod
    def delay(self, x, randtime=True, isprint=True, comment=''):
        """延迟一段时间，单位为秒

        Args:
            x (int): 延迟时间
            randtime (bool, optional): 是否启用加入随机秒. Defaults to True.
            isprint (bool, optional): 是否打印日志. Defaults to True.
            comment (str, optional): 日志注释. Defaults to ''.
        """
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
        """获得当前鼠标在窗口内的位置

        Returns:
            (x,y): 坐标
        """
        p = win32api.GetCursorPos()
        # print(p[0],p[1])
        #  GetWindowRect 获得整个窗口的范围矩形，窗口的边框、标题栏、滚动条及菜单等都在这个矩形内 
        x, y, w, h = win32gui.GetWindowRect(self.handle)
        # 鼠标坐标减去指定窗口坐标为鼠标在窗口中的坐标值
        pos_x = p[0] - x
        pos_y = p[1] - y
        return pos_x, pos_y

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
        """左键点击

        Args:
            x (int, optional): x. Defaults to -1.
            y (int, optional): y. Defaults to -1.
        """
        if type(x) == list:  # x为list类型时
            y = x[1]
            x = x[0]
        if x == -1:  # x为空时
            x, y = self.get_mouse_point()
        else:
            x = int(x)
            y = int(y)
            self.move_to(x, y)
            self.delay(0.8)

        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = 0 << 16 | 0
            self.PostMessageW(self.handle, self.WM_LBUTTONDOWN, wparam, lparam)
            self.delay(0.06, randtime=False, isprint=False)
            self.PostMessageW(self.handle, self.WM_LBUTTONUP, wparam, lparam)
        logger.debug('left click ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def left_down(self, x=-1, y=-1):
        """左键按下

        Args:
            x (int, optional): _description_. Defaults to -1.
            y (int, optional): _description_. Defaults to -1.
        """
        if type(x) == list:  # x为list类型时
            y = x[1]
            x = x[0]
        if x == -1:  # x为空时
            x, y = self.get_mouse_point()
        x = int(x)
        y = int(y)
        if not self.CONSOLE_ONLY:
            # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            # pyautogui.mouseDown()
            wparam = 0
            lparam = y << 16 | x
            self.PostMessageW(self.handle, self.WM_LBUTTONDOWN, wparam, lparam)
            time.sleep(0.01)
            self.PostMessageW(self.handle, self.WM_LBUTTONDOWN, wparam, lparam)
            time.sleep(0.01)
            self.PostMessageW(self.handle, self.WM_LBUTTONDOWN, wparam, lparam)

        logger.debug('left down' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def left_up(self, x=-1, y=-1):
        """左键抬起

        Args:
            x (int, optional): _description_. Defaults to -1.
            y (int, optional): _description_. Defaults to -1.
        """
        if x == -1:
            x, y = self.get_mouse_point()
        if not self.CONSOLE_ONLY:
            # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            # pyautogui.mouseUp()
            wparam = 0
            lparam = y << 16 | x
            self.PostMessageW(self.handle, self.WM_LBUTTONUP, wparam, lparam)
            time.sleep(0.01)
            self.PostMessageW(self.handle, self.WM_LBUTTONUP, wparam, lparam)
            time.sleep(0.01)
            self.PostMessageW(self.handle, self.WM_LBUTTONUP, wparam, lparam)

        logger.debug('left up ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def left_double_click(self, dt=0.05):
        """左键双击

        Args:
            dt (float, optional): 间隔时间. Defaults to 0.05.
        """
        if not self.CONSOLE_ONLY:
            self.left_click()
            self.delay(0.06, randtime=False, isprint=False)
            self.left_click()
        logger.debug('leftDoubleClick ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    def right_click(self, x=-1, y=-1):
        """右键单击

        Args:
            x (int, optional): _description_. Defaults to -1.
            y (int, optional): _description_. Defaults to -1.
        """
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
        """按下按键

        Args:
            key (str): 按键代号。查阅vkCode.py
            is_log (bool, optional): 是否打印日志. Defaults to True.
        """
        if key == 'w':
            static_lib.W_KEYDOWN = True

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
        """松开按键

        Args:
            key (str): 按键代号。查阅vkCode.py
            is_log (bool, optional): 是否打印日志. Defaults to True.
        """
        if key == 'w':
            static_lib.W_KEYDOWN = False

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
        """点击按键

        Args:
            key (str): 按键代号。查阅vkCode.py
        """
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
            x (int): 横坐标
            y (int): 纵坐标
            relative (bool): 是否为相对移动。
        """
        x = int(x)
        y = int(y)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousemove

        if relative:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)
            # pydirectinput.moveRel(x,y)
        else:

            # print(x,y)

            # lx,ly,w,h = win32gui.GetWindowRect(self.handle)

            # pyautogui.moveRel()
            # p = win32api.GetCursorPos()
            # mx=p[0]
            # my=p[1]
            # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)
            wx, wy, w, h = win32gui.GetWindowRect(self.handle)
            x += wx
            if self.isChromelessWindow:
                y += wy
            else:
                y = y + wy + 26
                
            # print(mx,my)
            # print(int((x-mx)/1.5), int((y-my)/1.5))
            # pydirectinput.moveTo(wx+x,wy+y)
            # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int((x-mx)/1.5), int((y-my)/1.5))
            win32api.SetCursorPos((x, y))

            # wparam = 0
            # lparam = y << 16 | x
            # self.PostMessageW(self.handle, self.WM_MOUSEMOVE, wparam, lparam)
            # self.PostMessageW(self.handle, self.WM_MOUSEMOVE, wparam, lparam)
            # self.PostMessageW(self.handle, self.WM_MOUSEMOVE, wparam, lparam)

    # @staticmethod
    def crop_image(self, imsrc, posilist):
        return imsrc[posilist[0]:posilist[2], posilist[1]:posilist[3]]

    def move_and_click(self, type='left', position=[0,0]):
        self.move_to(position[0], position[1])
        time.sleep(0.2)
        if type == 'left':
            self.left_click()
        else:
            self.right_click()

if __name__ == '__main__':
    ib = InteractionBGD()
    rootpath = "D:\Program Data\\vscode\GIA\genshin_impact_assistant\dist\imgs"
    # ib.similar_img_pixel(cv2.imread(rootpath+"\\yunjin_q.png"),cv2.imread(rootpath+"\\zhongli_q.png"))

    # print(win32api.GetCursorPos())
    # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 150, 150)
    # print(win32api.GetCursorPos())
    # a = ib.match_multiple_img(ib.capture(jpgmode=3), img_manager.get_img_from_name(img_manager.bigmap_TeleportWaypoint, reshape=False))
    # print(a)
    # ib.left_down()
    # time.sleep(1)
    ib.move_to(200, 200)

    # for i in range(20):
    #     pydirectinput.mouseDown(0,0)
    #     pydirectinput.moveRel(10,10)
    # win32api.SetCursorPos((300, 300))
    # pydirectinput.
    print()
    while 1:
        time.sleep(1)
        print(ib.get_img_existence(img_manager.motion_flying), ib.get_img_existence(img_manager.motion_climbing),
              ib.get_img_existence(img_manager.motion_swimming))

        # print(ib.get_img_existence(img_manager.USE_20X2RESIN_DOBLE_CHOICES))
        # ib.appear_then_click(imgname=img_manager.USE_20RESIN_DOBLE_CHOICES)
        # ib.move_to(100,100)
