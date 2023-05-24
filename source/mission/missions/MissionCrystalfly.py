from source.mission.mission_template import MissionExecutor
META={
    'name':{
        'zh_CN':'采集晶蝶',
        'en_US':'Collect Crystalfly'
    },
    'author':"GIA",
}
class MissionMain(MissionExecutor):
    def __init__(self):
        super().__init__(is_CFCF=True,is_PUO=True,is_TMCF=True)
        self.setName("MissionCrystalfly")
    
    def exec_mission(self):
        self.start_pickup()
        # self.move_along("Crystalfly16786174406", is_tp=True)
        self.move_along("Crystalfly167861751483", is_tp=True)
        self.move_along("Crystalfly167861762261", is_tp=True)
        self.stop_pickup()
        # self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
        
if __name__ == '__main__':
    mission = MissionMain()
    mission.start()
    mission.continue_threading()