#from interaction import *
from re import T
import pyautogui
import character,tastic,time,threading
from unit import *
from timer_module import Timer
from interaction_background import Interaction_BGD

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
        
        chara_list.append(
            character.Character(
                 name=cname,position=cposition,n=cn,priority=cpriority,
        E_short_cd_time=cE_short_cd_time,E_long_cd_time=cE_long_cd_time,Elast_time=cElast_time,
        Ecd_float_time=cEcd_float_time,tastic_group=ctastic_group,trigger=ctrigger,
        Epress_time=cEpress_time,Qlast_time=cQlast_time
                                )
            )
    return chara_list

class Combat_Loop(threading.Thread):
    def __init__(self,chara_list:list[character.Character],super_stop_func=stop_func_example):
        threading.Thread.__init__(self)
        
        self.start_loop_flag=False
        self.chara_list=chara_list
        self.chara_list.sort(key=sort_flag_1,reverse=False)
        self.tastic_exc=tastic.Tastic()
        self.stop_flag=False
        self.current_num=1
        self.switch_timer=Timer(diff_start_time=2)
        self.itt=Interaction_BGD()
        self.super_stop_func=super_stop_func
        
        
        #self.itt.delay(1)
        ...
    
    def checkupstop(self):
        if self.stop_func():
            print('ConsoleMessage: 停止自动战斗')
            return True
            
    def _switch_character(self,x:int):
        pyautogui.click(button='middle')
        t = self.switch_timer.getDiffTime()
        # if t>=1.1:
        #     pass
        # else:
        #     self.itt.delay(1.1-t)
        self.tastic_exc.chara_waiting()
        for i in range(30):
            self.itt.keyPress(str(x))
            print('try switching to '+str(x))
            time.sleep(0.1)
            if self.tastic_exc.get_current_chara_num()==x:
                break
        # self.itt.delay(0.1)
        self.current_num=x
        self.switch_timer.reset()
        self.itt.delay(0.1)
            
    def stop_func(self):
        if self.super_stop_func() or self.stop_flag:
            return True
    
    def stop(self):
        self.stop_flag=True
    
    def loop(self):
        idle=True
        for chara in self.chara_list:
            print(chara.name)
            if self.stop_flag:
                return 0
            if chara.trigger():
                if chara.n != self.current_num:
                    self._switch_character(chara.n)
                self.tastic_exc.run(chara.tastic_group,chara,stop_func=self.stop_func)
                idle=False
                return idle
            #time.sleep()
        return idle
    
    def start_loop(self):
        self.current_num=self.tastic_exc.get_current_chara_num()
        self.current_num=1
        self.stop_flag=False
        self.start_loop_flag=True
        
        
    def stop_loop(self):
        
        self.start_loop_flag=False
        self.stop_flag=True
    
    def run(self):
        while(1):
            if self.start_loop_flag:
                if self.checkupstop():
                    break
                ret=self.loop()
                print('\n','idle: ',ret,'\n')
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