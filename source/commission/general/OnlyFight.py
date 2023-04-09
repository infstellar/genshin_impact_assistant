from source.commission.commission_template import CommissionTemplate
from source.mission.mission_template import ERR_FAIL


class FightOnlyGeneral(CommissionTemplate):
    def __init__(self, commission_type, commission_position):
        super().__init__(commission_type, commission_position)

    def exec_mission(self):
        r = self.move_straight(self.commission_position, is_tp=True)
        if r == ERR_FAIL:return
        self.circle_search(self.commission_position, stop_rule="Combat")
        r = self.collect(is_combat=True, is_activate_pickup=self.is_pickup_spoils)
        if r == ERR_FAIL:return
        self.is_commission_succ = True

        
