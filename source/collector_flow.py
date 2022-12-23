from util import *
import math
import flow_state as ST
from interaction_background import InteractionBGD
import generic_lib
import pickup_operator
import combat_loop
from base_threading import BaseThreading
import timer_module
import combat_lib
import teyvat_move_flow
import numpy as np
import datetime
import static_lib
import button_manager
import img_manager

COLLECTION = 0
ENEMY = 1
MINERAL = 2

ALL_CHARACTER_DIED = 1

def load_feature_position(text, blacklist_id=[], ret_mode = 0):
    ita = load_json("itemall.json", "assests")
    ret_dict=[]
    i=0
    for feature in ita:
        i+=1
        if feature == None:
            continue
        for item in feature["features"]:
            if item["id"] in blacklist_id:
                continue
            if text in item["properties"]["popTitle"] :
                if ret_mode == 0:
                    ret_dict.append({
                        "id":item["id"],
                        "position":list(np.array( list(map(float,item["geometry"]["coordinates"])) )*1.5)
                    })
                elif ret_mode == 1:
                     ret_dict.append(list(np.array( list(map(float,item["geometry"]["coordinates"])) )*1.5))
    # print()
    return ret_dict  



class CollectorFlow(BaseThreading):
    def __init__(self):
        super().__init__()
        collector_config = load_json("auto_collector.json")
        self.collector_name = collector_config["collection_name"]
        if collector_config["collection_type"] == "COLLECTION":
            self.collector_type = COLLECTION
        elif collector_config["collection_type"] == "ENEMY":
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

        if not os.path.exists(os.path.join(root_path, "config\\auto_collector", "collection_log.json")):
            save_json({}, os.path.join(root_path, "config\\auto_collector", "collection_log.json"))
        self.collection_log = load_json("collection_log.json", default_path="config\\auto_collector")
        
        self.collector_posi_dict = load_feature_position(self.collector_name, self.collector_blacklist_id)
        self.current_state = ST.INIT_MOVETO_COLLECTOR
        self.current_position = static_lib.cvAutoTrackerLoop.get_position()[1:]
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
        
        
        chara_list = combat_loop.get_chara_list()
        self.cct = combat_loop.Combat_Controller(chara_list)
        self.cct.is_check_died = True
        self.cct.setDaemon(True)
        self.cct.add_stop_func(self.checkup_stop_func)
        self.cct.pause_threading()
        self.cct.start()
        
        
        self.IN_PICKUP_COLLECTOR_timeout = timer_module.TimeoutTimer(45)
        self.IN_MOVETO_COLLECTOR_timeout = timer_module.TimeoutTimer(260)
        self.itt = InteractionBGD()
        
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
    
    def checkup_stop_func(self):
        
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
    
    def recover_all(self):
        self.stop_all()
        self.current_position = static_lib.cvAutoTrackerLoop.get_position()[1:]
        self.tmf.reset_setting()
        gs_posi = load_feature_position(text="七天神像", ret_mode=1)
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
                logger.info("停止自动采集")
                return 0

            if self.last_err_code == ALL_CHARACTER_DIED:
                logger.error("所有角色都已嘎掉，正在中断此次采集")
                self.add_log("ALL_CHARACTER_DIED")
                self.stop_all()
                time.sleep(15)
                while 1:
                    time.sleep(1)
                    if self.checkup_stop_threading():
                        break
                    ret = self.itt.appear_then_click(button_manager.button_all_character_died)
                    
                    if self.itt.get_img_existence(img_manager.ui_main_win) and not self.itt.get_img_existence(button_manager.button_all_character_died):
                        break
                
                self.current_state = ST.AFTER_PICKUP_COLLECTOR
                self.last_err_code = None
                logger.info("重置完成。准备进行下一次采集")
                
            if self.cct.get_last_err_code() == combat_loop.CHARACTER_DIED:
                logger.warning("有人嘎了，正在停止此次采集")
                self.add_log("CHARACTER_DIED")
                self.stop_all()
                self.recover_all()
                self.current_state = ST.AFTER_PICKUP_COLLECTOR
                self.last_err_code = None
                logger.info("重置完成。准备进行下一次采集")
                self.cct.reset_err_code()
            
            if self.itt.get_img_existence(button_manager.button_all_character_died):
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
                
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            '''write your code below'''
            
                  
                
            if self.current_state == ST.INIT_MOVETO_COLLECTOR:
                
                self.collector_posi_dict = load_feature_position(self.collector_name, self.shielded_id)
                static_lib.while_until_no_excessive_error(self.checkup_stop_func)
                self.current_position = static_lib.cvAutoTrackerLoop.get_position()[1:]
                self.collector_posi_dict.sort(key=self.sort_by_eu)
                logger.info("switch Flow to: BEFORE_MOVETO_COLLECTOR")
                self.current_state = ST.BEFORE_MOVETO_COLLECTOR
                self.collector_i = 0
                
            if self.current_state == ST.BEFORE_MOVETO_COLLECTOR:
                self.collection_posi = self.collector_posi_dict[self.collector_i]["position"]
                self.collection_id = self.collector_posi_dict[self.collector_i]["id"]
                '''当两个collection坐标小于30时，认为是同一个。'''
                if euclidean_distance(self.collection_posi, self.last_collection_posi) <= 30:
                    logger.info(f"collection id: {self.collection_id} ; collection position: {self.collection_posi} ; last collection position: {self.last_collection_posi}")
                    logger.info(f"distance lower than 30, skip this collection.")
                    self.current_state = ST.AFTER_PICKUP_COLLECTOR
                    continue
                logger.info("正在前往：" + self.collector_name)
                logger.info(f"物品id：{self.collection_id}")
                while static_lib.cvAutoTrackerLoop.in_excessive_error:
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
                if self.tmf.pause_threading_flag:
                    logger.info(_("switch Flow to: AFTER_MOVETO_COLLECTOR"))
                    self.current_state = ST.AFTER_MOVETO_COLLECTOR
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
                elif self.collector_type == ENEMY:
                    self.IN_PICKUP_COLLECTOR_timeout.set_timeout_limit(120)
                    self.puo.max_distance_from_target = 60
                elif self.collector_type == MINERAL:
                    pass
                
                self.puo.reset_pickup_item_list()
                
                logger.info(_("switch Flow to: BEFORE_PICKUP_COLLECTOR"))
                time.sleep(1) # wait for CSDL detection
                self.current_state = ST.BEFORE_PICKUP_COLLECTOR
            
            if self.current_state == ST.BEFORE_PICKUP_COLLECTOR:
                if combat_lib.CSDL.get_combat_state() == False:
                    self.start_pickup()
                    self.puo.reset_err_code()
                    logger.info(_("switch Flow to: IN_PICKUP_COLLECTOR"))
                    self.IN_PICKUP_COLLECTOR_timeout.reset()
                    self.current_state = ST.IN_PICKUP_COLLECTOR
                    self.while_sleep = 0.2
                else:
                    self.start_combat()
                    self.while_sleep = 0.5
                    
            if self.current_state == ST.IN_PICKUP_COLLECTOR:
                if self.puo.pause_threading_flag:
                    logger.info(_("switch Flow to: AFTER_PICKUP_COLLECTOR"))
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