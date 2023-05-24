from source.mission.template.mission_just_collect import MissionJustCollect

META={
    'name':{
        'zh_CN':'采集塞西莉亚花',
        'en_US':'Collect Cecilia'
    },
    'author':"GIA",
}

class MissionMain(MissionJustCollect):
    def __init__(self):
        super().__init__("Cecilia20230513195754i0", "MissionCecilia")

if __name__ == '__main__':
    mission = MissionMain()
    mission.start()