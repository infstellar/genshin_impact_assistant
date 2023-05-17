from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集塞西莉亚花',
        'en_US':'Collect Cecilia'
    }
}
class MissionV2PTest(MissionJustCollect):
    def __init__(self):
        super().__init__("QXV20230513112241i0", "MissionV2PTest")
        
# MissionV2PTest().start()