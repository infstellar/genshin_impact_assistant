import threading



class Base_Threading(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pause_threading_flag=False
        self.stop_threading_flag=False
        self.working_flag=True
        
    def pause_threading(self):
        self.pause_threading_flag=True
        
    def continue_threading(self):
        self.pause_threading_flag=False
    
    def stop_threading(self):
        self.stop_threading_flag=True
        
    def checkup_stop_threading(self):
        if self.stop_threading_flag:
            return True
    
    def get_working_statement(self):
        return self.working_flag
    
    def checkup_stop_func(self):
        if self.pause_threading_flag or self.stop_threading_flag:
            return True
        
    def run():
        pass