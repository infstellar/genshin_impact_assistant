from source.mission.mission_template import MissionExecutor
from source.interaction.interaction_core import itt

class MissionSakuraBloom1(MissionExecutor):
    def __init__(self):
        super().__init__()
        self.setName("MissionSakuraBloom1")
        self.sakura_list = [
            "SakuraBloom167910986687",
            "SakuraBloom16791098987",
            "SakuraBloom167911020876",
            "SakuraBloom167911023658",
            "SakuraBloom167911025376",
            "SakuraBloom167911029108",
            "SakuraBloom167911031376",
            
            # "SakuraBloom16791103543", # will die
            
            "SakuraBloom167911045521",
            "SakuraBloom167911054242",
            "SakuraBloom167911055897",
            "SakuraBloom167911062777",
            "SakuraBloom167911064519",
            "SakuraBloom167911068928",
            
            # "SakuraBloom167911071712", # will fall
            
            # "SakuraBloom167911074985",
            # "SakuraBloom16791107662",
            # "SakuraBloom167911081932",
            # "SakuraBloom167911086202",
                            ]
        
    def exec_mission(self):
        for i in self.sakura_list:
            self.move_along(i)
            itt.key_press('e')
            itt.delay(2)
            self.pickup_once()     
            itt.delay(0.5)


        # self.stop_pickup()
        # self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
        
if __name__ == '__main__':
    mission = MissionSakuraBloom1()
    mission.start()
    mission.continue_threading()