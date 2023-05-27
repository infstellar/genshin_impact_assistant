from source.util import *
import inspect
import math
import random
import threading
import time
import cv2
import numpy as np
import win32api
import win32gui
from source.common import static_lib
from source.manager import img_manager, text_manager, button_manager


IMG_RATE = 0
IMG_POSI = 1
IMG_POINT = 2
IMG_RECT = 3
IMG_BOOL = 4
IMG_BOOLRATE = 5


winname_default = ["Genshin Impact", "原神"]

# process_name_cloud = ["云·原神"]

def before_operation(print_log=True):
    def outwrapper(func):
        def wrapper(*args, **kwargs):
            func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
            func_name_2 = inspect.getframeinfo(inspect.currentframe().f_back.f_back)[2]
            # bb=inspect.getframeinfo(inspect.currentframe().f_back.f_back)
            # cc=inspect.getframeinfo(inspect.currentframe().f_back.f_back.f_back)
            if print_log:
                logger.trace(f" operation: {func.__name__} | args: {args[1:]} | {kwargs} | function name: {func_name} & {func_name_2}")
                    
            if INTERACTION_MODE == INTERACTION_DESKTOP:
                winname = get_active_window_process_name()
                if winname not in PROCESS_NAME:
                    while 1:
                        if get_active_window_process_name() in PROCESS_NAME:
                            logger.info(t2t("恢复操作"))
                            break
                        logger.info(t2t("当前窗口焦点为") + str(winname) + t2t("不是原神窗口") + str(PROCESS_NAME) + t2t("，操作暂停 ") + str(5 - (time.time()%5)) +t2t(" 秒"))
                        time.sleep(5 - (time.time()%5))
            return func(*args, **kwargs)
        return wrapper
    return outwrapper

GetDC = ctypes.windll.user32.GetDC
CreateCompatibleDC = ctypes.windll.gdi32.CreateCompatibleDC
GetClientRect = ctypes.windll.user32.GetClientRect
CreateCompatibleBitmap = ctypes.windll.gdi32.CreateCompatibleBitmap
SelectObject = ctypes.windll.gdi32.SelectObject
BitBlt = ctypes.windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = ctypes.windll.gdi32.GetBitmapBits
DeleteObject = ctypes.windll.gdi32.DeleteObject
ReleaseDC = ctypes.windll.user32.ReleaseDC
PostMessageW = ctypes.windll.user32.PostMessageW
MapVirtualKeyW = ctypes.windll.user32.MapVirtualKeyW


