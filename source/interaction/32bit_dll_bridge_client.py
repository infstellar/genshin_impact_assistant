from socket import *
import threading, time, os
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
    target_pyfile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "32bit_dll_bridge_server.py")
    command = f'cd "{os.path.join(python_path, "../")}";&./python.exe "{target_pyfile_path}"'.replace(r"\\", "/").replace("\\", "/").replace('"', '"')
    print("run this command in an admin powershell\n", command)
    input("Enter to continue")

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
    
    def _send_function(self, func_name:str, para:tuple=None):
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
        return self._send_function('BindWindow',(hwnd, display, mouse, keypad, mode))
    
    def EnableBind(self, enable):
        return self._send_function('EnableBind',(enable))
    
    def UnBindWindow(self):
        print("unbind: ", self._send_function('UnBindWindow'))

if __name__ == "__main__":
    start_server(python_path="D:\\Program Files\\Anaconda\\envs\\GIA3732\\python.exe")
    connect()
    dmdll = DMDLL()
    dmdll.start()
    print(dmdll.ver())