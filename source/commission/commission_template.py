from source.util import *
from source.mission.mission_template import MissionExecutor
from source.map.position.position import *
from source.interaction.interaction_core import itt
from source.manager import asset
from source.common.timer_module import AdvanceTimer


class CommissionTemplate(MissionExecutor):
    def __init__(self, commission_type, commission_position,is_CFCF=True,is_PUO=True,is_TMCF=True,is_CCT=False):
        super().__init__(is_CFCF=is_CFCF,is_PUO=is_PUO,is_TMCF=is_TMCF,is_CCT=is_CCT)

        self.commission_name = commission_type
        self.commission_position = commission_position

        self.is_pickup_spoils = False 
        self.is_commission_succ = False
        self.is_commission_start = False
        self._commission_end_timer = AdvanceTimer(4,2)
        self._commission_end_timer.reset()

    def is_mission_succ(self):
        pass
        # itt.capture()

    def is_commission_complete(self):
        if self.is_commission_start == False:
            if self._is_in_commission():
                self.is_commission_start = True
                return False
            else:
                return False
        else:
            if not self._is_in_commission():
                return self._commission_end_timer.reached_and_reset()
                # for debug
                if self._commission_end_timer.reached_and_reset():
                    print()
                    return True
                else:
                    return False
            else:
                self._commission_end_timer.reset()
                
    
    def _is_in_commission(self):
        return itt.get_img_existence(asset.CommissionIcon)

