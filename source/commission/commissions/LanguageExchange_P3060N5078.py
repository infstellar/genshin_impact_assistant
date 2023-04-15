from source.commission.commission_template import CommissionTemplate
from source.talk.talk import Talk

meta = {
    "type":"LanguageExchange",
    "position":[3060,-5078]
}
class LanguageExchange_P3060N5078(CommissionTemplate, Talk):
    def __init__(self):
        CommissionTemplate.__init__(self, meta["type"], meta["position"], is_CFCF=True, is_TMCF=True)
        Talk.__init__(self)
    
    def exec_mission(self):
        self.move_along("LanguageExchange20230414230230i0", is_precise_arrival=True)
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        self.talk_wait(15)
        self.move_along("LanguageExchange20230414230337i1", is_precise_arrival=True)
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        self.talk_wait(10)
        self.move_straight(["LanguageExchange20230414230405i2","end_position"], is_precise_arrival=True)
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        self.collect(is_combat=True)
        self.move_straight(["LanguageExchange20230414230452i3","end_position"], is_precise_arrival=True)
        self.talk_with_npc()
        self.talk_skip(self.checkup_stop_func)
        
if __name__ == '__main__':
    execc = LanguageExchange_P3060N5078()
    execc.start()