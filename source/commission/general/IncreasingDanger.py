from source.commission.commission_template import CommissionTemplate
from source.mission.mission_template import ERR_FAIL
from source.funclib import movement
from source.util import *
from source.interaction.interaction_core import itt
from source.manager import asset


class IncreasingDangerGeneral(CommissionTemplate):
    def __init__(self, commission_position):
        super().__init__("IncreasingDanger", commission_position, is_CCT=True)
    
    def _aim_to_commission_icon(self):
        cap = itt.capture(jpgmode=0)
        ban_posi=asset.CommissionIcon.cap_posi
        cap[ban_posi[1]:ban_posi[3],ban_posi[0]:ban_posi[2]]=0
        r = movement.view_to_imgicon(cap, asset.CommissionIconInCommission)
        if not r:
            return False
        else:
            if r<=50:
                itt.key_down('w')
            else:
                itt.key_up('w')
    
    def exec_mission(self):
        r = self.move_straight(self.commission_position, is_tp=True)
        if r == ERR_FAIL:return
        r = self.collect(is_combat=True, is_activate_pickup=self.is_pickup_spoils)
        if r == ERR_FAIL:return