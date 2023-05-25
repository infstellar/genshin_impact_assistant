import threading
from source.util import *
from source.common import timer_module
import numpy as np
from source.common import static_lib
from source.util import np
import pyautogui



class Capture():
    def __init__(self):
        self.capture_cache = np.zeros_like((1080,1920,3), dtype="uint8")
        self.max_fps = 180
        self.fps_timer = timer_module.Timer(diff_start_time=1)
        self.capture_cache_lock = threading.Lock()
        self.capture_times = 0
        self.cap_per_sec = timer_module.CyclicCounter(limit=3).start()
        self.last_cap_times = 0

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
        if DEBUG_MODE:
            r = self.cap_per_sec.count_times()
            if r:
                if r != self.last_cap_times:
                    logger.trace(f"capps: {r/3}")
                    self.last_cap_times = r
                elif r >= 10*3:
                    logger.trace(f"capps: {r/3}")
                elif r >= 20*3:
                    logger.debug(f"capps: {r/3}")
                elif r >= 40*3:
                    logger.info(f"capps: {r/3}")
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
                        t2t(" waiting 2 sec.")+'\n'+
                        t2t("请确认原神窗口没有最小化，原神启动器关闭，原神分辨率为1080p"))
                    time.sleep(2)
                else:
                    break
            self.capture_cache_lock.release()
            # print(time.time()-testt)
        else:
            pass
    
from ctypes.wintypes import RECT
import win32print, win32api

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
    

    def __init__(self):
        super().__init__()
        self.max_fps = 30
        self.monitor_num = 1
        self.monitor_id = 0
        self.scale_factor = self._get_screen_scale_factor()
        
    def _check_shape(self, img:np.ndarray):
        if img.shape == (1080,1920,4):
            return True
        else:
            static_lib.search_handle()
            logger.info(t2t("research handle: ")+str(static_lib.HANDLE))
            if self.monitor_num>1:
                if self.monitor_id==(self.monitor_num-1):
                    self.monitor_id=0
                else:
                    self.monitor_id+=1
                logger.info(t2t("research monitor: ")+str(self.monitor_id))
            return False
    
    def _get_screen_scale_factor(self):
        monitors = win32api.EnumDisplayMonitors()
        self.monitor_num = len(monitors)
        monitor = monitors[self.monitor_id][0]
        if self.monitor_num>1:
            logger.info(t2t("multiple monitor detected: ")+str(self.monitor_num))
        # Get a pointer to a DEVICE_SCALE_FACTOR value
        scale_factor = ctypes.c_int()

        # Call the GetScaleFactorForMonitor function with the monitor handle and scale factor pointer
        ctypes.windll.shcore.GetScaleFactorForMonitor(ctypes.c_int(monitor), ctypes.byref(scale_factor))

        # Print the scale factor value
        return float(scale_factor.value/100)
    
    def _get_capture(self):
        r = RECT()
        self.GetClientRect(static_lib.HANDLE, ctypes.byref(r))
        width, height = r.right, r.bottom
        # left, top, right, bottom = win32gui.GetWindowRect(static_lib.HANDLE)
        # 获取桌面缩放比例
        #desktop_dc = self.GetDC(0)
        #scale_x = self.GetDeviceCaps(desktop_dc, 88)
        #scale_y = self.GetDeviceCaps(desktop_dc, 90)
        height=int(height)
        if height in list(map(int, [1080/0.75, 1080/1.25, 1080/1.5, 1080/1.75, 1080/2, 1080/2.25, 1080/2.5, 1080/2.75, 1080/3])):
            logger.warning_once(t2t("You seem to have monitor scaling set? It is automatically recognized and this does not affect usage."))
            width = 1920
            height = 1080
            # 计算实际截屏区域大小
            # width = int(int(width)*self.scale_factor)
            # height = int(int(height)*self.scale_factor)
        
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
    
class CloudCapture(Capture):
    def __init__(self):
        super().__init__()
    
    def _get_capture(self) -> np.ndarray:
        
        wx, wy, w, h = win32gui.GetWindowRect(static_lib.HANDLE)
        pyautogui.screenshot(region=[0,0,100,100])
    
    
class EmulatorCapture(Capture):
    def __init__(self):
        super().__init__()
    
    def _get_capture(self):
        pass

class CustomCapture(Capture):
    def __init__(self):
        super().__init__()
        self.curr_cap = np.zeros_like((1080,1920,3), dtype="uint8")
    
    def _check_shape(self, img):
        return True

    def _get_capture(self) -> np.ndarray:
        return self.curr_cap

    def set_cap(self, img):
        self.curr_cap = img

if __name__ == '__main__':
    wc = WindowsCapture()
    # wc._get_screen_scale_factor()
    while 1:
        cv2.imshow("capture test", wc.capture())
        cv2.waitKey(10)
        # time.sleep(0.01)