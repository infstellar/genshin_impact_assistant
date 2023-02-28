from source.util import *
from common import flow_state as ST, timer_module
from source.interaction.interaction_core import itt
from source.operator import pickup_operator
from source.flow import teyvat_move_flow
from source.interaction.minimap_tracker import tracker
from source.controller import combat_loop
import numpy as np
from funclib.err_code_lib import ERR_PASS, ERR_STUCK, ERR_COLLECTOR_FLOW_TIMEOUT
from source.util import *
from source.flow.flow_template import FlowController, FlowTemplate, FlowConnector, EndFlowTenplate
import source.flow.flow_code as FC
from source.controller import combat_loop
from common import flow_state as ST, timer_module
from source.funclib import generic_lib, movement, combat_lib
from source.funclib.err_code_lib import *
from source.manager import asset
from source.interaction.interaction_core import itt

COLLECTION = 0
ENEMY = 1
MINERAL = 2

ALL_CHARACTER_DIED = 1

SUCC_RATE_WEIGHTING = 6


"""Flow:

MoveToCollection_FollowPath -> PickUpCollection (if activate pickup)
PickUpCollection -> MoveToCollection_FollowPath (forever)
MoveToCollection_FollowPath <- (if not activate pickup)
MoveToCollection_FollowPath -> EndCollector (if no more path exist)

"""

class CollectorFlowConnector(FlowConnector):
    def __init__(self):
        super().__init__()
        # self.MODE = "NAME"
        self.MODE = "PATH"
        self.collection_path_list = []
        self.collection_path_index = 0
        self.collection_name = ""
        self.to_next_posi_offset = 1.0*5 # For CVAT's low precision
        self.special_keys_posi_offset = 1.5
        self.collector_type = COLLECTION

        self.tmf = teyvat_move_flow.TeyvatMoveFlow()
        self.puo = pickup_operator.PickupOperator()
        chara_list = combat_lib.get_chara_list()
        self.cct = combat_loop.Combat_Controller(chara_list)
        

    def stop_combat(self):
        self.cct.pause_threading()
    def start_combat(self):
        self.stop_pickup()
        self.stop_walk()
        self.cct.continue_threading()
    def stop_pickup(self):
        self.puo.pause_threading()
    def start_pickup(self):
        self.stop_combat()
        self.stop_walk()
        self.puo.continue_threading()
    def stop_walk(self):
        self.tmf.pause_threading()
    def start_walk(self):
        self.stop_combat()
        self.stop_pickup()
        self.tmf.continue_threading()
    def stop_all(self):
        self.stop_pickup()
        self.stop_combat()
        self.stop_walk()
        time.sleep(2)
    

class MoveToCollection_Automatic(FlowTemplate):
    def __init__(self, upper: CollectorFlowConnector):
        super().__init__(upper, flow_id=ST.INIT_MOVETO_COLLECTOR, next_flow_id=ST.INIT_PICKUP_COLLECTOR)
        
    def state_init(self):
        
        pass

class TeleportToStartingPoint(FlowTemplate):
    pass

class MoveToCollection_FollowPath(FlowTemplate):
    def __init__(self, upper: CollectorFlowConnector):
        super().__init__(upper, flow_id=ST.INIT_MOVETO_COLLECTOR, next_flow_id=ST.INIT_PICKUP_COLLECTOR)
        self.upper = upper
        self.curr_path_index = 0
        self.special_key_points = None
        
        self.curr_path = []
        self.curr_path_index = 0
        
    def _exec_special_key_points(self):
        ret_list = []
        for i in self.upper.collection_path_list[self.upper.collection_path_index]["special_keys"]:
            ret_list.append(i["position"])
        self.special_key_points = ret_list
    
    def _do_special_key(self, curr_posi):
        """执行special key

        Args:
            curr_posi (_type_): _description_
        """
        if self.special_key_points == None:
            self._exec_special_key_points()
        if quick_euclidean_distance_plist(curr_posi, self.special_key_points).min() <= self.upper.special_keys_posi_offset:
            for i in self.upper.collection_path_list[self.upper.collection_path_index]["special_keys"]:
                if euclidean_distance(i["position"], curr_posi) <= self.upper.special_keys_posi_offset:
                    itt.key_press(i["key_name"])
    
    def state_before(self):
        self.curr_path = self.upper.collection_path_list[self.upper.collection_path_index]["position_list"]
        self.curr_path_index = 0
        itt.key_down('w')
        self._next_rfc()
    
    def state_in(self):
        target_posi = self.curr_path[self.curr_path_index]["position"]
        curr_posi = tracker.get_position()
        if euclidean_distance(target_posi, curr_posi) <= self.upper.to_next_posi_offset:
            if len(self.curr_path) - 1 > self.curr_path_index:
                self.curr_path_index += 1
                logger.debug(f"index {self.curr_path_index} posi {self.curr_path[self.curr_path_index]}")
            else:
                logger.info("path end")
                self._next_rfc()
        self._do_special_key(curr_posi)
        movement.change_view_to_posi(target_posi, stop_func = self.upper.checkup_stop_func)
        
            
    def state_after(self):
        if self.upper.collection_path_list[self.upper.collection_path_index]["is_activate_pickup"] == False:
            self.next_flow_id = self.flow_id
        else:
            pass
        if len(self.upper.collection_path_list)-1 > self.upper.collection_path_index:
            self.upper.collection_path_index += 1
        else:
            logger.info("all path end")
            self.next_flow_id = ST.END_COLLECTOR
        self._next_rfc()
        
