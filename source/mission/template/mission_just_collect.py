from source.mission.mission_template import MissionExecutor

class MissionJustCollect(MissionExecutor):
    def __init__(self, dictname, name):
        super().__init__(is_CFCF=True,is_PUO=True,is_TMCF=True)
        self.dictname = dictname
        self.setName(name)
    
    def exec_mission(self):
        self.start_pickup()# SweatFlower167910289922 SweatFlowerV2P120230507180640i0 
        self.move_along(self.dictname, is_tp=True, is_precise_arrival=False)
        self.stop_pickup()
        # self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])

class MissionJustCollectGroup(MissionExecutor):
    def __init__(self, filenames:list, name):
        super().__init__(is_CFCF=True,is_PUO=True,is_TMCF=True)
        self.filenames = filenames
        self.setName(name)
    
    def _exec_group(self, filename):
        self.start_pickup()# SweatFlower167910289922 SweatFlowerV2P120230507180640i0 
        self.move_along(filename, is_tp=True, is_precise_arrival=False)
        self.stop_pickup()
    
    def exec_mission(self):
        for fn in self.filenames:
            self._exec_group(fn)