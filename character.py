from timer import Timer
def default_trigger_func():
    return True

class Character():
    def __init__(self,name,position,n,priority,E_short_cd_time,E_long_cd_time,Elast_time,Ecd_float_time,tastic_group,trigger:str):
        self.name=name
        self.position=position
        
        self.E_short_cd_time=E_short_cd_time
        self.E_long_cd_time=E_long_cd_time
        self.Elast_time=Elast_time
        self.Ecd_float_time=Ecd_float_time
        self.tastic_group=tastic_group
        self.priority=priority
        self.n=n
        
        if E_long_cd_time!=0:
            self.Ecd_time=E_long_cd_time
        else:
            self.Ecd_time=E_short_cd_time
        self.triggers=trigger
        self.trigger=default_trigger_func
        self.Ecd_timer=Timer(diff_start_time=self.Ecd_time)
        self.Elast_timer=Timer(diff_start_time=Elast_time)
        
        self._trigger_analyse()
        
    def _trigger_e_ready(self):
        if self.is_E_ready():
            return True
        
    def _trigger_q_ready(self):
        if self.is_Q_ready():
            return True
    
    def _trigger_analyse(self):
        if self.triggers == 'e_ready':
            self.trigger = self._trigger_e_ready
        elif self.triggers == 'q_ready':
            self.trigger = self._trigger_q_ready
    
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
        if self.get_Ecd_time()<=0:
            return True
        else:
            return False
        
    def is_Q_ready(self):
        return True
    
    def get_Ecd_last_time(self):
        t = self.Elast_timer.getDiffTime()
        t = self.Elast_time - t
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