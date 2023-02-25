from source.util import *
import keyboard
from source.flow.flow_template import FlowController, FlowTemplate, FlowConnector, EndFlowTenplate
import source.flow.flow_code as FC
from source.interaction.minimap_tracker import tracker
from source.controller import combat_loop
from common import flow_state as ST, timer_module
from source.funclib import generic_lib, movement, combat_lib
from source.funclib.err_code_lib import *
from source.manager import posi_manager as PosiM, asset
from source.interaction.interaction_core import itt

class CollectionPathConnector(FlowConnector):
    def __init__(self):
        super().__init__()

        

        self.collection_path_dict = {
            "all_position":[],
            "position_list":[],
            "special_keys":[]
        }

        self.min_distance = 1

        '''
        Template:
        {
        "all_position":[
            [point x, point y],
            [point x, point y],
            [point x, point y],
            ...
        ],
        "position_list":[
            {
                "position":list,
                "motion":str, include 'move'(or 'walk'), 'swim', 'climb', 'fly'.
                "id":int
            }, ...
        ],
        "special_keys":[
            {
                "position":list,
                "key name":str, include 'space', 'left click', 'left shift', 'x'.
                "id":int
            }, ...
        ]       
        }

        '''

    def set_hotkey(self):
        keyboard.add_hotkey("w", self._add_key_to_dict, args=('w',))
        keyboard.add_hotkey("space", self._add_key_to_dict, args=('space',))
        keyboard.add_hotkey("x", self._add_key_to_dict, args=('x',))
        keyboard.add_hotkey("shift", self._add_key_to_dict, args=('shift',))

    def unset_hotkey(self):
        keyboard.remove_hotkey("w")
        keyboard.remove_hotkey("space")
        keyboard.remove_hotkey("x")
        keyboard.remove_hotkey("shift")

    def _add_key_to_dict(self, key:str):
        curr_posi = tracker.get_position()
        if key == 'w':
            pass
        elif key == 'space':
            pass
        elif key == 'x':
            pass
        elif key == 'shift':
            pass
        curr_posi = tracker.get_position()
        self.collection_path_dict["special_keys"].append(
            {
                "position":curr_posi,
                "key name":key,
                "id":len(self.collection_path_dict["special_keys"])+1
            }
        )


class CollectionPathRecord(FlowTemplate):
    def __init__(self, upper: CollectionPathConnector):
        super().__init__(upper,flow_id=ST.COLLECTION_PATH_RECORD ,next_flow_id=ST.COLLECTION_PATH_END)

        

        self.upper = upper
        
    def _add_posi_to_dict(self, posi:list):
        curr_motion = movement.get_current_motion_state()
        self.upper.collection_path_dict["position_list"].append(
            {
                "position":posi,
                "motion":curr_motion,
                "id":len(self.upper.collection_path_dict["position_list"])+1
            }
        )
        self.upper.collection_path_dict["all_position"].append(posi)

    

    def state_in(self):

        all_posi = self.upper.collection_path_dict["all_position"]
        curr_posi = tracker.get_position()
        
        min_dist = quick_euclidean_distance_plist(curr_posi, all_posi).min()

        if min_dist >= self.upper.min_distance:
            self._add_posi_to_dict(curr_posi)

        return super().state_in()
        

