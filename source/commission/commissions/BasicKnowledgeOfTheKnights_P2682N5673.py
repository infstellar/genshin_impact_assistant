from source.commission.commission import *

AskDirectly = Text(zh="直接问吧",en="Ask Directly")
Librarian = Text(zh="图书管理员",en="Librarian")
CavalryCaptain = Text(zh="骑兵队长",en="Cavalry Captain")
Outrider = Text(zh="侦察骑士",en="Outrider")

class BasicKnowledgeOfTheKnights_P2682N5673(Commission):
    def __init__(self):
        super().__init__("BasicKnowledgeOfTheKnights", [2682,-5673], is_CFCF=True, is_TMCF=True)
        
    def exec_mission(self):
        self.move_along("BasicKnowledgeOfTheKnights20230409115353i0")
        self.talk_with_npc()
        self.talk_until_switch()
        self.talk_switch(AskDirectly)
        self.talk_with_npc()
        self.talk_until_switch()
        self.talk_switch(Librarian)
        self.talk_until_switch()
        self.talk_switch(CavalryCaptain)
        self.talk_until_switch()
        self.talk_switch(Outrider)
        self.talk_skip()
        self.is_commission_succ=True
        
if __name__ == '__main__':
    execc = BasicKnowledgeOfTheKnights_P2682N5673()
    execc.start()
        