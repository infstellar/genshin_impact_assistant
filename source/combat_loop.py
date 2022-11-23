# from interaction import *

import time

import character
from aim_operator import AimOperator
from base_threading import BaseThreading
from interaction_background import InteractionBGD
from switch_character_operator import SwitchCharacterOperator
import combat_lib
from util import *


def sort_flag_1(x: character.Character):
    return x.priority


def stop_func_example():  # True:stop;False:continue
    return False


def get_chara_list(team_name='team.json'):
    team_name = config_json["teamfile"]
    team = load_json(team_name)
    characters = load_json("character.json")
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
            ctastic_group = ccharacter["tastic_group"]
            cEpress_time = ccharacter["Epress_time"]
            cQlast_time = ccharacter["Qlast_time"]
        else:
            cposition = team_item["position"]
            cpriority = team_item["priority"]
            cE_short_cd_time = team_item["E_short_cd_time"]
            cE_long_cd_time = team_item["E_long_cd_time"]
            cElast_time = team_item["Elast_time"]
            cEcd_float_time = team_item["Ecd_float_time"]
            ctastic_group = team_item["tastic_group"]
            ctrigger = team_item["trigger"]
            cEpress_time = team_item["Epress_time"]
            cQlast_time = team_item["Qlast_time"]

        cn = team_item["n"]
        cname = team_item['name']
        cpriority = team_item["priority"]
        ctrigger = team_item["trigger"]

        if cEcd_float_time > 0:
            logger.info("角色 " + cname + " 的Ecd_float_time大于0，请确定该角色不是多段e技能角色。")

        chara_list.append(
            character.Character(
                name=cname, position=cposition, n=cn, priority=cpriority,
                E_short_cd_time=cE_short_cd_time, E_long_cd_time=cE_long_cd_time, Elast_time=cElast_time,
                Ecd_float_time=cEcd_float_time, tastic_group=ctastic_group, trigger=ctrigger,
                Epress_time=cEpress_time, Qlast_time=cQlast_time
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
        self.sco.setDaemon(True)
        self.sco.start()

        self.ao = AimOperator()
        self.ao.pause_threading()
        self.ao.setDaemon(True)
        self.ao.start()

        # self.super_stop_func=super_stop_func

    def run(self):
        while 1:
            time.sleep(0.2)
            if self.checkup_stop_threading():
                self.ao.stop_threading()
                self.sco.stop_threading()
                return 0

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
                else:
                    pass

            # print('6')
            # time.sleep(1)

    def checkup_stop_func(self):
        if self.pause_threading_flag or self.stop_threading_flag:
            logger.info('停止自动战斗')
            return True

    def checkup_stop_threading(self):
        if self.stop_threading_flag:
            logger.info('停止自动战斗')
            return True

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.current_num = combat_lib.get_current_chara_num(self.itt)
            self.current_num = 1
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
