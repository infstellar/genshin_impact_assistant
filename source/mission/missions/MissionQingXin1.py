from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集清心1',
        'en_US':'Collect Qing xin 1'
    }
}
class MissionQingXin1(MissionJustCollect):
    def __init__(self):
        super().__init__("QXV220230513083258i0", "MissionQingXin1")