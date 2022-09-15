import unit,character,tastic,time


def sort_flag_1(x:character.Character):
    return x.priority

class Combat_Loop():
    def __init__(self,chara_list:list[character.Character]):
        self.chara_list=chara_list
        self.chara_list.sort(key=sort_flag_1,reverse=False)
        self.tastic_exc=tastic.Tastic()
        self.stop_flag=False
        ...
    
    def stop(self):
        self.stop_flag=True
    
    def loop(self):
        idle=True
        for chara in self.chara_list:
            print(chara.name)
            if self.stop_flag:
                return 0
            if chara.trigger():
                self.tastic_exc.run(chara.tastic_group,chara)
                idle=False
                continue
                ...
            time.sleep(0.5)
        return idle
        ...