class InteractionBGD:
    """
    default size:1920x1080
    support size:1920x1080
    thanks for https://zhuanlan.zhihu.com/p/361569101
    """

    def __init__(self):
        logger.info("InteractionBGD created")
        self.WHEEL_DELTA = 120
        self.DEFAULT_DELAY_TIME = 0.05
        self.DEBUG_MODE = False
        self.CONSOLE_ONLY = False
        self.isBorderlessWindow = GIAconfig.General_BorderlessWindow
        self.itt_exec = None
        self.capture_obj = None
        self.operation_lock = threading.Lock()
        if INTERACTION_MODE == INTERACTION_DESKTOP:
            import source.interaction.interaction_normal
            self.itt_exec = source.interaction.interaction_normal.InteractionNormal()
        elif INTERACTION_MODE == INTERACTION_DESKTOP_BACKGROUND:
            import source.interaction.interaction_dm
            self.itt_exec = source.interaction.interaction_dm.InteractionDm()
        
        if IS_DEVICE_PC:
            from source.interaction.capture import WindowsCapture
            self.capture_obj = WindowsCapture()
        else:
            from source.interaction.capture import EmulatorCapture
            self.capture_obj = EmulatorCapture()
            
        self.key_status={'w':False}
        self.key_freeze={}
        
        
        # if handle != 0:
        #     static_lib.HANDLE = handle
        #     logger.debug(f"handle: {static_lib.HANDLE}")
        
        # if static_lib.HANDLE == 0:
        #     logger.error(t2t("未找到句柄，请确认原神窗口是否开启。"))
    
    def capture(self, posi=None, shape='yx', jpgmode=None, check_shape = True):
        """窗口客户区截图

        Args:
            posi ( [x1,y1,x2,y2] ): 截图区域的坐标, y2>y1,x2>x1. 全屏截图时为None。
            shape (str): 为'yx'或'xy'.决定返回数组是[1080,1920]或[1920,1080]。
            jpgmode(int): 
                0:return jpg (3 channels, delete the alpha channel)
                1:return genshin background channel, background color is black
                2:return genshin ui channel, background color is black

        Returns:
            numpy.ndarray: 图片数组
        """

        ret = self.capture_obj.capture()
        
        # if check_shape:
        #     if ret.shape != (1080, 1920, 4):
        #         logger.error(t2t("截图失败, shape=") + str(ret.shape) + t2t("将在2秒后重试。"))
        #         while 1:
        #             time.sleep(2)
        #             ret = self.capture_obj.capture()
        #             if ret.shape == (1080, 1920, 4):
        #                 break
        #             else:
        #                 logger.error(t2t("截图失败, shape=") + str(ret.shape) + t2t("将在2秒后重试。"))

        # img_manager.qshow(ret)
        if posi is not None:
            ret = crop(ret, posi)
        if ret.shape[2]==3:
            pass
        elif jpgmode == 0:
            ret = ret[:, :, :3]
        elif jpgmode == 1:
            ret = self.png2jpg(ret, bgcolor='black', channel='bg')
        elif jpgmode == 2:
            ret = self.png2jpg(ret, bgcolor='black', channel='ui')  # before v3.1
            # ret = self.png2jpg(ret, bgcolor='black', channel='bg', alpha_num = 175)
        elif jpgmode == 3:
            ret = ret[:, :, :3]
        return ret

    def match_multiple_img(self, img, template, is_gray=False, is_show_res: bool = False, ret_mode=IMG_POINT,
                           threshold=0.98, ignore_close=False):
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
        res = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
        # res = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)  # TM_CCOEFF_NORMED
        # img_manager.qshow(template)
        # h, w = template.shape[:2]  # 获取模板高和宽
        loc = np.where(res >= threshold)  # 匹配结果小于阈值的位置
        
        # Sort coordinates of matched pixels by their similarity score in descending order
        matched_coordinates = sorted(zip(*loc[::-1]), key=lambda x: res[x[1], x[0]], reverse=True)
        if ignore_close:
            ret_coordinates = []
            for i in matched_coordinates:
                if len(ret_coordinates) == 0:
                    ret_coordinates.append(i)
                    continue
                if min(euclidean_distance_plist(i, ret_coordinates))>=15:
                    ret_coordinates.append(i)
            return ret_coordinates
        # for pt in zip(*loc[::-1]):  # 遍历位置，zip把两个列表依次参数打包
        #     right_bottom = (pt[0] + w, pt[1] + h)  # 右下角位置
        #     if ret_mode == IMG_RECT:
        #         res_posi.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
        #     else:
        #         res_posi.append([pt[0] + w / 2, pt[1] + h / 2])
        #     # cv2.rectangle((show_img), pt, right_bottom, (0,0,255), 2) #绘制匹配到的矩阵
        # if is_show_res:
        #     show_img = img.copy()
        #     # print(*loc[::-1])
        #     for pt in zip(*loc[::-1]):  # 遍历位置，zip把两个列表依次参数打包
        #         right_bottom = (pt[0] + w, pt[1] + h)  # 右下角位置
        #         cv2.rectangle((show_img), pt, right_bottom, (0, 0, 255), 2)  # 绘制匹配到的矩阵
        #     cv2.imshow("img", show_img)
        #     cv2.imshow("template", template)
        #     cv2.waitKey(0)  # 获取按键的ASCII码
        #     cv2.destroyAllWindows()  # 释放所有的窗口

        return matched_coordinates

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

        if matching_rate >= imgicon.threshold:
            if imgicon.win_text != None:
                from source.api.pdocr_complete import ocr
                r = ocr.get_text_position(cap, imgicon.win_text)
                if r==-1:
                    matching_rate = -1
            # if imgicon.win_page != 'all':
            #     pn = scene_lib.get_current_pagename()
            #     if pn != imgicon.win_page:
            #         matching_rate = -2

        if imgicon.is_print_log(matching_rate >= imgicon.threshold):
            logger.debug('imgname: ' + imgicon.name + 'max_loc: ' + str(max_loc) + ' |function name: ' + upper_func_name)

        if matching_rate >= imgicon.threshold:
            return max_loc
        else:
            return False

    def get_img_existence(self, imgicon: img_manager.ImgIcon, is_gray=False, is_log=True, ret_mode = IMG_BOOL, show_res = False, cap = None):
        """检测图片是否存在

        Args:
            imgicon (img_manager.ImgIcon): imgicon对象
            is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.
            is_log (bool, optional): 是否打印日志. Defaults to False.

        Returns:
            bool: bool
        """
        upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if cap is None:
            cap = self.capture(posi=imgicon.cap_posi, jpgmode=imgicon.jpgmode)

        matching_rate = self.similar_img(cap, imgicon.image)
        
        if matching_rate >= imgicon.threshold:
            if imgicon.win_text != None:
                from source.api.pdocr_complete import ocr
                r = ocr.get_text_position(cap, imgicon.win_text)
                if r==-1:
                    matching_rate = 0
            # if imgicon.win_page != 'all':
            #     pn = scene_lib.get_current_pagename()
            #     if pn != imgicon.win_page:
            #         matching_rate = 0
        
        if show_res:
            cv2.imshow(imgicon.name, cap)
            cv2.waitKey(100)

        if imgicon.is_print_log(matching_rate >= imgicon.threshold) and is_log:
            logger.debug(
                'imgname: ' + imgicon.name + 'matching_rate: ' + str(
                    matching_rate) + ' |function name: ' + upper_func_name)
        if ret_mode == IMG_BOOL:
            if matching_rate >= imgicon.threshold:
                return True
            else:
                return False
        elif ret_mode == IMG_BOOLRATE:
            if matching_rate >= imgicon.threshold:
                return matching_rate
            else:
                return False
        elif ret_mode == IMG_RATE:
            return matching_rate
        
    def get_text_existence(self, textobj: text_manager.TextTemplate, is_gray=False, is_log = True, ret_mode = IMG_BOOL, show_res = False):
        from source.api.pdocr_complete import ocr
        cap = self.capture(posi = textobj.cap_area, jpgmode = 0)
        if ocr.get_text_position(cap, textobj.text) != -1:
            if is_log:
                logger.debug(f"get_text_existence: text: {textobj.text} Found")
            return True
        else:
            logger.debug(f"get_text_existence: text: {textobj.text} Not Found")
            return False

    def appear_then_click(self, inputvar, is_gray=False, is_log = False):
        """appear then click

        Args:
            inputvar (img_manager.ImgIcon/text_manager.TextTemplate/button_manager.Button)
            is_gray (bool, optional): 是否启用灰度匹配. Defaults to False.

        Returns:
            bool: bool,点击操作是否成功
        """
        
        if isinstance(inputvar, button_manager.Button):
            imgicon = inputvar
            upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]

            if not inputvar.click_retry_timer.reached():
                return False
            
            if inputvar.click_fail_timer.reached_and_reset():
                logger.error(t2t("appear then click fail"))
                logger.info(f"{inputvar.name} {inputvar.click_position}")
                return False
            
            cap = self.capture(posi=imgicon.cap_posi, jpgmode=imgicon.jpgmode)
            # min_rate = img_manager.matching_rate_dict[imgname]

            if inputvar.is_bbg == False:
                matching_rate, click_posi = self.similar_img(imgicon.image, cap, is_gray=is_gray, ret_mode=IMG_POSI)
            else:
                matching_rate = self.similar_img(imgicon.image, cap, is_gray=is_gray)

            if matching_rate >= imgicon.threshold:
                if imgicon.win_text != None:
                    from source.api.pdocr_complete import ocr
                    r = ocr.get_text_position(cap, imgicon.win_text)
                    if r==-1:
                        matching_rate = 0
            
            if imgicon.is_print_log(matching_rate >= imgicon.threshold) or is_log:
                logger.debug(
                'imgname: ' + imgicon.name + 'matching_rate: ' + str(
                    matching_rate) + ' |function name: ' + upper_func_name)

            if matching_rate >= imgicon.threshold:
                p = imgicon.cap_posi
                if inputvar.is_bbg == True:
                    self.move_and_click(position=imgicon.click_position())
                else:
                    self.move_and_click(position=click_posi)
                logger.debug(f"appear then click: True: {imgicon.name} func: {upper_func_name}")
                inputvar.click_fail_timer.reset()
                inputvar.click_retry_timer.reset()
                return True
            else:
                return False

        elif isinstance(inputvar, img_manager.ImgIcon):
            imgicon = inputvar
            upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]

            cap = self.capture(posi=imgicon.cap_posi, jpgmode=imgicon.jpgmode)
            # min_rate = img_manager.matching_rate_dict[imgname]

            matching_rate = self.similar_img(imgicon.image, cap, is_gray=is_gray)

            if matching_rate >= imgicon.threshold:
                if imgicon.win_text != None:
                    from source.api.pdocr_complete import ocr
                    r = ocr.get_text_position(cap, imgicon.win_text)
                    if r==-1:
                        matching_rate = 0
            
            if imgicon.is_print_log(matching_rate >= imgicon.threshold) or is_log:
                logger.debug('imgname: ' + imgicon.name + 'matching_rate: ' + str(matching_rate) + ' |function name: ' + upper_func_name)

            if matching_rate >= imgicon.threshold:
                p = imgicon.cap_posi
                center_p = [(p[0] + p[2]) / 2, (p[1] + p[3]) / 2]
                self.move_and_click([center_p[0], center_p[1]])  
                logger.debug(f"appear then click: True: {imgicon.name} func: {upper_func_name}")
                return True
            else:
                return False
            
        elif isinstance(inputvar, text_manager.TextTemplate):
            from source.api.pdocr_complete import ocr
            upper_func_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
            p1 = ocr.get_text_position(self.capture(jpgmode=0, posi=inputvar.cap_area), inputvar.text, cap_posi_leftup=inputvar.cap_area[:2])
            if is_log:
                logger.debug('text: ' + inputvar.text + 'position: ' + str(p1) + ' |function name: ' + upper_func_name)
            if p1 != -1:
                self.move_and_click([p1[0] + 5, p1[1] + 5], delay=1)
                logger.debug(f"appear then click: True: {inputvar.text} func: {upper_func_name}")
                return True
            else:
                return False
    
    def appear_then_click_groups(self, verify_img:img_manager.ImgIcon, inputvar_list:list, stop_func, verify_mode=False):
        """
        Click each inputvar in list.
        
        """
        succ_flags=[False for i in len(inputvar_list)]
        while 1:
            time.sleep(0.1)
            if stop_func:return False
            if all(succ_flags):
                if self.get_img_existence(verify_img) == verify_mode:
                    return True
            for i in len(inputvar_list):
                r = self.appear_then_click(inputvar_list[i])
                if r: succ_flags[i]=True
                

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

        if matching_rate >= imgicon.threshold:
            if imgicon.win_text != None:
                from source.api.pdocr_complete import ocr
                r = ocr.get_text_position(cap, imgicon.win_text)
                if r==-1:
                    matching_rate = 0
            # if imgicon.win_page != 'all':
            #     pn = scene_lib.get_current_pagename()
            #     if pn != imgicon.win_page:
            #         matching_rate = 0
        if imgicon.is_print_log(matching_rate >= imgicon.threshold):
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
    def delay(self, x, randtime=False, isprint=True, comment=''):
        """延迟一段时间，单位为秒

        Args:
            x : 延迟时间/key words
            randtime (bool, optional): 是否启用加入随机秒. Defaults to True.
            isprint (bool, optional): 是否打印日志. Defaults to True.
            comment (str, optional): 日志注释. Defaults to ''.
        """
        if x  == "animation":
            time.sleep(0.3)
            return
        if x  == "2animation":
            time.sleep(0.6)
            return
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

    # @before_operation(print_log = False)
    # def DONTUSEget_mouse_pointDONTUSE(self):
    #     """获得当前鼠标在窗口内的位置 不要用！
        
    #     Returns:
    #         (x,y): 坐标
    #     """
        
    #     p = win32api.GetCursorPos()
    #     # print(p[0],p[1])
    #     #  GetWindowRect 获得整个窗口的范围矩形，窗口的边框、标题栏、滚动条及菜单等都在这个矩形内 
    #     x, y, w, h = win32gui.GetWindowRect(static_lib.HANDLE)
    #     # 鼠标坐标减去指定窗口坐标为鼠标在窗口中的坐标值
    #     pos_x = p[0] - x
    #     pos_y = p[1] - y
    #     return pos_x, pos_y

    @before_operation()
    def left_click(self):
        """左键点击
        
        """
        
        self.operation_lock.acquire()
        if DEMO_MODE:
            logger.demo(t2t("左键点击"))
        # print('lock!')
        self.itt_exec.left_click()
        self.operation_lock.release()
        
        # logger.debug('left click ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    @before_operation()
    def left_down(self):
        """左键按下

        """
        
        self.operation_lock.acquire()
        if DEMO_MODE:
            logger.demo(t2t("左键按下"))
        # print('lock!')
        self.itt_exec.left_down()
        self.operation_lock.release()
        
        # logger.debug('left down' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    @before_operation()
    def left_up(self):
        """左键抬起

        """
        
        self.operation_lock.acquire()
        if DEMO_MODE:
            logger.demo(t2t("左键抬起"))
        # print('lock!')
        self.itt_exec.left_up()
        self.operation_lock.release()

        
        # logger.debug('left up ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    @before_operation()
    def left_double_click(self, dt=0.05):
        """左键双击

        Args:
            dt (float, optional): 间隔时间. Defaults to 0.05.
        """
        
        self.operation_lock.acquire()
        if DEMO_MODE:
            logger.demo(t2t("左键双击"))
        # print('lock!')
        self.itt_exec.left_double_click(dt=dt)
        self.operation_lock.release()
        
        # logger.debug('leftDoubleClick ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    @before_operation()
    def right_click(self):
        """右键单击

        """
        
        self.operation_lock.acquire()
        if DEMO_MODE:
            logger.demo(t2t("右键单击"))
        # print('lock!')
        self.itt_exec.right_click()
        self.operation_lock.release()
        
        
        # logger.debug('rightClick ' + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])
        self.delay(0.05)

    @before_operation()
    def middle_click(self):
        """点击鼠标中键
        """
        
        self.operation_lock.acquire()
        if DEMO_MODE:
            logger.demo(t2t("点击鼠标中键"))
        # print('lock!')
        self.itt_exec.middle_click()
        self.operation_lock.release()
    
    @before_operation()
    def key_down(self, key):
        """按下按键

        Args:
            key (str): 按键代号。查阅vkCode.py
        """
        
        self.operation_lock.acquire()
        if DEMO_MODE:
            logger.demo(t2t("按下按键: ")+str(key))
        # print('lock!')
        if key == 'w':
            static_lib.W_KEYDOWN = True
        self.itt_exec.key_down(key)
        self.key_status[key]=True
        self.operation_lock.release()
        
        # if is_log:
        #     logger.debug(
        #         "keyDown " + key + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    @before_operation()
    def key_up(self, key):
        """松开按键

        Args:
            key (str): 按键代号。查阅vkCode.py
        """
        
        self.operation_lock.acquire()
        if DEMO_MODE:
            logger.demo(t2t("松开按键: ")+str(key))
        # print('lock!')
        if key == 'w':
            static_lib.W_KEYDOWN = False
        self.itt_exec.key_up(key)
        self.key_status[key]=False
        self.operation_lock.release()
        
        # if is_log:
        #     logger.debug("keyUp " + key + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    @before_operation()
    def key_press(self, key):
        """点击按键

        Args:
            key (str): 按键代号。查阅vkCode.py
        """
        
        self.operation_lock.acquire()
        if DEMO_MODE:
            logger.demo(t2t("点击按键: ")+str(key))
        # print('lock!')
        self.itt_exec.key_press(key)
        self.key_status[key]=False
        self.operation_lock.release()
        
        # logger.debug("keyPress " + key + ' |function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])

    @before_operation(print_log=False)
    def move_to(self, x, y, relative=False):
        """移动鼠标到坐标（x, y)

        Args:
            x (int): 横坐标
            y (int): 纵坐标
            relative (bool): 是否为相对移动。
        """
        
        self.operation_lock.acquire()
        if DEMO_MODE:
            logger.demo(t2t("移动鼠标到坐标: ")+f"{round(x,0)},{round(y,0)}")
        # print('lock!')
        self.itt_exec.move_to(int(x), int(y), relative=relative, isBorderlessWindow=self.isBorderlessWindow)
        self.operation_lock.release()

    # @staticmethod
    def crop_image(self, imsrc, posilist):
        return imsrc[posilist[0]:posilist[2], posilist[1]:posilist[3]]

    @before_operation()
    def move_and_click(self, position, type='left', delay = 0.3):
        
        self.operation_lock.acquire()
        # print('lock!')
        if DEMO_MODE:
            logger.demo(t2t("移动鼠标到坐标: ")+f"{round(position[0],0)},{round(position[1],0)} 并点击")
        x = int(position[0])
        y = int(position[1])
        
        self.itt_exec.move_to(int(x), int(y), relative=False, isBorderlessWindow=self.isBorderlessWindow)
        time.sleep(delay)
        
        if type == 'left':
            self.itt_exec.left_click()
        else:
            self.itt_exec.right_click()
        
        self.operation_lock.release()

    @before_operation()
    def drag(self, origin_xy:list, targe_xy:list):
        self.operation_lock.acquire()
        # print('lock!')
        self.itt_exec.drag(origin_xy, targe_xy, isBorderlessWindow=self.isBorderlessWindow)
        self.operation_lock.release()
        
    def freeze_key(self, key, operate="down"):
        self.key_freeze[key] = self.key_status[key]
        if operate=="down":
            itt.key_down(key)
        else:
            itt.key_up(key)
    
    def unfreeze_key(self, key):
        operate = self.key_freeze[key]
        if operate:
            itt.key_down(key)
        else:
            itt.key_up(key)
