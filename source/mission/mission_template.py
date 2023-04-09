from source.util import *
from source.flow import collector_flow_upgrad, teyvat_move_flow_upgrad
from source.common.base_threading import BaseThreading
from source.operator.pickup_operator import PickupOperator
from source.interaction.minimap_tracker import tracker
from source.funclib import combat_lib, generic_lib, movement
from source.interaction.interaction_core import itt
from source.funclib.err_code_lib import ERR_PASS
from source.common.timer_module import AdvanceTimer
from source.controller.combat_controller import CombatController
from source.map.map import genshin_map


ERR_FAIL = "FAIL"
class CharacterNotFound(Exception):
    pass

class MissionEnd(Exception):pass
class CollectError(Exception):pass
class TeyvatMoveError(Exception):pass
class PickUpOperatorError(Exception):pass

class MissionExecutor(BaseThreading):
    def __init__(self, is_CFCF=False, is_TMCF=False, is_PUO=False, is_CCT=False):
        super().__init__()
        self.is_CFCF=is_CFCF
        self.is_TMCF=is_TMCF
        self.is_PUO=is_PUO
        self.is_CCT=is_CCT
        if is_CFCF:
            self.CFCF = collector_flow_upgrad.CollectorFlowController()
            self._add_sub_threading(self.CFCF, start=False)
        self.picked_list = []
        if is_TMCF:
            self.TMCF = teyvat_move_flow_upgrad.TeyvatMoveFlowController()
            self._add_sub_threading(self.TMCF, start=False)
        if is_PUO:
            self.PUO = PickupOperator()
            self._add_sub_threading(self.PUO, start=False)
        if is_CCT:
            self.CCT = CombatController()
            self._add_sub_threading(self.CCT, start=False)
        self.setName(__name__)
        self.last_move_along_position = [99999,99999]

        self._detect_exception_timer = AdvanceTimer(limit=2)
        self.exception_flag = False
        self.exception_list = {
            "FoundEnemy":False,                     
            "CharaDied":False,
            "LowHP":False
            }
        self.itt = itt

    def refresh_picked_list(self):
        self.picked_list = []
    
    def _detect_exception(self):
        if self.exception_list["FoundEnemy"]:
            if combat_lib.CSDL.is_low_health:
                self.exception_flag = True
                logger.warning(f"Detected Enemy Attack, Mission Break")
        if self.exception_list["LowHP"]:
            if combat_lib.CSDL.is_low_health:
                self.exception_flag = True
                logger.warning(f"HP Low, Mission Break")
        if self.exception_list["CharaDied"]:
            pass
        
    def _is_exception(self):
        if self._detect_exception_timer.reached_and_reset():
            self._detect_exception()
        return self.exception_flag    
    
    def _handle_exception(self):
        if self.checkup_stop_func():raise MissionEnd
        if self.exception_flag:
            logger.info(f"Handling exception: recover")
            # 跑到七天神像去回血
            tracker.reinit_smallmap()
            curr_posi = list(tracker.get_position())
            target_posi = list(tracker.bigmap_tp(posi=curr_posi, tp_type=["Statue"]).tianli)
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
    
    def move(self, MODE:str = None,
             stop_rule:int = None,
             target_posi:list = None,
             path_dict:dict = None,
             to_next_posi_offset:float = None,
             special_keys_posi_offset:float = None,
             reaction_to_enemy:str = None,
             is_tp:bool = None,
             is_reinit:bool = None, 
             is_precise_arrival:bool = None,
             stop_offset:int = None):
        self.TMCF.reset()
        self.TMCF.set_parameter(MODE=MODE,stop_rule=stop_rule,target_posi=target_posi,path_dict=path_dict,to_next_posi_offset=to_next_posi_offset,special_keys_posi_offset=special_keys_posi_offset,reaction_to_enemy=reaction_to_enemy,is_tp=is_tp,is_reinit=is_reinit,is_precise_arrival=is_precise_arrival,stop_offset=stop_offset)
        self.TMCF.start_flow()
        while 1:
            time.sleep(0.6)
            if self.TMCF.pause_threading_flag:
                break
            if self._is_exception():
                self.TMCF.pause_threading()
                break
        if self.TMCF.get_and_reset_err_code() != ERR_PASS:
            self.exception_flag = True
        return self._handle_exception()
        
    def move_straight(self, position, is_tp = False, is_precise_arrival=False, stop_rule=None):
        if isinstance(position[0], int) or isinstance(position[0], float):
            p = position
        elif isinstance(position[0], str):
            path_dict = self.get_path_file(position[0])
            p = path_dict[position[1]]
        r = self.move(MODE="AUTO", target_posi=p, is_tp = is_tp, is_precise_arrival=is_precise_arrival, stop_rule=stop_rule)
        return r
        
    def move_along(self, path, is_tp = None, is_precise_arrival=False):
        path_dict = self.get_path_file(path)
        is_reinit = True
        
        if is_tp is None:
            if euclidean_distance(self.last_move_along_position, path_dict["start_position"]) >= 50:
                is_tp = True
            else:
                is_tp = False
                is_reinit = False

        r = self.move(MODE="PATH", path_dict = path_dict, is_tp = is_tp, is_reinit=is_reinit, is_precise_arrival=is_precise_arrival)
        self.last_move_along_position = path_dict["end_position"]
        return r
    def start_combat(self, mode="Normal"):
        self.CCT.mode=mode
        self.CCT.continue_threading()
    
    def stop_combat(self):
        self.CCT.pause_threading()
    
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
    
    def circle_search(self, center_posi, stop_rule='F'):
        """进入一个循环，以中心坐标为圆心向外移动搜索。当符合stop_rule时退出。

        Args:
            center_posi (_type_): 中心坐标
            stop_rule (str, optional): 停止条件. Defaults to 'F'.

        Returns:
            _type_: _description_
        """
        points = get_circle_points(center_posi[0],center_posi[1])
        itt.key_down('w')
        for p in points:
            while 1:
                if self.checkup_stop_func():return
                movement.move_to_posi_LoopMode(p, self.checkup_stop_func)
                if euclidean_distance(p, genshin_map.get_position())<=2:
                    logger.debug(f"circle_search: {p} arrived")
                    break
                if stop_rule == 'F':
                    if generic_lib.f_recognition():
                        itt.key_up('w')
                        return True
                elif stop_rule == "Combat":
                    if combat_lib.CSDL.get_combat_state():
                        itt.key_up('w')
                        return True
        itt.key_up('w')
        return False
                
    
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
        
    def _reg_exception_low_hp(self, state=True):
        self.exception_list["LowHP"] = state
    
    def switch_character_to(self, name:str):
        r = combat_lib.get_characters_name()
        curr_n = combat_lib.get_current_chara_num(self.checkup_stop_func)
        if name in r:
            if curr_n != r.index(name)+1:
                itt.key_press(str(r.index(name)+1))
        else:
            logger.warning(f"{name} does not exist in current party.")
            r = combat_lib.set_party_setup(name)
            if not r:
                raise CharacterNotFound(f"Character {name} Not Found")
            
        
    def start_thread(self):
        if self.is_CFCF: self.CFCF.start()
        if self.is_TMCF: self.TMCF.start()
        if self.is_PUO: self.PUO.start()
        if self.is_CCT: self.CCT.start()
    
    def loop(self):
        self.start_thread()
        # self.mission_result = False
        try:
            self.exec_mission()
        except MissionEnd as e:
            logger.info("Mission end by exception.")
        # except CollectError as e:
        #     logger.error("Mission end: CollectError")
        # except TeyvatMoveError as e:
        #     logger.error("Mission end: TeyvatMoveError")
        except Exception as e:
            logger.error(f"ERROR in execute mission: {self.name} {e}")
            logger.exception(e)

        itt.key_up('w') # 让所有按键起飞
        self.pause_threading()
    
if __name__ == '__main__':
    me = MissionExecutor(is_CCT=True)
    # me.exception_flag = True
    # me._handle_exception()
    # me.start_combat(mode="Shield")
    me.circle_search([ 3834.9886,-6978.8201])
    while 1: time.sleep(1)

