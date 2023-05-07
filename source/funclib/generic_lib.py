from source.interaction.interaction_core import itt
from source.manager import posi_manager, asset
from source.funclib import big_map
from source.util import *
from source.ui.ui import ui_control
import source.ui.page as UIPage
from source.interaction.minimap_tracker import tracker


NORMAL = 0
NEGATIVE_Y = 1
NEGATIVE_X = 2
NEGATIVE_XY = 3
itt = itt

def f_recognition(mode='button_only'):
    if itt.get_img_existence(asset.IconGeneralFButton):
        return True
    else:
        return False

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
    if math.isnan(k):
        k = 0
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
    from source.api.pdocr_complete import ocr
    ui_control.ui_goto(UIPage.page_bigmap)
    gsp = big_map.get_middle_gs_point(stop_func)
    if len(gsp)==0:
        logger.info(t2t("获取传送锚点失败，正在重试"))
        big_map.reset_map_size()
        gsp = big_map.get_middle_gs_point(stop_func)
    itt.move_and_click(gsp)
    time.sleep(0.5)
    p1 = ocr.get_text_position(itt.capture(jpgmode=0), "七天神像")
    if p1 != -1:
        itt.move_and_click([p1[0] + 30, p1[1] + 30], delay=1)

    itt.move_and_click([posi_manager.tp_button[0], posi_manager.tp_button[1]], delay=1)
    # itt.delay(1)
    # itt.left_click()
    while not itt.get_img_existence(asset.IconUIEmergencyFood):
        if stop_func():
            break
        time.sleep(1)
    while tracker.in_excessive_error:
        if stop_func():
            break
        time.sleep(1)
    
    

def set_genshin_time(x=18, stop_func = lambda:False): # 调整时间至夜晚
    ui_control.ui_goto(UIPage.page_time)
    time.sleep(0.8)
    itt.move_to(asset.IconUITimeMenuCore.cap_center_position_xy[0],
                asset.IconUITimeMenuCore.cap_center_position_xy[1])
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
        ret = itt.appear_then_click(asset.ButtonGeneralExit)
        if ret:
            break
        if stop_func():
            break
        time.sleep(1)
    time.sleep(2)
    ui_control.ui_goto(UIPage.page_main)



def f():
    return False

if __name__ == '__main__':
    pass
    # recover_all(f)
    # p1 = [0,0]
    # p2 = np.array([[1,1],[2,2]])
    # euclidean_distance_plist(p1,p2)
    # print(get_characters_name())
    # set_genshin_time()
    # # print(points_angle([0, 0], [10, 10], NEGATIVE_Y))
    # # print(points_angle([10, 10], [0, 0], NEGATIVE_Y))
    # # print(points_angle([0, 0], [20, 10], NEGATIVE_Y))
    # # print(points_angle([0, 10], [10, 10], NEGATIVE_Y))
    # while 1:
    #     time.sleep(0.2)
    #     print(f_recognition(itt))
