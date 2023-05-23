from source.util import *
from common import flow_state as ST
from source.interaction.minimap_tracker import tracker
from source.funclib import collector_lib
import datetime
from source.ui.ui import ui_control
import source.ui.page as UIPage
from source.mission.mission_template import MissionExecutor, ERR_FAIL,ERR_PASS
from source.funclib.err_code_lib import ERR_NONE

META={
    'name':{
        'zh_CN':'通用自动采集',
        'en_US':'General Auto Collect'
    },
    'author':"GIA",
}

SUCC_RATE_WEIGHTING = 6
COLLECTION = 0
ENEMY = 1
MINERAL = 2
class MissionMain(MissionExecutor):
    
    def sort_by_distance_and_succrate(self, x):
        distance = euclidean_distance(x["position"], self.current_position)
        try:
            rate = float(self.collection_details[str(x["id"])]["succ_rate"])
        except KeyError as e:
            rate = 0.8
        if rate < 0.1:
            rate = 0.1
        ret = ((1/rate)*SUCC_RATE_WEIGHTING) * distance
        # logger.trace(f"ret: {ret} rate: {rate} distance:{distance} rate_weight: {(1/rate)*SUCC_RATE_WEIGHTING}")
        return ret
    
    def __init__(self):
        super().__init__(is_CFCF=True,is_PUO=True,is_TMCF=True)
        self.setName("MissionAutoCollector")
        
        self.collector_name = GIAconfig.Collector_CollectionName
        if GIAconfig.Collector_CollectionType == "COLLECTION":
            self.collector_type = COLLECTION
        elif GIAconfig.Collector_CollectionType == "ENEMY":
            self.collector_type = ENEMY
        self.collector_blacklist_id = load_json("collection_blacklist.json", default_path="config\\auto_collector", auto_create=True)
        self.collected_id = load_json("collected.json", default_path="config\\auto_collector", auto_create=True)
        self.shielded_id = []
        self.collection_id = 0
        try:
            self.shielded_id+=(self.collector_blacklist_id[self.collector_name])
        except:
            self.collector_blacklist_id[self.collector_name] = []
            save_json(self.collector_blacklist_id, "collection_blacklist.json", default_path="config\\auto_collector", sort_keys=False)
            
        try:
            self.shielded_id+=(self.collected_id[self.collector_name])
        except:
            self.collected_id[self.collector_name] = []
            save_json(self.collected_id, "collected.json", default_path="config\\auto_collector", sort_keys=False)

        if not os.path.exists(os.path.join(ROOT_PATH, "config\\auto_collector", "collection_log.json")):
            save_json({}, os.path.join(ROOT_PATH, "config\\auto_collector", "collection_log.json"))
        self.collection_log = load_json("collection_log.json", default_path="config\\auto_collector", auto_create=True)
        
        self.collector_posi_dict = []
        self.current_position = tracker.get_position()
        self.last_collection_posi = [9999,9999]
        # collector_lib.generate_masked_col_from_log()
        collector_lib.generate_collected_from_log()
        collector_lib.generate_col_succ_rate_from_log()
        logger.debug(f"generate collection_id_details succ")
        self.collection_details = load_json("collection_id_details.json", "config\\auto_collector", auto_create=True)
        
        
        self.collector_posi_dict = collector_lib.load_items_position(self.collector_name, blacklist_id=self.shielded_id)
        self.shielded_posi_list = collector_lib.load_items_position(self.collector_name, blacklist_id=self.shielded_id, ret_mode=1, check_mode=1)
        ui_control.ui_goto(UIPage.page_main)
        tracker.while_until_no_excessive_error()
        self.current_position = tracker.get_position()
        self.collection_details = load_json("collection_id_details.json", "config\\auto_collector", auto_create=True)
        self.collector_posi_dict.sort(key=self.sort_by_distance_and_succrate)
        logger.info("switch Flow to: BEFORE_MOVETO_COLLECTOR")
        self.current_state = ST.BEFORE_MOVETO_COLLECTOR
        self.collector_i = 0
    
    def _set_target_position(self):
        while 1:
            if self.checkup_stop_func():return
            self.collection_posi = self.collector_posi_dict[self.collector_i]["position"]
            self.collection_id = self.collector_posi_dict[self.collector_i]["id"]
            '''当两个collection坐标小于30时，认为是同一个。'''
            f1 = euclidean_distance(self.collection_posi, self.last_collection_posi) <= 30
            if len(self.shielded_posi_list)>0:
                f2 = euclidean_distance_plist(self.collection_posi, self.shielded_posi_list).min() <= 30
            else:
                f2=False
            if f1 or f2:
                if f1:
                    logger.info(f"collection id: {self.collection_id} ; collection position: {self.collection_posi} ; last collection position: {self.last_collection_posi}")
                if f2:
                    logger.info(f"collection id: {self.collection_id} ; collection position: {self.collection_posi} ; closest collection position distance: {euclidean_distance_plist(self.collection_posi, self.shielded_posi_list).min()}")
                logger.info(f"distance lower than 30, skip this collection.")
                self._set_collected_id()
                if not self._add_collection_i():
                    break
                continue
            logger.info("正在前往：" + self.collector_name)
            logger.info(f"物品id：{self.collection_id}")
            logger.info("目标坐标：" + str(self.collection_posi)+"当前坐标：" + str(self.current_position))
            break
    
    def _set_collected_id(self):
        self.collected_id[self.collector_name].append(self.collector_posi_dict[self.collector_i]["id"])
        save_json(self.collected_id, "collected.json", default_path="config\\auto_collector", sort_keys=False)
        
    
    def _add_logs(self,x):
        picked_list = []
        a = self.collection_log.setdefault(self.collector_name, [])
        picked_list = self.picked_list.copy()
        if not picked_list:
            picked_list.append('None')
        a.append({"time":str(datetime.datetime.now()),
                  "id": self.collection_id,
                  "error_code": x,
                  "picked item": picked_list})
        self.collection_log[self.collector_name] = a
        save_json(self.collection_log, "collection_log.json", default_path="config\\auto_collector")
        self.refresh_picked_list()
        self.PUO.reset_pickup_item_list()
    
    def _add_collection_i(self):
        if len(self.collector_posi_dict)-1 == self.collector_i:
            logger.info("exit")
            return False
        else:
            self.collector_i += 1
            self.last_collection_posi = self.collection_posi
            return True
    
    def exec_mission(self):
        
        while 1:
            if self.checkup_stop_func():return
            self._set_target_position()
            r = self.move_straight(self.collection_posi, is_tp = True, is_precise_arrival=True)
            if r == ERR_FAIL:
                self._add_logs("MOVE FAIL")
                self._set_collected_id()
                if not self._add_collection_i():
                    break
                continue
            
            r = self.collect(MODE="AUTO", collector_type=self.collector_type, is_combat = (self.collector_type==ENEMY), is_activate_pickup=True)
            if r == ERR_FAIL:
                err_info = self.CFCF.flow_connector.puo.get_last_err_code()
                self._add_logs(f"COLLECT FAIL: {err_info}")
                self._set_collected_id()
                if not self._add_collection_i():
                    break
                continue
            err_info = self.CFCF.flow_connector.puo.get_last_err_code()
            if err_info != ERR_NONE:
                self._add_logs("SUCCESS")
            else:
                self._add_logs(f"COLLECT FAIL: {err_info}")

            if not self._add_collection_i():
                break
        # self.start_pickup()
        # self.move_along("Crystalfly16786174406", is_tp=True)
        # self.move_along("Crystalfly167861751483", is_tp=True)
        # self.move_along("Crystalfly167861762261", is_tp=True)
        # self.stop_pickup()
        # self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
        
if __name__ == '__main__':
    mission = MissionMain()
    mission.start()
    mission.continue_threading()

