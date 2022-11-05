import math
import time

import cv2

import interaction_background, img_manager, generic_lib
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
    posi = itt.get_img_position(object_name, reshape=False)
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

def get_closest_TeleportWaypoint(object_name):
    return calculate_nearest_posi(
        itt.match_multiple_img(itt.capture(jpgmode = 0), img_manager.get_img_from_name(object_name, reshape=False)),
        get_navigation_posi())

if __name__ == '__main__':
    print(get_closest_TeleportWaypoint(img_manager.bigmap_AbyssMage))
    
    
    # for i in range(10):
    #     move_navigation_to_center()