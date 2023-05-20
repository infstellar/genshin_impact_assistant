from source.util import *
from common import timer_module
from source.flow import flow_state as ST
from source.interaction.interaction_core import itt
from source.pickup import pickup_operator
from source.interaction.minimap_tracker import tracker
from source.controller import combat_controller
from funclib.err_code_lib import ERR_PASS, ERR_STUCK, ERR_COLLECTOR_FLOW_TIMEOUT
from source.util import *
from source.flow.flow_template import FlowController, FlowTemplate, FlowConnector, EndFlowTemplate
import source.flow.flow_code as FC
from source.common import timer_module
from source.funclib import movement
from source.funclib import combat_lib
from source.funclib.err_code_lib import *
from source.interaction.interaction_core import itt

COLLECTION = 0
ENEMY = 1
MINERAL = 2

MODE_PATH = "PATH"
MODE_AUTO = "AUTO"

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
        self.MODE = "PATH"
        self.collection_name = ""
        self.collector_type = COLLECTION
        self.is_combat = True
        self.is_activate_pickup = False
        self.pickup_points = []

        self.combat_stop_func = combat_lib.CSDL.get_combat_state
        self.pickup_points_index = 0

        self.puo = pickup_operator.PickupOperator()
        self.cct = combat_controller.CombatController()

        
    
    def reset(self):
        self.MODE = "PATH"
        self.collection_name = ""
        self.combat_stop_func = combat_lib.CSDL.get_combat_state
        self.collector_type = COLLECTION
        self.is_combat = True
        self.is_activate_pickup = False
        self.pickup_points = []
        
        self.pickup_points_index = 0
        self.puo.set_search_mode(0)
   

    def stop_combat(self):
        self.cct.pause_threading()
    def start_combat(self):
        self.stop_pickup()
        self.cct.continue_threading()
    def stop_pickup(self):
        self.puo.pause_threading()
    def start_pickup(self):
        self.stop_combat()
        self.puo.continue_threading()
    def stop_all(self):
        self.stop_pickup()
        self.stop_combat()
        time.sleep(2)
    
class CollectionCombat(FlowTemplate):
    def __init__(self, upper: CollectorFlowConnector):
        super().__init__(upper, flow_id=ST.COLLECTION_COMBAT, next_flow_id=ST.COLLECTION_PICKUP, flow_timeout_time=300)
        self.upper=upper
        self.waiting_enemy_timer = timer_module.AdvanceTimer(30)
        
    def state_init(self):
        self.waiting_enemy_timer.reset()
        return super().state_init()
    
    def state_before(self):
        if not self.upper.is_combat:
            self._set_rfc(FC.END)
            return
        if combat_lib.CSDL.get_combat_state():
            self.upper.start_combat()
            self._next_rfc()
        elif self.waiting_enemy_timer.reached():
            self._set_rfc(FC.END)
            
    def state_in(self):
        if self.upper.combat_stop_func() == False and self.waiting_enemy_timer.reached():
            self.upper.stop_combat()
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
        super().__init__(upper, flow_id=ST.COLLECTION_PICKUP, next_flow_id=ST.END_COLLECTOR, flow_timeout_time=timeout_time)
    
    def state_before(self):
        
        if len(self.upper.pickup_points) > self.upper.pickup_points_index:
            movement.move_to_position(self.upper.pickup_points[self.upper.pickup_points_index])
            r = self.upper.puo.pickup_recognize()
            self.upper.pickup_points_index += 1
            logger.debug(f"pickup point:{self.upper.pickup_points[self.upper.pickup_points_index]}, {r}")
        else:
            if self.upper.is_activate_pickup:
                self.upper.puo.set_search_mode(1)
                self.upper.start_pickup()
                self.upper.puo.reset_err_code()
                self.flow_timeout.reset() # IMPORTANT
                self.IN_PICKUP_COLLECTOR_timeout.reset()
                self.while_sleep = 0.2
                self._next_rfc()
            else:
                self._set_rfc(FC.END)
    
    def state_in(self):
        if self.upper.puo.pause_threading_flag:
            self._next_rfc()
        
        if self.IN_PICKUP_COLLECTOR_timeout.istimeout():
            logger.info(f"IN_PICKUP_COLLECTOR timeout: {self.IN_PICKUP_COLLECTOR_timeout.timeout_limit}")
            logger.info(f"collect in xxx failed.")
            self._next_rfc()
            self._set_nfid(ST.END_COLLECTOR)
            self.upper.stop_pickup()
        if combat_lib.CSDL.get_combat_state():
            self.upper.stop_pickup()
            self._set_nfid(ST.COLLECTION_COMBAT)
            self._set_rfc(FC.END)
        
        

class EndCollector(EndFlowTemplate):
    def __init__(self, upper: CollectorFlowConnector):
        super().__init__(upper, flow_id=ST.END_COLLECTOR, err_code_id=ERR_PASS)
        
    def state_init(self):
        itt.key_up('w')
        return super().state_init()

    
    
class CollectorFlowController(FlowController):
    def __init__(self):
        self.flow_connector=CollectorFlowConnector()
        super().__init__(self.flow_connector, current_flow_id=ST.COLLECTION_COMBAT, flow_name="CollectorFlowController")
        
        # self._add_sub_threading(self.flow_connector.tmf)
        self._add_sub_threading(self.flow_connector.puo)
        self._add_sub_threading(self.flow_connector.cct)
        
        # self.append_flow(MoveToCollection_FollowPath(self.flow_connector))
        self.append_flow(CollectionCombat(self.flow_connector))
        self.append_flow(PickUpCollection(self.flow_connector))
        self.append_flow(EndCollector(self.flow_connector))
        
    def set_parameter(  
            self,
            MODE = None,
            collection_name =  None,
            collector_type =  None,
            is_combat =  None,
            combat_stop_func = None,
            is_activate_pickup =  None,
            pickup_points = None
            ):
        if MODE != None:
            self.flow_connector.MODE = MODE
        if collection_name != None:
            self.flow_connector.collection_name = collection_name
        if collector_type != None:
            self.flow_connector.collector_type = collector_type
        if is_combat != None:
            self.flow_connector.is_combat = is_combat
        if is_activate_pickup != None:
            self.flow_connector.is_activate_pickup = is_activate_pickup
        if pickup_points != None:
            self.flow_connector.pickup_points = pickup_points
        if combat_stop_func != None:
            self.flow_connector.combat_stop_func = combat_stop_func
        

    def reset(self):
        self.current_flow_id = ST.COLLECTION_COMBAT
        return super().reset()
    



if __name__ == '__main__':
    
    cfc = CollectorFlowController()
    cfc.set_parameter(is_activate_pickup=True) # collection_path_list=load_json("1678014849.9312954", "config\\collection_path")
    cfc.start()
    
    while 1:
        time.sleep(1)
        