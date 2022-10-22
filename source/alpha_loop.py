import threading
from unit import *
import combat_loop, character
from base_threading import Base_Threading

class Alpha_Loop(Base_Threading):
    
    @logger.catch
    def __init__(self):
        super().__init__()
        self.setName('Alpha_Loop')
        self.stop_flag=False
        chara_list = combat_loop.get_chara_list()
        self.combatloop = combat_loop.Combat_Controller(chara_list)
        self.combatloop.pause_threading()
        self.combatloop.start()
    
    @logger.catch 
    def run(self):
        self.combatloop.continue_threading()
        while(1):
            if self.stop_threading_flag:
                return 0
            
            if self.pause_threading_flag: 
                if self.working_flag == True:
                    self.working_flag = False
                if self.combatloop.get_working_statement()==True:
                    self.combatloop.pause_threading()
                time.sleep(1)
                continue
            
            if self.working_flag == False:
                if self.combatloop.get_working_statement()==False:
                    self.combatloop.continue_threading()
                self.working_flag = True

            time.sleep(2)
                
    # def stop_thread(self,mode:int=0):
    #     if mode==0:
    #         self.stop_flag=True
    #         self.combatloop.stop_threading()
    #     elif mode==1: #emergency stop
    #         thread_id = self.get_id() 
    #         res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
    #             ctypes.py_object(SystemExit)) 
    #         if res > 1: 
    #             ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
    #             logger.warning('Exception raise failure') 


if __name__=='__main__':
    #character_json=loadjson('character.json')
    # team=loadjson('team.json')
    al=Alpha_Loop()
    al.start()
    while(1):
        time.sleep(1)