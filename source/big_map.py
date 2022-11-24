import numpy as np
from util import *
import generic_lib
import img_manager, cv2
import interaction_background
import posi_manager

itt = interaction_background.InteractionBGD()

global priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum
priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum = None, None, None, None
priority_waypoints = load_json("priority_waypoints.json", default_path='assests')
def load_pw():
    global priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum
    priority_waypoints_list = []
    for i in priority_waypoints:
        priority_waypoints_list.append(i["position"])
    priority_waypoints_array = np.array(priority_waypoints_list)
    idnum = priority_waypoints[-1]["id"]

def move_map(x, y):
    x = x / 6
    y = y / 6
    for i in range(6):
        itt.left_down()
        itt.move_to(x, y, relative=True)
        # itt.delay(0.1)
    itt.left_up()
    itt.delay(0.1)
    itt.move_to(-x * 6, -y * 6, relative=True)


def move_navigation_to_center(object_name=img_manager.bigmap_AbyssMage):
    # template = img_manager.get_img_from_name(object_name, reshape=False)
    posi = itt.get_img_position(object_name)
    dx = posi[0] - 1920 / 2
    dy = posi[1] - 1080 / 2
    times = 2.5
    if abs(dx) >= 100:
        if dx > 0:
            move_map(-100 * times, 0)
        else:
            move_map(100 * times, 0)

    if abs(dy) >= 100:
        if dy > 0:
            move_map(0, -100 * times)
        else:
            move_map(0, 100 * times)

    # itt.move_to(1920/2,1080/2)


def get_navigation_posi(object_name=img_manager.bigmap_AbyssMage):
    res_posi = itt.get_img_position(object_name)
    return res_posi


def calculate_nearest_posi(posi_list, target_posi):
    mind = 9999
    minposi = None
    for plist in posi_list:
        d = generic_lib.euclidean_distance(plist, target_posi)
        if d <= mind:
            minposi = plist
            mind = d

        # print(d)

    return minposi, mind


def get_tw_points(bigmatMat):
    return itt.match_multiple_img(bigmatMat, img_manager.bigmap_TeleportWaypoint.image)


def get_closest_teleport_waypoint(object_img: img_manager.ImgIcon):
    return calculate_nearest_posi(
        itt.match_multiple_img(itt.capture(jpgmode=0), object_img.image),
        get_navigation_posi())
    
def reset_map_size():
    for i in range(8):        
        itt.move_and_click(position=posi_manager.posi_suoxiaoditu)
        time.sleep(0.2)
    time.sleep(1)
    for i in range(2):
        itt.move_and_click(position=posi_manager.posi_fangdaditu)
        time.sleep(0.2)

def bigmap_posi2teyvat_posi(current_teyvat_posi, bigmap_posi_list):
    bigmap_posi_list = bigmap_posi_list - [1920 / 2, 1080 / 2]
    bigmap_posi_list = bigmap_posi_list * 3.5  # 地图到提瓦特世界缩放比例
    bigmap_posi_list = bigmap_posi_list + current_teyvat_posi
    return bigmap_posi_list

def teyvat_posi2bigmap_posi(current_teyvat_posi, bigmap_posi_list):
    bigmap_posi_list = bigmap_posi_list - current_teyvat_posi
    bigmap_posi_list = bigmap_posi_list / 3.5
    bigmap_posi_list = bigmap_posi_list + [1920 / 2, 1080 / 2]
    return bigmap_posi_list

def nearest_big_map_tw_posi(current_posi, target_posi):
    twpoints = np.array(get_tw_points(itt.capture(jpgmode=0)))
    if len(twpoints) == 0:
        return []
    twpoints_teyvat = twpoints.copy()
    twpoints_teyvat = np.delete(twpoints_teyvat, np.where(abs(twpoints_teyvat[:,0]-1920/2)>(1920/2-80))[0], axis=0)
    twpoints_teyvat = np.delete(twpoints_teyvat, np.where(abs(twpoints_teyvat[:,1]-1080/2)>(1080/2-55))[0], axis=0)
    twpoints_teyvat = bigmap_posi2teyvat_posi(current_posi, twpoints_teyvat)
    p = calculate_nearest_posi(twpoints_teyvat, target_posi)
    a = np.where(twpoints_teyvat == p[0])[0][-1]
    return twpoints[a]

def nearest_teyvat_tw_posi(current_posi, target_posi):
    twpoints = np.array(get_tw_points(itt.capture(jpgmode=0)))
    twpoints_teyvat = twpoints.copy()
    twpoints_teyvat = bigmap_posi2teyvat_posi(current_posi, twpoints_teyvat)
    p = calculate_nearest_posi(twpoints_teyvat, target_posi)
    return p

if __name__ == '__main__':
    # print(get_closest_TeleportWaypoint(img_manager.bigmap_AbyssMage))
    # load_pw()
    reset_map_size()
    # p = teyvat_posi2bigmap_posi([2625.204978515623, -5274.091235473633], np.array(priority_waypoints_list))
    # show_bigmap_posi_in_window([2625.204978515623, -5274.091235473633], p)
    print()
    # for i in range(10):
    #     move_navigation_to_center()
