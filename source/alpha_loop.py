import threading
from unit import *
import combat_loop,character

class Alpha_Loop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        
        self.stop_flag=False
        chara_list=combat_loop.get_chara_list()
        self.combatloop=combat_loop.Combat_Loop(chara_list,super_stop_func=self.get_stop_flag)
        self.combatloop.stop_loop()
        self.combatloop.start()
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        self.combatloop.start_loop()
        while(True):
            time.sleep(1)
                
    def get_stop_flag(self):
        return self.stop_flag
    
    def stop_func(self):
        if self.stop_flag==True:
            return True
        else:
            return False
                
    def stop_thread(self,mode:int=0):
        if mode==0:
            self.stop_flag=True
            self.combatloop.stop()
        elif mode==1: #emergency stop
            thread_id = self.get_id() 
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
                ctypes.py_object(SystemExit)) 
            if res > 1: 
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
                print('Exception raise failure') 


if __name__=='__main__':
    #character_json=loadjson('character.json')
    # team=loadjson('team.json')
    al=Alpha_Loop()
    al.start()
    while(1):
        time.sleep(1)