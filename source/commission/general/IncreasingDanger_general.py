from source.commission.commission_template import CommissionTemplate
from source.mission.mission_template import ERR_FAIL


class IncreasingDangerGeneral(CommissionTemplate):
    def __init__(self, commission_position):
        super().__init__("IncreasingDanger", commission_position)

    def exec_mission(self):
        r = self.move_straight(self.commission_position, is_tp=True)
        if r == ERR_FAIL:return
        r = self.collect(is_combat=True, is_activate_pickup=self.is_pickup_spoils)
        if r == ERR_FAIL:return