import sys, os, json, time

def loadjson(json_name='config.json'):
    f = open('config/'+json_name, 'r')
    content = f.read()
    a = json.loads(content)
    f.close()
    return a
configjson=loadjson("config.json")
DEBUG_MODE=configjson["DEBUG"]

class Logger(object):
    def __init__(self, fileN='Terminal.log'):
        self.terminal = sys.stdout
        
        try:
            self.log = open(fileN, 'a')
        except FileNotFoundError:
            open(fileN,'w')
            self.log = open(fileN, 'a')
        self.log.write('\n\n\n')
        self.fileN=fileN

    def flush(self):
        pass
    
    def write(self, message):
        '''print实际相当于sys.stdout.write'''
        if DEBUG_MODE:
            self.terminal.write(message)
        else:
            if 'ConsoleMessage' in message:
                self.terminal.write(message+'\n')
        
        nowTime=str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        if message=='\n':
            pass
        else:
            a=open(self.fileN, 'a')
            a.write(nowTime+':    '+message+'\n')
            a.close()