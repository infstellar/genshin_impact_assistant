import pyautogui

import interaction_background
import small_map
from util import *
import cvAutoTrack
import generic_lib

itt = interaction_background.InteractionBGD()
AHEAD = 0
LEFT = 1
RIGHT = 2
BACK = 3
CORRECT_DEGREE = config_json["corr_degree"]
HORIZONTAL = 1
VERTICALLY = 2
VERTICALLY_AND_HORIZONTAL = 3


# >0:right; <0:left
def move(direction, distance=1):
    if direction == AHEAD:
        itt.key_down('w', is_log=False)
        itt.delay(0.1 * distance)
        itt.key_up('w', is_log=False)
    if direction == LEFT:
        itt.key_down('a', is_log=False)
        itt.delay(0.1 * distance)
        itt.key_up('a', is_log=False)
    if direction == RIGHT:
        itt.key_down('d', is_log=False)
        itt.delay(0.1 * distance)
        itt.key_up('d', is_log=False)
    if direction == BACK:
        itt.key_down('s', is_log=False)
        itt.delay(0.1 * distance)
        itt.key_up('s', is_log=False)


def cview(angle=10, mode=HORIZONTAL):  # left<0,right>0
    angle = (2 * angle)
    if abs(angle) < 1:
        if angle < 0:
            angle = -1
        else:
            angle = 1
    itt.move_to(int(angle), 0, relative=True)


def move_view_p(x, y):
    # x,y=point
    itt.move_to(x, y)


def reset_view():
    pyautogui.click(button='middle')

def view_to_angle_domain(angle=0, deltanum=0.65, maxloop=100, corrected_num=CORRECT_DEGREE):
    cap = itt.capture(posi=small_map.posi_map)
    degree = small_map.jwa_3(cap)
    i = 0
    while not abs(degree - (angle - corrected_num)) < deltanum:
        degree = small_map.jwa_3(itt.capture(posi=small_map.posi_map))
        # print(degree)
        cview((degree - (angle - corrected_num)))
        time.sleep(0.05)
        if i > maxloop:
            break
        i += 1
    if i > 1:
        logger.debug('last degree: ' + str(degree))


def view_to_angle_teyvat(angle=0, deltanum=1, maxloop=30, corrected_num=CORRECT_DEGREE):
    '''加一个场景检测'''
    i = 0
    while 1:
        b, degree = cvAutoTrack.cvAutoTrackerLoop.get_rotation()
        if not b:
            time.sleep(0.1)
            continue
        cview((degree - (angle - corrected_num)) / 2)
        time.sleep(0.05)
        if i > maxloop:
            break
        if abs(degree - (angle - corrected_num)) < deltanum:
            break
        i += 1
    if i > 1:
        logger.debug('last degree: ' + str(degree))

def change_view_to_posi(pl):
    td=0
    degree=100
    i = 0
    while abs(td-degree)>10:
        '''加一个场景检测'''
        time.sleep(0.05)
        tx, ty = cvAutoTrack.cvAutoTrackerLoop.get_position()[1:]
        td = cvAutoTrack.cvAutoTrackerLoop.get_rotation()[1]
        degree = generic_lib.points_angle([tx,ty], pl, coordinate=generic_lib.NEGATIVE_Y)
        cvn=td-degree
        if cvn>=50:
            cvn=50
        if cvn<=-50:
            cvn=-50
        cview(cvn)
        i+=1
        if i>=80:
            break

def reset_const_val():
    pass


# view_to_angle(-90)
if __name__ == '__main__':
    view_to_angle_domain(-90)
