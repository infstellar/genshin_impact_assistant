from source.commission.commission_template import CommissionTemplate
from source.talk.talk import Talk
from source.commission.assets import *

meta = {
    "type":"ReliableHelper",
    "position":[2966,-4774]
}
class ReliableHelper_P2966N4774(CommissionTemplate, Talk):
    def __init__(self):
        CommissionTemplate.__init__(self, meta["type"], meta["position"], is_CFCF=True, is_TMCF=True)
        Talk.__init__(self)
    
    def exec_mission(self):
        self._reg_default_arrival_mode(True)
        self._reg_fight_if_needed(True)
        self.move_along("ReliableHelper20230415184809i0")
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        self._reg_fight_if_needed(False)
        self.move_straight(["ReliableHelper20230415184946i1","end_position"], is_precise_arrival=False)
        self.collect(is_combat=True)
        self.move_straight(["ReliableHelper20230415185053i2","end_position"])
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        
if __name__ == '__main__':
    execc = ReliableHelper_P2966N4774()
    execc.start()