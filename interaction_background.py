import string
from unit import *
import win32api, win32con, win32gui
from ctypes.wintypes import RECT, HWND
import numpy as np
import cv2 
import vkcode 

class Interaction_BGD():
    '''
    default size:1920x1080
    support size:1920x1080
    thanks for https://zhuanlan.zhihu.com/p/361569101
    '''
    
    def __init__(self,hwnd=None):
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
        self.VK_CODE=vkcode.VK_CODE
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
        self.DEFAULT_DELAY_TIME=0.05
        self.DEBUG_MODE=False
        self.CONSOLE_ONLY=False
        if hwnd==None:
            self.handle=ctypes.windll.user32.FindWindowW(None, "原神")
        else:
            self.handle=hwnd
    
    def capture(self):
        """窗口客户区截图

        Args:
            handle (HWND): 要截图的窗口句柄

        Returns:
            numpy.ndarray: 截图数据
        """
        handle=self.handle
        # 获取窗口客户区的大小
        r = RECT()
        self.GetClientRect(handle, ctypes.byref(r))
        width, height = r.right, r.bottom
        # 开始截图
        dc = self.GetDC(handle)
        cdc = self.CreateCompatibleDC(dc)
        bitmap = self.CreateCompatibleBitmap(dc, width, height)
        self.SelectObject(cdc, bitmap)
        self.BitBlt(cdc, 0, 0, width, height, dc, 0, 0, self.SRCCOPY)
        # 截图是BGRA排列，因此总元素个数需要乘以4
        total_bytes = width*height*4
        buffer = bytearray(total_bytes)
        byte_array = ctypes.c_ubyte*total_bytes
        self.GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
        self.DeleteObject(bitmap)
        self.DeleteObject(cdc)
        self.ReleaseDC(handle, dc)
        # 返回截图数据为numpy.ndarray
        return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)

    def match_img(self,img_name:str,is_show_res:bool = False):
        image = self.capture()        
        # 转为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        # 读取图片，并保留Alpha通道
        template = cv2.imread('imgs/'+img_name, cv2.IMREAD_UNCHANGED)
        # 取出Alpha通道
        alpha = template[:,:,3]
        template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
        # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
        result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED, mask=alpha)
        # 获取结果中最大值和最小值以及他们的坐标
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        h, w = template.shape[:2]
        bottom_right = top_left[0] + w, top_left[1] + h
        # 在窗口截图中匹配位置画红色方框
        if is_show_res:
            cv2.rectangle(image, top_left, bottom_right, (0,0,255), 2)
            cv2.imshow('Match Template', image)
            cv2.waitKey()
        matching_rate = max_val
        return matching_rate, top_left, bottom_right
    
    def color_SD(self,x_col,target_col):#standard deviation
        ret=0
        for i in range(min(len(x_col),len(target_col))):
            t=abs(x_col[i]-target_col[i])
            math.pow(t,2)
            ret+=t
        return math.sqrt(ret/min(len(x_col),len(target_col)))
    
    def delay(self, x, randtime=True, isprint=True):
        a=random.randint(-10,10)
        if randtime:
            a=a*x*0.02
            if  x>0.2 and isprint:
                print('delay: ',x,'rand: ',x+a)
            time.sleep(x+a)
        else:
            if  x>0.2 and isprint:
                print('delay: ',x)
            time.sleep(x)
    
    def get_mouse_point(self):
        p = win32api.GetCursorPos()
        #print(p[0],p[1])
        #  GetWindowRect 获得整个窗口的范围矩形，窗口的边框、标题栏、滚动条及菜单等都在这个矩形内 
        x,y,w,h = win32gui.GetWindowRect(self.handle)
        # 鼠标坐标减去指定窗口坐标为鼠标在窗口中的坐标值
        pos_x = p[0] - x
        pos_y = p[1] - y
        return(pos_x,pos_y)
    
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
        
    def leftClick(self, x=-1, y=-1):
        if x==-1:
            x,y=self.get_mouse_point()
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = y << 16 | x
            self.PostMessageW(self.handle, self.WM_LBUTTONDOWN, wparam, lparam)
            self.delay(0.06,randtime=False, isprint=False)
            self.PostMessageW(self.handle, self.WM_LBUTTONUP, wparam, lparam)
        print('left click')
    
    def leftDown(self, x=-1, y=-1):
        if x==-1:
            x,y=self.get_mouse_point()
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = y << 16 | x
            self.PostMessageW(self.handle, self.WM_LBUTTONDOWN, wparam, lparam)
            
        print('left down')
    
    def leftUp(self, x=-1, y=-1):
        if x==-1:
            x,y=self.get_mouse_point()
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = y << 16 | x
            self.PostMessageW(self.handle, self.WM_LBUTTONUP, wparam, lparam)
        print('left up')    
         
    def leftDoubleClick(self, dt=0.05):
        if not self.CONSOLE_ONLY:
            self.leftClick()
            self.delay(0.06,randtime=False, isprint=False)
            self.leftClick()
        print('leftDoubleClick')
        
    def rightClick(self, x=-1, y=-1):
        if x==-1:
            x,y=self.get_mouse_point()
        if not self.CONSOLE_ONLY:
            wparam = 0
            lparam = y << 16 | x
            self.PostMessageW(self.handle, self.WM_RBUTTONDOWN, wparam, lparam)
            self.delay(0.06,randtime=False, isprint=False)
            self.PostMessageW(self.handle, self.WM_RBUTTONUP, wparam, lparam)
            #pyautogui.rightClick()
        print('rightClick')
        self.delay(0.05)
        
    def keyDown(self, key):
        if not self.CONSOLE_ONLY:
            vk_code = self.get_virtual_keycode(key)
            scan_code = self.MapVirtualKeyW(vk_code, 0)
            # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
            wparam = vk_code
            lparam = (scan_code << 16) | 1
            self.PostMessageW(self.handle, self.WM_KEYDOWN, wparam, lparam)
        print("keyDown",key)
    
    def keyUp(self, key):
        if not self.CONSOLE_ONLY:
            vk_code = self.get_virtual_keycode(key)
            scan_code = self.MapVirtualKeyW(vk_code, 0)
            # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
            wparam = vk_code
            lparam = (scan_code << 16) | 0XC0000001
            self.PostMessageW(self.handle, self.WM_KEYUP, wparam, lparam)
        print("keyUp",key)
    
    def keyPress(self, key):
        if not self.CONSOLE_ONLY:
            #win32api.keybd_event(key)
            self.keyDown(key) 
            time.sleep(0.01)
            self.keyUp(key)
            self.delay(self.DEFAULT_DELAY_TIME)
        print("keyPress",key)

