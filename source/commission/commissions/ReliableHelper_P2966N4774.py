from source.commission.commission import *

class ReliableHelper_P2966N4774(Commission):
    def __init__(self):
        super().__init__(commission_type='ReliableHelper', commission_position=[2966,-4774], is_CFCF=True, is_TMCF=True)
    
    def exec_mission(self):
        self.set_default_arrival_mode(True)
        self.reg_fight_if_needed(True)
        self.move_along("ReliableHelper20230415184809i0")
        self.talk_with_npc()
        self.talk_skip()
        self.reg_fight_if_needed(False)
        self.move_straight(["ReliableHelper20230415184946i1","end_position"], is_precise_arrival=False)
        self.collect(is_combat=True)
        self.move_straight(["ReliableHelper20230415185053i2","end_position"])
        self.talk_with_npc()
        self.talk_skip()
        
if __name__ == '__main__':
    execc = ReliableHelper_P2966N4774()
    execc.start()