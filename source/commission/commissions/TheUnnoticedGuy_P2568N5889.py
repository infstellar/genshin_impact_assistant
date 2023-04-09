from source.commission.commission_template import CommissionTemplate
from source.talk.talk import Talk
from source.commission.util import *

meta = {
    "type":"TheUnnoticedGuy",
    "position":[2568,-5889]
}

class TheUnnoticedGuy_P2568N5889(CommissionTemplate, Talk):
    def __init__(self):
        CommissionTemplate.__init__(self, meta["type"], meta["position"], is_TMCF=True)
        Talk.__init__(self)
        
    def exec_mission(self):
        r = self.move_along("CommissionGaiyi20230408091010i0")
        if r == ERR_FAIL: return
        r = self.move_straight(["CommissionGaiyi20230408091036i1","end_position"], is_precise_arrival=True)
        if r == ERR_FAIL: return
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        r = self.move_along("CommissionGaiyi20230408091231i2", is_precise_arrival=True)
        if r == ERR_FAIL: return
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        self.is_commission_succ=True
    
if __name__ == '__main__':
    execc = TheUnnoticedGuy_P2568N5889()
    execc.start()    
