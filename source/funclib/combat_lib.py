from source.manager import img_manager, posi_manager, asset
from source.util import *
from source.common.base_threading import BaseThreading
import numpy as np
from common import timer_module
from source.common import character
from source.interaction.interaction_core import itt
from source.interaction import interaction_core
from source.api.pdocr_light import ocr_light
from source.api.pdocr_complete import ocr
from source.ui.ui import ui_control
from source.ui import page as UIPage
from source.common.lang_data import translate_character

"""
战斗相关常用函数库。
"""

global only_arrow_timer, characters, load_err_times
only_arrow_timer = timer_module.Timer()
characters = load_json("character.json", default_path="config\\tactic")
load_err_times = 0

def default_stop_func():
    return False

class TacticKeyNotFoundError(RuntimeError):
    def __init__(self, arg):
        self.args = [arg]

class TacticKeyEmptyError(RuntimeError):
    def __init__(self, arg):
        self.args = [arg]

CREATE_WHEN_NOTFOUND = 0
RAISE_WHEN_NOTFOUND = 1


def get_param(team_item, para_name, auto_fill_flag, chara_name="", exception_mode = RAISE_WHEN_NOTFOUND, value_when_empty = None):
    global load_err_times
    if para_name not in team_item:
        if exception_mode == RAISE_WHEN_NOTFOUND:
            logger.error(f"{t2t('Tactic ERROR: INDEX NOT FOUND')}")
            logger.error(f"{t2t('parameter name')}: {para_name}; {t2t('character name')}: {chara_name}")
            raise TacticKeyNotFoundError(f"Key: {para_name}")
        elif exception_mode == CREATE_WHEN_NOTFOUND:
            pass
    else:
        if not auto_fill_flag:
            r = team_item[para_name]
        else:
            r = characters[chara_name]
    
    if r == '' or r == None:
        if value_when_empty != None:
            r = value_when_empty
        else:
            logger.error(f"{t2t('Tactic ERROR: Key Empty')}")
            logger.error(f"{t2t('parameter name')}: {para_name}; {t2t('character name')}: {chara_name}")
            load_err_times+=1
            # raise TacticKeyEmptyError(f"Key: {para_name}")
    logger.trace(f"character: {chara_name} para_name: {para_name} value: {r}")
    return r

def get_chara_list(team_name='team.json'):
    global load_err_times
    load_err_times = 0
    team_name = load_json("auto_combat.json",CONFIG_PATH_SETTING)["teamfile"]
    dpath = "config\\tactic"
    
    team = load_json(team_name, default_path=dpath)
    
    for team_n in team:
        team_item = team[team_n]
        team_item.setdefault("name", None)
        team_item.setdefault("position", None)
        team_item.setdefault("priority", None)
        team_item.setdefault("E_short_cd_time", None)
        team_item.setdefault("E_long_cd_time", None)
        team_item.setdefault("Elast_time", None)
        team_item.setdefault("n", None)
        team_item.setdefault("trigger", None)
        team_item.setdefault("Epress_time", None)
        team_item.setdefault("Qlast_time", None)
        team_item.setdefault("Qcd_time", None)
        team_item.setdefault("vision", None)
    save_json(team, team_name, default_path=dpath)
    
    # characters = load_json("character.json", default_path=dpath)
    chara_list = []
    for team_name in team:
        team_item = team[team_name]
        autofill_flag = False
        # autofill_flag = team_item["autofill"]
        cname = get_param(team_item, "name", autofill_flag, chara_name="", )
        c_position = get_param(team_item, "position", autofill_flag, chara_name=cname, value_when_empty='')
        c_priority = get_param(team_item, "priority", autofill_flag, chara_name=cname)
        cE_short_cd_time = get_param(team_item, "E_short_cd_time", autofill_flag, chara_name=cname)
        cE_long_cd_time = get_param(team_item, "E_long_cd_time", autofill_flag, chara_name=cname)
        cElast_time = get_param(team_item, "Elast_time", autofill_flag, chara_name=cname)
        cn = get_param(team_item, "n", autofill_flag, chara_name=cname)
        try:
            c_tactic_group = team_item["tactic_group"]
        except:
            c_tactic_group = team_item["tastic_group"]
            logger.warning(t2t("请将配对文件中的tastic_group更名为tactic_group. 已自动识别。"))
            
        c_trigger = get_param(team_item, "trigger", autofill_flag, chara_name=cname, value_when_empty="e_ready")
        cEpress_time = get_param(team_item, "Epress_time", autofill_flag, chara_name=cname)
        cQlast_time = get_param(team_item, "Qlast_time", autofill_flag, chara_name=cname)
        cQcd_time = get_param(team_item, "Qcd_time", autofill_flag, chara_name=cname)
        c_vision = get_param(team_item, "vision", autofill_flag, chara_name=cname)
    
        chara_list.append(
            character.Character(
                name=cname, position=c_position, n=cn, priority=c_priority,
                E_short_cd_time=cE_short_cd_time, E_long_cd_time=cE_long_cd_time, Elast_time=cElast_time,
                tactic_group=c_tactic_group, trigger=c_trigger,
                Epress_time=cEpress_time, Qlast_time=cQlast_time, Qcd_time=cQcd_time, vision = c_vision
            )
        )
    if load_err_times>0:
        raise TacticKeyEmptyError(t2t("Character Key Empty Error"))
        
    return chara_list

