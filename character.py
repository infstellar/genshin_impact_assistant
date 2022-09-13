from timer import Timer
class Character():
    def __init__(self,name,position,Ecd_time,Elast_time,Ecd_float_time,tactic_group):
        self.name=name
        self.position=position
        self.Ecd_time=Ecd_time
        self.Elast_time=Elast_time
        self.Ecd_float_time=Ecd_float_time
        self.tactic_group=tactic_group
        
        self.Ecd_timer=Timer(diff_start_time=Ecd_time)
        self.Elast_timer=Timer(diff_start_time=Elast_time)
    
    def get_Ecd_time(self):
        t = self.Ecd_timer.getDiffTime()
        t = self.Ecd_time - t
        if t <= 0 :
            return 0
        else:
            return t
    
    def used_E(self):
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