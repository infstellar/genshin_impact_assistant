
import time, math, shutil, sys, os, json
import win32gui, win32process, psutil, ctypes, pickle, traceback
import numpy as np
import cv2, yaml
from PIL import Image, ImageDraw, ImageFont
from collections import OrderedDict
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_PATH = ROOT_PATH + '\\source'
ASSETS_PATH = ROOT_PATH + '\\assets'
if sys.path[0] != ROOT_PATH:   sys.path.insert(0, ROOT_PATH)
if sys.path[1] != SOURCE_PATH: sys.path.insert(1, SOURCE_PATH)
from source.logger import logger
from source.config.config import GIAconfig
from source.i18n import t2t, GLOBAL_LANG
from source.path_lib import *
from source.cvars import *

time
yaml
shutil
pickle
traceback

DEBUG_MODE = GIAconfig.General_DEBUG
DEMO_MODE = False
INTERACTION_MODE = GIAconfig.General_InteractionMode
IS_DEVICE_PC = True

# load config file
def load_json(json_name='General.json', default_path='config\\settings', auto_create = False) -> dict:
    # if "$lang$" in default_path:
    #     default_path = default_path.replace("$lang$", GLOBAL_LANG)
    all_path = os.path.join(ROOT_PATH, default_path, json_name)
    try:
        return json.load(open(all_path, 'r', encoding='utf-8'), object_pairs_hook=OrderedDict)
    except:
        if not auto_create:
            logger.critical(f"尝试访问{all_path}失败")
            raise FileNotFoundError(all_path)
        else:
            json.dump({}, open(all_path, 'w', encoding='utf-8'))
            return json.load(open(all_path, 'r', encoding='utf-8'))
        


# try:
#     if INTERACTION_MODE not in [INTERACTION_EMULATOR, INTERACTION_DESKTOP_BACKGROUND, INTERACTION_DESKTOP]:
#         logger.warning("UNKNOWN INTERACTION MODE. SET TO \'Desktop\' Default.")
#         INTERACTION_MODE = INTERACTION_DESKTOP
# except:
#     logger.error("config文件导入失败，可能由于初次安装。跳过导入。 ERROR_IMPORT_CONFIG_002")
#     INTERACTION_MODE = INTERACTION_DESKTOP
# IS_DEVICE_PC = (INTERACTION_MODE == INTERACTION_DESKTOP_BACKGROUND)or(INTERACTION_MODE == INTERACTION_DESKTOP)
# load config file over

# load translation module
# def get_local_lang():
#     import locale
#     lang = locale.getdefaultlocale()[0]
#     logger.debug(f"locale: {locale.getdefaultlocale()}")
#     if lang in ["zh_CN", "zh_SG", "zh_MO", "zh_HK", "zh_TW"]:
#         return "zh_CN"
#     else:
#         return "en_US"

# if GLOBAL_LANG == "$locale$":
#     GLOBAL_LANG = get_local_lang()
#     GLOBAL_LANG = "zh_CN"
logger.info(f"language set as: {GLOBAL_LANG}")

# load translation module over



# verify path
if not os.path.exists(ROOT_PATH):
    logger.error(t2t("目录不存在：") + ROOT_PATH + t2t(" 请检查"))
if not os.path.exists(SOURCE_PATH):
    logger.error(t2t("目录不存在：") + SOURCE_PATH + t2t(" 请检查"))
# verify path over



# verify administration
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if not is_admin():
    logger.error(t2t("请用管理员权限运行"))
# verify administration over


# functions
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


def list2format_list_text(lst: list, inline = False) -> str:
    if lst is not None:  # 判断是否为空
        try:  # 尝试转换
            rt_str = json.dumps(lst, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)
        except:
            rt_str = str(lst)

    else:
        rt_str = str(lst)
    # print(rt_str)
    if inline:
        rt_str = rt_str.replace('\n', ' ')
    return rt_str


def is_json_equal(j1: str, j2: str) -> bool:
    try:
        return json.dumps(json.loads(j1), sort_keys=True) == json.dumps(json.loads(j2), sort_keys=True)
    except:
        return False

def is_int(x):
    try:
        int(x)
    except ValueError:
        return False
    else:
        return True

def points_angle(p1, p2, coordinate=ANGLE_NORMAL):
    # p1: current point
    # p2: target point
    x = p1[0]
    y = p1[1]
    tx = p2[0]
    ty = p2[1]
    if coordinate == ANGLE_NEGATIVE_Y:
        y = -y
        ty = -ty
    k = (ty - y) / (tx - x)
    degree = math.degrees(math.atan(k))
    if degree < 0:
        degree += 180
    if ty < y:
        degree += 180

    degree -= 90
    if degree > 180:
        degree -= 360
    return degree

