# -*- coding: UTF-8 -*-
"""
@Project ：pydmdll
@File ：damo.py
@Author ：Gao yongxian
@Date ：2021/10/23 12:47
@contact: g1695698547@163.com
"""
import os
import struct
import time
import ctypes


from win32com.client import Dispatch



class DM:
    """
    pydmdll是一个实现大漠插件免费功能的Python包，无需手动注册dll，直接导入包使用。
    可以模拟驱动级的鼠标键盘输入。不支持后台的鼠标键盘，以及所有付费功能都不支持。

    """

    def __init__(self, key, addition_key, dll_path) -> None:
        """
        初始化并且完成注册

        Args:
            dll_path: dm.dll路径。必须是全路径
        """

        if struct.calcsize("P") * 8 == 64:
            print("dm.dll不支持64位Python")
            return None
        else:
            self.dll_prefix = "dm.dll"
            
        self.dll_path = dll_path
        # if dll_path is None:
        #     self.dll_path = os.path.join(os.path.dirname(__file__.replace('/', '\\')), self.dll_prefix)
        self.cmd_dll = 'regsvr32 \"' + self.dll_path + '\" /s'
        print(self.cmd_dll)

        # 判断是否已经注册注册成功返回版本信息
        if self.__is_reg:
            print("成功注册：" + 'VER:', self.ver(), ',ID:', self.GetID(), ',PATH:',
                  os.path.join(self.GetBasePath(), self.dll_prefix))
        else:
            self.__reg_as_admin()
            if self.__is_reg:
                print("成功注册：" + 'VER:', self.ver(), ',ID:', self.GetID(), ',PATH:',
                      os.path.join(self.GetBasePath(), self.dll_prefix))
            else:
                print("注册失败：" + time.strftime('%Y-%m-%d-%H:%M:%S',
                                              time.localtime(time.time())) + self.dll_path + "：注册失败")

        r = self.dm.Reg(key, addition_key)
        print("注册结果：", r)
        
    def __unreg_as_admin(self) -> None:
        """
        删除注册的dll。

        Returns:
            无返回值。
        """
        self.cmd_un_dll = 'regsvr32 /u /s \"' + os.path.join(self.GetBasePath(), self.dll_prefix) + '\"'
        if self.__is_admin:
            os.system(self.cmd_un_dll)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", "/C %s" % self.cmd_un_dll, None, 1)
            time.sleep(3)
            print("删除注册：" + 'VER:', self.ver(), ',ID:', self.GetID(), ',PATH:',
                  os.path.join(self.GetBasePath(), self.dll_prefix))

    def __reg_as_admin(self) -> None:
        """
        注册dll。

        Returns:
            无返回值。
        """
        if self.__is_admin:
            os.system(self.cmd_dll)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", "/C %s" % self.cmd_dll, None, 1)
            time.sleep(3)

    @property
    def __is_reg(self) -> int:
        """
        判断dll是否调用成功。

        Returns:
            返回int数据类型，1代表调用成功，0代表调用失败。
        """
        try:
            self.dm = Dispatch('dm.dmsoft')
            return 1
        except Exception as e:
            print(e)
            print(
                "调用失败：" + time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())) + self.dll_path + "：调用失败")
            return 0

    @property
    def __is_admin(self) -> bool:
        """
        判断是否具有管理员权限。

        Returns:
            返回bool类型。
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def __repr__(self) -> str:
        """
        自我描述信息。

        Returns:
            自我描述信息。
        """
        ret = 'VER:' + self.ver() + ',ID:' + str(self.GetID()) + ',PATH:' + os.path.join(
            self.GetBasePath() + self.dll_prefix)
        return ret

    """----------------------------------------取消注册------------------------------------------------"""

    def Un_reg(self) -> None:
        """
        取消已经注册的dll

        Returns:
            无返回值
        """
        self.__unreg_as_admin()

    """----------------------------------------窗口设置------------------------------------------------"""
    def BindWindow(self,hwnd,display,mouse,keypad,mode):
        return self.dm.BindWindow(hwnd, display, mouse, keypad, mode)
    
    def EnableBind(self, enable):
        return self.dm.EnableBind(enable)
    
    def UnBindWindow(self):
        print("unbind: ", self.dm.UnBindWindow())
    
    
    def ClientToScreen(self, hwnd: int) -> tuple:
        """
        把窗口坐标转换为屏幕坐标

        Args:
            hwnd: 指定的窗口句柄.你可以使用GetWindow，FindWindow等返回窗口句柄的方法获取句柄

        Returns:
            返回元组数据类型,（窗口句柄，X坐标，Y坐标）.
        """
        return self.dm.ClientToScreen(hwnd, 1, 1)

    def EnumWindow(self, parent: int, title: str, class_name: str, _filter: int) -> str:
        """
        根据父窗口,枚举系统中符合条件的子窗口,可以枚举到按键自带的无法枚举到的窗口

        Args:
            parent: 获得的窗口句柄是该窗口的子窗口的窗口句柄,取0时为获得桌面句柄
            title: 窗口标题. 此参数是模糊匹配.
            class_name: 窗口类名. 此参数是模糊匹配.
            _filter: 取值定义如下
                        1 : 匹配窗口标题,参数title有效
                        2 : 匹配窗口类名,参数class_name有效.
                        4 : 只匹配指定父窗口的第一层孩子窗口
                        8 : 匹配所有者窗口为0的窗口,即顶级窗口
                        16 : 匹配可见的窗口
                        这些值可以相加,比如4+8+16就是类似于任务管理器中的窗口列表

        Returns:
            返回str数据类型，"hwnd1,hwnd2,hwnd3"，你可以字符串分割变成列表

        示例:

                hwnds = dm.EnumWindow(0,"QQ三国","",1+4+8+16)
                这句是获取到所有标题栏中有QQ三国这个字符串的窗口句柄集合
                hwnds = split(hwnds,",")
                转换为数组后,就可以处理了
                这里注意,hwnds数组里的是字符串,要用于使用,比如BindWindow时,还得强制类型转换,比如int(hwnds(0))
        """
        return self.dm.EnumWindow(parent, title, class_name, _filter)

    def EnumWindowByProcess(self, process_name: str, title: str, class_name: str, _filter: int) -> str:
        """
        根据指定进程以及其它条件,枚举系统中符合条件的窗口,可以枚举到按键自带的无法枚举到的窗口

        Args:
            process_name:进程映像名.比如(svchost.exe). 此参数是精确匹配,但不区分大小写.
            title:窗口标题. 此参数是模糊匹配.
            class_name:窗口类名. 此参数是模糊匹配.
            _filter:取值定义如下  1 : 匹配窗口标题,参数title有效2 : 匹配窗口类名,参数class_name有效4 : 只匹配指定映像的所对应的第一个进程. 可能有很多同映像名的进程，只匹配第一个进程的.8 : 匹配所有者窗口为0的窗口,即顶级窗口16 : 匹配可见的窗口

        Returns:
            返回str数据类型，返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
        """
        return self.dm.EnumWindowByProcess(process_name, title, class_name, _filter)

    def FindWindow(self, class_name: str = '', title_name: str = '') -> int:
        """
        查找符合类名或者标题名的顶层可见窗

        Args:
            class_name: 窗口类名，如果为空，则匹配所有. 这里的匹配是模糊匹配.
            title_name: 窗口标题,如果为空，则匹配所有.这里的匹配是模糊匹配.

        Returns:
            整数型表示的窗口句柄，没找到返回0

        For example:

            hwnd = dm.FindWindow("","记事本")

        """
        return self.dm.FindWindow(class_name, title_name)

    def FindWindowEx(self, parent: int, _class: str, title: str) -> int:
        """
        查找符合类名或者标题名的顶层可见窗口,如果指定了parent,则在parent的第一层子窗口中查找.

        Args:
            parent:父窗口句柄，如果为空，则匹配所有顶层窗口
            _class:窗口类名，如果为空，则匹配所有. 这里的匹配是模糊匹配.
            title:窗口标题,如果为空，则匹配所有. 这里的匹配是模糊匹配.

        Returns:
            表示的窗口句柄，没找到返回0

        For example:

            hwnd = dm.FindWindowEx(0,"","记事本")

        """
        return self.dm.FindWindowEx(parent, _class, title)

    def GetClientRect(self, hwnd: int) -> tuple:
        """
        获取窗口客户区域在屏幕上的位置

        Args:
            hwnd:指定的窗口句柄

        Returns:
            (窗口句柄,窗口客户区左上角X坐标,窗口客户区左上角Y坐标,窗口客户区右下角X坐标,窗口客户区右下角Y坐标)
        """
        return self.dm.GetClientRect(hwnd, 1, 1, 1, 1)

    def GetClientSize(self, hwnd: int) -> tuple:
        """
        获取窗口客户区域的宽度和高度

        Args:
            hwnd:指定的窗口句柄

        Returns:
            (指定的窗口句柄,宽度,高度)
        """
        return self.dm.GetClientSize(hwnd, 1, 1)

    def GetForegroundFocus(self) -> int:
        """
        获取顶层活动窗口中具有输入焦点的窗口句柄

        Returns:
            返回整型表示的窗口句柄
        """
        return self.dm.GetForegroundFocus()

    def GetForegroundWindow(self) -> int:
        """
        获取顶层活动窗口,可以获取到按键自带插件无法获取到的句柄

        Returns:
            返回整型表示的窗口句柄
        """
        return self.dm.GetForegroundWindow()

    def GetMousePointWindow(self) -> int:
        """
        获取鼠标指向的窗口句柄,可以获取到按键自带的插件无法获取到的句柄

        Returns:
            返回整型表示的窗口句柄
        """
        return self.dm.GetMousePointWindow()

    def GetPointWindow(self, x: int, y: int) -> int:
        """
        获取给定坐标的窗口句柄,可以获取到按键自带的插件无法获取到的句柄

        Args:
            x:屏幕X坐标
            y:屏幕Y坐标

        Returns:
            返回整型表示的窗口句柄
        """
        return self.dm.GetPointWindow(x, y)

    def GetSpecialWindow(self, flag: int) -> int:
        """
        获取特殊窗口

        Args:
            flag:取值定义如下
                    0 : 获取桌面窗口
                    1 : 获取任务栏窗口

        Returns:
            以整型数表示的窗口句柄
        """
        return self.dm.GetSpecialWindow(flag)

    def GetWindow(self, hwnd: int, flag: int) -> int:
        """
        获取给定窗口相关的窗口句柄

        Args:
            hwnd:窗口句柄
            flag:取值定义如下
                    0 : 获取父窗口
                    1 : 获取第一个儿子窗口
                    2 : 获取First 窗口
                    3 : 获取Last窗口
                    4 : 获取下一个窗口
                    5 : 获取上一个窗口
                    6 : 获取拥有者窗口
                    7 : 获取顶层窗口

        Returns:
            返回整型表示的窗口句柄
        """
        return self.dm.GetWindow(hwnd, flag)

    def GetWindowClass(self, hwnd: int) -> str:
        """
        获取窗口的类名

        Args:
            hwnd:指定的窗口句柄

        Returns:
            窗口的类名
        """
        return self.dm.GetWindowClass(hwnd)

    def GetWindowProcessId(self, hwnd: int) -> int:
        """
        获取指定窗口所在的进程ID.

        Args:
            hwnd:窗口句柄

        Returns:
            返回整型表示的是进程ID
        """
        return self.dm.GetWindowClass(hwnd)

    def GetWindowProcessPath(self, hwnd: int) -> str:
        """
        获取指定窗口所在的进程的exe文件全路径.

        Args:
            hwnd:窗口句柄

        Returns:
            返回字符串表示的是exe全路径名
        """
        return self.dm.GetWindowProcessPath(hwnd)

    def GetWindowRect(self, hwnd: int) -> tuple:
        """
        获取窗口在屏幕上的位置

        Args:
            hwnd:指定的窗口句柄

        Returns:
            (指定的窗口句柄,窗口左上角X坐标,窗口左上角Y坐标 窗口右下角X坐标,窗口右下角Y坐标)
        """
        return self.dm.GetWindowRect(hwnd, 1, 1, 1, 1)

    def GetWindowState(self, hwnd: int, flag: int) -> int:
        """
        获取指定窗口的一些属性

        Args:
            hwnd: 指定的窗口句柄
            flag: 取值定义如下:
                    0 : 判断窗口是否存在
                    1 : 判断窗口是否处于激活
                    2 : 判断窗口是否可见
                    3 : 判断窗口是否最小化
                    4 : 判断窗口是否最大化
                    5 : 判断窗口是否置顶
                    6 : 判断窗口是否无响应

        Returns:
            0代表失败，1代表成功

        """

        return self.dm.GetWindowState(hwnd, flag)

    def GetWindowTitle(self, hwnd: int) -> str:
        """
        获取窗口的标题

        Args:
            hwnd:指定的窗口句柄

        Returns:
            窗口的标题
        """
        return self.dm.GetWindowTitle(hwnd)

    def MoveWindow(self, hwnd: int, x: int, y: int) -> int:
        """
        移动指定窗口到指定位置

        Args:
            hwnd:指定的窗口句柄
            x:X坐标
            y:Y坐标

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.MoveWindow(hwnd, x, y)

    def ScreenToClient(self, hwnd: int) -> tuple:
        """
        把屏幕坐标转换为窗口坐标

        Args:
            hwnd:指定的窗口句柄

        Returns:
            返回元组（指定的窗口句柄，屏幕X坐标，屏幕Y坐标）
        """
        return self.dm.ScreenToClient(hwnd, 1, 1)

    def SendPaste(self, hwnd: int) -> int:
        """
        向指定窗口发送粘贴命令. 把剪贴板的内容发送到目标窗口.

        Args:
            hwnd:指定的窗口句柄

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.SendPaste(hwnd)

    def SendString(self, hwnd: int, str: str) -> int:
        """
        向指定窗口发送文本数据

        Args:
            hwnd:指定的窗口句柄
            str:发送的文本数据

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.SendString(hwnd, str)

    def SendString2(self, hwnd: int, str: str) -> int:
        """
        向指定窗口发送文本数据

        Args:
            hwnd: 指定的窗口句柄
            str: 发送的文本数据

        Returns:
            0代表失败，1代表成功

        注: 此接口为老的SendString，如果新的SendString不能输入，可以尝试此接口.
        """
        return self.dm.SendString2(hwnd, str)

    def SetClientSize(self, hwnd: int, width: int, height: int) -> int:
        """
        设置窗口客户区域的宽度和高度

        Args:
            hwnd: 指定的窗口句柄
            width: 宽度
            height: 高度

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.SetClientSize(hwnd, width, height)

    def SetWindowSize(self, hwnd: int, width: int, height: int) -> int:
        """
        设置窗口的大小

        Args:
            hwnd: 指定的窗口句柄
            width: 宽度
            height: 高度

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.SetWindowSize(hwnd, width, height)

    def SetWindowState(self, hwnd: int, flag: int) -> int:
        """
        设置窗口的状态

        Args:
            hwnd: 指定的窗口句柄
            flag: 取值定义如下
                    0 : 关闭指定窗口
                    1 : 激活指定窗口
                    2 : 最小化指定窗口,但不激活
                    3 : 最小化指定窗口,并释放内存,但同时也会激活窗口.
                    4 : 最大化指定窗口,同时激活窗口.
                    5 : 恢复指定窗口 ,但不激活
                    6 : 隐藏指定窗口
                    7 : 显示指定窗口
                    8 : 置顶指定窗口
                    9 : 取消置顶指定窗口
                    10 : 禁止指定窗口
                    11 : 取消禁止指定窗口
                    12 : 恢复并激活指定窗口
                    13 : 强制结束窗口所在进程.

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.SetWindowState(hwnd, flag)

    def SetWindowText(self, hwnd: int, title: str) -> int:
        """
        设置窗口的标题

        Args:
            hwnd: 指定的窗口句柄
            title: 标题

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.SetWindowText(hwnd, title)

    def SetWindowTransparent(self, hwnd: int, trans: int) -> int:
        """
        设置窗口的透明度

        Args:
            hwnd: 指定的窗口句柄
            trans: 透明度取值(0-255) 越小透明度越大 0为完全透明(不可见) 255为完全显示(不透明)

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.SetWindowTransparent(hwnd, trans)

    """----------------------------------------基本设置------------------------------------------------"""

    def GetBasePath(self) -> str:
        """
        获取注册在系统中的dm.dll的路径.

        Returns:
            返回dm.dll所在路径.
        """
        return self.dm.GetBasePath()

    def GetID(self) -> int:
        """
        返回当前大漠对象的ID值，这个值对于每个对象是唯一存在的。可以用来判定两个大漠对象是否一致.

        Returns:
            当前对象的ID值.
        """
        return self.dm.GetID()

    def GetLastError(self) -> int:
        """
        获取插件命令的最后错误

        Returns:
            返回值表示错误值。 0表示无错误.

        注: 此函数必须紧跟上一句函数调用，中间任何的语句调用都会改变这个值.
        """
        return self.dm.GetLastError()

    def GetPath(self) -> str:
        """
        获取全局路径.(可用于调试)

        Returns:
            以字符串的形式返回当前设置的全局路径
        """
        return self.dm.GetPath()

    def SetPath(self, path: str) -> int:
        """
        设置全局路径,设置了此路径后,所有接口调用中,相关的文件都相对于此路径. 比如图片,字库等.

        Args:
            path: 路径,可以是相对路径,也可以是绝对路径

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.GetPath(path)

    def SetShowErrorMsg(self, show: int) -> int:
        """
        设置是否弹出错误信息,默认是打开.

        Args:
            show: 0表示不打开,1表示打开.

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.SetShowErrorMsg(show)

    def ver(self) -> str:
        """
        返回当前插件版本号

        Returns:
            当前插件的版本描述字符串
        """
        return self.dm.ver()

    """----------------------------------------鼠标键盘------------------------------------------------"""
    '''
    key_str     虚拟键码    
    "1",          49    
    "2",          50    
    "3",          51    
    "4",          52   
    "5",          53   
    "6",          54   
    "7",          55    
    "8",          56    
    "9",          57    
    "0",          48    
    "-",          189    
    "=",          187   
    "back",       8         
    "a",          65  
    "b",          66   
    "c",          67    
    "d",          68   
    "e",          69  
    "f",          70  
    "g",          71  
    "h",          72   
    "i",          73   
    "j",          74  
    "k",          75  
    "l",          76  
    "m",          77   
    "n",          78   
    "o",          79   
    "p",          80   
    "q",          81   
    "r",          82  
    "s",          83  
    "t",          84   
    "u",          85    
    "v",          86   
    "w",          87   
    "x",          88    
    "y",          89 
    "z",          90   
    "ctrl",       17 
    "alt",        18  
    "shift",      16   
    "win",        91    
    "space",      32  
    "cap",        20 
    "tab",        9 
    "~",          192   
    "esc",        27  
    "enter",      13   
    "up",         38   
    "down",       40  
    "left",       37   
    "right",      39      
    "option",     93    
    "print",      44 
    "delete",     46
    "home",       36  
    "end",        35   
    "pgup",       33 
    "pgdn",       34    
    "f1",         112   
    "f2",         113   
    "f3",         114  
    "f4",         115  
    "f5",         116   
    "f6",         117
    "f7",         118  
    "f8",         119   
    "f9",         120   
    "f10",        121   
    "f11",        122   
    "f12",        123
    "[",          219  
    "]",          221   
    "\\",         220  
    ";",          186  
    "'",          222   
    ",",          188  
    ".",          190  
    "/",          191
    '''

    def GetCursorPos(self) -> tuple:
        """
        获取鼠标位置.

        Returns:
            (x,y)
        """
        return self.dm.GetCursorPos(1, 1)

    def GetKeyState(self, vk_code: int) -> int:
        """
        获取指定的按键状态.(前台信息,不是后台)

        Args:
            vk_code: 虚拟按键码

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.GetKeyState(vk_code)

    def KeyDown(self, vk_code: int) -> int:
        """
        按住指定的虚拟键码

        Args:
            vk_code: 虚拟按键码

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.KeyDown(vk_code)

    def KeyDownChar(self, key_str: str) -> int:
        """
        按住指定的虚拟键码

        Args:
            key_str: 符串描述的键码. 大小写无所谓. 点这里查看具体对应关系

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.KeyDownChar(key_str)

    def KeyPress(self, vk_code: int) -> int:
        """
        按下指定的虚拟键码

        Args:
            vk_code: 虚拟按键码

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.KeyPress(vk_code)

    def KeyPressChar(self, key_str: str) -> int:
        """
        按下指定的虚拟键码

        Args:
            key_str: 字符串描述的键码. 大小写无所谓. 点这里查看具体对应关系

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.KeyPressChar(key_str)

    def KeyUp(self, vk_code: int) -> int:
        """
        弹起来虚拟键vk_code

        Args:
            vk_code: 虚拟按键码

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.KeyUp(vk_code)

    def KeyUpChar(self, key_str: str) -> int:
        """
        弹起来虚拟键key_str

        Args:
            key_str: 字符串描述的键码. 大小写无所谓. 点这里查看具体对应关系.

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.KeyUpChar(key_str)

    def LeftClick(self) -> int:
        """
        按下鼠标左键

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.LeftClick()

    def LeftDoubleClick(self) -> int:
        """
        双击鼠标左键

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.LeftDoubleClick()

    def LeftDown(self) -> int:
        """
        按住鼠标左键

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.LeftDown()

    def LeftUp(self) -> int:
        """
        弹起鼠标左键

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.LeftUp()

    def MiddleClick(self) -> int:
        """
        按下鼠标中键

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.MiddleClick()

    def MoveR(self, rx: int, ry: int) -> int:
        """
        鼠标相对于上次的位置移动rx,ry

        Args:
            rx: 相对于上次的X偏移
            ry: 相对于上次的Y偏移

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.MoveR(rx, ry)

    def MoveTo(self, x: int, y: int) -> int:
        """
        把鼠标移动到目的点(x,y)

        Args:
            x: X坐标
            y: Y坐标

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.MoveTo(x, y)

    def RightClick(self) -> int:
        """
        按下鼠标右键

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.RightClick()

    def RightDown(self) -> int:
        """
        按住鼠标右键

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.RightDown()

    def RightUp(self) -> int:
        """
        弹起鼠标右键

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.RightUp()

    def WheelDown(self) -> int:
        """
        滚轮向下滚

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.WheelDown()

    def WheelUp(self) -> int:
        """
        滚轮向上滚

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.WheelUp()

    """----------------------------------------系统设置------------------------------------------------"""

    def Beep(self, duration: int = 1000, f: int = 800) -> int:
        """
        蜂鸣器

        Args:
            duration:时长(ms)
            f: 频率

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.Beep(f, duration)

    def ExitOs(self, _type: int) -> int:
        """
        退出系统(注销 重启 关机)

        Args:
            _type: 取值为以下类型 0 : 注销系统 1 : 关机 2 : 重新启动

        Returns:
            0代表失败，1代表成功

        """
        return self.dm.ExitOs(_type)

    def GetClipboard(self) -> str:
        """
        获取剪贴板的内容

        Returns:
            以字符串表示的剪贴板内容
        """
        return self.dm.GetClipboard()

    def GetMachineCode(self) -> str:
        """
        获取本机的机器码.(带网卡). 此机器码用于插件网站后台. 要求调用进程必须有管理员权限. 否则返回空串.

        Returns:
            字符串:字符串表达的机器机器码

        注: 此机器码包含的硬件设备有硬盘,显卡,网卡等. 其它不便透露. 重装系统不会改变此值.
        另要注意,插拔任何USB设备,(U盘，U盾,USB移动硬盘,USB键鼠等),以及安装任何网卡驱动程序,(开启或者关闭无线网卡等)都会导致机器码改变.

        """
        return self.dm.GetMachineCode()

    def GetDiskSerial(self) -> str:
        """
        获取本机的硬盘序列号.支持ide scsi硬盘. 要求调用进程必须有管理员权限. 否则返回空串.

        Returns:
            字符串表达的硬盘序列号

        """
        return self.dm.GetDiskSerial()

    def GetMachineCodeNoMac(self) -> str:
        """
        获取本机的机器码.(不带网卡) 要求调用进程必须有管理员权限. 否则返回空串.

        Returns:
            字符串表达的机器机器码

        注: 此机器码包含的硬件设备有硬盘,显卡,网卡等. 其它不便透露. 重装系统不会改变此值.
        另要注意,插拔任何USB设备,(U盘，U盾,USB移动硬盘,USB键鼠等),以及安装任何网卡驱动程序,(开启或者关闭无线网卡等)都会导致机器码改变.

        """
        return self.dm.GetMachineCodeNoMac()

    def GetScreenHeight(self) -> int:
        """
        获取屏幕的高度.

        Returns:
            返回屏幕的高度
        """
        return self.dm.GetScreenHeight()

    def GetScreenWidth(self) -> int:
        """
        获取屏幕的宽度.

        Returns:
            返回屏幕的宽度
        """
        return self.dm.GetScreenWidth()

    def GetTime(self) -> int:
        """
        获取当前系统从开机到现在所经历过的时间，单位是毫秒

        Returns:
            时间(单位毫秒)
        """
        return self.dm.GetTime()

    def SetClipboard(self, value: str) -> int:
        """
        设置剪贴板的内容

        Args:
            value: 以字符串表示的剪贴板内容

        Returns:
            0代表失败，1代表成功
        """
        return self.dm.SetClipboard(value)
