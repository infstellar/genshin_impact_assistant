# from interaction import *

from util import *
import character
from aim_operator import AimOperator
from base_threading import BaseThreading
from interaction_background import InteractionBGD
from switch_character_operator import SwitchCharacterOperator
import combat_lib
import img_manager
import button_manager
import asset
from path_lib import CONFIG_SETTING_PATH

CHARACTER_DIED = 1

def sort_flag_1(x: character.Character):
    return x.priority


def stop_func_example():  # True:stop;False:continue
    return False


def get_chara_list(team_name='team.json'):
    team_name = load_json("auto_combat.json",CONFIG_SETTING_PATH)["teamfile"]
    dpath = "config\\tactic"
    
    team = load_json(team_name, default_path=dpath)
    characters = load_json("character.json", default_path=dpath)
    chara_list = []
    for team_name in team:
        team_item = team[team_name]
        if team_item["autofill"]:
            ccharacter = characters[team_item["name"]]
            cposition = ccharacter["position"]
            cE_short_cd_time = ccharacter["E_short_cd_time"]
            cE_long_cd_time = ccharacter["E_long_cd_time"]
            cElast_time = ccharacter["Elast_time"]
            cEcd_float_time = ccharacter["Ecd_float_time"]
            try:
                ctactic_group = ccharacter["tactic_group"]
            except:
                ctactic_group = ccharacter["tastic_group"]
                logger.warning(_("请将配对文件中的tastic_group更名为tactic_group. 已自动识别。"))
            cEpress_time = ccharacter["Epress_time"]
            cQlast_time = ccharacter["Qlast_time"]
            cQcd_time = ccharacter["Qcd_time"]
        else:
            cposition = team_item["position"]
            cpriority = team_item["priority"]
            cE_short_cd_time = team_item["E_short_cd_time"]
            cE_long_cd_time = team_item["E_long_cd_time"]
            cElast_time = team_item["Elast_time"]
            cEcd_float_time = team_item["Ecd_float_time"]
            try:
                ctactic_group = team_item["tactic_group"]
            except:
                ctactic_group = team_item["tastic_group"]
                logger.warning(_("请将配对文件中的tastic_group更名为tactic_group. 已自动识别。"))
            ctrigger = team_item["trigger"]
            cEpress_time = team_item["Epress_time"]
            cQlast_time = team_item["Qlast_time"]
            cQcd_time = team_item["Qcd_time"]

        cn = team_item["n"]
        cname = team_item['name']
        cpriority = team_item["priority"]
        ctrigger = team_item["trigger"]

        if cEcd_float_time > 0:
            logger.info(_("角色 ") + cname + _(" 的Ecd_float_time大于0，请确定该角色不是多段e技能角色。"))

        chara_list.append(
            character.Character(
                name=cname, position=cposition, n=cn, priority=cpriority,
                E_short_cd_time=cE_short_cd_time, E_long_cd_time=cE_long_cd_time, Elast_time=cElast_time,
                Ecd_float_time=cEcd_float_time, tactic_group=ctactic_group, trigger=ctrigger,
                Epress_time=cEpress_time, Qlast_time=cQlast_time, Qcd_time=cQcd_time
            )
        )
    return chara_list


class Combat_Controller(BaseThreading):
    def __init__(self, chara_list=None):
        super().__init__()
        if chara_list is None:
            chara_list = get_chara_list()
        self.setName('Combat_Controller')

        self.chara_list = chara_list
        self.pause_threading_flag = False
        self.itt = InteractionBGD()

        self.sco = SwitchCharacterOperator(self.chara_list)
        self.sco.pause_threading()
        self.sco.add_stop_func(self.checkup_stop_func)
        self.sco.setDaemon(True)
        self.sco.start()

        self.ao = AimOperator()
        self.ao.pause_threading()
        self.ao.add_stop_func(self.checkup_stop_func)
        self.ao.setDaemon(True)
        self.ao.start()

        self.is_check_died = False
        
        # self.super_stop_func=super_stop_func

    def run(self):
        while 1:
            time.sleep(0.2)
            if self.checkup_stop_threading():
                self.ao.stop_threading()
                self.sco.stop_threading()
                return 0
            
            if self.is_check_died:
                if self.itt.get_img_existence(asset.character_died):
                    logger.info(_('有人嘎了，停止自动战斗'))
                    self.last_err_code = CHARACTER_DIED
                    while 1:
                        time.sleep(0.5)
                        r = self.itt.appear_then_click(button_manager.button_ui_cancel)
                        if r:
                            break
                    self.pause_threading()
            
            if not self.pause_threading_flag:
                if self.checkup_stop_func():
                    break

                if not self.sco.get_working_statement():
                    self.sco.continue_threading()
                    time.sleep(1)
                else:
                    time.sleep(0.2)

                if not self.ao.get_working_statement():
                    self.ao.continue_threading()
                else:
                    pass

            else:
                if self.sco.get_working_statement():
                    self.sco.pause_threading()
                    time.sleep(1)

                if self.ao.get_working_statement():
                    self.ao.pause_threading()
                    time.sleep(1)
                
                continue
                
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            # print('6')
            # time.sleep(1)

    def checkup_stop_func(self):
        if self.pause_threading_flag or self.stop_threading_flag:
            logger.info(_('停止自动战斗'))
            return True
        
        
    def checkup_stop_threading(self):
        if self.stop_threading_flag:
            logger.info(_('停止自动战斗'))
            return True

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.current_num = combat_lib.get_current_chara_num(self.itt, self.checkup_stop_func)
            # self.current_num = 1
            self.pause_threading_flag = False
            self.sco.continue_threading()
            self.ao.continue_threading()

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.sco.pause_threading()
            self.ao.pause_threading()

    def checkup_trapped(self):
        pass
        # if self.itt.capture(posi=posiM)

    def stop_threading(self):
        self.stop_threading_flag = True


if __name__ == '__main__':
    cl = Combat_Controller()
    cl.start()
    # a = get_chara_list()
    # print()
