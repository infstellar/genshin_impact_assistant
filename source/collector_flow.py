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

def load_feature_position(text="清心"):
    ita = load_json("itemall.json", "assests")
    ret_dict=[]
    i=0
    for feature in ita:
        i+=1
        if feature == None:
            continue
        for item in feature["features"]:
            if item["properties"]["popTitle"] == text:
                ret_dict.append({
                    "id":item["id"],
                    "position":item["geometry"]["coordinates"]
                })
    print()
    return ret_dict  

class CollectorFlow(BaseThreading):
    def __init__(self):
        super().__init__()
        self.collector_name = "甜甜花 - 蒙德"
        self.collector_posi_dict = load_feature_position(self.collector_name)
        self.current_state = ST.INIT_MOVETO_COLLECTOR
        
        self.tmf = teyvat_move_flow.TeyvatMoveFlow()
        self.tmf.setDaemon(True)
        self.tmf.pause_threading()
        self.tmf.start()
        
        self.puo = pickup_operator.PickupOperator()
        self.puo.setDaemon(True)
        self.puo.pause_threading()
        self.puo.start()
        
    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.pause_threading_flag = False

    def stop_threading(self):
        self.stop_threading_flag = True
        
    def set_collector_name(self, text):
        self.collector_name = text
        self.collector_posi_dict = load_feature_position(self.collector_name)

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
                self.collector_posi_dict = load_feature_position(self.collector_name)
                self.current_state = ST.BEFORE_MOVETO_COLLECTOR
                self.collector_id = 0
                
            if self.current_state == ST.BEFORE_MOVETO_COLLECTOR:
                self.collector_posi = list(map(float, self.collector_posi_dict[self.collector_id]["position"]))
                self.tmf.set_target_posi(self.collector_posi)
                self.tmf.continue_threading()
                self.current_state = ST.IN_MOVETO_COLLECTOR
                
            if self.current_state == ST.IN_MOVETO_COLLECTOR:
                if self.tmf.pause_threading_flag:
                    self.current_state = ST.AFTER_MOVETO_COLLECTOR
            
            if self.current_state == ST.AFTER_MOVETO_COLLECTOR:
                self.tmf.pause_threading()
                self.current_state = ST.END_MOVETO_COLLECTOR
                self.current_state = ST.INIT_PICKUP_COLLECTOR
                
            if self.current_state == ST.INIT_PICKUP_COLLECTOR:
                self.current_state = ST.BEFORE_PICKUP_COLLECTOR
            
            if self.current_state == ST.BEFORE_PICKUP_COLLECTOR:
                self.puo.continue_threading()
                self.current_state = ST.IN_PICKUP_COLLECTOR
                
            if self.current_state == ST.IN_PICKUP_COLLECTOR:
                if self.puo.pause_threading_flag:
                    self.current_state = ST.AFTER_PICKUP_COLLECTOR
                    
            if self.current_state == ST.AFTER_PICKUP_COLLECTOR:
                self.puo.pause_threading()
                if len(self.collector_posi_dict)-1 == self.collector_id:
                    print("exit")
                    self.current_state = ST.END_COLLECTOR
                else:
                    self.collector_id += 1
                    self.current_state = ST.BEFORE_MOVETO_COLLECTOR
            
            if self.current_state == ST.END_COLLECTOR:
                self.pause_threading()
                time.sleep(1)
                
if __name__ == '__main__':
    cof = CollectorFlow()
    cof.start()
    while 1:
        time.sleep(1)