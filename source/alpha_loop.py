import threading
from unit import *
import combat_loop,character

class Alpha_Loop(threading.Thread):
    
    @logger.catch
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_flag=False
        chara_list=combat_loop.get_chara_list()
        self.combatloop = combat_loop.Combat_Loop(chara_list)
        self.combatloop.pause_threading()
        self.combatloop.start()
    
    @logger.catch 
    def run(self):
        self.combatloop.continue_threading()
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
            self.combatloop.stop_threading()
        elif mode==1: #emergency stop
            thread_id = self.get_id() 
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
                ctypes.py_object(SystemExit)) 
            if res > 1: 
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
                logger.warning('Exception raise failure') 


if __name__=='__main__':
    #character_json=loadjson('character.json')
    # team=loadjson('team.json')
    al=Alpha_Loop()
    al.start()
    while(1):
        time.sleep(1)