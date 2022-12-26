import img_manager
import time
from interaction_background import InteractionBGD
import math
import numpy as np
import scene_manager
import button_manager
import big_map
import static_lib
from util import *
import posi_manager

NORMAL = 0
NEGATIVE_Y = 1
NEGATIVE_X = 2
NEGATIVE_XY = 3
itt = InteractionBGD()

def f_recognition(mode='button_only'):
    if itt.get_img_existence(img_manager.F_BUTTON):
        return True
    else:
        return False


# def euclidean_distance(p1, p2):
#     return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# def euclidean_distance_plist(p1, p2):
#     return np.sqrt((p1[0] - p2[:,0]) ** 2 + (p1[1] - p2[:,1]) ** 2)

# def manhattan_distance(p1, p2):
#     return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

# def manhattan_distance_plist(p1, p2):
#     return abs(p1[0]-p2[:,0]) + abs(p1[1]-p2[:,1])

def points_angle(p1, p2, coordinate=NORMAL):
    # p1: current point
    # p2: target point
    x = p1[0]
    y = p1[1]
    tx = p2[0]
    ty = p2[1]
    if coordinate == NEGATIVE_Y:
        y = -y
        ty = -ty
    # x=-x
    # tx=-tx
    k = (ty - y) / (tx - x)
    degree = math.degrees(math.atan(k))
    if degree < 0:
        degree += 180
    # if coordinate == NORMAL:
    if ty < y:
        degree += 180
    # elif coordinate == NEGATIVE_Y:
    #     if y<ty:
    #         degree+=180

    degree -= 90

    if degree > 180:
        degree -= 360
    return degree

def recover_all(stop_func):
    import pdocr_api
    scene_manager.switch_to_page(scene_manager.page_bigmap, stop_func)
    gsp = big_map.get_middle_gs_point(stop_func)
    if len(gsp)==0:
        logger.info(_("获取传送锚点失败，正在重试"))
        big_map.reset_map_size()
        gsp = big_map.get_middle_gs_point(stop_func)
    itt.move_and_click(gsp)
    time.sleep(0.5)
    p1 = pdocr_api.ocr.get_text_position(itt.capture(jpgmode=0), "七天神像")
    if p1 != -1:
        itt.move_and_click([p1[0] + 30, p1[1] + 30], delay=1)

    itt.move_and_click([posi_manager.tp_button[0], posi_manager.tp_button[1]], delay=1)
    # itt.delay(1)
    # itt.left_click()
    while not itt.get_img_existence(img_manager.ui_main_win):
        if stop_func():
            break
        time.sleep(1)
    while static_lib.cvAutoTrackerLoop.in_excessive_error:
        if stop_func():
            break
        time.sleep(1)
    
    

def set_genshin_time(x=18, stop_func = scene_manager.default_stop_func): # 调整时间至夜晚
    scene_manager.switch_to_page(scene_manager.page_time, stop_func)
    time.sleep(0.8)
    itt.move_to(img_manager.ui_time_menu_core.cap_center_position_xy[0],img_manager.ui_time_menu_core.cap_center_position_xy[1])
    itt.left_down()
    time.sleep(0.8)
    itt.move_to(-10,0,relative=True)
    time.sleep(0.2)
    itt.move_to(0,-30,relative=True)
    time.sleep(0.2)
    for i in range(5):
        itt.move_to(20,0,relative=True)
        time.sleep(0.2)
    itt.move_to(0,30,relative=True)
    time.sleep(0.2)
    itt.left_up()
    itt.move_and_click(position = [1454,1021])
    time.sleep(0.8)
    while 1:
        ret = itt.appear_then_click(button_manager.button_exit)
        if ret:
            break
        if stop_func():
            break
        time.sleep(1)
    time.sleep(2)
    scene_manager.switch_to_page(scene_manager.page_main, stop_func)

def f():
    return False

if __name__ == '__main__':
    # recover_all(f)
    # p1 = [0,0]
    # p2 = np.array([[1,1],[2,2]])
    # euclidean_distance_plist(p1,p2)
    set_genshin_time()
    # print(points_angle([0, 0], [10, 10], NEGATIVE_Y))
    # print(points_angle([10, 10], [0, 0], NEGATIVE_Y))
    # print(points_angle([0, 0], [20, 10], NEGATIVE_Y))
    # print(points_angle([0, 10], [10, 10], NEGATIVE_Y))
    while 1:
        time.sleep(0.2)
        print(f_recognition(itt))