def save_json(x, json_name='General.json', default_path='config\\settings', sort_keys=True, auto_create=False):
    if not os.path.exists(default_path):
        logger.error(f"CANNOT FIND PATH: {default_path}")
    if sort_keys:
        json.dump(x, open(os.path.join(default_path, json_name), 'w', encoding='utf-8'), sort_keys=True, indent=2,
              ensure_ascii=False)
    else:
        json.dump(x, open(os.path.join(default_path, json_name), 'w', encoding='utf-8'),
              ensure_ascii=False)

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def euclidean_distance_plist(p1, plist) -> np.ndarray:
    if not isinstance(p1, np.ndarray):
        p1 = np.array(p1)
    if not isinstance(plist, np.ndarray):
        plist = np.array(plist)
    return np.sqrt((p1[0] - plist[:,0]) ** 2 + (p1[1] - plist[:,1]) ** 2)

def manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def manhattan_distance_plist(p1, p2) -> np.ndarray:
    return abs(p1[0]-p2[:,0]) + abs(p1[1]-p2[:,1])

def quick_euclidean_distance_plist(p1, plist, max_points_num = 50)-> np.ndarray:
    if not isinstance(p1, np.ndarray):
        p1 = np.array(p1)
    if not isinstance(plist, np.ndarray):
        plist = np.array(plist)
    # 计算当前点到所有优先点的曼哈顿距离
    md = manhattan_distance_plist(p1, plist)
    nearly_pp_arg = np.argsort(md)
    ed = md.copy()
    # 计算当前点到距离最近的50个优先点的欧拉距离
    # cache_num = min(max_points_num, len(nearly_pp_arg))
    i = 0
    for i in nearly_pp_arg:
        ed[i] = euclidean_distance(plist[i], p1)
        i += 1
        if i >= max_points_num:
            break
    # nearly_pp = plist[nearly_pp_arg[:cache_num]]
    # ed = euclidean_distance_plist(p1, nearly_pp)
    return ed

    # 将点按欧拉距离升序排序
    nearly_pp_arg = np.argsort(ed)
    nearly_pp = nearly_pp[nearly_pp_arg]
    # print(currentp, closest_pp)
    return nearly_pp
    


    return np.sqrt((p1[0] - plist[:,0]) ** 2 + (p1[1] - plist[:,1]) ** 2)



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



def get_active_window_process_name():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return(psutil.Process(pid[-1]).name())
    except:
        pass

def maxmin(x,nmax,nmin):
    x = min(x, nmax)
    x = max(x, nmin)
    return x

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

def recorp(image, area, size=None):
    if size is None:
        size=[1920,1080,3]
    r = np.zeros((size[1], size[0], size[2]), dtype='uint8')
    r[area[1]:area[3], area[0]:area[2], :] = image
    return r
    

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


def get_bbox(image, black_offset=15):
    """
    A numpy implementation of the getbbox() in pillow.
    Args:
        image (np.ndarray): Screenshot.
    Returns:
        tuple: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
    """
    if image_channel(image) == 3:
        image = np.max(image, axis=2)
    x = np.where(np.max(image, axis=0) > black_offset)[0]
    y = np.where(np.max(image, axis=1) > black_offset)[0]
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

def convert_text_to_img(text=""):
    # 加载一个中文字体文件
    font = ImageFont.truetype("simhei.ttf", 32)

    # 获取一段中文文字的宽度和高度
    width, height = font.getsize(text)

    # 创建一个白色背景的图片，大小刚好能容纳文字
    img = Image.new("RGB", (width, height), "white")

    # 创建一个绘图对象
    draw = ImageDraw.Draw(img)

    # 在图片上绘制文字，位置为左上角
    draw.text((0, 0), text, font=font, fill="black")

    # 将图片转换回OpenCV格式
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    return img

def replace_text_format(text:str):
    text = text.replace("：",":")
    text = text.replace("！","!")
    text = text.replace("？","?")
    text = text.replace("，",",")
    text = text.replace("。",".")
    text = text.replace("“","\"")
    text = text.replace("”","\"")
    text = text.replace("‘","\'")
    text = text.replace("’","\'")
    return text

