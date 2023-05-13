from source.mission.template.mission_just_collect import MissionJustCollect

class MissionCecilia(MissionJustCollect):
    def __init__(self):
        super().__init__("Cecilia20230513195754i0", "MissionCecilia")

if __name__ == '__main__':
    mission = MissionCecilia()
    mission.start()