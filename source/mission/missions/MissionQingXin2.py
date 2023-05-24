from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集清心2',
        'en_US':'Collect Qing xin 2'
    },
    'author':"GIA",
}
class MissionMain(MissionJustCollect):
    def __init__(self):
        super().__init__("QXV220230513090727i0", "MissionQingXin2")