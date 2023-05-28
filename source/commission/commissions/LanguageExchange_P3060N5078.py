from source.commission.commission import *

class LanguageExchange_P3060N5078(CommissionTemplate):
    def __init__(self):
        CommissionTemplate.__init__(self, "LanguageExchange", [3060,-5078], is_CFCF=True, is_TMCF=True)
    
    def exec_mission(self):
        self.move_along("LanguageExchange20230414230230i0", is_precise_arrival=True)
        self.talk_with_npc()
        self.talk_skip()
        self.talk_wait(15)
        self.move_along("LanguageExchange20230414230337i1", is_precise_arrival=True)
        self.talk_with_npc()
        self.talk_skip()
        self.talk_wait(10)
        self.move_straight(["LanguageExchange20230414230405i2","end_position"], is_precise_arrival=True)
        self.talk_with_npc()
        self.talk_skip()
        self.collect(is_combat=True)
        self.move_straight(["LanguageExchange20230414230452i3","end_position"], is_precise_arrival=True)
        self.talk_with_npc()
        self.talk_skip()
        
if __name__ == '__main__':
    execc = LanguageExchange_P3060N5078()
    execc.start()