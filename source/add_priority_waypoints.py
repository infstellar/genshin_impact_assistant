from util import *
import cvAutoTrack, generic_lib, numpy as np
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
load_pw()
while 1:
    currentp=list(cvAutoTrack.cvAutoTrackerLoop.get_position()[1:])
    if currentp == [0,0]:
        print("获取坐标失败")
        time.sleep(1)
        continue
    # 计算当前点到所有优先点的曼哈顿距离
    md = generic_lib.manhattan_distance_plist(currentp, priority_waypoints_array)
    nearly_pp_arg = np.argsort(md)
    # 计算当前点到所有优先点的欧拉距离
    nearly_pp = priority_waypoints_array[nearly_pp_arg[:9]]
    ed = generic_lib.euclidean_distance_plist(currentp, nearly_pp)
    # 将点按欧拉距离升序排序
    nearly_pp_arg = np.argsort(ed)
    nearly_pp = nearly_pp[nearly_pp_arg]
    
    closest_pp = nearly_pp[0]
    if ed[0]>30:
        priority_waypoints.append(
            {
            "id" : idnum+1,
            "position":list(currentp)
        }
            )
        load_pw()
        save_json(priority_waypoints, "priority_waypoints.json", default_path='assests')
        print('add position', list(currentp))
    # print()