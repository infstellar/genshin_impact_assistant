from source.commission.commission_template import CommissionTemplate
from source.talk.talk import Talk
from source.commission.assets import *

meta = {
    "type":"PigeonsGoAWOL",
    "position":[2671,-5095]
}
class PigeonsGoAWOL_P2671N5095(CommissionTemplate, Talk):
    def __init__(self):
        CommissionTemplate.__init__(self, meta["type"], meta["position"], is_CFCF=True, is_TMCF=True)
        Talk.__init__(self)
    
    def exec_mission(self):
        self._reg_raise_exception()
        self.move_along("PigeonsGoAWOL20230415140236i0", is_precise_arrival=True)
        self.talk_with_npc()
        self.talk_until_switch(self.checkup_stop_func)
        self.talk_switch(RegardingThesePigeons)
        self.talk_skip(self.checkup_stop_func)
        self.move_along("PigeonsGoAWOL20230415140918i1")
        self.move_along("PigeonsGoAWOL20230415141050i2")
        self.talk_with_npc()
        self.talk_until_switch(self.checkup_stop_func)
        self.talk_switch(RegardingThesePigeons)
        self.talk_skip(self.checkup_stop_func)
        
if __name__ == '__main__':
    execc = PigeonsGoAWOL_P2671N5095()
    execc.start()