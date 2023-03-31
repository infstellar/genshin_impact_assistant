from source.mission.mission_template import MissionExecutor
from source.map.position.position import *


class CommissionTemplate(MissionExecutor):
    def __init__(self, commission_name, commission_position):
        super().__init__()

        self.commission_name = commission_name
        self.commission_position = TianLiPosition(commission_position)


