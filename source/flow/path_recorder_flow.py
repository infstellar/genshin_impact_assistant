from source.util import *
import keyboard
from source.flow.flow_template import FlowController, FlowTemplate, FlowConnector, EndFlowTemplate
import source.flow.flow_code as FC, source.flow.flow_state as ST
from source.interaction.minimap_tracker import tracker
from source.funclib import movement, generic_lib, collector_lib
from source.funclib.err_code_lib import *
from source.interaction.interaction_core import itt
import pytz, datetime
from source.ui.ui import ui_control
from source.ui import page as UIPage
from common.timer_module import AdvanceTimer


class PathRecorderConnector(FlowConnector):
    def __init__(self):
        super().__init__()


        # self.total_collection_list = []
        self.checkup_stop_func = None
        self.collection_path_dict = {
            "time":"",
            "name":"",
            "start_position":[],
            "end_position":[],
            "break_position":[],
            "position_list":[]
        }

        self.min_distance = 1
        # self.set_hotkey()
        self.path_name = ""
        self.last_direction = 999
        self.is_pickup_mode = False
        self.coll_name = ""
        '''
        Template:
        {
            "name":"",
            "start_position":[],
            "end_position":[],
            "break_position":[],
            "position_list":[
                {
                    "position":list,
                    "motion":str, include 'move'(or 'walk'), 'swim', 'climb', 'fly'.
                    "id":int
                    "special_key":str
                }, ...
            ]
        }

        '''

    # def set_hotkey(self):
    #     self.listener.start()

    # def unset_hotkey(self):
    #     self.listener.stop()
    #     pass

    # def _add_key_to_dict(self, key):
    #     if key == KeyCode.from_char('f'):
    #         key = 'f'
    #     elif key == Key.space:
    #         key = 'space'
    #     elif key == KeyCode.from_char('x'):
    #         key = 'x'
    #     elif key == Key.shift:
    #         key = 'shift'
    #     elif key == KeyCode.from_char('e'):
    #         key = 'e'
    #     else:
    #         return
    #     curr_posi = tracker.get_position()
    #     self.collection_path_dict["position_list"].append(
    #         {
    #             "position":list(curr_posi),
    #             "motion":None,
    #             "id":len(self.collection_path_dict["position_list"])+1,
    #             "special_key":key
    #         }
    #     )
    #     # self.collection_path_dict["all_position"].append(curr_posi)
    #     logger.info(t2t("special key added:")+
    #                 str(key)
    #                 )


