from source.interaction.interaction_core import itt
from source.funclib import small_map
from source.util import *
from source.funclib import generic_lib
from source.map.map import genshin_map
from source.manager import asset

itt = itt
AHEAD = 0
LEFT = 1
RIGHT = 2
BACK = 3
CORRECT_DEGREE = config_json["corr_degree"]
HORIZONTAL = 1
VERTICALLY = 2
VERTICALLY_AND_HORIZONTAL = 3

CLIMBING = "CLIMBING"
SWIMMING = "SWIMMING"
WALKING = "WALKING"
FLYING = "FLYING"

# >0:right; <0:left
def move(direction, distance=1):
    if IS_DEVICE_PC:
        if direction == AHEAD:
            itt.key_down('w')
            itt.delay(0.1 * distance)
            itt.key_up('w')
        if direction == LEFT:
            itt.key_down('a')
            itt.delay(0.1 * distance)
            itt.key_up('a')
        if direction == RIGHT:
            itt.key_down('d')
            itt.delay(0.1 * distance)
            itt.key_up('d')
        if direction == BACK:
            itt.key_down('s')
            itt.delay(0.1 * distance)
            itt.key_up('s')

def angle2movex(angle):
    cvn = maxmin(angle*10,500,-500) # 10: magic num, test from test246.py
    return cvn

def cview(angle=10, mode=HORIZONTAL, rate=0.9):  # left<0,right>0
    # logger.debug(f"cview: angle: {angle} mode: {mode}")
    if IS_DEVICE_PC:
        cvn = angle2movex(angle)*rate
        if abs(cvn) < 1:
            if cvn < 0:
                cvn = -1
            else:
                cvn = 1
        if mode == HORIZONTAL:
            itt.move_to(int(cvn), 0, relative=True)
        else:
            itt.move_to(0, int(angle), relative=True)


def move_view_p(x, y):
    # x,y=point
    itt.move_to(x, y)

def reset_view():
    if IS_DEVICE_PC:
        itt.middle_click()
        time.sleep(1)

def calculate_delta_angle(cangle,tangle):
    dangle = cangle - tangle
    if dangle>180:
        dangle = -(360-dangle)
    elif dangle<-180:
        dangle = (360+dangle)
    return dangle

def change_view_to_angle(tangle, stop_func=lambda:False, maxloop=25, offset=5, print_log=True):
    i = 0
    while 1:
        cangle = genshin_map.get_rotation()
        dangle = calculate_delta_angle(cangle,tangle)
        if abs(dangle) < offset:
            break
        rate = min((0.6/50)*abs(dangle)+0.4,1)
        
        """
        rate: 
        
        """
        
        # print(cangle, dangle, rate)
        cview(dangle, rate=rate)
        time.sleep(0.05)
        if i > maxloop:
            break
        if stop_func():
            break
        i += 1
        if i > 1:
            logger.trace(f"cangle {cangle} dangle {dangle} rate {rate}")

def view_to_angle_domain(angle, stop_func, deltanum=0.65, maxloop=100, corrected_num=CORRECT_DEGREE):
    if IS_DEVICE_PC:
        cap = itt.capture(posi=small_map.posi_map)
        degree = small_map.jwa_3(cap)
        i = 0
        if not abs(degree - (angle - corrected_num)) < deltanum:
            logger.debug(f"view_to_angle_domain: angle: {angle} deltanum: {deltanum} maxloop: {maxloop} ")
        while not abs(degree - (angle - corrected_num)) < deltanum:
            degree = small_map.jwa_3(itt.capture(posi=small_map.posi_map))
            # print(degree)
            cview((degree - (angle - corrected_num)))
            time.sleep(0.05)
            if i > maxloop:
                break
            if stop_func():
                break
            i += 1
        if i > 1:
            logger.debug('last degree: ' + str(degree))

