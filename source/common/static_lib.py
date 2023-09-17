from source.util import *

global W_KEYDOWN, HANDLE
W_KEYDOWN = False

if GIAconfig.General_CaptureMode == "compatibility":
    d3d_capture = None
else:
    d3d_capture = None
def get_handle():
    """获得句柄

    Returns:
        _type_: _description_
    """
    if not GIAconfig.General_CloudGenshin:
        handle = ctypes.windll.user32.FindWindowW(None, 'Genshin Impact')
        if handle != 0:
            return handle
        handle = ctypes.windll.user32.FindWindowW(None, '原神')
        if handle != 0:
            return handle
    else:
        handle = ctypes.windll.user32.FindWindowW("Qt5152QWindowIcon", '云·原神')
        if handle != 0:
            return handle
    logger.warning(t2t("CANNOT FIND HANDLE"))

HANDLE = get_handle()
class handle_obj():
    def __init__(self) -> None:
        self.handle = get_handle()
    def get_handle(self):
        return self.handle
    def refresh_handle(self):
        self.handle = get_handle()
HANDLEOBJ = handle_obj()
def search_handle():
    global HANDLE
    HANDLE = get_handle()

if __name__ == '__main__':
    pass
