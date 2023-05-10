from source.util import *
import source.flow.flow_code as FC
from common import flow_state as FlowState, flow_state as ST
from source.common import base_threading, timer_module
from source.funclib.err_code_lib import *


class FlowConnector():
    def __init__(self):
        self.while_sleep = 0.1
        self.checkup_stop_func = None

    def get_while_sleep(self):
        return self.while_sleep
    
    def reset(self):
        pass

class FlowTemplate():
    def __init__(self, upper:FlowConnector, flow_id:str, next_flow_id:str, flow_timeout_time:float = -1, flow_name=None):
        self.upper = upper
        self.flow_id = flow_id
        self.rfc = FC.INIT
        self.next_flow_id = next_flow_id
        self.flow_timeout = timer_module.TimeoutTimer(flow_timeout_time)
        if flow_name is None:
            self.flow_name = flow_id
        
    def _before_timeout(self):
        logger.warning(f"TIMEOUT: {self.flow_id}")
          
    def enter_flow(self):
        if self.rfc == FC.INIT:
            self.flow_timeout.reset()
            self.state_init()
        elif self.rfc == FC.BEFORE:
            self.state_before()
        elif self.rfc == FC.IN:
            self.state_in()
        elif self.rfc == FC.AFTER:
            self.state_after()
        elif self.rfc == FC.END:
            self.state_end()
            self.rfc = FC.INIT
            logger.info(f"Flow Switch To: {self.next_flow_id}")
            return self.next_flow_id
        if self.flow_timeout.istimeout():
            self._before_timeout()
            return self.next_flow_id
            
        return self.flow_id

    def _next_rfc(self):
        if self.rfc < 5:
            self.rfc += 1
        else:
            self.rfc = 5
        logger.debug(f"{self.flow_name} switch rfc to {self.rfc}")

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
        logger.debug(f"{self.flow_name} set next flow id to {self.next_flow_id}")
        
    def _set_rfc(self, rfc):
        self.rfc = rfc
        logger.debug(f"{self.flow_name} set rfc to {self.rfc}")

class EndFlowTemplate(FlowTemplate):
    def __init__(self, upper:FlowConnector, flow_id:str, err_code_id = ERR_PASS):
        self.upper = upper
        self.flow_id = flow_id # flow id <0
        self.rfc = FC.INIT
        self.err_code_id = err_code_id
    
    def enter_flow(self):
        self.state_init()
        self.state_before()
        self.state_in()
        self.state_after()
        self.state_end()
        return self.err_code_id
    
    def _set_ecid(self, fid):
        self.err_code_id = fid


class FlowController(base_threading.AdvanceThreading):
    def __init__(self, flow_connector:FlowConnector, current_flow_id, flow_name=None):
        super().__init__(thread_name = flow_name)
        if flow_name != None:
            self.flow_name = flow_name
        else:
            self.flow_name=""
        self.last_err_code = ERR_NONE
        self.flow_dict = {}
        self.current_flow_id = current_flow_id
        # self.end_flow_id = None
        self.flow_connector = flow_connector
        self.get_while_sleep = flow_connector.get_while_sleep
        self.flow_connector.checkup_stop_func = self.checkup_stop_func
    
    def start_flow(self):
        self.continue_threading()
        
    def append_flow(self, flow:FlowTemplate):
        self.flow_dict[str(flow.flow_id)] = flow
    
    def set_current_flow_id(self, id):
        self.current_flow_id = id

    def reset(self):
        self.flow_connector.reset()
        
    # def set_end_flow_id(self, id):
    #     self.end_flow_id = id
    
    def _err_code_exec(self) -> bool:
        """_summary_

        Returns:
            bool: if True, then mean pause thread.
        """
        return True
    
    def loop(self):
        rcode = self.flow_dict[self.current_flow_id].enter_flow()
        if "$END$" in rcode:
            self.last_err_code = self.flow_dict[rcode].enter_flow()
            logger.debug(f"Flow END, code:{self.last_err_code}")
            self.pause_threading()
        else:
            self.current_flow_id = rcode
    
    def run(self) -> None:
        '''if you're using this class, copy this'''
        while 1:
            time.sleep(self.get_while_sleep())
            if self.stop_threading_flag:
                return

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

            rcode = self.flow_dict[self.current_flow_id].enter_flow()
            if "$END$" in rcode:
                self.last_err_code = self.flow_dict[rcode].enter_flow()
                logger.debug(f"Flow END, code:{self.last_err_code}")
                self.pause_threading()
            else:
                self.current_flow_id = rcode
