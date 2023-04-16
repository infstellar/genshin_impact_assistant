from socket import *
from time import ctime
import threading, json, os
import dmlib as dmlib
HOST = '127.0.0.1'
PORT = 21568
BUFSIZE = 1024
ADDR = (HOST,PORT)
 
tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
jso = json.load(open(os.path.join(root_path, "config\\settings\\dm.json"), 'r', encoding='utf-8'))
key = jso["key"]
addition_key = jso["addition_key"]
dll_path = jso["dll_path"]

dmdll = dmlib.DM(key, addition_key, dll_path)

def exec_rdata(rdata):
    func_name = rdata.split('$')[0]
    parameters = rdata.split('$')[1].split('#')[:-1]
    print(f"recieve: {func_name} {parameters}")
    if func_name == 'ver':
        return dmdll.ver()
    elif func_name == 'BindWindow':
        return dmdll.BindWindow(int(parameters[0]),str(parameters[1]),str(parameters[2]),str(parameters[3]),int(parameters[4]))
    elif func_name == 'EnableBind':
        return dmdll.EnableBind(int(parameters[0]))
    elif func_name == 'UnBindWindow':
        return dmdll.UnBindWindow()
    elif func_name == 'KeyDown':
        return dmdll.KeyDown(int(parameters[0]))
    elif func_name == 'KeyUp':
        return dmdll.KeyUp(int(parameters[0]))
    elif func_name == 'KeyPress':
        return dmdll.KeyPress(int(parameters[0]))
    elif func_name == 'LeftDown':
        return dmdll.LeftDown()
    elif func_name == 'LeftUp':
        return dmdll.LeftUp()
    elif func_name == 'LeftClick':
        return dmdll.LeftClick()
    elif func_name == 'RightClick':
        return dmdll.RightClick()
    elif func_name == 'MiddleClick':
        return dmdll.MiddleClick()
    elif func_name == 'MoveR':
        return dmdll.MoveR(int(parameters[0]), int(parameters[1]))
    elif func_name == 'MoveTo':
        return dmdll.MoveTo(int(parameters[0]), int(parameters[1]))
    elif func_name == 'GetLastError':
        return dmdll.GetLastError()
class server(threading.Thread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            print('waiting for connection...')
            tcpCliSock, addr = tcpSerSock.accept()
            print('...connnecting from:', addr)

            while True:
                data = tcpCliSock.recv(BUFSIZE)
                if not data:
                    break
                
                rdata = data.decode('utf-8')
                sdata = exec_rdata(rdata)
                
                tcpCliSock.send(str(sdata).encode())
                # tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode())
            tcpCliSock.close()
        tcpSerSock.close()

server().start()
import time
while 1:
    time.sleep(1)