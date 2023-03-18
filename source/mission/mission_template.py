from source.util import *
from source.flow import collector_flow_upgrad, teyvat_move_flow_upgrad
from source.controller import combat_loop
from source.common.base_threading import BaseThreading
from source.operator.pickup_operator import PickupOperator
from source.interaction.minimap_tracker import tracker

class MissionExecutor(BaseThreading):
    def __init__(self):
        super().__init__()
        self.CFCF = collector_flow_upgrad.CollectorFlowController()
        self._add_sub_threading(self.CFCF,start=False)
        self.TMCF = teyvat_move_flow_upgrad.TeyvatMoveFlowController()
        self._add_sub_threading(self.TMCF,start=False)
        self.PUO = PickupOperator()
        self._add_sub_threading(self.PUO,start=False)
        self.setName(__name__)
        self.last_move_along_position = [99999,99999]

    def get_path_file(self, path_file_name:str):
        return load_json(path_file_name+".json","assets\\TeyvatMovePath")
    
    def move(self, MODE:str = None,stop_rule:int = None,target_posi:list = None,path_dict:dict = None,to_next_posi_offset:float = None,special_keys_posi_offset:float = None,reaction_to_enemy:str = None,is_tp:bool=None,is_reinit:bool=None):
        self.TMCF.reset()
        self.TMCF.set_parameter(MODE=MODE,stop_rule=stop_rule,target_posi=target_posi,path_dict=path_dict,to_next_posi_offset=to_next_posi_offset,special_keys_posi_offset=special_keys_posi_offset,reaction_to_enemy=reaction_to_enemy,is_tp=is_tp,is_reinit=is_reinit)
        self.TMCF.start_flow()
        while 1:
            time.sleep(0.2)
            if self.TMCF.get_working_statement() == False:
                break
    
    def move_straight(self, position, is_tp = False):
        self.move(MODE="AUTO", target_posi=position, is_tp = is_tp)
        
    def move_along(self, path, is_tp = None):
        path_dict = self.get_path_file(path)
        is_reinit = True
        
        if is_tp is None:
            if euclidean_distance(self.last_move_along_position, path_dict["start_position"]) >= 50:
                is_tp = True
            else:
                is_tp = False
                is_reinit = False

        self.move(MODE="PATH", path_dict = path_dict, is_tp = is_tp, is_reinit=is_reinit)
        self.last_move_along_position = path_dict["end_position"]
    def combat(self):
        pass

    def pickup_once(self):
        self.PUO.pickup_recognize()
    
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
    
    def start_thread(self):
        self.PUO.start()
        self.CFCF.start()
        self.TMCF.start()
    
    def loop(self):
        self.start_thread()
        self.exec_mission()
        self.pause_threading()
    


