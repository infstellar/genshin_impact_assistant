#from interaction import *
from re import T
import pyautogui
import character,tastic,time,threading, img_manager as imgM, posi_manager as posiM
from unit import *
from timer_module import Timer
from interaction_background import Interaction_BGD
from base_threading import Base_Threading

def sort_flag_1(x:character.Character):
    return x.priority

def stop_func_example():#True:stop;False:continue
    return False

def get_chara_list(teamname='team.json'):
    teamname=configjson["teamfile"]
    team=loadjson(teamname)
    characters=loadjson("character.json")
    chara_list=[]
    for team_name in team:
        team_item=team[team_name]
        if team_item["autofill"]==True:
            ccharacter=characters[team_item["name"]]
            cposition=ccharacter["position"]
            cE_short_cd_time=ccharacter["E_short_cd_time"]
            cE_long_cd_time=ccharacter["E_long_cd_time"]
            cElast_time=ccharacter["Elast_time"]
            cEcd_float_time=ccharacter["Ecd_float_time"]
            ctastic_group=ccharacter["tastic_group"]
            cEpress_time=ccharacter["Epress_time"]
            cQlast_time=ccharacter["Qlast_time"]
        else:
            cposition=team_item["position"]
            cpriority=team_item["priority"]
            cE_short_cd_time=team_item["E_short_cd_time"]
            cE_long_cd_time=team_item["E_long_cd_time"]
            cElast_time=team_item["Elast_time"]
            cEcd_float_time=team_item["Ecd_float_time"]
            ctastic_group=team_item["tastic_group"]
            ctrigger=team_item["trigger"]
            cEpress_time=team_item["Epress_time"]
            cQlast_time=team_item["Qlast_time"]
        
        cn=team_item["n"]
        cname=team_item['name']
        cpriority=team_item["priority"]
        ctrigger=team_item["trigger"]
        
        if cEcd_float_time>0:
            logger.info("角色 "+cname+" 的Ecd_float_time大于0，请确定该角色不是多段e技能角色。")

        chara_list.append(
            character.Character(
                 name=cname,position=cposition,n=cn,priority=cpriority,
        E_short_cd_time=cE_short_cd_time,E_long_cd_time=cE_long_cd_time,Elast_time=cElast_time,
        Ecd_float_time=cEcd_float_time,tastic_group=ctastic_group,trigger=ctrigger,
        Epress_time=cEpress_time,Qlast_time=cQlast_time
                                )
            )
    return chara_list

class Combat_Loop(Base_Threading):
    def __init__(self,chara_list:list[character.Character],super_stop_func=stop_func_example):
        super().__init__()
        
        self.chara_list=chara_list
        self.chara_list.sort(key=sort_flag_1,reverse=False)
        self.tastic_exc=tastic.Tastic()
        self.pause_threading_flag=False
        self.current_num=1
        self.switch_timer=Timer(diff_start_time=2)
        self.itt=Interaction_BGD()
        self.super_stop_func=super_stop_func
    
    def checkup_stop_func(self):
        if self.super_stop_func() or self.pause_threading_flag or self.stop_threading_flag:
            logger.info('停止自动战斗')
            return True
        
    def checkup_stop_threading(self):
        if self.stop_threading_flag:
            logger.info('停止自动战斗')
            return True
    
    def continue_threading(self):
        self.current_num=self.tastic_exc.get_current_chara_num()
        self.current_num=1
        self.pause_threading_flag=False
        
        
    def pause_threading(self):
        self.pause_threading_flag=True
    
    def checkup_trapped(self):
        pass
        # if self.itt.capture(posi=posiM)
            
    def _switch_character(self,x:int):
        pyautogui.click(button='middle')
        t = self.switch_timer.getDiffTime()
        # if t>=1.1:
        #     pass
        # else:
        #     self.itt.delay(1.1-t)
        self.tastic_exc.chara_waiting()
        for i in range(30):
            self.tastic_exc.unconventionality_situlation_detection()
            self.itt.keyPress(str(x))
            logger.debug('try switching to '+str(x))
            time.sleep(0.1)
            if self.tastic_exc.get_current_chara_num()==x:
                break
        # self.itt.delay(0.1)
        self.current_num=x
        self.switch_timer.reset()
        self.itt.delay(0.1)
            
    def stop_threading(self):
        self.stop_threading_flag=True
    
    def loop(self):
        idle=True
        for chara in self.chara_list:
            logger.debug('check up in: '+chara.name)
            if self.checkup_stop_func():
                return 0
            if chara.trigger():
                if chara.n != self.current_num:
                    self._switch_character(chara.n)
                self.tastic_exc.run(chara.tastic_group,chara)
                idle=False
                return idle
            #time.sleep()
        return idle

    def run(self):
        while(1):
            if self.pause_threading_flag==False:
                if self.checkup_stop_func():
                    break
                ret=self.loop()
                logger.debug('idle: '+str(ret))
                if ret:
                    time.sleep(0.2)
                else:
                    pass
                    # time.sleep(0.1)
            else:
                time.sleep(1)
                
if __name__=='__main__':
    a = get_chara_list()
    print()