from source.mission.mission_template import MissionExecutor, ERR_PASS, ERR_FAIL
from source.interaction.interaction_core import itt
from source.util import *
META={
    'name':{
        'zh_CN':'采集绯樱绣球1',
        'en_US':'Collect Sakura Bloom 1'
    },
    'author':"GIA",
    'note':t2t("Need Lisa")
}


class MissionMain(MissionExecutor):
    """13 SakuraBloom

    Args:
        MissionExecutor (_type_): _description_
    """
    def __init__(self):
        super().__init__(is_CFCF=True,is_PUO=True,is_TMCF=True)
        self.setName("MissionSakuraBloom1")
        self.sakura1 = [
            "SakuraBloom167910986687",
            "SakuraBloom16791098987",
            "SakuraBloom167911020876",
            "SakuraBloom167911023658",
            "SakuraBloom167911025376",
            "SakuraBloom167911029108",
            "SakuraBloom167911031376",
            
            # "SakuraBloom16791103543", # will die
            
            # "SakuraBloom167911071712", # will fall
            # "SakuraBloom167911074985", # fall
            # "SakuraBloom16791107662", # fall
            # "SakuraBloom167911081932", # fall
            # "SakuraBloom167911086202", # fall
                            ]
        
        self.sakura2=[
            "SakuraBloom167911045521",
            "SakuraBloom167911054242",
            "SakuraBloom167911055897",]
        
        self.sakura3=[
            "SakuraBloom167911062777",
            "SakuraBloom167911064519",
            "SakuraBloom167911068928",]
        
    def exec_mission(self):
        self.switch_character_to("Lisa")
        # 每一个list是连续的。如果其中有一次执行寄了，就必须退出所有list。
        self.reg_exception_chara_died()
        self.reg_exception_low_hp()
        for i in self.sakura1:
            r = self.move_along(i, is_precise_arrival=True)
            if r == ERR_FAIL:
                break
            itt.key_press('e')
            itt.delay(2)
            self.pickup_once()     
            itt.delay(0.5)
        self.switch_character_to("Lisa")    
        for i in self.sakura2:
            r = self.move_along(i, is_precise_arrival=True)
            if r == ERR_FAIL:
                break
            itt.key_press('e')
            itt.delay(2)
            self.pickup_once()     
            itt.delay(0.5)
        self.switch_character_to("Lisa")    
        for i in self.sakura3:
            r = self.move_along(i, is_precise_arrival=True)
            if r == ERR_FAIL:
                break
            itt.key_press('e')
            itt.delay(2)
            self.pickup_once()     
            itt.delay(0.5)
        self.reg_exception_chara_died(False)
        self._reg_exception_found_enemy(False)

        # self.stop_pickup()
        # self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
        
if __name__ == '__main__':
    mission = MissionMain()
    mission.start()
    mission.continue_threading()