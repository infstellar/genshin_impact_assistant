from ctypes import *
from unit import *

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
        self.__lib.GetTransform.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float)]
        self.__lib.GetTransform.restype = c_bool

        # bool GetPosition(double & x, double & y)
        self.__lib.GetPosition.argtypes = [POINTER(c_double), POINTER(c_double)]
        self.__lib.GetPosition.restype = c_bool

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

    def init(self):
        return self.__lib.init()

    def verison(self):
        return self.__lib.verison()
    
    def uninit(self):
        return self.__lib.uninit()

    def get_last_error(self):
        return self.__lib.GetLastErr()

    def set_handle(self, hwnd: int):
        return self.__lib.SetHandle(hwnd)

    def get_transform(self):
        x, y, a = c_double(0), c_double(0), c_double(0)
        ret = self.__lib.GetTransform(x, y, a)
        return ret, x.value, y.value, a.value

    def get_position(self):
        x, y = c_double(0), c_double(0)
        ret = self.__lib.GetPosition(x, y)
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
    
    def SetWorldCenter(self,x,y):
        ret = self.__lib.SetWorldCenter(c_double(x),c_double(y))
        return ret
    
    def translate_posi(self, x, y):
        return  -(x-793.9)/2 , -(y-(-1237.8))/2
    
cvAutoTracker = AutoTracker('source\\cvAutoTrack_6.3\\CVAUTOTRACK.dll')
cvAutoTracker.init()
logger.info('1) err' + str(cvAutoTracker.get_last_error()))
# logger.info(cvAutoTracker.verison())

# 以下是对被封装的类的简单演示。
# 使用命令行 `python ./main.py` 直接运行本文件即可。
if __name__ == '__main__':
    # 等待五秒钟以便切换到原神窗口：
    # sleep(5)

    # print(cvAutoTracker.SetWorldCenter(793.9, -1237.8))
    
    # 加载同一目录下的DLL：
    # tracker = AutoTracker('source\\CVAUTOTRACK.dll')

    # 初始化并打印错误：
    # tracker.init()
    # print('1) err', tracker.get_last_error(), '\n')

    # 获取当前人物所在位置以及角度（箭头朝向）并打印错误：
    print(cvAutoTracker.get_position())
    print('2) err', cvAutoTracker.get_position(), '\n')

    # 获取UID并打印错误：
    print(cvAutoTracker.get_uid())
    print('3) err', cvAutoTracker.get_last_error(), '\n')

    print(cvAutoTracker.get_direction())
    print('4) err', cvAutoTracker.get_last_error(), '\n')

    print(cvAutoTracker.get_rotation())
    print('5) err', cvAutoTracker.get_last_error(), '\n')

    while 1:
        # print(cvAutoTracker.get_rotation())
        
        ret = cvAutoTracker.get_position()
        # posi = cvAutoTracker.translate_posi(ret[1],ret[2])
        print(ret)
        time.sleep(0.2)
    
    # 卸载相关内存：（这一步不是必须的，但还是建议手动调用）
    cvAutoTracker.uninit()

# 0 263.25 0 -> 793.9 -1237.8

# 10 263.8 10 -> 773 -1258

# -10 -10 -> 811 -1217

# 740 -1012
# 684 -1518
# 3.3 3.4