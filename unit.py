import sys, os, json, time, pickle

class Logger(object):
    def __init__(self, fileN='Terminal.log'):
        self.terminal = sys.stdout
        
        try:
            self.log = open(fileN, 'a')
        except FileNotFoundError:
            open(fileN,'w')
            self.log = open(fileN, 'a')
        self.messageCache=''
        self.log.write('\n\n\n')

    def write(self, message):
        '''print实际相当于sys.stdout.write'''
        self.terminal.write(message)
        nowTime=str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        if message!='\n':
            self.messageCache+=message
        else:
            self.log.write(nowTime+':    '+self.messageCache+'\n')
            self.messageCache=''

    def flush(self):
        pass


sys.stdout = Logger()#'G:/2.0/test.txt'

def loadjson(json_name='config.json'):
    f = open(json_name, 'r')
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

def Asavefile():
    for i in a:
        with open('wordlist//'+i+'.wl', 'w+b') as fp: # 把 t 对象存到文件中
            pickle.dump(TotalList, fp)
