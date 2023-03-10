from source.mission.mission_template import MissionExecutor

class MissionTest(MissionExecutor):
    def exec_mission(self):
        self.move(MODE="AUTO",target_posi=[-200,200])
        
if __name__ == '__main__':
    mission = MissionTest()
    mission.start()
    mission.continue_threading()