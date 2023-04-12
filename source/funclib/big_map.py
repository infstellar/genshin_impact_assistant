from source.util import *
from source.interaction.interaction_core import itt
from source.manager import scene_manager, img_manager, posi_manager, asset
from source.ui.ui import ui_control
import source.ui.page as UIPage

itt = itt

global priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum
priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum = None, None, None, None
priority_waypoints = load_json("priority_waypoints.json", default_path='assets')
def load_pw(): # 加载json中的所有优先点
    global priority_waypoints, priority_waypoints_list, priority_waypoints_array, idnum
    priority_waypoints_list = []
    for i in priority_waypoints:
        priority_waypoints_list.append(i["position"])
    priority_waypoints_array = np.array(priority_waypoints_list)
    idnum = priority_waypoints[-1]["id"]

def move_map(x:int, y:int)->None:
    """移动大地图

    Args:
        x (int): x方向上移动大小
        y (int): y方向上移动大小
    """
    x = x / 6
    y = y / 6
    logger.debug(f"move map x: {x} y: {y}")
    for i in range(6):
        itt.left_down()
        itt.move_to(x, y, relative=True)
        # itt.delay(0.1)
    itt.left_up()
    itt.delay(0.1)
    itt.move_to(-x * 6, -y * 6, relative=True)


def move_navigation_to_center(object_name: img_manager.ImgIcon)->None:
    """移动导航点到中心，暂不使用。

    Args:
        object_name (ImgIcon, optional): _description_. Defaults to img_manager.bigmap_AbyssMage.
    """
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


def get_navigation_posi(object_name: img_manager.ImgIcon)->list:
    """获得导航点的坐标，暂不使用。

    Args:
        object_name (img_manager.ImgIcon, optional): _description_. Defaults to img_manager.bigmap_AbyssMage.

    Returns:
        _type_: _description_
    """
    res_posi = itt.get_img_position(object_name)
    return res_posi


def calculate_nearest_posi(posi_list:list, target_posi:list):
    """计算最近坐标。

    Args:
        posi_list (list): _description_
        target_posi (list): _description_

    Returns:
        _type_: _description_
    """
    mind = 9999
    minposi = None
    for plist in posi_list: # 垃圾实现，以后改 XCYD
        d = euclidean_distance(plist, target_posi)
        if d <= mind:
            minposi = plist
            mind = d

        # print(d)

    return minposi, mind


def get_tw_points(bigmatMat, stop_func):
    """获得传送锚点的坐标

    Args:
        bigmatMat (Mat): 截图

    Returns:
        list: 坐标列表
    """
    ret = itt.match_multiple_img(bigmatMat, asset.IconBigmapTeleportWaypoint.image)
    if len(ret) == 0: # 自动重试
        logger.warning("获取传送锚点坐标失败，正在重试")
        time.sleep(5)
        bigmatMat = itt.capture(jpgmode=0)
        ui_control.ui_goto(UIPage.page_bigmap)
        # scene_manager.switchto_bigmapwin(scene_manager.default_stop_func)
        return get_tw_points(bigmatMat, stop_func)
    return ret

def get_gs_points(bigmatMat, stop_func):
    """获得传送锚点的坐标

    Args:
        bigmatMat (Mat): 截图

    Returns:
        list: 坐标列表
    """
    ret = itt.match_multiple_img(bigmatMat, asset.IconBigmapGodStatue.image, threshold=0.98)
    if len(ret) == 0: # 自动重试
        logger.warning("获取七天神像坐标失败，正在重试")
        time.sleep(5)
        bigmatMat = itt.capture(jpgmode=0)
        ui_control.ui_goto(UIPage.page_bigmap)
        # scene_manager.switchto_bigmapwin(scene_manager.default_stop_func)
        return get_gs_points(bigmatMat, stop_func)
    return np.asarray(ret)

def get_dm_points(bigmatMat, stop_func):
    """获得domain的坐标

    Args:
        bigmatMat (Mat): 截图

    Returns:
        list: 坐标列表
    """
    ret = itt.match_multiple_img(bigmatMat, asset.IconBigmapDomain.image, threshold=0.98)
    return np.asarray(ret)

def get_middle_gs_point(stop_func):
    """获得离屏幕中心最近的七天神像的坐标

    Returns:
        list: [x,y]
    """
    a = itt.capture(jpgmode=0)
    b = get_gs_points(a, stop_func)
    b = np.asarray(b)
    c = euclidean_distance_plist([1080/2,1920/2],b)
    d = np.argmin(c)
    e = b[d]
    return e

def get_closest_teleport_waypoint(object_img: img_manager.ImgIcon):
    """abandon

    Args:
        object_img (img_manager.ImgIcon): _description_

    Returns:
        _type_: _description_
    """
    return calculate_nearest_posi(
        itt.match_multiple_img(itt.capture(jpgmode=0), object_img.image),
        get_navigation_posi())
    
