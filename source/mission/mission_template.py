from source.util import *
from source.flow import collector_flow_upgrad, teyvat_move_flow_upgrad
from source.controller import combat_loop
from source.common.base_threading import BaseThreading
from source.operator.pickup_operator import PickupOperator

class MissionExecutor(BaseThreading):
    def __init__(self):
        super().__init__(thread_name=__name__)
        self.CFCF = collector_flow_upgrad.CollectorFlowController()
        self._add_sub_threading(self.CFCF)
        self.TMCF = teyvat_move_flow_upgrad.TeyvatMoveFlowController()
        self._add_sub_threading(self.TMCF)
        self.PUO = PickupOperator()
        self._add_sub_threading(self.PUO)

    def get_path_file(self, path_file_name:str):
        return load_json(path_file_name+".json","assets\\TeyvatMovePath")
    
    def move(self, MODE:str = None,stop_rule:int = None,target_posi:list = None,path_list:list = None,to_next_posi_offset:float = None,special_keys_posi_offset:float = None,reaction_to_enemy:str = None,is_tp:bool=None):
        self.TMCF.reset()
        self.TMCF.set_parameter(MODE=MODE,stop_rule=stop_rule,target_posi=target_posi,path_dict=path_list,to_next_posi_offset=to_next_posi_offset,special_keys_posi_offset=special_keys_posi_offset,reaction_to_enemy=reaction_to_enemy,is_tp=is_tp)
        self.TMCF.start_flow()
        while 1:
            time.sleep(0.2)
            if self.TMCF.get_working_statement() == False:
                break
    
    def move_straight(self, position, is_tp = False):
        self.move(MODE="AUTO", target_posi=position, is_tp = is_tp)
        
    def move_along(self, path, is_tp = False):
        self.move(MODE="PATH", path_list=self.get_path_file(path), is_tp = is_tp)
            
    def combat(self):
        pass

    def collect(self, MODE = None,
                collection_name =  None,
                collector_type =  None,
                is_combat =  None,
                is_activate_pickup = None,
                pickup_points = None
                ):
        self.CFCF.reset()
        self.CFCF.set_parameter(MODE=MODE,collection_name=collection_name,collector_type=collector_type,is_combat=is_combat,is_activate_pickup=is_activate_pickup,pickup_points=pickup_points)
        self.CFCF.start_flow()
        time.sleep(1)
        while 1:
            time.sleep(0.2)
            if self.CFCF.get_working_statement() == False:
                break
    
    def start_pickup(self):
        self.PUO.continue_threading()
    
    def stop_pickup(self):
        self.PUO.pause_threading()
            
    def exec_mission(self):
        pass
    
    def run(self):
        '''if you're using this class, copy this'''
        while 1:
            time.sleep(self.while_sleep)
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
                self.pause_threading_flag = True
                continue
            '''write your code below'''
            self.exec_mission()
            self.pause_threading()
    