def unconventionality_situation_detection(itt: interaction_core.InteractionBGD,
                                           autoDispose=True, detect_type='abc', stop_func=lambda:False):
    # unconventionality situlation detection
    # situlation 1: coming_out_by_space

    situation_code = -1
    if 'a' in detect_type:
        while itt.get_img_existence(asset.COMING_OUT_BY_SPACE):
            if stop_func:break
            situation_code = 1
            itt.key_press('spacebar')
            logger.debug('Unconventionality Situation: COMING_OUT_BY_SPACE')
            time.sleep(0.1)
    if 'b' in detect_type:
        while itt.get_img_existence(asset.motion_swimming):
            if stop_func:break
            situation_code = 2
            itt.key_down('w')
            logger.debug('Unconventionality Situation: SWIMMING')
            if autoDispose:
                time.sleep(5)
            itt.key_up('w')
            time.sleep(0.1)
    if 'c' in detect_type:
        while itt.get_img_existence(asset.motion_climbing):
            if stop_func:break
            situation_code = 3
            logger.debug('Unconventionality Situation: CLIMBING')
            if autoDispose:
                itt.key_press('x')
            time.sleep(0.1)

    return situation_code

def is_character_busy(stop_func, print_log = True):
    cap = itt.capture(jpgmode=2)
    # cap = itt.png2jpg(cap, channel='ui')
    t1 = 0
    t2 = 0
    for i in range(4):
        if stop_func():
            return 0
        p = posi_manager.chara_head_list_point[i]
        if cap[p[0], p[1]][0] > 0 and cap[p[0], p[1]][1] > 0 and cap[p[0], p[1]][2] > 0:
            t1 += 1
    for i in range(4):
        p = posi_manager.chara_num_list_point[i]
        # print(min(cap[p[0], p[1]]))
        if min(cap[p[0], p[1]]) > 248:
            t2 += 1
    
    # elif t == 4:
    #     logger.debug("function: get_character_busy: t=4： 测试中功能，如果导致换人失败，反复输出 waiting 请上报。")
    #     return True
    
    if t1 >= 3 and t2 == 3:
        return False
    else:
        if print_log:
            logger.trace(f"waiting: character busy: t1{t1} t2{t2}")
        return True

def chara_waiting(itt:interaction_core.InteractionBGD, stop_func, mode=0, max_times = 1000):
    unconventionality_situation_detection(itt)
    i=0
    while is_character_busy(stop_func) and (not stop_func()):
        i+=1
        if stop_func():
            logger.debug('chara_waiting stop')
            return 0
        # logger.debug('waiting')
        itt.delay(0.1)
        if i>=max_times:
            break

def get_current_chara_num(itt: interaction_core.InteractionBGD, stop_func = default_stop_func, max_times = 1000):
    """获得当前所选角色序号。

    Args:
        itt (InteractionBGD): InteractionBGD对象

    Returns:
        int: character num.
    """
    chara_waiting(itt, stop_func, max_times = max_times)
    cap = itt.capture(jpgmode=2)
    for i in range(4):
        p = posi_manager.chara_num_list_point[i]
        # print(min(cap[p[0], p[1]]))
        if min(cap[p[0], p[1]]) > 248:
            continue
        else:
            return i + 1
        
    logger.warning(t2t("获得当前角色编号失败"))
    return 0


    
