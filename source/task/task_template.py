from source.util import *
from source.common.base_threading import BaseThreading
from source.flow.flow_template import FlowController

class TaskTemplate(BaseThreading):
    def __init__(self):
        super().__init__()
        self.flow_list = []
        
    def _add_sub_flow(self, flow:FlowController):
        self._add_sub_threading(flow)
        self.flow_list.append(flow)
    
    def get_flow_statement(self):
        statement = []
        for i in self.flow_list:
            statement.append(
                {
                    "name":i.flow_name,
                    "statement":i.current_flow_id,
                    "rfc":i.flow_dict[i.current_flow_id].rfc
                }
            )
        return statement
    
    def loop(self):
        pass

    def run(self) -> None:
        '''if you're using this class, copy this'''
        while 1:
            time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True
                
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            '''write your code below'''
            
            self.loop()

    def end_task(self):
        self.stop_threading()
        return
            
            
            