from source.commission.commission import *
from source.mission.mission_template import ERR_FAIL


class FightOnlyGeneral(Commission):
    def __init__(self, commission_type, commission_position):
        super().__init__(commission_type, commission_position)

    def exec_mission(self):
        r = self.move_straight(self.commission_position, is_tp=True, stop_rule=STOP_RULE_ARRIVE)
        self.handle_tmf_stuck_then_raise(r)
        
        self.circle_search(self.commission_position, stop_rule=STOP_RULE_COMBAT)
        
        self.fight_until_commission_complete()
        
        if self.is_pickup_spoils:
            r = self.collect(is_activate_pickup=self.is_pickup_spoils)
            if r == ERR_FAIL:return
        self.commission_succ()

        