def view_to_imgicon(cap:np.ndarray, imgicon:asset.ImgIcon):
    corr_rate=1
    ret_points = itt.match_multiple_img(cap, imgicon.image)
    if len(ret_points)==0:return False
    points_length=[]
    for point in ret_points:
        mx, my = SCREEN_CENTER_X,SCREEN_CENTER_Y
        points_length.append((point[0] - mx) ** 2 + (point[1] - my) ** 2)
    closest_point = ret_points[points_length.index(min(points_length))] # 获得距离鼠标坐标最近的一个坐标
    px, py = closest_point
    mx, my = SCREEN_CENTER_X,SCREEN_CENTER_Y
    px = (px - mx) / (2.4*corr_rate)
    py = (py - my) / (2*corr_rate) + 35 # 获得鼠标坐标偏移量
    # print(px,py)
    px=maxmin(px,350,-350)
    py=maxmin(py,350,-350)
    itt.move_to(px, py, relative=True)
    return int(math.sqrt(px**2+py**2)) # threshold: 50
    

# def view_to_angle_teyvat(angle, stop_func, deltanum=1, maxloop=30, corrected_num=CORRECT_DEGREE):
#     if IS_DEVICE_PC:
#         '''加一个场景检测'''
#         i = 0
        
#         if not abs(degree - (angle - corrected_num)) < deltanum:
#             logger.debug(f"view_to_angle_teyvat: angle: {angle} deltanum: {deltanum} maxloop: {maxloop}")
#         while 1:
#             degree = tracker.get_rotation()
#             change_view_to_angle(degree)
#             time.sleep(0.05)
#             if i > maxloop:
#                 break
#             if abs(degree - (angle - corrected_num)) < deltanum:
#                 break
#             if stop_func():
#                 break
#             i += 1
#         if i > 1:
#             logger.debug('last degree: ' + str(degree))

def calculate_posi2degree(pl):
    tx, ty = genshin_map.get_position()
    degree = generic_lib.points_angle([tx, ty], pl, coordinate=generic_lib.NEGATIVE_Y)
    if abs(degree)<1:
        return 0
    if math.isnan(degree):
        print({"NAN"})
        degree = 0
    return degree
    
def change_view_to_posi(pl, stop_func, max_loop=25, offset=5, print_log = True):
    if IS_DEVICE_PC:
        degree = calculate_posi2degree(pl)
        if print_log:
            if abs(degree)>=2:
                logger.debug(f"change_view_to_posi: pl: {pl}")
        change_view_to_angle(degree, maxloop=max_loop, stop_func=stop_func, offset=offset, print_log=print_log)

def move_to_position(posi, offset=5, stop_func=lambda:False, delay=0.1):
    itt.key_down('w')
    while 1:
        time.sleep(delay)
        curr_posi = genshin_map.get_position()
        if abs(euclidean_distance(curr_posi, posi))<=offset:
            break
  
        # print(abs(euclidean_distance(curr_posi, posi)))
        change_view_to_posi(posi,stop_func)
    itt.key_up('w')
    

def reset_const_val():
    pass

def f():
    return False
    
def get_current_motion_state() -> str:
    if itt.get_img_existence(asset.motion_climbing):
        return CLIMBING
    elif itt.get_img_existence(asset.motion_flying):
        return FLYING
    elif itt.get_img_existence(asset.motion_swimming):
        return SWIMMING
    else:
        return WALKING

def move_to_posi_LoopMode(target_posi, stop_func):
    """移动到指定坐标。适合用于while循环的模式。

    Args:
        target_posi (_type_): 目标坐标
        stop_func (_type_): 停止函数
    """
    delta_degree = abs(calculate_delta_angle(genshin_map.get_rotation(),calculate_posi2degree(target_posi)))
    if delta_degree >= 20:
        itt.key_up('w')
        change_view_to_posi(target_posi, stop_func = stop_func)
        itt.key_down('w')
    else:
        change_view_to_posi(target_posi, stop_func = stop_func, max_loop=4, offset=2, print_log = False)

# view_to_angle(-90)
if __name__ == '__main__':
    while 1:
        time.sleep(0.05)
        cap = itt.capture(jpgmode=0)
        ban_posi=asset.CommissionIcon.cap_posi
        cap[ban_posi[1]:ban_posi[3],ban_posi[0]:ban_posi[2]]=0
        print(view_to_imgicon(cap, asset.CommissionIconInCommission))
    # cview(-90, VERTICALLY)
    move_to_position([71, -2205])