def itt_test(itt: InteractionBGD):
    pass

itt = InteractionBGD()

# ge = source.common.generic_event.GenericEvent()
# ge.start()

if __name__ == '__main__':
    ib = InteractionBGD()
    rootpath = "D:\\Program Data\\vscode\\GIA\\genshin_impact_assistant\\dist\\imgs"
    # ib.similar_img_pixel(cv2.imread(rootpath+"\\yunjin_q.png"),cv2.imread(rootpath+"\\zhongli_q.png"))
    from source.manager import asset
    itt.appear_then_click(asset.ButtonFoodEgg, is_log=True)
    # print(win32api.GetCursorPos())
    # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 150, 150)
    # print(win32api.GetCursorPos())
    # a = ib.match_multiple_img(ib.capture(jpgmode=3), img_manager.get_img_from_name(img_manager.bigmap_TeleportWaypoint, reshape=False))
    # print(a)
    # ib.left_down()
    # time.sleep(1)
    # ib.move_to(200, 200)
    # img_manager.qshow(ib.capture())
    # ib.appear_then_click(button_manager.button_exit)
    # for i in range(20):
    #     pydirectinput.mouseDown(0,0)
    #     pydirectinput.moveRel(10,10)
    # win32api.SetCursorPos((300, 300))
    # pydirectinput.
    # a = ib.get_text_existence(asset.LEYLINEDISORDER)
    # print(a)
    # img_manager.qshow(ib.capture())
    print()
    while 1:
        # time.sleep(1)
        # print(ib.get_img_existence(img_manager.motion_flying), ib.get_img_existence(img_manager.motion_climbing),
        #       ib.get_img_existence(asset.motion_swimming))
        time.sleep(2)
        ib.move_and_click([100,100], type="left")
        # print(ib.get_img_existence(img_manager.USE_20X2RESIN_DOBLE_CHOICES))
        # ib.appear_then_click(imgname=asset.USE_20RESIN_DOBLE_CHOICES)
        # ib.move_to(100,100)
