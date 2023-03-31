from source.util import *
from source.mission.mission_template import MissionExecutor
from source.map.position.position import *
from source.interaction.interaction_core import itt



class CommissionTemplate(MissionExecutor):
    def __init__(self, commission_type, commission_position):
        super().__init__()

        self.commission_name = commission_type
        self.commission_position = commission_position

        self.is_pickup_spoils = False 

    def is_mission_succ(self):
        pass
        # itt.capture()


