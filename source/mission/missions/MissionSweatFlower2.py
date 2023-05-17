from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集塞西莉亚花',
        'en_US':'Collect Cecilia'
    }
}
class MissionSweatFlower2(MissionJustCollect):
    def __init__(self):
        super().__init__("SweatFlowerV2P120230507180640i0", "MissionSweatFlower2")