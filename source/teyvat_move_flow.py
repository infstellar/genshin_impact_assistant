from unit import *
import math
import pyautogui
import flow_state as ST
from cvAutoTrack import cvAutoTracker
import generic_lib
import img_manager
import interaction_background
import movement
import posi_manager
import text_manager
import timer_module
from base_threading import BaseThreading
# from pdocr_api import ocr

def get_target_relative_angle(x, y, tx, ty):
    x=-x
    tx=-tx
    k = (ty-y)/(tx-x)
    degree = math.degrees(math.atan(k))
    if degree<0:
        degree+=180
    if ty<y:
        degree+=180
    degree-=90
    if degree>180:
        degree-=360
    return degree


class TeyvatMoveFlow(BaseThreading):
    def __init__(self):
        super().__init__()
        
    def align_position(self,tx,ty):
        b,x,y = cvAutoTracker.get_position()
        if b:
            angle = get_target_relative_angle(x,y,tx,ty)
            movement.view_to_angle_teyvat(angle)
            print(x,y,angle)
        return 0
        
if __name__=='__main__':
    tmf=TeyvatMoveFlow()
    while 1:
        tmf.align_position(0,0)
        time.sleep(0.2)
# print(get_target_relative_angle(0,0,1,1))