def get_arrow_img(img):
    img = itt.png2jpg(img, channel='ui', alpha_num=150)
    red_num = 250
    blue_num = 90
    green_num = 90
    float_num = 30
 
    def extract_red(img):   
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        # 区间1
        lower_red = np.array([0, 43, 46])
        upper_red = np.array([10, 255, 255])
        mask0 = cv2.inRange(img_hsv,lower_red,upper_red)
        # 区间2
        lower_red = np.array([170, 43, 46])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(img_hsv,lower_red,upper_red)
        # 拼接两个区间
        mask = mask0 + mask1
        return mask# cv2.bitwise_and(img,img,mask=mask)
    mask = np.zeros_like(img[:,:,0])
    cv2.ellipse(mask, (960, 540-17), (510+20+10, 430+20), 0, 0, 360, 255, -1)
    cv2.ellipse(mask, (960, 540-17), (510-40+10, 430-40), 0, 0, 360, 0, -1)

    
    # cv2.ellipse(mask, (960, 540), (510+30-1, 430+30-1), 0, 0, 360, 0, -1)
    
    # cv2.ellipse(mask, (960, 540), (510-50+1, 430-50+1), 0, 0, 360, 255, -1)
    
    
    # Apply mask to image
    im_src = cv2.bitwise_and(img, img, mask=mask)
    arrow_img = extract_red(im_src)

    # cv2.ellipse(arrow_img, (960, 540-17), (510+21+10, 430+21), 0, 0, 360, [255,255,255], 1)
    # cv2.ellipse(arrow_img, (960, 540-17), (510-40+10-1, 430-40-1), 0, 0, 360, [255,255,255], 1)
    
    # arrow_img = np.zeros_like(im_src[:,:,0])
    # arrow_img[:,:]=255
    # arrow_img[im_src[:, :, 2] < red_num] = 0
    # arrow_img[im_src[:, :, 0] > blue_num + float_num] = 0
    # arrow_img[im_src[:, :, 0] < blue_num - float_num] = 0
    # arrow_img[im_src[:, :, 1] > green_num + float_num] = 0
    # arrow_img[im_src[:, :, 1] < green_num - float_num] = 0

    if False:
        # cv2.imshow("mask",mask)
        cv2.imshow("2131231", arrow_img)
        cv2.waitKey(10)
    
    return arrow_img

def get_enemy_arrow_direction():
    orsrc = itt.capture()
    arrow_img = get_arrow_img(orsrc.copy())
    ret_contours = img_manager.get_rect(arrow_img, orsrc, ret_mode=3)
    # ret_range = img_manager.get_rect(imsrc2, orsrc, ret_mode=0)
    if len(ret_contours)!=0:
        angle = points_angle([SCREEN_CENTER_X,SCREEN_CENTER_Y],ret_contours[0][0],coordinate=ANGLE_NEGATIVE_Y)
    return int(angle)

def get_enemy_blood_bar_img(img):
    red_num = 255
    bg_num = 90
    im_src = img
    im_src = itt.png2jpg(im_src, channel='ui', alpha_num=254)
    im_src[990:1080, :, :] = 0
    im_src[:, :, 2][im_src[:, :, 2] != red_num] = 0
    im_src[:, :, 2][im_src[:, :, 0] != bg_num] = 0
    im_src[:, :, 2][im_src[:, :, 1] != bg_num] = 0
    # _, imsrc2 = cv2.threshold(imsrc[:, :, 2], 1, 255, cv2.THRESH_BINARY)
    blood_bar_img = im_src[:, :, 2]
    if False:
        # cv2.imshow("mask",mask)
        cv2.imshow("21312231", im_src)
        cv2.imshow("2131231", blood_bar_img)
        cv2.waitKey(10)
    return blood_bar_img
    
def combat_statement_detection():
    # return: ret[0]: blood bar; ret[1]: enemy arrow
    ret = [False,False]
    
    im_src = itt.capture()
    orsrc = im_src.copy()
    blood_bar_img = get_enemy_blood_bar_img(orsrc)
    
    flag_is_blood_bar_exist = blood_bar_img.max() > 0
    
    # print('flag_is_blood_bar_exist ',flag_is_blood_bar_exist)
    if flag_is_blood_bar_exist:
        only_arrow_timer.reset()
        ret[0]=True
    
    '''-----------------------------'''
    
    
    # im_src3 = orsrc.copy()
    # img_manager.qshow(imsrc)

    '''可以用圆形遮挡优化'''

    arrow_img = get_arrow_img(orsrc.copy())
    # _, imsrc2 = cv2.threshold(imsrc2[:, :, 2], 1, 255, cv2.THRESH_BINARY)
    # img_manager.qshow(imsrc2)
    
    # if True:
    #     if len(ret_contours) != 0:
    #         angle = cv2.minAreaRect(ret_contours)[2]
    #         print(angle)
    #         img = im_src.copy()[:, :, 2]
    #         img = img[ret_range[0]:ret_range[2],ret_range[1]:ret_range[3]]
    #         h, w = img.shape
    #         center = (w//2, h//2)
    #         M = cv2.getRotationMatrix2D(center, angle, 1.0)
    #         rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)    
    #         cv2.imshow('123', rotated)
    #         cv2.waitKey(50)
        
    red_arrow_num = len(np.where(arrow_img>=254)[-1])
    # print(red_arrow_num)
    if red_arrow_num > 180:
        ret[1]=True

    

    return ret

