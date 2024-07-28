from source.mission.mission_template import MissionExecutor, time
from source.cvars import STOP_RULE_F

class MissionJustCollect(MissionExecutor):
    def __init__(self, dictname, name:str):
        """

        Args:
            dictname: dict(support) or str(not recommend)
            name:
        """
        super().__init__(is_CFCF=True,is_PUO=True,is_TMCF=True)
        self.dictname = dictname
        self.setName(name)
    
    def exec_mission(self):
        self.start_pickup()# SweatFlower167910289922 SweatFlowerV2P120230507180640i0 
        self.move_along(self.dictname, is_tp=True, is_precise_arrival=False)
        time.sleep(2) # 如果路径结束时可能仍有剩余采集物，等待。
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
        time.sleep(2)
        self.stop_pickup()
    
    def exec_mission(self):
        for fn in self.filenames:
            self._exec_group(fn)

class MissionJustCollectMoveStraight(MissionExecutor):
    def __init__(self, pos:list, name):
        super().__init__(is_CFCF=True,is_PUO=True,is_TMCF=True)
        self.pos=pos
        self.setName(name)

    def exec_mission(self):
        self.start_pickup()  # SweatFlower167910289922 SweatFlowerV2P120230507180640i0
        self.move_straight(self.pos, is_tp=True, is_precise_arrival=False,stop_rule=STOP_RULE_F)
        time.sleep(2)  # 如果路径结束时可能仍有剩余采集物，等待。
        self.stop_pickup()


class MissionCollectArtifact(MissionExecutor):
    def __init__(self, dictname, name: str):
        """

        Args:
            dictname: dict(support) or str(not recommend)
            name:
        """
        super().__init__(is_CFCF=True, is_PUO=True, is_TMCF=True)
        self.dictname = dictname
        self.setName(name)

    def exec_mission(self):
        self.set_puo_crazy_f(True)
        self.start_pickup()  # SweatFlower167910289922 SweatFlowerV2P120230507180640i0
        self.TMCF.flow_connector.is_nahida = False
        self.move_along(self.dictname, is_tp=True, is_precise_arrival=False)
        time.sleep(2)  # 如果路径结束时可能仍有剩余采集物，等待。
        self.stop_pickup()
        # self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])