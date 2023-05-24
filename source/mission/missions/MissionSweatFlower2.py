from source.mission.template.mission_just_collect import MissionJustCollect
META={
    'name':{
        'zh_CN':'采集甜甜花2',
        'en_US':'Collect Sweat Flower 2'
    },
    'author':"GIA"
}
class MissionMain(MissionJustCollect):
    def __init__(self):
        super().__init__("SweatFlowerV2P120230507180640i0", "MissionSweatFlower2")