from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集琉璃袋1',
        'en_US':'Collect Violetgrass 1'
    }
}
class MissionMain(MissionJustCollect):
    def __init__(self):
        super().__init__("LLDV2P120230507182352i0", "MissionVioletgrass1")