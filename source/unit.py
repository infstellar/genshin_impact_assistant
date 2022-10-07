import ctypes, sys
DEBUG_MODE=False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if not is_admin():
    print('try to get administrator')
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    print('administrator have been obtained')

import os, json, time, pickle, math, random, pytweening
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path1 = path+'\\source'
if sys.path[0]!=path:
    sys.path.insert(0, path)
if sys.path[1]!=path1:
    sys.path.insert(1, path1)



# print('test')

def isint(x):
    try:
        a = int(x)
    except ValueError:
        return False
    else:
        return True

def loadjson(json_name='config.json'):
    f = open('config/'+json_name, 'r')
    content = f.read()
    a = json.loads(content)
    f.close()
    return a

def savejson(x,json_name='config.json'):
    b = json.dumps(x,sort_keys=True, indent=4)
    f2 = open(json_name, 'w')
    f2.write(b)
    f2.close()
        
def loadfileP(filename):
    with open('wordlist//'+filename+'.wl', 'rb') as fp:
        list1=pickle.load(fp)
    return list1
        
def savefileP(filename,item):
    with open('wordlist//'+filename+'.wl', 'w+b') as fp: # 把 t 对象存到文件中
        pickle.dump(item, fp)
        
global configjson        
configjson=loadjson("config.json")
DEBUG_MODE=configjson["DEBUG"]
def reflash_config():
    global configjson
    configjson=loadjson("config.json")
import logger_module
sys.stdout = logger_module.Logger()#'G:/2.0/test.txt'