from source.mission.template.mission_just_collect import MissionJustCollect

class MissionV2PTest(MissionJustCollect):
    def __init__(self):
        super().__init__("V2Ptest1120230509225205i0", "MissionV2PTest")
        
MissionV2PTest().start()