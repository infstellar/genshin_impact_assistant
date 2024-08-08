from source.commission.commission import *
from source.mission.mission_template import ERR_FAIL


class ImpregnableDefense_P2428N2566(Commission):
    def __init__(self, commission_position):
        super().__init__("ImpregnableDefense", commission_position)

    def exec_mission(self):
        r = self.move_along(ImpregnableDefenseTLPP, is_tp=True, stop_rule=STOP_RULE_ARRIVE)
        self.handle_tmf_stuck_then_raise(r)
        self.circle_search(self.commission_position, stop_rule=STOP_RULE_COMBAT)

        self.fight_until_commission_complete()

        # TODO: 等收集模块完善后加入

        # if self.is_pickup_spoils:
        #     r = self.collect(is_activate_pickup=self.is_pickup_spoils)
        #     if r == ERR_FAIL:return
        self.commission_succ()


ImpregnableDefenseTLPP = {'start_position': [2820.33, -2678.9], 'end_position': [2428.45, -2566.25], 'position_list': [{'id': 1, 'motion': 'ANY', 'position': [2820.33, -2678.9], 'special_key': None}, {'id': 2, 'motion': 'ANY', 'position': [2703.84, -2535.55], 'special_key': None}, {'id': 3, 'motion': 'ANY', 'position': [2542.23, -2549.18], 'special_key': None}, {'id': 4, 'motion': 'ANY', 'position': [2428.45, -2566.25], 'special_key': None}], 'break_position': [[2820.33, -2678.9], [2703.84, -2535.55], [2542.23, -2549.18], [2428.45, -2566.25]], 'time': '', 'additional_info': {'path_recorder': '1.0', 'manually_modified': 'true'}, 'adsorptive_position': [[ 2694.5666, -2536.2883],[ 2422.7575, -2570.2964]], 'generate_from': 'path recorder 1.0'}
