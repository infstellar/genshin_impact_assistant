from source.mission.template.mission_just_collect import MissionJustCollectGroup

class MissionGlazeLily(MissionJustCollectGroup):
    def __init__(self):
        super().__init__(['GlazeLily20230513214207i0',
                          'GlazeLily20230513214422i0',
                          'GlazeLily20230513214617i0'
                          ],
                           name='MissionGlazeLily')

if __name__ == '__main__':
    import time
    MissionGlazeLily().start()
    while 1:time.sleep(1)