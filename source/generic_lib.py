import img_manager
import time
from interaction_background import InteractionBGD
import math
import numpy as np
import scene_manager

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


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def euclidean_distance_plist(p1, p2):
    return np.sqrt((p1[0] - p2[:,0]) ** 2 + (p1[1] - p2[:,1]) ** 2)

def manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def manhattan_distance_plist(p1, p2):
    return abs(p1[0]-p2[:,0]) + abs(p1[1]-p2[:,1])

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

def set_genshin_time(x=18, stop_func = scene_manager.default_stop_func): # 调整时间至夜晚
    scene_manager.switchto_time_menu(stop_func)
    itt.move_to(img_manager.ui_time_menu_core.cap_center_position_xy[0],img_manager.ui_time_menu_core.cap_center_position_xy[1])
    itt.left_down()
    time.sleep(0.5)
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

if __name__ == '__main__':
    set_genshin_time()
    # p1 = [0,0]
    # p2 = np.array([[1,1],[2,2]])
    # euclidean_distance_plist(p1,p2)
    
    # print(points_angle([0, 0], [10, 10], NEGATIVE_Y))
    # print(points_angle([10, 10], [0, 0], NEGATIVE_Y))
    # print(points_angle([0, 0], [20, 10], NEGATIVE_Y))
    # print(points_angle([0, 10], [10, 10], NEGATIVE_Y))
    # while 1:
    #     time.sleep(0.2)
    #     print(f_recognition(itt))
