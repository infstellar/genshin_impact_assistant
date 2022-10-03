import os


def get_extra_params():
    # 项目根目录
    root_path = "D:\Program Files\Anaconda\envs\GIA_py"
    extra_data = [
        #("src\\res", "src\\res"),
        #("config", "config"),
        ("Lib\\site-packages\\Shapely.libs", "Shapely.libs"),
        ("Lib\\site-packages\\paddle", "paddle"),
        ("Lib\\site-packages\\paddleocr", "paddleocr"),
        ("Lib\\site-packages\\PIL", "PIL"),
        ("Lib\\site-packages\\pywt", "pywt"),
        ("Lib\\site-packages\\lmdb", "lmdb"),
        ("Lib\\site-packages\\shapely", "shapely"),
        ("Lib\\site-packages\\skimage", "skimage"),
        ("Lib\\site-packages\\pyclipper", "pyclipper"),
        ("Lib\\site-packages\\scipy", "scipy"),
        ("Lib\\site-packages\\imgaug", "imgaug"),
        ("Lib\\site-packages\\imageio", "imageio"),
        ("Lib\\site-packages\\attrdict", "attrdict")]
    params = []
    for item in extra_data:
        src_path = os.path.join(root_path, item[0])
        params.extend(["--add-data", f"{src_path};{item[1]}"])
    t=''
    for i in params:
        if i=='--add-data':
            t=t+((i+' '))
        else:
            t=t+(('\"'+i+'\"'+' '))
    return t


#import paddleocr


print(get_extra_params())