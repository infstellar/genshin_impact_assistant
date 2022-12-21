import time
from ctypes import *
from util import *
import timer_module
from base_threading import BaseThreading


class AutoTracker:
    def __init__(self, dll_path: str):
        self.__lib = CDLL(dll_path)

        # bool init();
        self.__lib.init.restype = c_bool

        # bool uninit();
        self.__lib.uninit.restype = c_bool

        # bool SetHandle(long long int handle);
        self.__lib.SetHandle.argtypes = [c_longlong]
        self.__lib.SetHandle.restype = c_bool

        # bool GetTransform(float &x, float &y, float &a)
        self.__lib.GetTransformOfMap.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_int)]
        self.__lib.GetTransformOfMap.restype = c_bool

        # bool GetPosition(double & x, double & y)
        self.__lib.GetPositionOfMap.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int)]
        self.__lib.GetPositionOfMap.restype = c_bool

        # bool GetDirection(double &a);
        self.__lib.GetDirection.argtypes = [POINTER(c_double)]
        self.__lib.GetDirection.restype = c_bool

        # bool GetUID(int &uid);
        self.__lib.GetUID.argtypes = [POINTER(c_int)]
        self.__lib.GetUID.restype = c_bool

        # bool GetRotation(double &a);
        self.__lib.GetRotation.argtypes = [POINTER(c_double)]
        self.__lib.GetRotation.restype = c_bool

        self.__lib.SetWorldCenter.argtypes = [POINTER(c_double), POINTER(c_double)]
        self.__lib.SetWorldCenter.restype = c_bool

        self.__lib.verison.restype = c_char
        
        # self.__lib.SetDisableFileLog.restype = c_bool

    def init(self):
        return self.__lib.init()

    def verison(self):
        return self.__lib.verison()

    def disable_log(self):
        # return self.__lib.SetDisableFileLog()
        pass
    
    def uninit(self):
        return self.__lib.uninit()

    def get_last_error(self):
        return self.__lib.GetLastErr()

    def set_handle(self, hwnd: int):
        return self.__lib.SetHandle(hwnd)

    def get_transform(self):
        x, y, a, b = c_double(0), c_double(0), c_double(0), c_int(0)
        ret = self.__lib.GetTransformOfMap(x, y, a, b)
        return ret, x.value, y.value, a.value

    def get_position(self):
        x, y, b = c_double(0), c_double(0), c_int(0)
        ret = self.__lib.GetPositionOfMap(x, y, b)
        # retx,rety=self.translate_posi(x.value, y.value)
        return ret, x.value, y.value

    def get_direction(self):
        a = c_double(0)
        ret = self.__lib.GetDirection(a)
        return ret, a.value

    def get_uid(self):
        uid = c_int(0)
        ret = self.__lib.GetUID(uid)
        return ret, uid.value

    def get_rotation(self):
        a = c_double(0)
        ret = self.__lib.GetRotation(a)
        return ret, a.value

    def set_world_center(self, x, y):
        ret = self.__lib.SetWorldCenter(c_double(x), c_double(y))
        return ret

    @staticmethod
    def translate_posi(x, y):
        return -(x - 793.9) / 2, -(y - (-1237.8)) / 2

def del_log():
    logger.debug(_("cleaning cvautotrack files"))
    for root, dirs, files in os.walk(os.path.join(root_path)):
        for f in files:
            if f == "autoTrack.log":
                os.remove(os.path.join(root_path, "autoTrack.log"))
                logger.debug(_("autoTrack.log 1 cleaned"))
    for root, dirs, files in os.walk(os.path.join(root_path, "source")):
        for f in files:
            if f == "autoTrack.log":
                os.remove(os.path.join(root_path, "source", "autoTrack.log"))
                logger.debug(_("autoTrack.log 2 cleaned"))
    for root, dirs, files in os.walk(os.path.join(root_path, "source", "webio")):
        for f in files:
            if f == "autoTrack.log":
                os.remove(os.path.join(root_path, "source", "webio", "autoTrack.log"))
                logger.debug(_("autoTrack.log 3 cleaned"))