class PathRecorderCore(FlowTemplate):
    
    
    
    def __init__(self, upper: PathRecorderConnector):
        super().__init__(upper,flow_id=ST.PATH_RECORDER ,next_flow_id=ST.PATH_RECORDER_END)

        keyboard.add_hotkey('\\', self._start_stop_recording)
        self.COLLECTION_POSITION = []
        for i in load_json("all_position.json", fr"{ROOT_PATH}/assets/POI_JSON_API"):
            self.COLLECTION_POSITION.append(tracker.convert_kongying_to_cvAutoTrack(i))
        self.upper = upper
        self.enter_flag = False
        self.upper.while_sleep = 0.05
        self.record_index=0
        self.pickup_icon_timer = AdvanceTimer(1).reset().start()
        self.used_collection_position = []
        # self.all_position = []

    def _add_posi_to_dict(self, posi:list):
        curr_motion = movement.get_current_motion_state()
        self.upper.collection_path_dict["position_list"].append(
            {
                "position":posi,
                "motion":curr_motion,
                "id":len(self.upper.collection_path_dict["position_list"])+1,
                "special_key":None
            }
        )
        # self.upper.collection_path_dict["all_position"].append(posi)
        logger.info(t2t("position added:")+
                    f"{posi} {curr_motion}"
                    )

    def get_all_position(self, posi_dict):
        all_posi = []
        for i in posi_dict["position_list"]:
            all_posi.append(i["position"])
        return all_posi
    
    def state_init(self):
        pass
        # self._next_rfc()

    def state_before(self):

        self.upper.collection_path_dict = {
            "name":"",
            "time":"",
            "start_position":[],
            "break_position":[],
            "end_position":[],
            "position_list":[],
            "additional_info":{
                "pickup_points":[]
            }
        }
        self.force_add_flag = False
        if self.upper.coll_name != "":
            self.COLLECTION_POSITION = collector_lib.load_items_position(self.upper.coll_name)
            self.COLLECTION_POSITION = [i['position'] for i in self.COLLECTION_POSITION]
            self.force_add_flag = True
        self.enter_flag = False
        self.used_collection_position = []
        self.record_index=0
        self.pickup_icon_timer = AdvanceTimer(1).reset().start()
        # if not 
        # tracker.reinit_smallmap()
        curr_posi = tracker.get_position()
        self._add_break_position(curr_posi)
        self._next_rfc()

    def _start_stop_recording(self):
        if self.rfc == FC.INIT:
            self.rfc = FC.BEFORE
            logger.info(t2t("ready to start recording"))
        if self.rfc == FC.IN:
            self.rfc = FC.AFTER
            logger.info(t2t("ready to stop recording"))

    def _fix_position(self, p, offset=9.3):
        ed_list = quick_euclidean_distance_plist(p, self.COLLECTION_POSITION)
        if min(ed_list)<offset:
            rp = self.COLLECTION_POSITION[np.argmin(ed_list)]
            if list(rp) in self.used_collection_position:
                logger.info(f"position refix fail: {rp} used.")
                return p,False
            else:
                logger.info(f"position refix succ: {p} -> {rp}")
                self.used_collection_position.append(list(rp))
                return rp,True
        else:
            if min(ed_list)<15:
                logger.info(f"position refix fail: {p} {self.COLLECTION_POSITION[np.argmin(ed_list)]} 9<{min(ed_list)}<15")
            return p,False
    
    def _add_break_position(self, posi, f_exist=False, is_end = False):
        
        bpindex = len(self.upper.collection_path_dict["break_position"])
        if len(self.upper.collection_path_dict["break_position"])==0:
            self.upper.collection_path_dict["break_position"].append(list(posi))
            logger.info(f"break position added {posi}")
        elif (abs(euclidean_distance(posi,self.upper.collection_path_dict["break_position"][-1])) >= 5.2):
            if self.upper.is_pickup_mode:
                posi,succ = self._fix_position(posi)
                if self.force_add_flag:
                    if succ:
                        f_exist = True
            self.upper.collection_path_dict["break_position"].append(list(posi))
            logger.info(f"break position added {posi}")
            
            if self.upper.is_pickup_mode and f_exist:
                self.upper.collection_path_dict["additional_info"]["pickup_points"].append(bpindex)
                logger.info(f"pickup bp added: {bpindex}")
        else:
            logger.warning(f"break position too close")
            if is_end and self.upper.is_pickup_mode and self.force_add_flag:
                posi,succ = self._fix_position(posi, offset=20)
                if succ:
                    self.upper.collection_path_dict["break_position"].append(list(posi))
                    self.upper.collection_path_dict["additional_info"]["pickup_points"].append(bpindex)
                    logger.info(f"break position added {posi}")
                    logger.info(f"last pickup bp added: {bpindex}")
            if self.upper.is_pickup_mode:
                if f_exist:
                    if bpindex-1 not in self.upper.collection_path_dict["additional_info"]["pickup_points"]:
                        self.upper.collection_path_dict["additional_info"]["pickup_points"].append(bpindex-1)
                        logger.info(f"pickup bp added to bp-1: {bpindex-1}")
    
    def state_in(self):
        if not ui_control.verify_page(UIPage.page_main):
            return super().state_in()
        all_posi = self.get_all_position(self.upper.collection_path_dict)
        curr_posi = tracker.get_position()
        if self.upper.is_pickup_mode and not self.force_add_flag:
            if generic_lib.f_recognition():
                logger.info(f"found f")
                self._add_break_position(curr_posi, f_exist=True)
        curr_direction = tracker.get_direction()
        if len(all_posi)>10:
            min_dist = quick_euclidean_distance_plist(curr_posi, all_posi[-10:-1]).min()
        elif len(all_posi)>0:
            min_dist = quick_euclidean_distance_plist(curr_posi, all_posi).min()
        else:
            min_dist = 99999

        if min_dist >= self.upper.min_distance:
            self._add_posi_to_dict(list(curr_posi))

        if abs(movement.calculate_delta_angle(curr_direction, self.upper.last_direction)) >= 3.5:
            self._add_break_position(curr_posi)
            self.upper.last_direction = curr_direction
        
        if not self.enter_flag:
            logger.info(t2t("start recording"))
            self.enter_flag = True
            self.upper.collection_path_dict["start_position"]=list(tracker.get_position())
        return super().state_in()

    def _fix_bps(self):
        logger.info(f'bps fix {len(self.upper.collection_path_dict["break_position"])} -> {self.upper.collection_path_dict["additional_info"]["pickup_points"][-1]+1}')
        self.upper.collection_path_dict["break_position"] = \
        self.upper.collection_path_dict["break_position"]   \
        [:self.upper.collection_path_dict["additional_info"]["pickup_points"][-1]+1]
        return True
    
    def state_after(self):
        # self.upper.total_collection_list.append(self.upper.collection_path_dict)
        curr_posi = tracker.get_position()
        self.upper.collection_path_dict["end_position"]=list(curr_posi)
        self._add_break_position(curr_posi, is_end=True)
        tz = pytz.timezone('Etc/GMT-8')
        t = datetime.datetime.now(tz)
        date = t.strftime("%Y%m%d%H%M%S")
        jsonname = f"{self.upper.path_name}{date}i{self.record_index}.json"
        self.record_index+=1
        # if self.upper.is_pickup_mode:
        #     self._fix_bps() # 这个功能好像与is_end=True功能冲突...
        save_json(self.upper.collection_path_dict,json_name=jsonname,default_path=f"assets\\TeyvatMovePath")
        logger.info(f"recording save as {jsonname}")
        self.rfc = FC.INIT


class PathRecorderEnd(EndFlowTemplate):
    def __init__(self, upper: FlowConnector):
        super().__init__(upper, flow_id=ST.PATH_RECORDER_END, err_code_id=ERR_PASS)

class PathRecorderController(FlowController):
    def __init__(self):
        super().__init__(PathRecorderConnector(), current_flow_id =  ST.PATH_RECORDER)
        self.flow_connector = self.flow_connector # type: PathRecorderConnector
        self.flow_connector.checkup_stop_func = self.checkup_stop_func

        self.pc = PathRecorderCore(self.flow_connector)

        self.append_flow(self.pc)   
        self.append_flow(PathRecorderEnd(self.flow_connector))

    def reset(self):
        pass

if __name__ == '__main__':
    pn = input("input your path name")
    prc = PathRecorderController()
    prc.flow_connector.path_name = pn
    prc.start()
    logger.info(f"Load over.")
    logger.info(f"ready to start.")
    while 1:
        time.sleep(1)