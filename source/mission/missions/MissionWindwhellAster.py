from source.mission.template.mission_just_collect import MissionJustCollectGroup
META={
    'name':{
        'zh_CN':'采集风车菊',
        'en_US':'Collect Windwhell Aster'
    },
    'author':"GIA",
    'time':'UTC+08 2023-05-15'
}
class MissionMain(MissionJustCollectGroup):
    def __init__(self):
        super().__init__(['WindwheelAster20230513192646i0',
                          'WindwheelAster20230513192116i0',
                          'WindwheelAster20230513191805i0', 
                          'WindwheelAster20230513192722i0', 
                          'WindwheelAster20230513192455i0', 
                          'WindwheelAster20230513192553i0', 
                          'WindwheelAster20230513192411i0'
                          ],
                           name='MissionWindwhellAster')

if __name__ == '__main__':
    import time
    MissionMain().start()
    while 1:time.sleep(1)