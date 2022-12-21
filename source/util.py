import inspect
import json
import os
import sys
import time  # 8药删了，qq了
import math
import numpy as np
import gettext

# 配置基本目录
try:
    from path_lib import *
except:
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_path = root_path + '\\source'
    if sys.path[0] != root_path:
        sys.path.insert(0, root_path)
    if sys.path[1] != source_path:
        sys.path.insert(1, source_path)
# root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# source_path = root_path + '\\source'
# if sys.path[0] != root_path:
#     sys.path.insert(0, root_path)
# if sys.path[1] != source_path:
#     sys.path.insert(1, source_path)
from loguru import logger
# load translation module
l10n = gettext.translation("zh_CN", localedir=os.path.join(root_path, "language/locale"), languages=["zh_CN"])
l10n.install()
_ = l10n.gettext
time.time()  # 防自动删除


def list_text2list(text: str) -> list:
    if text is not None:  # 判断是否为空
        try:  # 尝试转换
            rt_list = json.loads(text)
        except:
            rt_list = []

        if type(rt_list) != list:  # 判断类型(可能会为dict)
            rt_list = list(rt_list)

    else:
        rt_list = []

    return rt_list


def list2list_text(lst: list) -> str:
    if lst is not None:  # 判断是否为空
        try:  # 尝试转换
            rt_str = json.dumps(lst, ensure_ascii=False)
        except:
            rt_str = str(lst)

    else:
        rt_str = str(lst)

    return rt_str


def list2format_list_text(lst: list) -> str:
    if lst is not None:  # 判断是否为空
        try:  # 尝试转换
            rt_str = json.dumps(lst, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)
        except:
            rt_str = str(lst)

    else:
        rt_str = str(lst)
    print(rt_str)
    return rt_str


def is_json_equal(j1: str, j2: str) -> bool:
    try:
        return json.dumps(json.loads(j1), sort_keys=True) == json.dumps(json.loads(j2), sort_keys=True)
    except:
        return False





# 加载json
def load_json(json_name='config.json', default_path='config\\settings'):
    try:
        return json.load(open(os.path.join(root_path, default_path, json_name), 'r', encoding='utf-8'))
    except:
        json.dump({}, open(os.path.join(root_path, default_path, json_name), 'w', encoding='utf-8'))
        return json.load(open(os.path.join(root_path, default_path, json_name), 'r', encoding='utf-8'))

try:
    config_json = load_json("config.json")
    DEBUG_MODE = config_json["DEBUG"] if "DEBUG" in config_json else False
except:
    logger.error("config文件导入失败，可能由于初次安装。跳过导入。")
    DEBUG_MODE = False

# 设置debug


# 设置env path
# env_folder_path = config_json["env_floder_path"]
# env_path = os.path.abspath(os.path.join(root_path, env_folder_path))
# if True:
#     if sys.path[2] != env_path:
#         sys.path.insert(2, env_path)

# import asyncio
# import threading
# from source.webio import webio
# from pywebio import platform
# def server_thread():
#     # https://zhuanlan.zhihu.com/p/101586682
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     ###

# platform.tornado.start_server(webio.main, auto_open_webbrowser=True, debug=DEBUG_MODE)
# threading.Thread(target=server_thread, daemon=False).start()

# 配置logger
logger.remove(handler_id=None)
logger.add(os.path.join(root_path, os.path.join(root_path, 'Logs', "{time:YYYY-MM-DD}.log")), level="TRACE", backtrace=True, retention='15 days')
if DEBUG_MODE:
    logger.add(sys.stdout, level="TRACE", backtrace=True)
else:
    logger.add(sys.stdout, level="INFO", backtrace=True)

def add_logger_to_GUI(mode=0):
    import cccloggingaaa
    f = cccloggingaaa.flag1
    if mode == 1:
        cccloggingaaa.flag1 = True
    if not f:
        return 0
    import webio.log_handler
    cb_func = webio.log_handler.webio_poster
    if DEBUG_MODE:
        logger.add(cb_func, level="TRACE", backtrace=True)
    else:
        logger.add(cb_func, level="INFO", backtrace=True)
    logger.info("test")
