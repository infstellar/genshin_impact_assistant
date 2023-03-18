from source.mission.mission_template import MissionExecutor

class MissionSweatFlower1(MissionExecutor):
    def __init__(self):
        super().__init__()
        self.setName("MissionSweatFlower1")
    
    def exec_mission(self):
        self.start_pickup()
        self.move_along("SweatFlower167910289922", is_tp=True)
        self.stop_pickup()
        # self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
        
if __name__ == '__main__':
    mission = MissionSweatFlower1()
    mission.start()
    mission.continue_threading()