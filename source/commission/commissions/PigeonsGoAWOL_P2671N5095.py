from source.commission.commission import *

class PigeonsGoAWOL_P2671N5095(Commission):
    def __init__(self):
        super().__init__("PigeonsGoAWOL", [2671,-5095], is_CFCF=True, is_TMCF=True)
    
    def exec_mission(self):
        self.set_raise_exception()
        self.move_along("PigeonsGoAWOL20230415140236i0", is_precise_arrival=True)
        self.talk_with_npc()
        self.talk_until_switch()
        self.talk_switch(RegardingThesePigeons)
        self.talk_skip()
        self.move_along("PigeonsGoAWOL20230415140918i1")
        self.move_along("PigeonsGoAWOL20230415141050i2")
        self.talk_with_npc()
        self.talk_until_switch()
        self.talk_switch(RegardingThesePigeons)
        self.talk_skip()
        
if __name__ == '__main__':
    execc = PigeonsGoAWOL_P2671N5095()
    execc.start()