def reset_map_size():
    """重置地图大小为标准值
    """
    while not ui_control.verify_page(UIPage.page_bigmap):
        ui_control.ui_goto(UIPage.page_bigmap)
        time.sleep(2)
        
    
    for i in range(8):        
        itt.move_and_click(position=posi_manager.posi_suoxiaoditu, delay=0.2)
    time.sleep(1)
    for i in range(2):
        itt.move_and_click(position=posi_manager.posi_fangdaditu, delay=0.2)

def bigmap_posi2teyvat_posi(current_teyvat_posi:list, bigmap_posi_list:list) -> list:
    """将大地图上的坐标转换为提瓦特世界坐标。注意：中心必须为当前位置。

    Args:
        current_teyvat_posi (list): 当前位置在提瓦特世界的坐标
        bigmap_posi_list (list): 需要转换的大地图坐标

    Returns:
        list: 提瓦特坐标
    """
    bigmap_posi_list = bigmap_posi_list - [1920 / 2, 1080 / 2]
    bigmap_posi_list = bigmap_posi_list * 3.4  # 地图到提瓦特世界缩放比例
    bigmap_posi_list = bigmap_posi_list + current_teyvat_posi
    return bigmap_posi_list

def teyvat_posi2bigmap_posi(current_teyvat_posi, teyvat_posi_list):
    """提瓦特世界坐标转换为大地图坐标。注意：中心必须为当前位置。

    Args:
        current_teyvat_posi (list): 当前位置在提瓦特世界的坐标
        teyvat_posi_list (list): 需要转换的提瓦特世界坐标

    Returns:
        list: 大地图坐标
    """
    teyvat_posi_list = teyvat_posi_list - current_teyvat_posi
    teyvat_posi_list = teyvat_posi_list / 3.4
    teyvat_posi_list = teyvat_posi_list + [1920 / 2, 1080 / 2]
    return teyvat_posi_list

def nearest_big_map_tw_posi(current_posi, target_posi, stop_func, include_gs = True, include_dm = False):
    """获得距离目标坐标最近的大地图传送锚点坐标

    Args:
        current_posi (_type_): 当前提瓦特世界坐标
        target_posi (_type_): 目标坐标

    Returns:
        _type_: 最近的传送锚点坐标
    """
    twpoints = np.array(get_tw_points(itt.capture(jpgmode=0), stop_func)) # 获得所有传送锚点坐标
    if include_gs:
        twpoints = np.concatenate((twpoints, get_gs_points(itt.capture(jpgmode=0), stop_func)))
    if include_dm:
        if len(get_dm_points(itt.capture(jpgmode=0), stop_func)) > 0:
            twpoints = np.concatenate((twpoints, get_dm_points(itt.capture(jpgmode=0), stop_func)))
    if len(twpoints) == 0:
        return []
    twpoints_teyvat = twpoints.copy() # 拷贝
    twpoints_teyvat = np.delete(twpoints_teyvat, np.where(abs(twpoints_teyvat[:,0]-1920/2)>(1920/2-80))[0], axis=0) # 删除x方向上超过限定值的坐标，避免误触
    twpoints_teyvat = np.delete(twpoints_teyvat, np.where(abs(twpoints_teyvat[:,1]-1080/2)>(1080/2-55))[0], axis=0) # 删除y方向上超过限定值的坐标，避免误触
    twpoints_teyvat = bigmap_posi2teyvat_posi(current_posi, twpoints_teyvat) # 将大地图坐标转换为提瓦特坐标
    p = np.argmin(euclidean_distance_plist(target_posi, twpoints_teyvat)) # 计算最近的目标坐标（提瓦特）# 获得该坐标index
    return teyvat_posi2bigmap_posi(current_posi, twpoints_teyvat[p])

def nearest_teyvat_tw_posi(current_posi, target_posi, stop_func, include_gs = True):
    """获得距离目标坐标最近的传送锚点坐标

    Args:
        current_posi (_type_): _description_
        target_posi (_type_): _description_

    Returns:
        _type_: _description_
    """
    twpoints = np.array(get_tw_points(itt.capture(jpgmode=0), stop_func)) # 获得传送锚点坐标
    if include_gs:
        twpoints = np.concatenate((twpoints, get_gs_points(itt.capture(jpgmode=0), stop_func)))
    twpoints_teyvat = twpoints.copy() # copy
    twpoints_teyvat = bigmap_posi2teyvat_posi(current_posi, twpoints_teyvat) # 转换为提瓦特坐标
    p = np.argmin(euclidean_distance_plist(target_posi, twpoints_teyvat))
    # p = calculate_nearest_posi(twpoints_teyvat, target_posi)
    return twpoints_teyvat[p]
def f():
    return False
if __name__ == '__main__':
    # print(get_closest_TeleportWaypoint(img_manager.bigmap_AbyssMage))
    # load_pw()
    # reset_map_size()
    # a = get_gs_points()
    # a = get_middle_gs_point(f)
    # p = teyvat_posi2bigmap_posi([2625.204978515623, -5274.091235473633], np.array(priority_waypoints_list))
    # show_bigmap_posi_in_window([2625.204978515623, -5274.091235473633], p)
    reset_map_size()
    #a = nearest_big_map_tw_posi([0,0],[1,1],f)
    print()
    # itt.move_and_click(a)
    # for i in range(10):
    #     move_navigation_to_center()