def compare_texts(text1, text2, is_show_res = False, ignore_warning = False):
    # 读取两个短文本的图片
    
    if not ignore_warning:
        if len(text1) != len(text2):
            logger.trace(f"compare_texts警告：不相同的文字长度:{text1}, {text2}")
    
    font = ImageFont.truetype("simhei.ttf", 16)
    width1, height1 = font.getsize(text1)
    width2, height2 = font.getsize(text2)
    width = max(width1, width2)
    height = max(height1, height2)
    img1 = Image.new("RGB", (width, height), "white")
    img2 = Image.new("RGB", (width, height), "white")
    draw1 = ImageDraw.Draw(img1)
    draw1.text((0, 0), text1, font=font, fill="black")
    draw2 = ImageDraw.Draw(img2)
    draw2.text((0, 0), text2, font=font, fill="black")
    img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
    img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
        
    
    # 将图片转换为灰度图
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 计算两个灰度图之间的绝对差异
    diff = cv2.absdiff(gray1, gray2)

    # 设置一个阈值，将差异大于阈值的像素标记为白色，小于阈值的像素标记为黑色
    thresh = 50
    mask = diff > thresh

    # 将掩码转换为uint8类型，并乘以255，得到二值化后的差异图像
    mask = mask.astype(np.uint8) * 255

    matching_rate = 1 - len(np.where(mask==255)[0])/len(np.where(mask!=256)[0])
    logger.trace(f"texts matching rate:{matching_rate} text1 {text1} text2 {text2}")
    if len(text1) != len(text2):
        matching_rate = max( matching_rate - 0.06*abs(len(text1) - len(text2)), 0)
        logger.trace(f"fixed matching rate:{matching_rate}")
    if is_show_res:
        # 在原始图片上绘制红色边框，表示差异区域
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(img1,(x,y),(x+w,y+h),(0,0,255),3)
            cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),3)

        # 显示结果图片
        cv2.imshow("Image 1", img1)
        cv2.imshow("Image 2", img2)
        cv2.imshow("Difference", mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    return matching_rate

def extract_white_letters(image, threshold=128):
    """Set letter color to black, set background color to white.
    This function will discourage color pixels (Non-gray pixels)
    Args:
        image: Shape (height, width, channel)
        threshold (int):
    Returns:
        np.ndarray: Shape (height, width)
    """
    r, g, b = cv2.split(cv2.subtract((255, 255, 255, 0), image))
    minimum = cv2.min(cv2.min(r, g), b)
    maximum = cv2.max(cv2.max(r, g), b)
    return cv2.multiply(cv2.add(maximum, cv2.subtract(maximum, minimum)), 255.0 / threshold)

def load_json_from_folder(path, black_file:list=None):
    json_list = []
    if black_file is None:
        black_file = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f[f.index('.') + 1:] == "json":
                if f[:f.index('.')] not in black_file:
                    j = json.load(open(os.path.join(path, f), 'r', encoding='utf-8'))
                    json_list.append({"label": f, "json": j})
    return json_list

def color_similarity(color1, color2):
    """
    Args:
        color1 (tuple): (r, g, b)
        color2 (tuple): (r, g, b)
    Returns:
        int:
    """
    diff = np.array(color1).astype(int) - np.array(color2).astype(int)
    diff = np.max(np.maximum(diff, 0)) - np.min(np.minimum(diff, 0))
    return diff


def color_similar(color1, color2, threshold=10):
    """Consider two colors are similar, if tolerance lesser or equal threshold.
    Tolerance = Max(Positive(difference_rgb)) + Max(- Negative(difference_rgb))
    The same as the tolerance in Photoshop.
    Args:
        color1 (tuple): (r, g, b)
        color2 (tuple): (r, g, b)
        threshold (int): Default to 10.
    Returns:
        bool: True if two colors are similar.
    """
    # print(color1, color2)
    diff = np.array(color1).astype(int) - np.array(color2).astype(int)
    diff = np.max(np.maximum(diff, 0)) - np.min(np.minimum(diff, 0))
    return diff <= threshold


def color_similar_1d(image, color, threshold=10):
    """
    Args:
        image (np.ndarray): 1D array.
        color: (r, g, b)
        threshold(int): Default to 10.
    Returns:
        np.ndarray: bool
    """
    diff = image.astype(int) - color
    diff = np.max(np.maximum(diff, 0), axis=1) - np.min(np.minimum(diff, 0), axis=1)
    return diff <= threshold


def color_similarity_2d(image, color):
    """
    Args:
        image: 2D array.
        color: (r, g, b)
    Returns:
        np.ndarray: uint8
    """
    r, g, b = cv2.split(cv2.subtract(image, (*color, 0)))
    positive = cv2.max(cv2.max(r, g), b)
    r, g, b = cv2.split(cv2.subtract((*color, 0), image))
    negative = cv2.max(cv2.max(r, g), b)
    return cv2.subtract(255, cv2.add(positive, negative))

def circle_mask(img,inner_r, outer_r):
    # 指定内半径和外半径
    inner_radius = inner_r
    outer_radius = outer_r

    # 创建一个黑色的图像作为遮罩
    mask = np.zeros_like(img)

    # 在遮罩上绘制圆环
    cv2.circle(mask, (img.shape[1]//2, img.shape[0]//2), outer_radius, (255, 255, 255), -1)
    cv2.circle(mask, (img.shape[1]//2, img.shape[0]//2), inner_radius, (0, 0, 0), -1)

    # 将遮罩应用于原图
    masked_img = cv2.bitwise_and(img, mask)
    
    return masked_img

def get_circle_points(x,y,  show_res = False):
    if show_res:
        import turtle
        turtle.speed(0)
    points = []
    for r in range(5, 5*6, 5):
        n = int(2 * math.pi * r / (5))
        for i in range(n):
            angle = 2 * math.pi / n * i
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            if show_res:
                turtle.penup()
                turtle.goto(px, py)
                turtle.pendown()
                turtle.dot(2)
            points.append((px, py))
    return points



if __name__ == '__main__':
    # a = load_jsons_from_folder(os.path.join(root_path, "config\\tactic"))
    print(load_json("team_example_1.json", fr"{CONFIG_PATH}/tactic"))
    print()
    pass
    # load_jsons_from_floder((root_path, "config\\tactic"))