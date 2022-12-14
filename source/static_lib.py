import threading
from ctypes.wintypes import RECT

import numpy as np

from timer_module import Timer
from util import *
import cvAutoTrack



def get_handle():
    handle = ctypes.windll.user32.FindWindowW(None, '原神')
    if handle != 0:
        return handle
    handle = ctypes.windll.user32.FindWindowW(None, 'Genshin Impact')
    if handle != 0:
        return handle


class ScreenCapture:
    def __init__(self):
        logger.debug('static_lib_created')

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
        self.PostMessageW = ctypes.windll.user32.PostMessageW
        self.MapVirtualKeyW = ctypes.windll.user32.MapVirtualKeyW
        self.VkKeyScanA = ctypes.windll.user32.VkKeyScanA
        self.handle = get_handle()

        self.fps = 1 / 30
        self.cap_timer = Timer()
        self.wrtting_flag = False
        self.last_cap1 = self.capture_handle()
        self.last_cap2 = self.capture_handle()
        self.ret_cap_id = 1
        self.caping_flag = False
        self.caping = self.capture_handle()
        self.cap_timer.reset()

    def capture_handle(self):
        # 获取窗口客户区的大小
        handle = self.handle
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
        total_bytes = width * height * 4
        buffer = bytearray(total_bytes)
        byte_array = ctypes.c_ubyte * total_bytes
        self.GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
        self.DeleteObject(bitmap)
        self.DeleteObject(cdc)
        self.ReleaseDC(handle, dc)
        # 返回截图数据为numpy.ndarray
        ret = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
        return ret

    def get_capture(self):
        # 摆烂了
        return self.capture_handle().copy()
        
        # if self.cap_timer.get_diff_time() >= self.fps:
        #     self.cap_timer.reset()
        #     # print('recap', self.cap_timer.getDiffTime())
        #     if self.ret_cap_id == 1:
        #         self.last_cap2 = self.capture_handle().copy()
        #         self.ret_cap_id = 2
        #     else:
        #         self.last_cap1 = self.capture_handle().copy()
        #         self.ret_cap_id = 1
        #     print(self.cap_timer.get_diff_time())    
            
        # else:
        #     # print('recap', self.cap_timer.getDiffTime())
        #     # self.last_cap = self.capture_handle()
        #     # self.cap_timer.reset()
        #     print('returncap')
        #     pass
        # # print(self.last_cap.shape)
        # # print(self.ret_cap_id)
        # if self.ret_cap_id == 1:
        #     return self.last_cap1
        # else:
        #     return self.last_cap2


SCREENCAPTURE = ScreenCapture()
W_KEYDOWN = False

cvAutoTrackerLoop = cvAutoTrack.AutoTrackerLoop()
cvAutoTrackerLoop.setDaemon(True)
cvAutoTrackerLoop.start()
time.sleep(1)

def while_until_no_excessive_error(stop_func):
    while cvAutoTrackerLoop.is_in_excessive_error():
        if stop_func():
            return 0
        time.sleep(1)

class TestTest(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while 1:
            SCREENCAPTURE.get_capture()


if __name__ == '__main__':
    import cv2
    while_until_no_excessive_error()
    while 1:
        cv2.imshow("123",SCREENCAPTURE.get_capture())
        cv2.waitKey(100)
