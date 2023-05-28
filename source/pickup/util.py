from source.util import *
from source.interaction.interaction_core import itt
import pyautogui
from source.funclib.generic_lib import f_recognition
from source.api.pdocr_complete import ocr
from source.manager import asset

def get_coll_name():
    ret = itt.get_img_position(asset.IconGeneralFButton)
    y1 = asset.IconGeneralFButton.cap_posi[1]
    x1 = asset.IconGeneralFButton.cap_posi[0]
    cap = itt.capture()
    cap = crop(cap, [x1 + ret[0] + 53, y1 + ret[1] - 20, x1 + ret[0] + 361,  y1 + ret[1] + 54])
    cap = itt.png2jpg(cap, channel='ui', alpha_num=160)
    res = ocr.get_all_texts(cap,mode=1)
    return res

def get_all_colls_name():
    coll_names = []
    for i in range(12):
        pyautogui.scroll(10)
        time.sleep(0.01)
    for i in range(50):
        if not f_recognition():break
        res = get_coll_name()
        if res not in coll_names:
            coll_names.append(res)
        else:
            break
        pyautogui.scroll(-1)
        itt.delay("animation")
    return coll_names

def pickup_specific_item(x:str) -> bool:
    for i in range(12):
        pyautogui.scroll(10)
        time.sleep(0.01)
    last_res = ""
    for i in range(50):
        if not f_recognition():break
        res = get_coll_name()
        if x in res:
            itt.key_press('f')
            return True
        if last_res == res:break
        last_res = res
        pyautogui.scroll(-1)
        itt.delay("animation")
    return False

if __name__ == '__main__':
    for i in range(12):
        pyautogui.scroll(1)
        time.sleep(0.01)