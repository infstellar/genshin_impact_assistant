from source.mission.mission_template import MissionExecutor
META={
    'name':{
        'zh_CN':'采集甜甜花1',
        'en_US':'Collect Sweat Flower 1'
    },
    'author':"GIA"
}
class MissionMain(MissionExecutor):
    def __init__(self):
        super().__init__(is_CFCF=True,is_PUO=True,is_TMCF=True)
        self.setName("MissionSweatFlower1")
    
    def exec_mission(self):
        self.start_pickup()
        self.move_along("SweatFlower167910289922", is_tp=True, is_precise_arrival=False)
        self.stop_pickup()
        # self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
        
if __name__ == '__main__':
    mission = MissionMain()
    mission.start()
    mission.continue_threading()