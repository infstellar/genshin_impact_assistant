from source.commission.commission_template import CommissionTemplate
from source.talk.talk import Talk
from source.commission.assets import *


meta = {
    "type":"FloralFresh",
    "position":[2556,-5813]
}
class FloralFresh_P2556N5813(CommissionTemplate, Talk):
    def __init__(self):
        CommissionTemplate.__init__(self, meta["type"], meta["position"], is_CFCF=True, is_TMCF=True)
        Talk.__init__(self)
        
    def exec_mission(self):
        self._reg_default_arrival_mode(True)
        self.move_along("FloralFresh20230416160023i0")
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        self.move_along("FloralFresh20230416160216i2")
        self.itt.key_press('f')
        self.move_along("FloralFresh20230416160340i3")
        self.itt.key_press('f')
        self.move_along("FloralFresh20230416160509i4", is_precise_arrival=False)
        self.collect(is_combat=True)
        self.move_straight(["FloralFresh20230416160744i5","end_position"])
        self.itt.key_press('f')
        self.itt.delay(1)
        self.move_along("FloralFresh20230416160023i0")
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        
if __name__ == '__main__':
    execc = FloralFresh_P2556N5813()
    execc.start()
        