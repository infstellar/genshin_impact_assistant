import threading
from unit import *
import combat_loop,character

class Alpha_Loop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        
        self.stop_flag=False
        
        self.team=loadjson('team.json')
        self.chara_list=[]
        for team_name in self.team:
            team_item=self.team[team_name]
            self.chara_list.append(
                character.Character(team_item['name'],team_item["position"],team_item["n"],team_item["priority"],
                                    team_item["E_short_cd_time"],team_item["E_long_cd_time"],team_item["Elast_time"],
                                    team_item["Ecd_float_time"],team_item["tastic_group"],team_item["trigger"]
                                    )
                )
        self.combat=combat_loop.Combat_Loop(self.chara_list,stop_func=self.stop_func)
    
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 

        while(True):
            self._do_loop()
            if self.stop_flag:
                break
                

    
    def stop_func(self):
        if self.stop_flag==True:
            return True
        else:
            return False
    
    def _do_loop(self):
        ret=self.combat.loop()
        print('\n','idle: ',ret,'\n')
        if ret:
            time.sleep(0.2)
        else:
            time.sleep(0.1)
                
    def stop_thread(self,mode:int=0):
        if mode==0:
            self.stop_flag=True
            self.combat.stop()
        elif mode==1: #emergency stop
            thread_id = self.get_id() 
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
                ctypes.py_object(SystemExit)) 
            if res > 1: 
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
                print('Exception raise failure') 


if __name__=='__main__':
    #character_json=loadjson('character.json')
    team=loadjson('team.json')
    chara_list=[]
    for team_name in team:
        team_item=team[team_name]
        chara_list.append(
            character.Character(team_item['name'],team_item["position"],team_item["n"],team_item["priority"],
                                team_item["E_short_cd_time"],team_item["E_long_cd_time"],team_item["Elast_time"],
                                team_item["Ecd_float_time"],team_item["tastic_group"],team_item["trigger"]
                                )
            )
    combat=combat_loop.Combat_Loop(chara_list)
    #while(True):
    for i in range(10):
        ret=combat.loop()
        print('\n','idle: ',ret,'\n')
        if ret:
            time.sleep(0.2)
        else:
            time.sleep(0.1)