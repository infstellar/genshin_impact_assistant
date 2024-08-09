from source.mission.mission_template import MissionExecutor, time, ENEMY_REACTION_FIGHT
from source.cvars import STOP_RULE_COMBAT


class MissionCombat(MissionExecutor):
    def __init__(self, dictname, name: str):
        """

        Args:
            dictname: dict(support) or str(not recommend)
            name:
        """
        super().__init__(is_CFCF=True, is_PUO=True, is_TMCF=True, is_CCT=True)
        self.dictname = dictname
        self.setName(name)

    def exec_mission(self):
        self.start_pickup()  # SweatFlower167910289922 SweatFlowerV2P120230507180640i0
        self.move_along(self.dictname, is_tp=True, is_precise_arrival=False, adsorb=True, absorption_reaction_to_enemy=ENEMY_REACTION_FIGHT)
        time.sleep(2)  # 如果路径结束时可能仍有剩余采集物，等待。
        self.stop_pickup()
        # self.collect(MODE="AUTO",pickup_points=[[71, -2205],[65,-2230]])
