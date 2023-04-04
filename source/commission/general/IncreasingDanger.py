from source.commission.commission_template import CommissionTemplate
from source.mission.mission_template import ERR_FAIL
from source.funclib import movement
from source.util import *
from source.interaction.interaction_core import itt
from source.manager import asset
from source.common.timer_module import AdvanceTimer


class IncreasingDangerGeneral(CommissionTemplate):
    def __init__(self, commission_position):
        super().__init__("IncreasingDanger", commission_position, is_CCT=True, is_CFCF=False)
    
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
            return r
    
    def exec_mission(self):
        attack_timer = AdvanceTimer(0.6)
        r = self.move_straight(self.commission_position, is_tp=True)
        if r == ERR_FAIL:return
        self.start_combat(mode="Shield")
        while 1:
            if self.checkup_stop_func():
                self.stop_combat()
                return
            if self._aim_to_commission_icon()<=20:
                if attack_timer.reached_and_reset():itt.left_click()
            if self.is_commission_complete():
                self.stop_combat()
                break
        self.is_commission_succ=True
        # self.pause_threading()
        
if __name__ == '__main__':
    idg = IncreasingDangerGeneral([3447.9764219999997,
      -4490.925582000001])
    idg.start()
    idg.continue_threading()
    while 1:
        time.sleep(1)