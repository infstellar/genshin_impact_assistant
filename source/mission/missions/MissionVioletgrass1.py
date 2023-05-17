from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集塞西莉亚花',
        'en_US':'Collect Cecilia'
    }
}
class MissionVioletgrass1(MissionJustCollect):
    def __init__(self):
        super().__init__("LLDV2P120230507182352i0", "MissionVioletgrass1")