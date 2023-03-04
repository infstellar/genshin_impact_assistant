import threading
from source.util import *
from source.common import timer_module
import numpy as np
from source.common import static_lib


class Capture():
    def __init__(self, ignore_shape = False):
        self.capture_cache = np.zeros_like((1080,1920,3), dtype="uint8")
        self.max_fps = 180
        self.fps_timer = timer_module.Timer()
        self.capture_cache_lock = threading.Lock()
        self.capture_times = 0
        self.ignore_shape = ignore_shape

    def _get_capture(self) -> np.ndarray:
        """
        需要根据不同设备实现该函数。
        """
    
    def _check_shape(self, img:np.ndarray):
        if img is None:
            return False
        if img.shape == [1080,1920,4] or img.shape == [768,1024,3]:
            return True
        else:
            return False
        

    def capture(self, is_next_img = False) -> np.ndarray:
        """
        is_next_img: 强制截取下一张图片
        """
        self._capture(is_next_img)
        self.capture_cache_lock.acquire()
        cp = self.capture_cache.copy()
        self.capture_cache_lock.release()
        return cp
    
    def _capture(self, is_next_img) -> None:
        if (self.fps_timer.get_diff_time() >= 1/self.max_fps) or is_next_img:
            # testt=time.time()
            self.fps_timer.reset()
            self.capture_cache_lock.acquire()
            self.capture_times+=1
            self.capture_cache = self._get_capture()
            while 1:
                self.capture_cache = self._get_capture()
                if not self._check_shape(self.capture_cache):
                    logger.warning(
                        t2t("Fail to get capture: ")+
                        f"shape: {self.capture_cache.shape},"+
                        t2t(" waiting 2 sec."))
                    time.sleep(2)
                else:
                    break
            self.capture_cache_lock.release()
            # print(time.time()-testt)
        else:
            pass
    
from ctypes.wintypes import RECT
import win32print

class WindowsCapture(Capture):
    """
    支持Windows10, Windows11的截图。
    """
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
    GetDeviceCaps = win32print.GetDeviceCaps
    

    def __init__(self, ignore_shape=False):
        """_summary_

        Args:
            ignore_shape (bool, optional): 忽略截图大小检测. Defaults to False. 如果电脑设置了不同的缩放比例，必须设置该值为True。
        """
        static_lib.HANDLE = static_lib.HANDLE
        super().__init__(ignore_shape=ignore_shape)
        self.max_fps = 30
        
    
    def _check_shape(self, img:np.ndarray):
        if self.ignore_shape:
            if self.capture_cache[:,:,:3].max() <= 0:
                logger.warning(t2t("警告：你启用了设置\'忽略截图大小检测\'，但截图黑屏。"))
                logger.warning(t2t("截图黑屏，请检查窗口。"))
                static_lib.search_handle()
                return False
        if img.shape == (1080,1920,4):
            return True
        else:
            logger.info(t2t("research handle"))
            static_lib.search_handle()
            return False
    
    def _get_capture(self):
        r = RECT()
        self.GetClientRect(static_lib.HANDLE, ctypes.byref(r))
        width, height = r.right, r.bottom
        # left, top, right, bottom = win32gui.GetWindowRect(static_lib.HANDLE)
        # 获取桌面缩放比例
        #desktop_dc = self.GetDC(0)
        #scale_x = self.GetDeviceCaps(desktop_dc, 88)
        #scale_y = self.GetDeviceCaps(desktop_dc, 90)

        # 计算实际截屏区域大小
        # width = (right - left)# * scale_x // 100
        # height = (bottom - top)# * scale_y // 100
        if self.ignore_shape:
            width = 1920
            height = 1080
        # 开始截图
        dc = self.GetDC(static_lib.HANDLE)
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
        self.ReleaseDC(static_lib.HANDLE, dc)
        # 返回截图数据为numpy.ndarray
        ret = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
        return ret
    
class EmulatorCapture(Capture):
    def __init__(self):
        super().__init__()
    
    def _get_capture(self):
        pass
    
if __name__ == '__main__':
    wc = WindowsCapture(ignore_shape=False)
    while 1:
        cv2.imshow("capture test", wc.capture())
        cv2.waitKey(10)
        # time.sleep(0.01)