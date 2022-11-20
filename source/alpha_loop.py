import time

import combat_loop
from base_threading import BaseThreading
from util import *


class AlphaLoop(BaseThreading):

    @logger.catch
    def __init__(self):
        super().__init__()
        self.setName('Alpha_Loop')
        self.stop_flag = False
        chara_list = combat_loop.get_chara_list()
        self.combat_loop = combat_loop.Combat_Controller(chara_list)
        self.combat_loop.pause_threading()
        self.combat_loop.start()

    @logger.catch
    def run(self):
        self.combat_loop.continue_threading()
        while 1:
            time.sleep(2)
            if self.stop_threading_flag:
                self.combat_loop.stop_threading()
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                if self.combat_loop.get_working_statement():
                    self.combat_loop.pause_threading()
                time.sleep(1)
                continue

            if not self.working_flag:
                if not self.combat_loop.get_working_statement():
                    self.combat_loop.continue_threading()
                self.working_flag = True

    # def stop_thread(self,mode:int=0):
    #     if mode==0:
    #         self.stop_flag=True
    #         self.combat_loop.stop_threading()
    #     elif mode==1: #emergency stop
    #         thread_id = self.get_id() 
    #         res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
    #             ctypes.py_object(SystemExit)) 
    #         if res > 1: 
    #             ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
    #             logger.warning('Exception raise failure') 


if __name__ == '__main__':
    # character_json=load_json('character.json')
    # team=load_json('team.json')
    al = AlphaLoop()
    al.start()
    while 1:
        time.sleep(1)
