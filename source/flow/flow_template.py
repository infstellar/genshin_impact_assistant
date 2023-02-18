from source.util import *
import source.flow.flow_code as FC
from source.constant import flow_state as FlowState
from source.common import base_threading
from source.funclib.err_code_lib import *
from source.constant import flow_state as ST


class FlowConnector():
    def __init__(self):
        self.while_sleep = 0.1

    def get_while_sleep(self):
        return self.while_sleep

class FlowTemplate():
    def __init__(self, upper:FlowConnector):
        self.upper = upper
        self.flow_id = 0
        self.rfc = FC.INIT
        self.next_flow_id = self.flow_id
        
    def enter_flow(self):
        if self.rfc == FC.INIT:
            self.state_init()
        elif self.rfc == FC.BEFORE:
            self.state_before()
        elif self.rfc == FC.IN:
            self.state_in()
        elif self.rfc == FC.AFTER:
            self.state_after()
        elif self.rfc == FC.END:
            self.state_end()
            return self.next_flow_id
        return self.flow_id

    def _next_rfc(self):
        if self.rfc < 5:
            self.rfc += 1
        else:
            self.rfc = 5

    def state_init(self):
        self.rfc = FC.BEFORE
        
    
    def state_before(self):
        self.rfc = FC.IN
        
    
    def state_in(self):
        self.rfc = FC.IN
        
    
    def state_after(self):
        self.rfc = FC.END
        
    
    def state_end(self):
        self.rfc = FC.OVER
        
    def _set_nfid(self, fid):
        self.next_flow_id = fid


class FlowController(base_threading.BaseThreading):
    def __init__(self):
        super().__init__()
        self.last_err_code = ERR_NONE
        self.flow_dict = {}
        self.current_flow_id = None
        self.end_flow_id = None
        self.get_while_sleep = None
        
    def append_flow(self, flow:FlowTemplate):
        self.flow_dict[str(flow.flow_id)] = flow
    
    def set_current_flow_id(self, id):
        self.current_flow_id = id
        
    def set_end_flow_id(self, id):
        self.end_flow_id = id
    
    def _err_code_exec(self) -> bool:
        """_summary_

        Returns:
            bool: if True, then mean pause thread.
        """
        return True
        
    def run(self) -> None:
        '''if you're using this class, copy this'''
        while 1:
            time.sleep(self.get_while_sleep())
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
                r = self._err_code_exec()
                if r:
                    self.pause_threading_flag = True
                    continue
            '''write your code below'''

            for i in self.flow_dict:
                if i == str(self.current_flow_id):
                    rcode = self.flow_dict[i].enter_flow()
                    self.current_flow_id = rcode
            
            if rcode == ST.END:
                logger.info("Flow END")
                self.last_err_code = ERR_PASS
                self.pause_threading()
