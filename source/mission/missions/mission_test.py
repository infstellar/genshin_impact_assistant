from source.mission.mission_template import MissionExecutor

class MissionTest(MissionExecutor):
    def loop(self):
        self.move(MODE="AUTO",target_posi=[0,0])
        
if __name__ == '__main__':
    mission = MissionTest()
    mission.start()
    mission.continue_threading()