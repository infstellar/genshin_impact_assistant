from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集琉璃袋3',
        'en_US':'Collect Violetgrass 3'
    },
    'author':"GIA"
}
class MissionMain(MissionJustCollect):
    def __init__(self):
        super().__init__("VioletgrassV220230513100802i0", "MissionVioletgrass3")