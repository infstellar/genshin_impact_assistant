import threading
from source.util import *
from source.common import timer_module
import numpy as np
from source.funclib import static_lib

class Capture():
    def __init__(self):
        self.capture_cache = np.zeros_like((1080,1920,3), dtype="uint8")
        self.max_fps = 30
        self.fps_timer = timer_module.Timer()
        self.capture_cache_lock = threading.Lock()

    def _get_capture(self) -> np.ndarray:
        """
        需要根据不同设备实现该函数。
        """
        

    def capture(self) -> np.ndarray:
        self.capture_cache_lock.acquire()
        cp = self.capture_cache.copy()
        self.capture_cache_lock.release()
        return cp
    
    def _capture(self) -> None:
        if self.fps_timer.get_diff_time() >= 1/self.max_fps:
            self.capture_cache_lock.acquire()
            self.capture_cache = self._get_capture()
            self.capture_cache_lock.release()
    
from ctypes.wintypes import RECT

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
    HANDLE = static_lib.HANDLE

    def __init__(self):
        super().__init__()
    
    def _get_capture(self):
        r = RECT()
        self.GetClientRect(self.HANDLE, ctypes.byref(r))
        width, height = r.right, r.bottom
        # 开始截图
        dc = self.GetDC(self.HANDLE)
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
        self.ReleaseDC(self.HANDLE, dc)
        # 返回截图数据为numpy.ndarray
        ret = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
        return ret
    
class EmulatorCapture(Capture):
    def __init__(self):
        super().__init__()
    
    def _get_capture(self):
        pass