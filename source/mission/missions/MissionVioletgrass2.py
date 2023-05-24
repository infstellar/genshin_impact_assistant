from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集琉璃袋2',
        'en_US':'Collect Violetgrass 2'
    },
    'author':"GIA"
}
class MissionMain(MissionJustCollect):
    def __init__(self):
        super().__init__("VioletgrassV220230513100544i0", "MissionVioletgrass2")