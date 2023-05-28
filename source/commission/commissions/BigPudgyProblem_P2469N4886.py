from source.commission.commission import *

class BigPudgyProblem_P2469N4886(CommissionTemplate):
    def __init__(self):
        CommissionTemplate.__init__(self, "BigPudgyProblem", [2469,-4886], is_CFCF=True, is_TMCF=True)
        
    def exec_mission(self):
        self.move_along("BigPudgyProblem20230409110116i0")
        self.collect(is_combat=True)
        self.move_straight(["BigPudgyProblem20230409110140i1", "end_position"], is_tp=False)
        self.talk_with_npc()
        self.talk_skip()
        self.move_along("BigPudgyProblem20230409110225i2", is_tp=True)
        # self.switch_character_to("Sucrose")
        # self.itt.key_press('e')
        # self.collect(is_combat=True)
        self.is_commission_succ=True

if __name__ == '__main__':
    execc = BigPudgyProblem_P2469N4886()
    execc.start()
        