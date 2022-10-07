import os, cv2
import time
from timer_module import Timer
from interaction_background import Interaction_BGD
import posi_manager
def default_trigger_func():
    return True

class Character():
    def __init__(self,name=None,position=None,n=None,priority=None,
                 E_short_cd_time=None,E_long_cd_time=None,
                 Elast_time=None,Ecd_float_time=None,
                 tastic_group=None,trigger:str=None,
                 Epress_time=None,Qlast_time=0):
        self.name=name
        self.position=position
        
        self.E_short_cd_time=E_short_cd_time
        self.E_long_cd_time=E_long_cd_time
        self.Elast_time=Elast_time
        self.Qlast_time=Qlast_time
        
        self.Ecd_float_time=Ecd_float_time
        self.tastic_group=tastic_group
        self.priority=priority
        self.n=n
        self.Epress_time=Epress_time
        self.itt=Interaction_BGD()
        
        if E_long_cd_time!=0:
            self.Ecd_time=E_long_cd_time
        else:
            self.Ecd_time=E_short_cd_time
        self.triggers=trigger
        self.trigger=default_trigger_func
        self.Ecd_timer=Timer(diff_start_time=self.Ecd_time)
        self.Elast_timer=Timer(diff_start_time=Elast_time)
        self.Qlast_timer=Timer(diff_start_time=Qlast_time)
        
        self._trigger_analyse()
        
    def _trigger_e_ready(self):
        if self.is_E_ready():
            return True
        
    def _trigger_q_ready(self):
        cap = self.itt.capture(jpgmode=2)
        p=posi_manager.posi_charalist_q_point[self.n-1]
        if cap[p[0],p[1]].max()>0:
            return True
        else:
            return False
        # name = self.name
        # filename='imgs/'+name+'_listq.png'
        # if os.path.exists(filename):
        #     img = cv2.imread(filename)
        #     mr = self.itt.similar_img(name+'_listq.png',self.itt.capture(),posi_manager.posi_charalist_q[self.n-1])
        #     print('Qmr= ',mr)
        #     if mr>=0.9:
        #         return True
        #     else:
        #         return False
        # else:
        #     return True
        
    def _trigger_idle(self):
        return True   
        
    def _trigger_analyse(self):
        if self.triggers == 'e_ready':
            self.trigger = self._trigger_e_ready
        elif self.triggers == 'q_ready':
            self.trigger = self._trigger_q_ready
        elif self.triggers == 'idle':
            self.trigger = self._trigger_idle
    
    def get_Ecd_time(self):
        t = self.Ecd_timer.getDiffTime()
        t = self.Ecd_time - t
        if t <= 0 :
            return 0
        else:
            return t
    
    def used_E(self):
        if self.is_E_ready():
            self.Ecd_time=self.E_short_cd_time
            self.Ecd_timer.reset()
            self.Elast_timer.reset()
            
    
    def used_longE(self):
        if self.is_E_ready():
            self.Ecd_time=self.E_long_cd_time
            self.Ecd_timer.reset()
            self.Elast_timer.reset()
    
    def is_E_ready(self):
        if self.get_Ecd_time()<=self.Ecd_float_time:
            return True
        else:
            return False
        
    def is_chara_Q_ready(self):
        name = self.name
        filename='imgs/'+name+'_q.png'
        if os.path.exists(filename):
            img = cv2.imread(filename)
            mr = self.itt.similar_img(name+'_q.png',self.itt.capture(),posi_manager.posi_chara_q)
            print('Qmr= ',mr)
            if mr>=0.9:
                return True
            else:
                return False
        else:
            return True
    
    
    
    def get_Ecd_last_time(self):
        t = self.Elast_timer.getDiffTime()
        t = self.Elast_time - t
        if t <=0:
            return 0
        else:
            return t
        
    def get_Q_last_time(self):
        t = self.Qlast_timer.getDiffTime()
        t = self.Qlast_time - t
        if t <=0:
            return 0
        else:
            return t
    
    def is_E_pass(self):
        t = self.get_Ecd_last_time()
        if t <= 0 :
            return True
        else:
            return False
        
    def is_Q_pass(self):
        t = self.get_Q_last_time()
        if t <= 0 :
            return True
        else:
            return False
        
if __name__=='__main__':
    chara=Character('3','none',3,0,1,2,2,1,'none','q_ready')
    while(1):
        time.sleep(0.1)
        print(chara._trigger_q_ready(),end=' ')
