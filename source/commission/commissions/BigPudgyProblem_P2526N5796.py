from source.commission.commission import *

class BigPudgyProblem_P2526N5796(CommissionTemplate):
    def __init__(self):
        CommissionTemplate.__init__(self, "BigPudgyProblem", [2526,-5796], is_CFCF=True, is_TMCF=True)
        
    def exec_mission(self):
        self.move_along("BigPudgyProblemP2526N5796t20230405122438i0")
        self.collect(is_combat=True)
        self.move_straight([2609,-5950], is_tp=False)
        self.talk_with_npc()
        self.talk_skip()
        self.move_along("BigPudgyProblemP2526N5796t20230405122622i2", is_tp=True)
        self.switch_character_to("Sucrose")
        self.itt.key_press('e')
        self.collect(is_combat=True)
        self.is_commission_succ=True

if __name__ == '__main__':
    execc = BigPudgyProblem_P2526N5796()
    execc.start()
        