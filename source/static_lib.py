import numpy as np
from util import *

global W_KEYDOWN, cvAutoTrackerLoop
W_KEYDOWN = False
cvAutoTrackerLoop = None
if config_json["capture_mode"] == "compatibility":
    import d3dshot
    d3d_capture = d3dshot.create(capture_output="numpy")
else:
    d3d_capture = None
def get_handle():
    if not config_json["cloud_genshin"]:
        handle = ctypes.windll.user32.FindWindowW(None, 'Genshin Impact')
        if handle != 0:
            return handle
        handle = ctypes.windll.user32.FindWindowW(None, '原神')
        if handle != 0:
            return handle
        
    else:
        handle = ctypes.windll.user32.FindWindowW("Qt5152QWindowIcon", '云·原神')
        if handle != 0:
            return 331454

def static_lib_init():
    global W_KEYDOWN, cvAutoTrackerLoop
    logger.debug("import cvAutoTrack")
    import cvAutoTrack
    cvAutoTrackerLoop = cvAutoTrack.AutoTrackerLoop()
    cvAutoTrackerLoop.setDaemon(True)
    cvAutoTrackerLoop.start()
    time.sleep(1)

def while_until_no_excessive_error(stop_func):
    logger.info(_("等待cvautotrack获取坐标"))
    cvAutoTrackerLoop.start_sleep_timer.reset()
    while cvAutoTrackerLoop.is_in_excessive_error():
        if stop_func():
            return 0
        time.sleep(1)

static_lib_init()


if __name__ == '__main__':
    import cv2
    while_until_no_excessive_error()
