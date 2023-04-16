from socket import *
import threading, time, os

"""
如何配置DM后台操作
1. anaconda powershell:(administrator)
2. set CONDA_FORCE_32BIT=1
3. conda create -n XXXX python==3.7.6
4. y
5. conda activate XXXX;pip install pywin32
6. 把地址放到config里
7. 在config/setting新建dm.json,复制
{
    key:0,
    addition_key:0,
    dll_path:xxx    
}
填入对应信息。
"""
class Timer:
    def __init__(self, diff_start_time=0):
        self.start_time = time.time()
        self.start_time = self.start_time - diff_start_time
        self.end_time = time.time()

    def reset(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
    
    def get_diff_time(self):  # new
        self.stop()
        return self.end_time - self.start_time

    def loop_time(self):
        t = self.get_diff_time()
        self.reset()
        return t

class TimeoutTimer(Timer):
    def __init__(self, timeout_limit):
        super().__init__()
        self.timeout_limit=timeout_limit
        self.reset()
    
    def set_timeout_limit(self, t):
        self.timeout_limit = t
        
    def istimeout(self):
        if self.get_diff_time() >= self.timeout_limit:
            return True
        else:
            return False

def start_server(python_path):
    target_pyfile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bit32_dll_bridge_server.py")
    command = f'cd "{os.path.dirname(python_path)}" && start cmd /k python.exe "{target_pyfile_path}"'.replace(r"\\", "/").replace("\\", "/").replace('"', '"')
    os.system(f"{command}")
    print("waiting for connection")
    time.sleep(5)
    # print("run this command in an admin powershell\n", command)
    # input("Enter to continue")

global HOST, PORT, BUFSIZE, ADDR, tcpCliSock
def connect():
    global HOST, PORT, BUFSIZE, ADDR, tcpCliSock
    HOST = '127.0.0.1' # or 'localhost'
    PORT = 21568
    BUFSIZE = 1024
    ADDR = (HOST,PORT)

    tcpCliSock = socket(AF_INET,SOCK_STREAM)
    tcpCliSock.connect(ADDR)

class DLLClient(threading.Thread):
    global HOST, PORT, BUFSIZE, ADDR, tcpCliSock
    def __init__(self):
        super().__init__()
        self._send_list = []
        self.activate_timeout=TimeoutTimer(5)
        self.setName("DLLClient")
    
    def _send_function(self, func_name:str, para:list=None):
        """_summary_

        Args:
            func_name (_type_): _description_
            para (tuple): _description_
        """
        self.activate_timeout.reset()
        send_para = ""
        if para != None:
            for i in para:
                send_para+=f"{i}#"
        else:
            send_para="#"
        data1 = func_name+'$'+send_para
        tcpCliSock.send(data1.encode())
        data2 = tcpCliSock.recv(BUFSIZE)
        return data2.decode('utf-8')
    
    def run(self):
        while True:
            if self.activate_timeout.istimeout():
                time.sleep(0.1)
            else:
                time.sleep(0.02)

class DMDLL(DLLClient):
    def __init__(self):
        super().__init__()
    
    def ver(self):
        return self._send_function("ver")
    
    def BindWindow(self,hwnd,display,mouse,keypad,mode):
        return self._send_function('BindWindow',[hwnd, display, mouse, keypad, mode])
    
    def EnableBind(self, enable):
        return self._send_function('EnableBind',[enable])
    
    def UnBindWindow(self):
        return self._send_function('UnBindWindow')

    def KeyDown(self,vkcode):
        return self._send_function('KeyDown',[vkcode])
    
    def KeyUp(self,vkcode):
        return self._send_function('KeyUp',[vkcode])
    
    def KeyPress(self,vkcode):
        return self._send_function('KeyPress',[vkcode])
    
    def LeftDown(self):
        return self._send_function('LeftDown')
    
    def LeftUp(self):
        return self._send_function('LeftUp')
    
    def LeftClick(self):
        return self._send_function('LeftClick')
    
    def RightClick(self):
        return self._send_function('RightClick')
    
    def MiddleClick(self):
        return self._send_function('MiddleClick')
    
    def MoveR(self,x,y):
        return self._send_function('MoveR',(x,y))
    
    def MoveTo(self,x,y):
        return self._send_function('MoveTo',(x,y))
    
    def GetLastError(self):
        return self._send_function('GetLastError')
    
    
if __name__ == "__main__":
    start_server(python_path="D:\\Program Files\\Anaconda\\envs\\GIA3732\\python.exe")
    connect()
    dmdll = DMDLL()
    dmdll.start()
    print(dmdll.ver())