class PickUpCollection(FlowTemplate):
    def __init__(self, upper: CollectorFlowConnector):
        self.upper = upper
        self.IN_PICKUP_COLLECTOR_timeout = timer_module.TimeoutTimer(45)
        if self.upper.collector_type == COLLECTION:
            timeout_time = 150
        elif self.upper.collector_type == ENEMY:
            self.upper.puo.max_distance_from_target = 60
            timeout_time = 300
        elif self.upper.collector_type == MINERAL:
            pass
        super().__init__(upper, flow_id=ST.INIT_PICKUP_COLLECTOR, next_flow_id=ST.INIT_MOVETO_COLLECTOR, flow_timeout_time=timeout_time)
    
    def state_before(self):
        if combat_lib.CSDL.get_combat_state() == False:
            self.upper.start_pickup()
            self.upper.puo.reset_err_code()
            self.flow_timeout.reset() # IMPORTANT
            self.while_sleep = 0.2
            self._next_rfc()
        else:
            self.upper.start_combat()
            self.while_sleep = 0.5
    
    def state_in(self):
        if self.upper.puo.pause_threading_flag:
            self._next_rfc()
        if self.IN_PICKUP_COLLECTOR_timeout.istimeout():
            logger.info(f"IN_PICKUP_COLLECTOR timeout: {self.IN_PICKUP_COLLECTOR_timeout.timeout_limit}")
            logger.info(f"collect in xxx failed.")
            self._next_rfc()
            self.upper.stop_pickup()
        if combat_lib.CSDL.get_combat_state():
            self.upper.stop_pickup()
            self.rfc = FC.BEFORE
        
        

class EndCollector(EndFlowTenplate):
    def __init__(self, upper: CollectorFlowConnector):
        super().__init__(upper, flow_id=ST.END_COLLECTOR, err_code_id=ERR_PASS)

    
    
class CollectorFlowController(FlowController):
    def __init__(self):
        self.flow_connector=CollectorFlowConnector()
        super().__init__(self.flow_connector, current_flow_id=ST.INIT_MOVETO_COLLECTOR)
        
        self._add_sub_threading(self.flow_connector.tmf)
        self._add_sub_threading(self.flow_connector.puo)
        self._add_sub_threading(self.flow_connector.cct)
        
        self.append_flow(MoveToCollection_FollowPath(self.flow_connector))
        self.append_flow(PickUpCollection(self.flow_connector))
        
    def set_parameter(self, collection_path_list = None, collection_name = None, to_next_posi_offset = None, special_keys_posi_offset = None):
        if collection_path_list != None:
            self.flow_connector.collection_path_list = collection_path_list
        if collection_name != None:
            self.flow_connector.collection_name = collection_name
        if to_next_posi_offset != None:
            self.flow_connector.to_next_posi_offset = to_next_posi_offset
        if special_keys_posi_offset != None:
            self.flow_connector.special_keys_posi_offset = special_keys_posi_offset



if __name__ == '__main__':
    
    cfc = CollectorFlowController()
    cfc.set_parameter(collection_path_list=load_json("1677407787.4955494", "config\\collection_path"))
    cfc.start()
    
    while 1:
        time.sleep(1)