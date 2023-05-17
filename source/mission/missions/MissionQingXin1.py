from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集塞西莉亚花',
        'en_US':'Collect Cecilia'
    }
}
class MissionQingXin1(MissionJustCollect):
    def __init__(self):
        super().__init__("QXV220230513083258i0", "MissionQingXin1")