add_logger_to_GUI()
# logger.add(webio.log_handler.webio_handler)
# 校验目录
if not os.path.exists(root_path):
    logger.error("目录不存在：" + root_path + " 请检查")
if not os.path.exists(source_path):
    logger.error("目录不存在：" + source_path + " 请检查")
# if not os.path.exists(env_path):
#     logger.error("目录不存在：" + env_path + " 请检查")

import ctypes, pickle


# 检查管理员
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if not is_admin():
    # print('try to get administrator')
    # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    # print('administrator have been obtained')
    logger.error("请用管理员权限运行")


def is_int(x):
    try:
        int(x)
    except ValueError:
        return False
    else:
        return True

def save_json(x, json_name='config.json', default_path='config', sort_keys=True):
    if sort_keys:
        json.dump(x, open(os.path.join(default_path, json_name), 'w', encoding='utf-8'), sort_keys=True, indent=2,
              ensure_ascii=False)
    else:
        json.dump(x, open(os.path.join(default_path, json_name), 'w', encoding='utf-8'),
              ensure_ascii=False)


def loadfileP(filename):
    with open('wordlist//' + filename + '.wl', 'rb') as fp:
        list1 = pickle.load(fp)
    return list1


def savefileP(filename, item):
    with open('wordlist//' + filename + '.wl', 'w+b') as fp:
        pickle.dump(item, fp)


def reflash_config():
    global config_json
    config_json = load_json("config.json")

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def euclidean_distance_plist(p1, p2):
    return np.sqrt((p1[0] - p2[:,0]) ** 2 + (p1[1] - p2[:,1]) ** 2)

def manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def manhattan_distance_plist(p1, p2):
    return abs(p1[0]-p2[:,0]) + abs(p1[1]-p2[:,1])

if __name__ == '__main__':
    logger.info("test")


def is_number(s):
    """
    懒得写,抄的
    https://www.runoob.com/python3/python3-check-is-number.html
    """
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

import cv2
from PIL import Image

def crop(image, area):
    """
    Crop image like pillow, when using opencv / numpy.
    Provides a black background if cropping outside of image.
    Args:
        image (np.ndarray):
        area:
    Returns:
        np.ndarray:
    """
    x1, y1, x2, y2 = map(int, map(round, area))
    h, w = image.shape[:2]
    border = np.maximum((0 - y1, y2 - h, 0 - x1, x2 - w), 0)
    x1, y1, x2, y2 = np.maximum((x1, y1, x2, y2), 0)
    image = image[y1:y2, x1:x2].copy()
    if sum(border) > 0:
        image = cv2.copyMakeBorder(image, *border, borderType=cv2.BORDER_CONSTANT, value=(0, 0, 0))
    return image

def get_color(image, area):
    """Calculate the average color of a particular area of the image.
    Args:
        image (np.ndarray): Screenshot.
        area (tuple): (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
    Returns:
        tuple: (r, g, b)
    """
    temp = crop(image, area)
    color = cv2.mean(temp)
    return color[:3]


def get_bbox(image, offset=5):
    """
    A numpy implementation of the getbbox() in pillow.
    Args:
        image (np.ndarray): Screenshot.
    Returns:
        tuple: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
    """
    if image_channel(image) == 3:
        image = np.max(image, axis=2)
    x = np.where(np.max(image, axis=0) > offset)[0]
    y = np.where(np.max(image, axis=1) > offset)[0]
    return (x[0], y[0], x[-1] + 1, y[-1] + 1)

def area_offset(area, offset):
    """
    Args:
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        offset: (x, y).
    Returns:
        tuple: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
    """
    return tuple(np.array(area) + np.append(offset, offset))

def image_channel(image):
    """
    Args:
        image (np.ndarray):
    Returns:
        int: 0 for grayscale, 3 for RGB.
    """
    return image.shape[2] if len(image.shape) == 3 else 0


def image_size(image):
    """
    Args:
        image (np.ndarray):
    Returns:
        int, int: width, height
    """
    shape = image.shape
    return shape[1], shape[0]

