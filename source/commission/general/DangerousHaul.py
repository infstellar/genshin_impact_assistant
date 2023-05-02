from source.commission.commission_template import CommissionTemplate
from source.mission.mission_template import ERR_FAIL
from source.funclib import movement, combat_lib
from source.util import *
from source.interaction.interaction_core import itt
from source.manager import asset
from source.common.timer_module import AdvanceTimer
from source.api.pdocr_light import ocr_light


class DangerousHaulGeneral(CommissionTemplate):
    def __init__(self, commission_position):
        super().__init__("DangerousHaul", commission_position, is_CCT=True, is_CFCF=False)
    
    def _aim_to_commission_icon(self):
        cap = itt.capture(jpgmode=0)
        ban_posi=asset.IconCommissionCommissionIcon.cap_posi
        cap[ban_posi[1]:ban_posi[3],ban_posi[0]:ban_posi[2]]=0
        r = movement.view_to_imgicon(cap, asset.IconCommissionInCommission)
        if not r:
            return False
        if r<=30:
            dist_cap = itt.capture([SCREEN_CENTER_X-80,SCREEN_CENTER_Y-100,SCREEN_CENTER_X+80,SCREEN_CENTER_Y+40],jpgmode=0)
            dist_cap = extract_white_letters(dist_cap, threshold=90)
            # is_num, dist = ocr.is_img_num_plus(dist_cap)
            res = ocr_light.get_all_texts(dist_cap)
            n=False
            for i in res:
                if 'm' in i:
                    x=i.replace('m','')
                    if is_int(x):
                        n=int(i.replace('m',''))
            if n:
                if DEBUG_MODE:
                    print(n)
                if n<=3: 
                    itt.key_up('w')
                    return True
                else:
                    itt.key_down('w')
        return False
    
    def exec_mission(self):
        attack_timer = AdvanceTimer(0.1).start()
        r = self.move_straight(self.commission_position, is_tp=True)
        if r == ERR_FAIL:return
        self.start_combat()
        reset_view_timer = AdvanceTimer(20)
        while 1:
            if self.checkup_stop_func():
                self.stop_combat()
                return
            if reset_view_timer.reached_and_reset():
                movement.reset_view()
            movement.jump_in_loop(8)
            if self._aim_to_commission_icon():
                pass
                # if attack_timer.reached_and_reset():itt.left_click()
            if not combat_lib.CSDL.get_combat_state():
                self.stop_combat()
                break
        self.is_commission_succ=True
        # self.pause_threading()
        
if __name__ == '__main__':
    idg = DangerousHaulGeneral([3070.957,-6539.2718])
    # while 1:
    #     idg._aim_to_commission_icon()
    idg.start()
    idg.continue_threading()
    while 1:
        time.sleep(1)