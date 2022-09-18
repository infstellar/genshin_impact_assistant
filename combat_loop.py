#from interaction import *
import unit,character,tastic,time,threading
from timer import Timer
from interaction_background import Interaction_BGD

def sort_flag_1(x:character.Character):
    return x.priority

def stop_func_example():#True:stop;False:continue
    return False

class Combat_Loop(threading.Thread):
    def __init__(self,chara_list:list[character.Character],stop_func=stop_func_example):
        threading.Thread.__init__(self)
        
        
        self.chara_list=chara_list
        self.chara_list.sort(key=sort_flag_1,reverse=False)
        self.tastic_exc=tastic.Tastic()
        self.stop_flag=False
        self.current_num=1
        self.switch_timer=Timer(diff_start_time=2)
        self.itt=Interaction_BGD()
        self.stop_func=stop_func
        
        self._switch_character(1)
        #self.itt.delay(1)
        ...
    
    def _switch_character(self,x:int):
        t = self.switch_timer.getDiffTime()
        # if t>=1.1:
        #     pass
        # else:
        #     self.itt.delay(1.1-t)
        while self.tastic_exc.get_character_busy():
            time.sleep(0.1)    
        self.itt.keyPress(str(x))
        self.current_num=x
        self.switch_timer.reset()
        self.itt.delay(0.1)
            
            
    
    def stop(self):
        self.stop_flag=True
    
    def loop(self):
        idle=True
        for chara in self.chara_list:
            print(chara.name)
            if self.stop_flag:
                return 0
            if chara.trigger():
                if chara.n != self.current_num:
                    self._switch_character(chara.n)
                self.tastic_exc.run(chara.tastic_group,chara,stop_func=self.stop_func)
                idle=False
                return idle
            #time.sleep()
        return idle