from source.commission.commission_template import CommissionTemplate
from source.talk.talk import Talk

meta = {
    "type":"BigPudgyProblem",
    "position":[2526,-5796]
}
class BigPudgyProblem_P2526N5796(CommissionTemplate, Talk):
    def __init__(self):
        CommissionTemplate.__init__(self, meta["type"], meta["position"], is_CFCF=True, is_TMCF=True)
        Talk.__init__(self)
        
    def exec_mission(self):
        self.move_along("BigPudgyProblemP2526N5796t20230405122438i0")
        self.collect(is_combat=True)
        self.move_straight([2609,-5950], is_tp=False)
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        self.move_along("BigPudgyProblemP2526N5796t20230405122622i2", is_tp=True)
        self.switch_character_to("Sucrose")
        self.itt.key_press('e')
        self.collect(is_combat=True)
        self.is_commission_succ=True

if __name__ == '__main__':
    execc = BigPudgyProblem_P2526N5796()
    execc.start()
        