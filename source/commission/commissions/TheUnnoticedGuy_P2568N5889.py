from source.commission.commission import Commission

class TheUnnoticedGuy_P2568N5889(Commission):
    def __init__(self):
        super().__init__("TheUnnoticedGuy", [2568,-5889], is_TMCF=True)
        
    def exec_mission(self):
        r = self.move_along("CommissionGaiyi20230408091010i0")
        self.handle_tmf_stuck_then_raise(r)
        r = self.move_straight(["CommissionGaiyi20230408091036i1","end_position"], is_precise_arrival=True)
        self.handle_tmf_stuck_then_raise(r)
        self.talk_with_npc()
        self.talk_skip()
        r = self.move_along("CommissionGaiyi20230408091231i2", is_precise_arrival=True)
        self.handle_tmf_stuck_then_raise(r)
        self.talk_with_npc()
        self.talk_skip()
        self.is_commission_succ=True
    
if __name__ == '__main__':
    execc = TheUnnoticedGuy_P2568N5889()
    execc.start()    
