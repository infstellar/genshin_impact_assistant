from source.mission.mission_template import MissionExecutor

class MissionTest(MissionExecutor):
    def __init__(self):
        super().__init__()
        self.setName("MissionTest")
    
    def exec_mission(self):
        # self.move_straight([-200,200])
        self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
        
if __name__ == '__main__':
    mission = MissionTest()
    mission.start()
    mission.continue_threading()