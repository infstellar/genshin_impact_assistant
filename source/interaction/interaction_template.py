import string
from common import vkcode
import ctypes
VkKeyScanA = ctypes.windll.user32.VkKeyScanA

class InteractionTemplate():
    def __init__(self):
        pass
    
    def left_click(self):
        pass
    
    def left_down(self):
        pass
    
    def left_up(self):
        pass
    
    def left_double_click(self):
        pass
    
    def right_click(self):
        pass
    
    def middle_click(self):
        pass
    
    def key_down(self, key):
        pass
    
    def key_up(self, key):
        pass
    
    def key_press(self, key):
        pass
    
    def move_to(self, x: int, y: int, relative=False, isBorderlessWindow=False):
        pass
    
    def drag(self, origin_xy:list, targe_xy:list):
        pass
    
    def get_virtual_keycode(self, key: str):
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
            if key == "space":
                key = 'spacebar'
            return vkcode.VK_CODE[key]