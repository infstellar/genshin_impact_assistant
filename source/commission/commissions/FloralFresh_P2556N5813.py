from source.commission.commission import *

class FloralFresh_P2556N5813(Commission):
    def __init__(self):
        super().__init__("FloralFresh", [2556,-5813], is_CFCF=True, is_TMCF=True, support_lang='en_US')
        
    def exec_mission(self):
        self.set_default_arrival_mode(True)
        self.move_along("FloralFresh20230416160023i0")
        self.talk_with_npc()
        self.talk_skip()
        self.move_along("FloralFresh20230416160216i2", is_precise_arrival=True, stop_rule=STOP_RULE_F)
        self.itt.key_press('f')
        self.move_along("FloralFresh20230416160340i3", is_precise_arrival=True, stop_rule=STOP_RULE_F)
        self.itt.key_press('f')
        self.move_along("FloralFresh20230416160509i4", is_precise_arrival=False, stop_rule=STOP_RULE_COMBAT)
        self.collect(is_combat=True)
        self.move_straight(["FloralFresh20230416160744i5","end_position"])
        self.itt.key_press('f')
        self.itt.delay(1)
        self.move_along("FloralFresh20230416160023i0")
        self.talk_with_npc()
        self.talk_skip()
        self.commission_succ()
        
if __name__ == '__main__':
    execc = FloralFresh_P2556N5813()
    execc.start()
        