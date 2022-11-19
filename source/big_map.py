import math
import time

import cv2

import interaction_background, img_manager, generic_lib
import numpy as np
from unit import *

itt = interaction_background.InteractionBGD()

def move_map(x,y):
    x=x/6
    y=y/6
    for i in range(6):
        itt.left_down()
        itt.move_to(x,y,relative=True)
        # itt.delay(0.1)
    itt.left_up()
    itt.delay(0.1)
    itt.move_to(-x*6,-y*6,relative=True)

def move_navigation_to_center(object_name=img_manager.bigmap_AbyssMage):
    # template = img_manager.get_img_from_name(object_name, reshape=False)
    posi = itt.get_img_position(object_name)
    dx = posi[0] - 1920/2
    dy = posi[1] - 1080/2
    times=2.5
    if abs(dx)>=100:
        if dx>0:
            move_map(-100*times,0)
        else:
            move_map(100*times,0)

    if abs(dy)>=100:
        if dy>0:
            move_map(0,-100*times)
        else:
            move_map(0,100*times)
    
    # itt.move_to(1920/2,1080/2)

def get_navigation_posi(object_name=img_manager.bigmap_AbyssMage):
    res_posi = itt.get_img_position(object_name)
    return res_posi

def calculate_nearest_posi(posi_list, target_posi):
    mind=9999
    minposi=None
    for plist in posi_list:
        d = generic_lib.points_distance(plist, target_posi)
        if d<=mind:
            minposi = plist
            mind = d

        # print(d)
            
    return minposi, mind

def get_TW_points(bigmatMat):
    return itt.match_multiple_img(bigmatMat, img_manager.bigmap_TeleportWaypoint.image)

def get_closest_TeleportWaypoint(object_img:img_manager.ImgIcon):
    return calculate_nearest_posi(
        itt.match_multiple_img(itt.capture(jpgmode = 0), object_img.image),
        get_navigation_posi())

def bigmap_posi2teyvat_posi(current_teyvat_posi, bigmap_posi_list):
    bigmap_posi_list = bigmap_posi_list - [1920/2,1080/2]
    bigmap_posi_list = bigmap_posi_list * 3.5 # 地图到提瓦特世界缩放比例
    bigmap_posi_list = bigmap_posi_list + current_teyvat_posi
    return bigmap_posi_list

def get_nearest_TW_posi_in_bigmap(current_posi=[[683,-1519]], target_posi=[0,0]):
    twpoints = np.array(get_TW_points(itt.capture(jpgmode = 0)))
    twpoints_teyvat = twpoints.copy()
    twpoints_teyvat = bigmap_posi2teyvat_posi(current_posi, twpoints_teyvat)
    p = calculate_nearest_posi(twpoints_teyvat, target_posi)
    a = np.where(twpoints_teyvat==p[0])[0][-1]
    return twpoints[a]
    

if __name__ == '__main__':
    # print(get_closest_TeleportWaypoint(img_manager.bigmap_AbyssMage))
    a = get_nearest_TW_posi_in_bigmap()
    itt.move_to(a[0], a[1])
    print()
    # for i in range(10):
    #     move_navigation_to_center()