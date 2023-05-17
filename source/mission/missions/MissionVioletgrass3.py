from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集塞西莉亚花',
        'en_US':'Collect Cecilia'
    }
}
class MissionVioletgrass3(MissionJustCollect):
    def __init__(self):
        super().__init__("VioletgrassV220230513100802i0", "MissionVioletgrass3")