from source.util import *
from source.flow import collector_flow_upgrad, teyvat_move_flow_upgrad
from source.common.base_threading import BaseThreading
from source.operator.pickup_operator import PickupOperator
from source.interaction.minimap_tracker import tracker
from source.funclib import combat_lib, generic_lib
from source.interaction.interaction_core import itt
from source.funclib.err_code_lib import ERR_PASS
from source.common.timer_module import AdvanceTimer


ERR_FAIL = "FAIL"
class CharacterNotFound(Exception):
    pass
    

class MissionExecutor(BaseThreading):
    def __init__(self):
        super().__init__()
        self.CFCF = collector_flow_upgrad.CollectorFlowController()
        self._add_sub_threading(self.CFCF,start=False)
        self.picked_list = []
        self.TMCF = teyvat_move_flow_upgrad.TeyvatMoveFlowController()
        self._add_sub_threading(self.TMCF,start=False)
        self.PUO = PickupOperator()
        self._add_sub_threading(self.PUO,start=False)
        self.setName(__name__)
        self.last_move_along_position = [99999,99999]

        self._detect_exception_timer = AdvanceTimer(limit=2)
        self.exception_flag = False
        self.exception_list = {
            "FoundEnemy":False,                     
            "CharaDied":False
            }

    def refresh_picked_list(self):
        self.picked_list = []
    
    def _detect_exception(self):
        if self.exception_list["FoundEnemy"]:
            if combat_lib.CSDL.is_low_health:
                self.exception_flag = True
                logger.warning(f"Detected Enemy Attack, Mission Break")
        if self.exception_list["CharaDied"]:
            pass
        
    def _is_exception(self):
        if self._detect_exception_timer.reached_and_reset():
            self._detect_exception()
        return self.exception_flag    
    
    def _handle_exception(self):
        if self.exception_flag:
            logger.info(f"Handling exception: recover")
            # 跑到七天神像去回血
            tracker.reinit_smallmap()
            curr_posi = list(tracker.get_position())
            target_posi = list(tracker.bigmap_tp(posi=curr_posi, tp_type=["Statue"]))
            self.TMCF.reset()
            self.TMCF.set_parameter(MODE="AUTO",stop_rule=1,target_posi=target_posi,is_tp=False)
            self.TMCF.start_flow()
            while 1:
                time.sleep(0.2)
                if self.TMCF.get_working_statement() == False:
                    break
            itt.delay(5,comment="Waiting for revival")
            self.exception_flag = False
            logger.info(f"End of handling exception")
            return ERR_FAIL
        else:
            return ERR_PASS
    
    def get_path_file(self, path_file_name:str):
        return load_json(path_file_name+".json","assets\\TeyvatMovePath")
    
    def move(self, MODE:str = None,stop_rule:int = None,target_posi:list = None,path_dict:dict = None,to_next_posi_offset:float = None,special_keys_posi_offset:float = None,reaction_to_enemy:str = None,is_tp:bool=None,is_reinit:bool=None, is_precise_arrival:bool=None):
        self.TMCF.reset()
        self.TMCF.set_parameter(MODE=MODE,stop_rule=stop_rule,target_posi=target_posi,path_dict=path_dict,to_next_posi_offset=to_next_posi_offset,special_keys_posi_offset=special_keys_posi_offset,reaction_to_enemy=reaction_to_enemy,is_tp=is_tp,is_reinit=is_reinit,is_precise_arrival=is_precise_arrival)
        self.TMCF.start_flow()
        while 1:
            time.sleep(0.2)
            if self.TMCF.pause_threading_flag:
                break
            if self._is_exception():
                self.TMCF.pause_threading()
                break
        if self.TMCF.get_and_reset_err_code() != ERR_PASS:
            self.exception_flag = True
        return self._handle_exception()
        
    def move_straight(self, position, is_tp = False):
        r = self.move(MODE="AUTO", target_posi=position, is_tp = is_tp)
        return r
        
    def move_along(self, path, is_tp = None):
        path_dict = self.get_path_file(path)
        is_reinit = True
        
        if is_tp is None:
            if euclidean_distance(self.last_move_along_position, path_dict["start_position"]) >= 50:
                is_tp = True
            else:
                is_tp = False
                is_reinit = False

        r = self.move(MODE="PATH", path_dict = path_dict, is_tp = is_tp, is_reinit=is_reinit)
        self.last_move_along_position = path_dict["end_position"]
        return r
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
            if self.CFCF.pause_threading_flag == True:
                break
            if self._is_exception():
                self.CFCF.pause_threading()
                break
        if self.CFCF.get_and_reset_err_code() != ERR_PASS:
            self.exception_flag = True
        else:
            self.picked_list.append(self.CFCF.flow_connector.puo.pickup_item_list.copy())
            self.CFCF.flow_connector.puo.reset_pickup_item_list()
        return self._handle_exception()
    
    def start_pickup(self):
        self.PUO.continue_threading()
    
    def stop_pickup(self):
        self.PUO.pause_threading()
            
    def exec_mission(self):
        pass
    
    def _reg_exception_found_enemy(self, state=True):
        self.exception_list["FoundEnemy"] = state

    def _reg_exception_chara_died(self, state=True):
        self.exception_list["CharaDied"] = state
    
    def switch_character_to(self, n:str):
        r = generic_lib.get_characters_name()
        curr_n = combat_lib.get_current_chara_num(itt)
        if n in r:
            if curr_n != r.index(n)+1:
                itt.key_press(str(r.index(n)+1))
        else:
            raise CharacterNotFound(f"Character {n} Not Found")
        
    def start_thread(self):
        self.PUO.start()
        self.CFCF.start()
        self.TMCF.start()
    
    def loop(self):
        self.start_thread()
        try:
            self.exec_mission()
        except Exception as e:
            logger.error(f"ERROR in execute mission: {self.name} {e}")
        self.pause_threading()
    
if __name__ == '__main__':
    me = MissionExecutor()
    me.exception_flag = True
    me._handle_exception()