def get_chara_blood():
    img = itt.capture(jpgmode=0,posi=asset.BloodBar.position)
    img = extract_white_letters(img, threshold=251)
    t = ocr_light.get_all_texts(img)
    t2 = ','.join(str(i) for i in t).replace(',','')
    cb=""
    tb=""
    for i in t2:
        if is_number(i):
            cb+=i
        else:
            break
    for i in range(len(t2)):
        if is_number(t2[-(i+1)]):
            tb += t2[-(i+1)]
        else:
            break
    tb=tb[::-1]
    if cb=="" or tb=="":
        return None
    if int(tb) <= 100:
        return None
    return int(cb),int(tb)

def get_chara_blood_percentage():
    r = get_chara_blood()
    if r != None:
        return r[0]/r[1]
    else:
        return None

def is_character_healthy():
    if ui_control.verify_page(UIPage.page_main):
        img = itt.capture(jpgmode=0)
        if IS_DEVICE_PC:
            col = img[1011,847]
        target_col = [35,215,150]
        return color_similar(col,target_col,threshold=20)

def get_characters_name():
    img = itt.capture(jpgmode=0)
    ret_list = []
    for i in [asset.CharacterName1,asset.CharacterName2,asset.CharacterName3,asset.CharacterName4]:
        img2=img.copy()
        t = ocr.get_all_texts(crop(img2,i.position), mode=1)
        ret_list.append(translate_character(t, language=GLOBAL_LANG))
    return ret_list

def get_team_chara_names_in_party_setup():
    ui_control.ensure_page(UIPage.page_configure_team)
    text_list = []
    for i in [asset.PartySetupCharaName1,asset.PartySetupCharaName2,asset.PartySetupCharaName3,asset.PartySetupCharaName4]:
        img = itt.capture(jpgmode=0, posi=i.position)
        img2 = extract_white_letters(img)
        text = ocr.get_all_texts(img2)
        text_list.append(text[0])
    return text_list

def set_party_setup(names):
    ui_control.ensure_page(UIPage.page_configure_team)
    itt.delay("animation")
    def is_accord():
        curr_chara_list =  get_team_chara_names_in_party_setup()
        for i in range(4):
            if isinstance(names, list):
                if names[i] is None:
                    continue
                if translate_character(curr_chara_list[i]) != translate_character(names[i]):
                    return False
            elif isinstance(names, str):
                if translate_character(curr_chara_list[i]) in translate_character(names):
                    return True
        if isinstance(names, list):
            return True
        else:
            return False
    def switch_select():
        for i in range(5):
            if is_accord(): return True
            itt.appear_then_click(asset.SwitchTeamLeft)
            itt.delay("animation")
        return False
    if switch_select():
        itt.appear_then_click(asset.GoToFight)
        itt.delay("animation")
        ui_control.ui_goto(UIPage.page_main)
        return True
    else:
        logger.error(f"CANNOT Set Party To: {names}")
        return False
    
    
    
class CombatStatementDetectionLoop(BaseThreading):
    def __init__(self):
        super().__init__()
        self.setName("CombatStatementDetectionLoop")
        self.itt = itt
        self.current_state = False
        self.state_counter = 0
        self.while_sleep = 0.4
        self.is_low_health = False
    
    def get_combat_state(self):
        return self.current_state
    
    def loop(self):
        r = is_character_healthy()
        if r != None:
            self.is_low_health = not r
 
        if only_arrow_timer.get_diff_time()>=30:
            if self.current_state == True:
                logger.debug("only arrow but blood bar is not exist over 30s, ready to exit combat mode.")
            r = combat_statement_detection()
            state = r[0] or r[1]
            state = False
        else:
            r = combat_statement_detection()
            state = r[0] or r[1]
        if state != self.current_state:
            
            if self.current_state == True: # 切换到无敌人慢一点, 4s
                self.state_counter += 1
                self.while_sleep = 0.4
            elif self.current_state == False: # 快速切换到遇敌
                self.while_sleep = 0.02
                self.state_counter += 1
        else:
            self.state_counter = 0
            self.while_sleep = 0.4
        if self.state_counter >= 10:
            logger.debug('combat_statement_detection change state')
            # if self.current_state == False:
            #     only_arrow_timer.reset()
            self.state_counter = 0
            self.current_state = state
    
            
                

CSDL = CombatStatementDetectionLoop()
CSDL.start()

if __name__ == '__main__':
    # get_chara_list()
    # print()
    # set_party_setup("Lisa")
    while 1:
        time.sleep(0.1)
        combat_statement_detection()
        # print(get_character_busy(itt, default_stop_func))
        # time.sleep(0.2)
