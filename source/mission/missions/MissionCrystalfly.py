from source.mission.mission_template import MissionExecutor

class MissionCrystalfly(MissionExecutor):
    def __init__(self):
        super().__init__()
        self.setName("MissionCrystalfly")
    
    def exec_mission(self):
        self.start_pickup()
        # self.move_along("Crystalfly16786174406", is_tp=True)
        self.move_along("Crystalfly167861751483", is_tp=True)
        self.move_along("Crystalfly167861762261", is_tp=True)
        self.stop_pickup()
        # self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
        
if __name__ == '__main__':
    mission = MissionCrystalfly()
    mission.start()
    mission.continue_threading()