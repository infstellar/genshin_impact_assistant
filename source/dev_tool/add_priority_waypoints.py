from source.util import *
import numpy as np
from source.funclib import big_map
from source.interaction.minimap_tracker import tracker
import cv2

global priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum
priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum = None, None, None, None
priority_waypoints = load_json("priority_waypoints.json", default_path='assets')
itt = big_map.itt
def load_pw():
    global priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum
    priority_waypoints_list = []
    for i in priority_waypoints:
        priority_waypoints_list.append(i["position"])
    priority_waypoints_array = np.array(priority_waypoints_list)
    idnum = priority_waypoints[-1]["id"]
load_pw()

def show_bigmap_posi_in_window(current_teyvat_posi, bigmap_posi_list):
    global priority_waypoints
    
    bigmap_posi_list = np.delete(bigmap_posi_list, np.where(abs(bigmap_posi_list[:,0])>1920)[0], axis=0)
    bigmap_posi_list = np.delete(bigmap_posi_list, np.where(abs(bigmap_posi_list[:,1])>1080)[0], axis=0)
    origin_show_img = itt.capture(jpgmode=0).copy()
    show_img = origin_show_img.copy()
    
    for i in list(bigmap_posi_list):
        origin_show_img = cv2.drawMarker(origin_show_img, position=(int(i[0]), int(i[1])), color=(0, 0, 255), markerSize=5, markerType=cv2.MARKER_CROSS, thickness=1)
        origin_bpl = big_map.bigmap_posi2teyvat_posi(current_teyvat_posi, np.array(i))
        cid = -1
        for ii in priority_waypoints:
            if list(map(int,ii["position"])) == list(map(int, list(origin_bpl))):
                cid = ii["id"]
        if cid == -1:
            logger.error(f"CANNOT FIND img id! position: {list(map(int, list(origin_bpl)))}")
        origin_show_img = cv2.putText(origin_show_img, str(cid), (int(i[0]), int(i[1])+5), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 255, 255), 1)
    cv2.imshow('win',origin_show_img)
    cv2.waitKey(0)

def add_mode():
    global priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum
    while 1:
        currentp=list(tracker.get_position())
        if currentp == [0,0]:
            print("获取坐标失败")
            time.sleep(1)
            continue
        # 计算当前点到所有优先点的曼哈顿距离
        md = manhattan_distance_plist(currentp, priority_waypoints_array)
        nearly_pp_arg = np.argsort(md)
        # 计算当前点到所有优先点的欧拉距离
        nearly_pp = priority_waypoints_array[nearly_pp_arg[:9]]
        ed = euclidean_distance_plist(currentp, nearly_pp)
        # 将点按欧拉距离升序排序
        nearly_pp_arg = np.argsort(ed)
        nearly_pp = nearly_pp[nearly_pp_arg]
        
        closest_pp = nearly_pp[0]
        if ed[0]>25:
            priority_waypoints.append(
                {
                "id" : idnum+1,
                "position":list(currentp)
            }
                )
            load_pw()
            save_json(priority_waypoints, "priority_waypoints.json", default_path='assets')
            print('add position', list(currentp))
        # print()
        
def edit_mode():
    global priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum
    input("请切换至大世界界面后，等待数秒，按下回车")
    cp=list(tracker.get_position())
    input("请切换至地图界面后按下回车")
    while 1:
        load_pw()
        p = big_map.teyvat_posi2bigmap_posi(cp, np.array(priority_waypoints_list))
        show_bigmap_posi_in_window(cp, p)
        delid = list(map(int, input("del id:").split(',')))
        if delid == 0 or delid == [0]:
            break
        for ii in delid:
            for i in priority_waypoints:
                if i["id"] == ii:
                    del(priority_waypoints[priority_waypoints.index(i)])
    save_json(priority_waypoints, json_name="priority_waypoints.json", default_path='assets')

def show_current_posi():
    while 1:
        time.sleep(0.2)
        print(tracker.get_position())

time.sleep(1)
# add_mode()
edit_mode()
# show_current_posi()
