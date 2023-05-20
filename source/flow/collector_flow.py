from source.util import *
from common import flow_state as ST, timer_module
from source.interaction.interaction_core import itt
from source.pickup import pickup_operator
from source.flow import teyvat_move_flow
from source.interaction.minimap_tracker import tracker
from source.controller import combat_controller
from source.common.base_threading import BaseThreading
from source.funclib import collector_lib, generic_lib, combat_lib
import numpy as np
import datetime
from source.manager import asset
from funclib.err_code_lib import ERR_PASS, ERR_STUCK, ERR_COLLECTOR_FLOW_TIMEOUT
from source.ui.ui import ui_control
import source.ui.page as UIPage

COLLECTION = 0
ENEMY = 1
MINERAL = 2

ALL_CHARACTER_DIED = 1

SUCC_RATE_WEIGHTING = 6



class CollectorFlow(BaseThreading):
    def __init__(self):
        super().__init__()
        self.setName("CollectorFlow")
        # collector_config = load_json("auto_collector.json")
        self.collector_name = GIAconfig.Collector_CollectionName
        if GIAconfig.Collector_CollectionType == "COLLECTION":
            self.collector_type = COLLECTION
        elif GIAconfig.Collector_CollectionType == "ENEMY":
            self.collector_type = ENEMY
        self.collector_blacklist_id = load_json("collection_blacklist.json", default_path="config\\auto_collector")
        self.collected_id = load_json("collected.json", default_path="config\\auto_collector")
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
        self.collection_log = load_json("collection_log.json", default_path="config\\auto_collector")
        
        self.collector_posi_dict = None
        self.current_state = ST.INIT_MOVETO_COLLECTOR
        self.current_position = tracker.get_position()
        self.last_collection_posi = [9999,9999]
        self.picked_list = []
        self.recover_timeout = timer_module.TimeoutTimer(200)
        
        self.tmf = teyvat_move_flow.TeyvatMoveFlow()
        self.tmf.setDaemon(True)
        self.tmf.add_stop_func(self.checkup_stop_func)
        self.tmf.pause_threading()
        self.tmf.start()
        
        
        self.puo = pickup_operator.PickupOperator()
        self.puo.setDaemon(True)
        self.puo.add_stop_func(self.checkup_stop_func)
        self.puo.pause_threading()
        self.puo.start()
        self.puo.set_search_mode(1)
        
        
        self.cct = combat_controller.CombatController()
        self.cct.is_check_died = True
        self.cct.setDaemon(True)
        self.cct.add_stop_func(self.checkup_stop_func)
        self.cct.pause_threading()
        self.cct.start()
        
        
        self.IN_PICKUP_COLLECTOR_timeout = timer_module.TimeoutTimer(45)
        self.IN_MOVETO_COLLECTOR_timeout = timer_module.TimeoutTimer(240)
        self.Flow_timeout = timer_module.TimeoutTimer(340)
        # collector_lib.generate_masked_col_from_log()
        collector_lib.generate_collected_from_log()
        collector_lib.generate_col_succ_rate_from_log()
        logger.debug(f"generate collection_id_details succ")
        self.collection_details = load_json("collection_id_details.json", "config\\auto_collector")
        self.itt = itt
        
        
        
    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.tmf.pause_threading()
            self.puo.pause_threading()
            self.cct.pause_threading()

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.pause_threading_flag = False
            self.tmf.continue_threading()
            self.puo.continue_threading()
            self.cct.continue_threading()

    def stop_threading(self):
        self.stop_threading_flag = True
        self.tmf.stop_threading()
        self.puo.stop_threading()
        self.cct.stop_threading()
        self.add_log("USER_STOP")
    
    def checkup_stop_func(self):
        if self.Flow_timeout.istimeout():
            self.last_err_code = ERR_COLLECTOR_FLOW_TIMEOUT
            return True
        return super().checkup_stop_func()    
        
    def set_collector_name(self, text):
        self.collector_name = text

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
    
    def sort_by_eu(self, x):
        return euclidean_distance(x["position"], self.current_position)
    
    def sort_by_succ_rate(self, x):
        try:
            ret = self.collection_details[str(x["id"])]
        except KeyError as e:
            return 0.8
        return self.collection_details[str(x["id"])]
    
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
    
    def add_log(self, x):
        a = self.collection_log.setdefault(self.collector_name, [])
        self.picked_list = self.puo.pickup_item_list.copy()
        if not self.picked_list:
            self.picked_list.append('None')
        a.append({"time":str(datetime.datetime.now()),
                  "id": self.collection_id,
                  "error_code": x,
                  "picked item": self.picked_list})
        self.collection_log[self.collector_name] = a
        save_json(self.collection_log, "collection_log.json", default_path="config\\auto_collector")
        self.picked_list = []
        self.puo.reset_pickup_item_list()
    
    def recover_all(self):
        self.stop_all()
        self.current_position = tracker.get_position()
        self.tmf.reset_setting()
        gs_posi = collector_lib.load_items_position(marker_title=asset.QTSX.text, ret_mode=1, match_mode=1)
        gs_posi = np.asarray(gs_posi)
        d = euclidean_distance_plist(self.current_position, gs_posi)
        gs_posi = gs_posi[np.argmin(d)]
        self.tmf.set_target_position(gs_posi)
        self.tmf.set_stop_rule(1)
        self.start_walk()
        self.recover_timeout.reset()
        while 1:
            time.sleep(0.05)
            if self.checkup_stop_func():
                return
            if generic_lib.f_recognition():
                logger.info("识别到f，正在退出")
                break
            if self.recover_timeout.istimeout():
                logger.info("回血超时，正在退出")
                break
        self.stop_all()
        time.sleep(10)
        self.tmf.set_stop_rule(0)
    
    def run(self):
        '''if you're using this class, copy this'''
        while 1:
            time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                logger.info(t2t("停止自动采集"))
                return 0

            if self.last_err_code == ALL_CHARACTER_DIED:
                logger.error(t2t("所有角色都已嘎掉，正在中断此次采集"))
                self.add_log("ALL_CHARACTER_DIED")
                self.stop_all()
                time.sleep(15)
                while 1:
                    time.sleep(1)
                    if self.checkup_stop_threading():
                        break
                    ret = self.itt.appear_then_click(asset.ButtonGeneralAllCharacterDied)
                    
                    if self.itt.get_img_existence(asset.IconUIEmergencyFood) and not self.itt.get_img_existence(
                            asset.ButtonGeneralAllCharacterDied):
                        break
                
                self.current_state = ST.AFTER_PICKUP_COLLECTOR
                self.reset_err_code()
                logger.info(t2t("重置完成。准备进行下一次采集"))
                self.pause_threading_flag = False
            elif self.last_err_code == ERR_COLLECTOR_FLOW_TIMEOUT:
                self.stop_all()
                logger.warning(t2t("Flow timeout"))
                self.add_log("FLOW_TIMEOUT")
                self.current_state = ST.AFTER_PICKUP_COLLECTOR
                logger.info(t2t("重置完成。准备进行下一次采集"))
                self.Flow_timeout.reset()
                self.reset_err_code()
                self.pause_threading_flag = False
            elif self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            
            if self.cct.get_last_err_code() == combat_controller.CHARACTER_DIED:
                logger.warning(t2t("有人嘎了，正在停止此次采集"))
                self.add_log("CHARACTER_DIED")
                self.stop_all()
                self.recover_all()
                self.current_state = ST.AFTER_PICKUP_COLLECTOR
                self.reset_err_code()
                logger.info(t2t("重置完成。准备进行下一次采集"))
                self.cct.reset_err_code()
            
            if self.itt.get_img_existence(asset.ButtonGeneralAllCharacterDied):
                self.last_err_code = ALL_CHARACTER_DIED
                logger.warning("ALL_CHARACTER_DIED")
                self.stop_all()
            
            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True
                
            
            '''write your code below'''
            
                  
                
            if self.current_state == ST.INIT_MOVETO_COLLECTOR:
                
                self.collector_posi_dict = collector_lib.load_items_position(self.collector_name, blacklist_id=self.shielded_id)
                self.shielded_posi_list = collector_lib.load_items_position(self.collector_name, blacklist_id=self.shielded_id, ret_mode=1, check_mode=1)
                ui_control.ui_goto(UIPage.page_main)
                tracker.while_until_no_excessive_error()
                self.current_position = tracker.get_position()
                self.collection_details = load_json("collection_id_details.json", "config\\auto_collector")
                if True:
                    self.collector_posi_dict.sort(key=self.sort_by_distance_and_succrate)
                else:
                    self.collector_posi_dict.sort(key=self.sort_by_eu)
                logger.info("switch Flow to: BEFORE_MOVETO_COLLECTOR")
                self.current_state = ST.BEFORE_MOVETO_COLLECTOR
                self.collector_i = 0
                
            if self.current_state == ST.BEFORE_MOVETO_COLLECTOR:
                self.Flow_timeout.reset()
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
                    self.current_state = ST.AFTER_PICKUP_COLLECTOR
                    continue
                logger.info("正在前往：" + self.collector_name)
                logger.info(f"物品id：{self.collection_id}")
                while tracker.in_excessive_error:
                    if self.checkup_stop_func():
                        break
                    time.sleep(1)
                logger.info("目标坐标：" + str(self.collection_posi)+"当前坐标：" + str(self.current_position))
                
                
                self.tmf.set_target_position(self.collection_posi)
                self.puo.set_target_position(self.collection_posi)
                self.puo.set_target_name(self.collector_name)
                self.start_walk()
                logger.info("switch Flow to: IN_MOVETO_COLLECTOR")
                self.IN_MOVETO_COLLECTOR_timeout.reset()
                self.current_state = ST.IN_MOVETO_COLLECTOR
                
            if self.current_state == ST.IN_MOVETO_COLLECTOR:
                if self.tmf.get_last_err_code() == ERR_PASS:
                    self.tmf.reset_err_code()
                    logger.info(t2t("switch Flow to: AFTER_MOVETO_COLLECTOR"))
                    self.current_state = ST.AFTER_MOVETO_COLLECTOR
                elif self.tmf.get_last_err_code() == ERR_STUCK:
                    self.tmf.reset_err_code()
                    logger.info(t2t("collect in") +f"{self.collector_name} {self.collection_id} {self.collection_posi} "+t2t("failed. reason: stuck"))
                    logger.info("switch Flow to: AFTER_PICKUP_COLLECTOR")
                    self.add_log("IN_PICKUP_COLLECTOR_STUCK")
                    self.current_state = ST.AFTER_PICKUP_COLLECTOR

                if self.IN_MOVETO_COLLECTOR_timeout.istimeout():
                    logger.info(f"IN_MOVETO_COLLECTOR timeout: {self.IN_MOVETO_COLLECTOR_timeout.timeout_limit}")
                    logger.info(f"collect in{self.collector_name} {self.collection_id} {self.collection_posi} failed.")
                    self.add_log("IN_MOVETO_COLLECTOR_TIMEOUT")
                    self.current_state = ST.AFTER_PICKUP_COLLECTOR
                    self.tmf.pause_threading()
            
            if self.current_state == ST.AFTER_MOVETO_COLLECTOR:
                self.stop_walk()
                self.current_state = ST.END_MOVETO_COLLECTOR
                logger.info("switch Flow to: INIT_PICKUP_COLLECTOR")
                self.current_state = ST.INIT_PICKUP_COLLECTOR
                
            if self.current_state == ST.INIT_PICKUP_COLLECTOR:
                if self.collector_type == COLLECTION:
                    self.IN_PICKUP_COLLECTOR_timeout.set_timeout_limit(120)
                    self.Flow_timeout.set_timeout_limit(300)
                elif self.collector_type == ENEMY:
                    self.IN_PICKUP_COLLECTOR_timeout.set_timeout_limit(120)
                    self.puo.max_distance_from_target = 60
                    self.Flow_timeout.set_timeout_limit(380)
                elif self.collector_type == MINERAL:
                    pass
                
                
                
                logger.info(t2t("switch Flow to: BEFORE_PICKUP_COLLECTOR"))
                time.sleep(1) # wait for CSDL detection
                self.current_state = ST.BEFORE_PICKUP_COLLECTOR
            
            if self.current_state == ST.BEFORE_PICKUP_COLLECTOR:
                if combat_lib.CSDL.get_combat_state() == False:
                    self.start_pickup()
                    self.puo.reset_err_code()
                    logger.info(t2t("switch Flow to: IN_PICKUP_COLLECTOR"))
                    self.IN_PICKUP_COLLECTOR_timeout.reset()
                    self.current_state = ST.IN_PICKUP_COLLECTOR
                    self.while_sleep = 0.2
                else:
                    self.start_combat()
                    self.while_sleep = 0.5
                    
            if self.current_state == ST.IN_PICKUP_COLLECTOR:
                if self.puo.pause_threading_flag:
                    logger.info(t2t("switch Flow to: AFTER_PICKUP_COLLECTOR"))
                    self.add_log(str(self.puo.last_err_code))
                    self.current_state = ST.AFTER_PICKUP_COLLECTOR
                if self.IN_PICKUP_COLLECTOR_timeout.istimeout():
                    logger.info(f"IN_PICKUP_COLLECTOR timeout: {self.IN_PICKUP_COLLECTOR_timeout.timeout_limit}")
                    logger.info(f"collect in{self.collector_name} {self.collection_id} {self.collection_posi} failed.")
                    logger.info("switch Flow to: AFTER_PICKUP_COLLECTOR")
                    self.add_log("IN_PICKUP_COLLECTOR_TIMEOUT")
                    self.current_state = ST.AFTER_PICKUP_COLLECTOR
                    self.stop_pickup()
                if combat_lib.CSDL.get_combat_state():
                    self.stop_pickup()
                    self.current_state = ST.BEFORE_PICKUP_COLLECTOR
                    
            if self.current_state == ST.AFTER_PICKUP_COLLECTOR:
                self.stop_all()
                self.collected_id[self.collector_name].append(self.collector_posi_dict[self.collector_i]["id"])
                save_json(self.collected_id, "collected.json", default_path="config\\auto_collector", sort_keys=False)
                if len(self.collector_posi_dict)-1 == self.collector_i:
                    logger.info("exit")
                    logger.info("switch Flow to: END_COLLECTOR")
                    self.current_state = ST.END_COLLECTOR
                else:
                    self.collector_i += 1
                    self.last_collection_posi = self.collection_posi
                    logger.info("switch Flow to: BEFORE_MOVETO_COLLECTOR")
                    self.current_state = ST.BEFORE_MOVETO_COLLECTOR
                    self.tmf.reset_setting()
            
            if self.current_state == ST.END_COLLECTOR:
                self.pause_threading()
                time.sleep(1)
                
if __name__ == '__main__':
    cof = CollectorFlow()
    # cof.recover_all()
    cof.start()
    while 1:
        time.sleep(1)