del_log()
cvAutoTracker = AutoTracker(os.path.join(root_path, 'source\\cvAutoTrack_7.2.3\\CVAUTOTRACK.dll'))
cvAutoTracker.init()
logger.info(_("cvAutoTrack DLL has been loaded."))
logger.info('1) err' + str(cvAutoTracker.get_last_error()))


class AutoTrackerLoop(BaseThreading):
    def __init__(self):
        super().__init__()
        # logger.debug(f"cvautotrack log: {cvAutoTracker.disable_log()}")
        # scene_manager.switchto_mainwin(max_time=5)
        time.sleep(2)
        self.position = cvAutoTracker.get_position()
        self.last_position = self.position
        self.rotation = cvAutoTracker.get_rotation()
        self.in_excessive_error = False
        self.start_sleep_timer = timer_module.Timer(diff_start_time=61)
        

    def run(self):
        ct = 0
        time.sleep(0.1)
        while 1:
            time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True

            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            
            if self.start_sleep_timer.get_diff_time() >= 60:
                if self.start_sleep_timer.get_diff_time() <= 62:
                    logger.debug("cvAutoTrackerLoop switch to sleep mode.")
                time.sleep(0.8)
                continue

            self.rotation = cvAutoTracker.get_rotation()
            self.position = cvAutoTracker.get_position()
            if not self.position[0]:
                print("坐标获取失败")
                self.position = (False, 0, 0)
                self.in_excessive_error = True
                time.sleep(0.5)
                continue
            if ct >= 30:
                self.last_position = self.position
                self.in_excessive_error = False
                logger.debug("位置已重置")
                ct = 0
            if euclidean_distance(self.position[1:], self.last_position[1:]) >= 50:
                # print("误差过大")
                self.in_excessive_error = True
                ct += 1
            else:
                self.last_position = self.position
                self.in_excessive_error = False
                ct = 0
            # print(self.last_position)

    def get_position(self):
        self.start_sleep_timer.reset()
        return self.position

    def get_rotation(self):
        self.start_sleep_timer.reset()
        return self.rotation

    def is_in_excessive_error(self):
        self.start_sleep_timer.reset()
        return self.in_excessive_error
    
# logger.info(cvAutoTracker.verison())

# 以下是对被封装的类的简单演示。
# 使用命令行 `python ./main.py` 直接运行本文件即可。
if __name__ == '__main__':
    cal=AutoTrackerLoop()
    a = cal.get_position()
    print()
    # # 等待五秒钟以便切换到原神窗口：
    # # sleep(5)
    #
    # # print(cvAutoTracker.SetWorldCenter(793.9, -1237.8))
    #
    # # 加载同一目录下的DLL：
    # # tracker = AutoTracker('source\\CVAUTOTRACK.dll')
    #
    # # 初始化并打印错误：
    # # tracker.init()
    # # print('1) err', tracker.get_last_error(), '\n')
    #
    # # 获取当前人物所在位置以及角度（箭头朝向）并打印错误：
    # print(cvAutoTrackerLoop.get_position())
    # print('2) err', cvAutoTrackerLoop.get_position(), '\n')
    #
    # # 获取UID并打印错误：
    # # print(cvAutoTrackerLoop.get_uid())
    # # print('3) err', cvAutoTrackerLoop.get_last_error(), '\n')
    #
    # # print(cvAutoTrackerLoop.get_direction())
    # # print('4) err', cvAutoTrackerLoop.get_last_error(), '\n')
    #
    # print(cvAutoTrackerLoop.get_rotation())
    # # print('5) err', cvAutoTrackerLoop.get_last_error(), '\n')
    #
    # while 1:
    #     # print(cvAutoTracker.get_rotation())
    #
    #     # ret = cvAutoTracker.get_position()
    #     # posi = cvAutoTracker.translate_posi(ret[1],ret[2])
    #     print(cvAutoTrackerLoop.get_position())
    #     time.sleep(0.2)
    #
    # # 卸载相关内存：（这一步不是必须的，但还是建议手动调用）
    # cvAutoTracker.uninit()
    pass

# 0 263.25 0 -> 793.9 -1237.8

# 10 263.8 10 -> 773 -1258

# -10 -10 -> 811 -1217

# 740 -1012
# 684 -1518
# 3.3 3.4
