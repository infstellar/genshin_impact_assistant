from util import *
import math
import flow_state as ST
import cvAutoTrack
from interaction_background import InteractionBGD
import teyvat_move_controller
import generic_lib
import img_manager
import pickup_operator
import movement
import posi_manager
import big_map
import combat_loop
import pdocr_api
from base_threading import BaseThreading
import pyautogui
import interaction_background
import text_manager
import timer_module
import combat_lib
import teyvat_move_flow
import numpy as np

COLLECTION = 0
ENEMY = 1
MINERAL = 2

def load_feature_position(text="清心", blacklist_id=[]):
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
            if item["properties"]["popTitle"] == text:
                ret_dict.append({
                    "id":item["id"],
                    "position":list(np.array( list(map(float,item["geometry"]["coordinates"])) )*1.5)
                })
    # print()
    return ret_dict  



class CollectorFlow(BaseThreading):
    def __init__(self):
        super().__init__()
        self.collector_name = "甜甜花 - 蒙德"
        self.collector_type = COLLECTION
        self.collector_blacklist_id = load_json("collection_blacklist.json", default_path="config\\auto_collector")
        self.collected_id = load_json("collected.json", default_path="config\\auto_collector")
        self.shielded_id = []
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
        
        self.collector_posi_dict = load_feature_position(self.collector_name, blacklist_id=self.collector_blacklist_id)
        self.current_state = ST.INIT_MOVETO_COLLECTOR
        self.current_position = cvAutoTrack.cvAutoTrackerLoop.get_position()[1:]
        
        self.tmf = teyvat_move_flow.TeyvatMoveFlow()
        self.tmf.setDaemon(True)
        self.tmf.pause_threading()
        self.tmf.start()
        
        self.puo = pickup_operator.PickupOperator()
        self.puo.setDaemon(True)
        self.puo.pause_threading()
        self.puo.start()
        
        chara_list = combat_loop.get_chara_list()
        self.cct = combat_loop.Combat_Controller(chara_list)
        self.cct.setDaemon(True)
        self.cct.pause_threading()
        self.cct.start()
        
        self.pickup_timer = timer_module.Timer()
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
        
        
    def set_collector_name(self, text):
        self.collector_name = text

    def stop_combat(self):
        self.cct.pause_threading()
    def start_combat(self):
        self.cct.continue_threading()
        self.stop_pickup()
        self.stop_walk()
    def stop_pickup(self):
        self.puo.pause_threading()
    def start_pickup(self):
        self.puo.continue_threading()
        self.stop_combat()
        self.stop_walk()
    def stop_walk(self):
        self.tmf.pause_threading()
    def start_walk(self):
        self.tmf.continue_threading()
        self.stop_combat()
        self.stop_pickup()
    
    def sort_by_eu(self, x):
        return generic_lib.euclidean_distance(x["position"], self.current_position)
    
    def run(self):
        '''if you're using this class, copy this'''
        while 1:
            time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True
            '''write your code below'''
            
            if self.current_state == ST.INIT_MOVETO_COLLECTOR:
                
                self.collector_posi_dict = load_feature_position(self.collector_name, blacklist_id=self.shielded_id)
                self.current_position = cvAutoTrack.cvAutoTrackerLoop.get_position()[1:]
                self.collector_posi_dict.sort(key=self.sort_by_eu)
                logger.info("switch Flow to: BEFORE_MOVETO_COLLECTOR")
                self.current_state = ST.BEFORE_MOVETO_COLLECTOR
                self.collector_i = 0
                
            if self.current_state == ST.BEFORE_MOVETO_COLLECTOR:
                self.collector_posi = self.collector_posi_dict[self.collector_i]["position"]
                logger.info("正在前往：" + self.collector_name)
                logger.info("物品id：" + str(self.collector_posi_dict[self.collector_i]["id"]))
                while cvAutoTrack.cvAutoTrackerLoop.in_excessive_error:
                    time.sleep(1)
                logger.info("目标坐标：" + str(self.collector_posi)+"当前坐标：" + str(cvAutoTrack.cvAutoTrackerLoop.get_position()[1:]))
                self.collected_id[self.collector_name].append(self.collector_posi_dict[self.collector_i]["id"])
                save_json(self.collected_id, "collected.json", default_path="config\\auto_collector", sort_keys=False)
                
                self.tmf.set_target_position(self.collector_posi)
                self.puo.set_target_position(self.collector_posi)
                self.puo.set_target_name(self.collector_name)
                self.start_walk()
                logger.info("switch Flow to: IN_MOVETO_COLLECTOR")
                self.current_state = ST.IN_MOVETO_COLLECTOR
                
            if self.current_state == ST.IN_MOVETO_COLLECTOR:
                if self.tmf.pause_threading_flag:
                    logger.info("switch Flow to: AFTER_MOVETO_COLLECTOR")
                    self.current_state = ST.AFTER_MOVETO_COLLECTOR
            
            if self.current_state == ST.AFTER_MOVETO_COLLECTOR:
                self.stop_walk()
                self.current_state = ST.END_MOVETO_COLLECTOR
                logger.info("switch Flow to: INIT_PICKUP_COLLECTOR")
                self.current_state = ST.INIT_PICKUP_COLLECTOR
                
            if self.current_state == ST.INIT_PICKUP_COLLECTOR:
                if self.collector_type == COLLECTION:
                    # self.start_pickup()
                    pass
                elif self.collector_type == ENEMY:
                    self.start_combat()
                elif self.collector_type == MINERAL:
                    pass
                logger.info("switch Flow to: BEFORE_PICKUP_COLLECTOR")
                time.sleep(1) # wait for CSDL detection
                self.current_state = ST.BEFORE_PICKUP_COLLECTOR
            
            if self.current_state == ST.BEFORE_PICKUP_COLLECTOR:
                if self.collector_type == COLLECTION:
                    if combat_lib.CSDL.get_combat_state() == False:
                        self.start_pickup()
                        logger.info("switch Flow to: IN_PICKUP_COLLECTOR")
                        self.current_state = ST.IN_PICKUP_COLLECTOR
                        self.while_sleep = 0.2
                    else:
                        self.start_combat()
                        self.while_sleep = 0.5
                
            if self.current_state == ST.IN_PICKUP_COLLECTOR:
                if self.puo.pause_threading_flag:
                    logger.info("switch Flow to: AFTER_PICKUP_COLLECTOR")
                    self.current_state = ST.AFTER_PICKUP_COLLECTOR
                if self.puo.pickup_timer.get_diff_time() >= 45:
                    logger.info("自动拾取超时: 45s")
                    logger.info("switch Flow to: AFTER_PICKUP_COLLECTOR")
                    self.current_state = ST.AFTER_PICKUP_COLLECTOR
                
                    
            if self.current_state == ST.AFTER_PICKUP_COLLECTOR:
                self.stop_pickup()
                if len(self.collector_posi_dict)-1 == self.collector_i:
                    print("exit")
                    logger.info("switch Flow to: END_COLLECTOR")
                    self.current_state = ST.END_COLLECTOR
                else:
                    self.collector_i += 1
                    logger.info("switch Flow to: BEFORE_MOVETO_COLLECTOR")
                    self.current_state = ST.BEFORE_MOVETO_COLLECTOR
                    self.tmf.reset_setting()
            
            if self.current_state == ST.END_COLLECTOR:
                self.pause_threading()
                time.sleep(1)
                
if __name__ == '__main__':
    cof = CollectorFlow()
    cof.start()
    while 1:
        time.sleep(1)