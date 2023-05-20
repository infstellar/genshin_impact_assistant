from source.mission.mission_template import MissionExecutor
META={
    'name':{
        'zh_CN':'测试',
        'en_US':'TEST'
    }
}
class MissionTest(MissionExecutor):
    def __init__(self):
        super().__init__(is_CFCF=True,is_PUO=True,is_TMCF=True)
        self.setName("MissionTest")
    
    def exec_mission(self):
        self.move_along("167858534153", is_tp=True)
        self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
        
if __name__ == '__main__':
    mission = MissionTest()
    mission.start()
    mission.continue_threading()